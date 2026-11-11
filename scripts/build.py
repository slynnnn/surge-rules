#!/usr/bin/env python3
"""四源合一构建：抓取 blackmatrix7 / LceAn / Rabbit-Spec 的 Surge .list，
按类目合并、规范化、去重，生成 rules/merged/*.list。
Loyalsoldier 走 DOMAIN-SET/RULE-SET 直引（其 release 分支每日更新），不并入本地文件。
抓取失败的源跳过并记入 BUILD-LOG.md，绝不让单源故障拖垮整仓。
"""
import re, sys, urllib.request, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "rules" / "merged"
UA = {"User-Agent": "ochiai-surge-rules-build"}

BM7 = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge"
LCE = "https://raw.githubusercontent.com/LceAn/proxy-filter-rules/main/rules"
RAB = "https://raw.githubusercontent.com/Rabbit-Spec/Surge/Master/Rules"

# 类目 -> 上游文件清单
CATEGORIES = {
    "ai": [
        f"{BM7}/OpenAI/OpenAI.list", f"{BM7}/Claude/Claude.list", f"{BM7}/Gemini/Gemini.list", f"{BM7}/Copilot/Copilot.list", f"{BM7}/BardAI/BardAI.list",
        f"{LCE}/AI.list", f"{LCE}/OpenAI.list", f"{LCE}/Claude.list", f"{LCE}/Gemini.list",
        f"{RAB}/AIGC.list",
    ],
    "streaming": [
        f"{BM7}/Netflix/Netflix.list", f"{BM7}/YouTube/YouTube.list", f"{BM7}/Disney/Disney.list",
        f"{BM7}/Spotify/Spotify.list", f"{BM7}/TikTok/TikTok.list",
        f"{LCE}/Netflix.list", f"{LCE}/YouTube.list", f"{LCE}/Disney.list", f"{LCE}/Spotify.list",
        f"{RAB}/Netflix.list", f"{RAB}/YouTube.list", f"{RAB}/Disney.list", f"{RAB}/Spotify.list",
        f"{RAB}/TikTok.list", f"{RAB}/GlobalMedia.list",
    ],
    "social": [
        f"{BM7}/Telegram/Telegram.list", f"{BM7}/Twitter/Twitter.list",
        f"{BM7}/Facebook/Facebook.list", f"{BM7}/Instagram/Instagram.list",
        f"{LCE}/Telegram.list", f"{LCE}/Twitter.list", f"{LCE}/Facebook.list", f"{LCE}/Instagram.list",
        f"{RAB}/Telegram.list", f"{RAB}/Facebook.list", f"{RAB}/Instagram.list", f"{RAB}/Whatsapp.list",
    ],
    "global": [
        f"{BM7}/Apple/Apple.list", f"{BM7}/Google/Google.list", f"{BM7}/Microsoft/Microsoft.list",
        f"{BM7}/GitHub/GitHub.list", f"{BM7}/PayPal/PayPal.list", f"{BM7}/Steam/Steam.list",
        f"{LCE}/GitHub.list", f"{LCE}/Google.list", f"{LCE}/Microsoft.list", f"{LCE}/PayPal.list", f"{LCE}/Steam.list",
        f"{RAB}/Google.list", f"{RAB}/Apple.list", f"{RAB}/Microsoft.list", f"{RAB}/PayPal.list",  # Rabbit Proxy.list 是 2.2 万条大集，与 Loyalsoldier proxy/gfw 直引重复，不并入
    ],
    "china": [
        f"{BM7}/BiliBili/BiliBili.list", f"{BM7}/China/China.list",
        f"{LCE}/China.list", f"{LCE}/BiliBili.list", f"{LCE}/WeChat.list", f"{LCE}/XiaoHongShu.list", f"{LCE}/Zhihu.list",
        f"{RAB}/China.list", f"{RAB}/BiliBili.list", f"{RAB}/ChinaMedia.list",
    ],
    # 广告不用 typed 合并：BM7 Advertising 全集约 29 万条，走 DOMAIN-SET（见 main 末尾 ads.txt）
}

# 四源未覆盖的 AI 服务补充（仓内自维护，构建时并入 ai）
EXTRA = {
    "ai": [
        "DOMAIN-SUFFIX,mistral.ai",
        "DOMAIN-SUFFIX,huggingface.co",
        "DOMAIN-SUFFIX,cdn-lfs.huggingface.co",
        "DOMAIN-SUFFIX,cohere.com",
        "DOMAIN-SUFFIX,cohere.ai",
        "DOMAIN-SUFFIX,midjourney.com",
        "DOMAIN-SUFFIX,you.com",
        "DOMAIN-SUFFIX,phind.com",
        "DOMAIN-SUFFIX,character.ai",
        "DOMAIN-SUFFIX,v0.dev",
        "DOMAIN-SUFFIX,bolt.new",
        "DOMAIN-SUFFIX,replit.com",
        "DOMAIN-SUFFIX,codeium.com",
        "DOMAIN-SUFFIX,windsurf.com",
    ],
}


