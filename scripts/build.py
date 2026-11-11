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


def emit_grouped(path, title, sections):
    """sections: [(小节名, set[规则])]，按顺序先到先得去重，每节带注释头，方便人读。
    返回总条数。"""
    seen, blocks, total = set(), [], 0
    for name, rules in sections:
        fresh = sorted(r for r in rules if r not in seen)
        seen.update(fresh)
        if not fresh:
            continue
        total += len(fresh)
        blocks.append(f"\n# ── {name}（{len(fresh)} 条）──\n" + "\n".join(fresh))
    path.write_text(f"# {title}\n# 规则数：{total}\n# 由 scripts/build.py 生成，勿手改；改源请改 build.py\n"
                    + "\n".join(blocks) + "\n", encoding="utf-8")
    return total

def fetch_set(urls, log_src=None):
    out = set()
    for u in urls:
        try:
            text = fetch(u)
        except Exception:
            continue
        for raw in text.splitlines():
            v = normalize(raw)
            if v:
                out.add(v)
    return out

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    log = [f"# BUILD-LOG", f"", f"构建时间：{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", ""]
    total = 0

    GROUPS = {
        "ai": [
            ("OpenAI / ChatGPT / Sora", [f"{BM7}/OpenAI/OpenAI.list", f"{LCE}/OpenAI.list"]),
            ("Claude", [f"{BM7}/Claude/Claude.list", f"{LCE}/Claude.list"]),
            ("Gemini / Bard", [f"{BM7}/Gemini/Gemini.list", f"{BM7}/BardAI/BardAI.list", f"{LCE}/Gemini.list"]),
            ("Copilot", [f"{BM7}/Copilot/Copilot.list"]),
            ("其他 AI（Grok / Perplexity / Poe / Meta AI / Cursor 等聚合）", [f"{RAB}/AIGC.list", f"{LCE}/AI.list"]),
            ("仓内补充（四源未覆盖）", []),
        ],
        "streaming": [
            ("Netflix", [f"{BM7}/Netflix/Netflix.list", f"{LCE}/Netflix.list", f"{RAB}/Netflix.list"]),
            ("YouTube", [f"{BM7}/YouTube/YouTube.list", f"{LCE}/YouTube.list", f"{RAB}/YouTube.list"]),
            ("Disney", [f"{BM7}/Disney/Disney.list", f"{LCE}/Disney.list", f"{RAB}/Disney.list"]),
            ("Spotify", [f"{BM7}/Spotify/Spotify.list", f"{LCE}/Spotify.list", f"{RAB}/Spotify.list"]),
            ("TikTok", [f"{BM7}/TikTok/TikTok.list", f"{RAB}/TikTok.list"]),
            ("其他流媒体（GlobalMedia 聚合）", [f"{RAB}/GlobalMedia.list"]),
        ],
        "social": [
            ("Telegram", [f"{BM7}/Telegram/Telegram.list", f"{LCE}/Telegram.list", f"{RAB}/Telegram.list"]),
            ("Twitter / X", [f"{BM7}/Twitter/Twitter.list", f"{LCE}/Twitter.list"]),
            ("Facebook", [f"{BM7}/Facebook/Facebook.list", f"{LCE}/Facebook.list", f"{RAB}/Facebook.list"]),
            ("Instagram", [f"{BM7}/Instagram/Instagram.list", f"{LCE}/Instagram.list", f"{RAB}/Instagram.list"]),
            ("WhatsApp", [f"{RAB}/Whatsapp.list"]),
        ],
        "global": [
            ("Google", [f"{BM7}/Google/Google.list", f"{LCE}/Google.list", f"{RAB}/Google.list"]),
            ("Apple", [f"{BM7}/Apple/Apple.list", f"{RAB}/Apple.list"]),
            ("Microsoft", [f"{BM7}/Microsoft/Microsoft.list", f"{LCE}/Microsoft.list", f"{RAB}/Microsoft.list"]),
            ("GitHub", [f"{BM7}/GitHub/GitHub.list", f"{LCE}/GitHub.list"]),
            ("PayPal", [f"{BM7}/PayPal/PayPal.list", f"{LCE}/PayPal.list", f"{RAB}/PayPal.list"]),
            ("Steam", [f"{BM7}/Steam/Steam.list", f"{LCE}/Steam.list"]),
        ],
        "china": [
            ("Bilibili", [f"{BM7}/BiliBili/BiliBili.list", f"{LCE}/BiliBili.list", f"{RAB}/BiliBili.list"]),
            ("微信", [f"{LCE}/WeChat.list"]),
            ("小红书", [f"{LCE}/XiaoHongShu.list"]),
            ("知乎", [f"{LCE}/Zhihu.list"]),
            ("国内媒体", [f"{RAB}/ChinaMedia.list"]),
            ("国内站点", [f"{BM7}/China/China.list", f"{LCE}/China.list", f"{RAB}/China.list"]),
        ],
    }
    for cat, sections in GROUPS.items():
        built = []
        for name, urls in sections:
            rules = fetch_set(urls)
            if cat == "ai" and name.startswith("仓内补充"):
                rules = set(EXTRA.get("ai", []))
            built.append((name, rules))
        n = emit_grouped(OUT / f"{cat}.list", f"{cat}.list — 四源合一（blackmatrix7 + LceAn + Rabbit-Spec）", built)
        log += [f"## {cat}.list：{n} 条（分 {len([b for b in built if b[1]])} 节）", ""]
        total += n
        print(f"{cat}: {n}")

    # ---- 细分类生成：按服务 / 按企业（同样分组写出，服务内按来源分节） ----
    svc_dir = ROOT / "rules" / "service"; svc_dir.mkdir(parents=True, exist_ok=True)
    comp_dir = ROOT / "rules" / "company"; comp_dir.mkdir(parents=True, exist_ok=True)
    svc_rules = {}
    for name, urls in SERVICES.items():
        by_src = [("blackmatrix7", [u for u in urls if "blackmatrix7" in u]),
                  ("LceAn", [u for u in urls if "LceAn" in u]),
                  ("Rabbit-Spec", [u for u in urls if "Rabbit-Spec" in u])]
        built = [(src, fetch_set(us)) for src, us in by_src if us]
        n = emit_grouped(svc_dir / f"{name}.list", f"service/{name}.list — 按服务细分类（四源合并去重）", built)
        svc_rules[name] = set()
        for _, rs in built:
            svc_rules[name].update(rs)
        print(f"service/{name}: {n}")
    for name, spec in COMPANIES.items():
        built = [(svc, set(svc_rules.get(svc, []))) for svc in spec["services"]]
        if spec["literals"]:
            built.append(("仓内补充", set(spec["literals"])))
        n = emit_grouped(comp_dir / f"{name}.list", f"company/{name}.list — 按企业细分类（旗下服务打包）", built)
        print(f"company/{name}: {n}")
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
