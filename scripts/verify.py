#!/usr/bin/env python3
"""常设验证：三件套
1) 链接存活：两份配置引用的全部远程规则集逐个探活（须 200）
2) 格式合法：全部生成列表逐行扫规则类型与形态
3) 抽样命中模拟：代表域名按 Ochiai.conf 的规则顺序模拟匹配，
   看最终落点（策略组）是否与预期一致，并列出被多份列表同时命中的交叉项
结果写入 VERIFY-LOG.md；硬失败（死链/非法行/落点不符）以非零码退出。
"""
import re, sys, pathlib, datetime, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = {"User-Agent": "ochiai-surge-rules-verify"}

# Ochiai.conf 中 merged 列表的评估顺序与策略组
CONF_ORDER = [
    ("rules/merged/ads.txt", "广告拦截"),
    ("rules/merged/ai.list", "AI"),
    ("rules/merged/streaming.list", "流媒体"),
    ("rules/merged/social.list", "社交"),
    ("rules/merged/global.list", "节点选择"),
    ("rules/merged/china.list", "DIRECT"),
]

# 抽样域名 -> 预期落点
SAMPLES = {
    "chatgpt.com": "AI", "claude.ai": "AI", "gemini.google.com": "AI",
    "copilot.microsoft.com": "AI", "perplexity.ai": "AI", "grok.com": "AI",
    "netflix.com": "流媒体", "youtube.com": "流媒体", "disneyplus.com": "流媒体",
    "spotify.com": "流媒体", "tiktok.com": "流媒体",
    "telegram.org": "社交", "x.com": "社交", "facebook.com": "社交",
    "instagram.com": "社交", "whatsapp.com": "社交",
    "google.com": "节点选择", "github.com": "节点选择", "microsoft.com": "节点选择",
    "paypal.com": "节点选择", "steampowered.com": "节点选择",
    "bilibili.com": "DIRECT", "zhihu.com": "DIRECT", "xiaohongshu.com": "DIRECT",
}

RULE_TYPES = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6",
              "IP-ASN", "USER-AGENT", "URL-REGEX", "GEOIP", "DEST-PORT",
              "PROCESS-NAME", "AND", "OR", "NOT", "HOSTNAME-TYPE", "SRC-IP-CIDR"}

def load_rules(path):
    rules = []
    for ln in (ROOT / path).read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        if path.endswith("ads.txt"):
            d = ln.lstrip(".")
            rules.append(("DOMAIN-SUFFIX" if ln.startswith(".") else "DOMAIN", d))
            continue
        parts = ln.split(",", 2)
        if len(parts) >= 2:
            rules.append((parts[0].strip().upper(), parts[1].strip()))
    return rules

def matches(rules, domain):
    for t, v in rules:
        if t == "DOMAIN" and domain == v:
            return True
        if t == "DOMAIN-SUFFIX" and (domain == v or domain.endswith("." + v)):
            return True
        if t == "DOMAIN-KEYWORD" and v in domain:
            return True
    return False

def check_links():
    urls = set()
    for conf in ["Surge/Ochiai.conf", "Surge/Ochiai-Detailed.conf"]:
        text = (ROOT / conf).read_text(encoding="utf-8")
        for u in re.findall(r"https://[^\s,]+", text):
            if "dns-query" not in u and "github.com/slynnnn/surge-rules$" not in u:
                urls.add(u)
    dead = []
    for u in sorted(urls):
        try:
            req = urllib.request.Request(u, headers=UA, method="GET")
            with urllib.request.urlopen(req, timeout=20) as r:
                r.read(64)
                if r.status != 200:
                    dead.append((u, r.status))
        except Exception as e:
            dead.append((u, type(e).__name__))
    return sorted(urls), dead

def check_format():
    bad = []
    files = list((ROOT / "rules").rglob("*.list"))
    for f in files:
        for i, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            s = ln.strip()
            if not s or s.startswith("#"):
                continue
            t = s.split(",", 1)[0].strip().upper()
            if t not in RULE_TYPES or "," not in s:
                bad.append(f"{f.relative_to(ROOT)}:{i} {s[:60]}")
    # 域名集型 .txt（ads.txt + extended/*.txt）：每行须是合法域名形态
    dom_re = re.compile(r"\.?[A-Za-z0-9_-]+(\.[A-Za-z0-9_-]+)+$")
    for f in (ROOT / "rules").rglob("*.txt"):
        files.append(f)
        for i, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            s = ln.strip()
            if not s or s.startswith("#"):
                continue
            if not dom_re.fullmatch(s):
                bad.append(f"{f.relative_to(ROOT)}:{i} {s[:60]}")
    return files, bad

def check_module_links():
    """modules.yaml 索引链接存活：失效只警告记账，不硬失败（上游模块下线不该拖垮规则构建）。"""
    text = (ROOT / "modules.yaml").read_text(encoding="utf-8")
    urls = sorted(set(re.findall(r"url:\s*(https://\S+)", text)))
    dead = []
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=UA, method="GET")
            with urllib.request.urlopen(req, timeout=20) as r:
                r.read(64)
                if r.status != 200:
                    dead.append((u, r.status))
        except Exception as e:
            dead.append((u, type(e).__name__))
    return urls, dead

def main():
    lines = ["# VERIFY-LOG", "",
             f"验证时间：{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", ""]
    hard_fail = False

    urls, dead = check_links()
    lines += [f"## 链接存活：{len(urls)} 个引用，死链 {len(dead)}", ""]
    lines += [f"- ✗ {u}（{c}）" for u, c in dead] or ["- 全部可达"]
    lines.append("")
    if dead: hard_fail = True

    files, bad = check_format()
    lines += [f"## 格式合法：{len(files)} 份列表，非法行 {len(bad)}", ""]
    lines += [f"- ✗ {b}" for b in bad[:20]] or ["- 全部合法"]
    lines.append("")
    if bad: hard_fail = True

    loaded = [(p, g, load_rules(p)) for p, g in CONF_ORDER]
    lines += ["## 抽样命中模拟（按 Ochiai.conf 顺序）", "",
              "| 域名 | 预期 | 实际落点 | 同时命中 |", "|---|---|---|---|"]
    miss = 0
    for domain, expect in SAMPLES.items():
        hits = [g for _, g, rs in loaded if matches(rs, domain)]
        actual = hits[0] if hits else "（未命中，走 FINAL）"
        ok = actual == expect
        if not ok: miss += 1
        lines.append(f"| {domain} | {expect} | {actual} {'✓' if ok else '✗'} | {', '.join(hits) if len(hits) > 1 else '—'} |")
    lines += ["", f"抽样 {len(SAMPLES)} 个，落点不符 {miss} 个"]
    if miss: hard_fail = True

    murls, mdead = check_module_links()
    lines += ["", f"## 模块索引链接存活（软巡检）：{len(murls)} 个，失效 {len(mdead)}", ""]
    lines += [f"- ⚠ {u}（{c}）" for u, c in mdead] or ["- 全部可达"]

    (ROOT / "VERIFY-LOG.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"links: {len(urls)} urls, {len(dead)} dead | format: {len(files)} files, {len(bad)} bad | samples: {len(SAMPLES)}, {miss} miss")
    sys.exit(1 if hard_fail else 0)

if __name__ == "__main__":
    main()