# ===== 细分类一：按服务（单个产品一份） =====
SERVICES = {
    "youtube":   [f"{BM7}/YouTube/YouTube.list", f"{LCE}/YouTube.list", f"{RAB}/YouTube.list"],
    "netflix":   [f"{BM7}/Netflix/Netflix.list", f"{LCE}/Netflix.list", f"{RAB}/Netflix.list"],
    "disney":    [f"{BM7}/Disney/Disney.list", f"{LCE}/Disney.list", f"{RAB}/Disney.list"],
    "spotify":   [f"{BM7}/Spotify/Spotify.list", f"{LCE}/Spotify.list", f"{RAB}/Spotify.list"],
    "tiktok":    [f"{BM7}/TikTok/TikTok.list", f"{RAB}/TikTok.list"],
    "bilibili":  [f"{BM7}/BiliBili/BiliBili.list", f"{LCE}/BiliBili.list", f"{RAB}/BiliBili.list"],
    "telegram":  [f"{BM7}/Telegram/Telegram.list", f"{LCE}/Telegram.list", f"{RAB}/Telegram.list"],
    "twitter":   [f"{BM7}/Twitter/Twitter.list", f"{LCE}/Twitter.list"],
    "facebook":  [f"{BM7}/Facebook/Facebook.list", f"{LCE}/Facebook.list", f"{RAB}/Facebook.list"],
    "instagram": [f"{BM7}/Instagram/Instagram.list", f"{LCE}/Instagram.list", f"{RAB}/Instagram.list"],
    "whatsapp":  [f"{RAB}/Whatsapp.list"],
    "google":    [f"{BM7}/Google/Google.list", f"{LCE}/Google.list", f"{RAB}/Google.list"],
    "apple":     [f"{BM7}/Apple/Apple.list", f"{RAB}/Apple.list"],
    "microsoft": [f"{BM7}/Microsoft/Microsoft.list", f"{LCE}/Microsoft.list", f"{RAB}/Microsoft.list"],
    "github":    [f"{BM7}/GitHub/GitHub.list", f"{LCE}/GitHub.list"],
    "paypal":    [f"{BM7}/PayPal/PayPal.list", f"{LCE}/PayPal.list", f"{RAB}/PayPal.list"],
    "steam":     [f"{BM7}/Steam/Steam.list", f"{LCE}/Steam.list"],
    "openai":    [f"{BM7}/OpenAI/OpenAI.list", f"{LCE}/OpenAI.list"],
    "claude":    [f"{BM7}/Claude/Claude.list", f"{LCE}/Claude.list"],
    "gemini":    [f"{BM7}/Gemini/Gemini.list", f"{LCE}/Gemini.list", f"{BM7}/BardAI/BardAI.list"],
    "copilot":   [f"{BM7}/Copilot/Copilot.list"],
}

# ===== 细分类二：按企业（旗下服务打包） =====
COMPANIES = {
    "google":    {"services": ["google", "youtube", "gemini"], "literals": []},
    "meta":      {"services": ["facebook", "instagram", "whatsapp"],
                  "literals": ["DOMAIN-SUFFIX,threads.net", "DOMAIN-SUFFIX,threads.com",
                               "DOMAIN-SUFFIX,meta.ai", "DOMAIN-SUFFIX,oculus.com", "DOMAIN-SUFFIX,meta.com"]},
    "microsoft": {"services": ["microsoft", "copilot"], "literals": []},
    "apple":     {"services": ["apple"], "literals": []},
}

RULE_RE = re.compile(r"^(DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD|IP-CIDR|IP-CIDR6|IP-ASN|USER-AGENT|URL-REGEX|HOSTNAME-TYPE|PROCESS-NAME|DEST-PORT|SRC-IP-CIDR|GEOIP|AND|OR|NOT|IP-ASN)\s*,\s*(.+)$", re.I)

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def normalize(line):
    line = line.strip()
    if not line or line.startswith(("#", "//", ";")):
        return None
    # 去掉行尾策略与 no-resolve 等参数，只留 规则类型,值
    if "," not in line:
        # DOMAIN-SET 式纯域名行（BM7 Advertising_Domain）：.foo.com = 后缀匹配
        d = line.strip()
        if re.fullmatch(r"\.?[A-Za-z0-9_-]+(\.[A-Za-z0-9_-]+)+", d):
            return f"DOMAIN-SUFFIX,{d[1:]}" if d.startswith(".") else f"DOMAIN,{d}"
        return None
    # 复合逻辑规则与 URL-REGEX 内部含逗号，整行保留（上游 RULE-SET 本就不带策略后缀）
    if re.match(r"^(AND|OR|NOT|URL-REGEX)\s*,", line, re.I):
        return line
    parts = [p.strip() for p in line.split(",")]
    if len(parts) < 2:
        return None
    m = RULE_RE.match(parts[0] + "," + parts[1])
    if not m:
        return None
    rtype, value = parts[0].upper(), parts[1]
    if rtype in ("IP-CIDR", "IP-CIDR6") and len(parts) >= 3 and parts[2].replace(".", "").isdigit():
        value = parts[1]  # 保持原值，掩码在 parts[1] 内或独立段
    return f"{rtype},{value}"

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    log = [f"# BUILD-LOG", f"", f"构建时间：{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", ""]
    total = 0
    for cat, urls in CATEGORIES.items():
        seen, per_src = set(), []
        for u in urls:
            try:
                text = fetch(u)
            except Exception as e:
                per_src.append(f"- ✗ {u} （{type(e).__name__}）")
                continue
            n0 = len(seen)
            for raw in text.splitlines():
                v = normalize(raw)
                if v:
                    seen.add(v)
            per_src.append(f"- ✓ {u} （累计去重后 {len(seen)}，本源新增 {len(seen)-n0}）")
        for extra in EXTRA.get(cat, []):
            seen.add(extra)
        rules = sorted(seen)
        header = [
            f"# {cat}.list — 四源合一（blackmatrix7 + LceAn + Rabbit-Spec）",
            f"# 规则数：{len(rules)}",
            f"# 由 scripts/build.py 生成，勿手改；改源请改 build.py 的 CATEGORIES",
            "",
        ]
        (OUT / f"{cat}.list").write_text("\n".join(header + rules) + "\n", encoding="utf-8")
        log += [f"## {cat}.list：{len(rules)} 条", ""] + per_src + [""]
        total += len(rules)
        print(f"{cat}: {len(rules)}")

    # ---- 细分类生成：按服务 / 按企业 ----
    svc_dir = ROOT / "rules" / "service"; svc_dir.mkdir(parents=True, exist_ok=True)
    comp_dir = ROOT / "rules" / "company"; comp_dir.mkdir(parents=True, exist_ok=True)
    svc_rules = {}
    for name, urls in SERVICES.items():
        seen = set()
        for u in urls:
            try:
                text = fetch(u)
            except Exception:
                continue
            for raw in text.splitlines():
                v = normalize(raw)
                if v:
                    seen.add(v)
        svc_rules[name] = sorted(seen)
        (svc_dir / f"{name}.list").write_text(
            f"# service/{name}.list — 按服务细分类（四源合并去重）\n# 规则数：{len(seen)}\n# 由 scripts/build.py 生成\n\n"
            + "\n".join(svc_rules[name]) + "\n", encoding="utf-8")
        print(f"service/{name}: {len(seen)}")
    for name, spec in COMPANIES.items():
        seen = set(spec["literals"])
        for svc in spec["services"]:
            seen.update(svc_rules.get(svc, []))
        rules = sorted(seen)
        (comp_dir / f"{name}.list").write_text(
            f"# company/{name}.list — 按企业细分类（旗下服务打包）\n# 规则数：{len(rules)}\n# 由 scripts/build.py 生成\n\n"
            + "\n".join(rules) + "\n", encoding="utf-8")
        print(f"company/{name}: {len(rules)}")
    log += ["", "## 细分类", "",
            "按服务：" + "、".join(f"{k} {len(v)}" for k, v in svc_rules.items()), ""]
    # 广告 DOMAIN-SET：原样清洗 BM7 Advertising_Domain（去注释/空行、去重排序）
    try:
        raw = fetch(f"{BM7}/Advertising/Advertising_Domain.list")
        doms = sorted({ln.strip() for ln in raw.splitlines() if ln.strip() and not ln.strip().startswith("#")})
        (OUT / "ads.txt").write_text(
            "# ads.txt — 广告域名集（DOMAIN-SET 用），源：blackmatrix7 Advertising_Domain\n"
            f"# 域名数：{len(doms)}\n" + "\n".join(doms) + "\n", encoding="utf-8")
        log += [f"## ads.txt（DOMAIN-SET）：{len(doms)} 个域名", ""]
        print(f"ads(domain-set): {len(doms)}")
    except Exception as e:
        log += [f"## ads.txt 构建失败：{type(e).__name__}", ""]
    log.insert(3, f"总计：{total} 条（去重后）")
    (ROOT / "BUILD-LOG.md").write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"total: {total}")

if __name__ == "__main__":
    main()
