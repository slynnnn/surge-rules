#!/usr/bin/env python3
"""分平台生成：以 rules/ 下的 Surge  canonical 列表为唯一数据源，
转换出 Clash(mihomo) / Loon / Shadowrocket / QuantumultX / v2ray(geosite) / sing-box 六平台文件。
各平台不支持的规则类型会被丢弃并计数，明细写入 PLATFORM-LOG.md。
"""
import json, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "platforms"

SOURCES = {}
for f in sorted((ROOT / "rules" / "merged").glob("*.list")):
    SOURCES[f"merged/{f.stem}"] = f
for f in sorted((ROOT / "rules" / "service").glob("*.list")):
    SOURCES[f"service/{f.stem}"] = f
for f in sorted((ROOT / "rules" / "company").glob("*.list")):
    SOURCES[f"company/{f.stem}"] = f

QX_POLICY = {"merged/ai": "AI", "merged/streaming": "Streaming", "merged/social": "Social",
             "merged/global": "Global", "merged/china": "DIRECT", "merged/ads": "REJECT"}

def parse(path):
    """返回 [(section, type, value)]，保留分节。"""
    out, section = [], "默认"
    for ln in path.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if s.startswith("# ──"):
            section = s.strip("# ─").split("（")[0].strip()
            continue
        if not s or s.startswith("#"):
            continue
        parts = s.split(",", 1)
        if len(parts) == 2:
            out.append((section, parts[0].strip().upper(), parts[1].strip()))
    return out

def parse_ads():
    out = []
    for ln in (ROOT / "rules" / "merged" / "ads.txt").read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        out.append(("广告域名", "DOMAIN-SUFFIX" if s.startswith(".") else "DOMAIN", s.lstrip(".")))
    return out

def group_sections(rows):
    g = collections.OrderedDict()
    for sec, t, v in rows:
        g.setdefault(sec, []).append((t, v))
    return g

def write_grouped(path, grouped, fmt, header):
    lines = [header]
    for sec, rows in grouped.items():
        lines.append(f"\n# ── {sec}（{len(rows)} 条）──")
        lines += [fmt(t, v) for t, v in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

def conv_clash(t, v):
    if t in ("USER-AGENT", "URL-REGEX"): return None
    return f"{t},{v}"
def conv_loon(t, v):
    if t in ("PROCESS-NAME", "AND", "OR", "NOT"): return None
    if t == "IP-CIDR6": return f"IP-CIDR,{v}"
    return f"{t},{v}"
def conv_sr(t, v):
    if t in ("PROCESS-NAME", "AND", "OR", "NOT"): return None
    return f"{t},{v}"
def make_qx(policy):
    m = {"DOMAIN": "HOST", "DOMAIN-SUFFIX": "HOST-SUFFIX", "DOMAIN-KEYWORD": "HOST-KEYWORD",
         "IP-CIDR": "IP-CIDR", "IP-CIDR6": "IP-CIDR", "USER-AGENT": "USER-AGENT"}
    def f(t, v):
        if t not in m: return None
        return f"{m[t]},{v},{policy}"
    return f

def build():
    log = ["# PLATFORM-LOG", "", "各平台由 Surge canonical 列表转换；丢弃数 = 该平台不支持的规则类型。", ""]
    all_rows = {name: parse(f) for name, f in SOURCES.items()}
    all_rows["merged/ads"] = parse_ads()
    for name, rows in all_rows.items():
        grouped = group_sections(rows)
        rel = name + ".list"
        stats = {}
        def run(platform, conv, suffix=".list"):
            kept = collections.OrderedDict(); dropped = 0
            for sec, rs in grouped.items():
                out = [c for t, v in rs if (c := conv(t, v)) is not None]
                dropped += len(rs) - len(out)
                if out: kept[sec] = [(None, None)] and out
            # write_grouped 需要 (t,v) 形式，这里直接写已格式化行
            p = OUT / platform / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            lines = [f"# {platform}/{rel} — 由 surge-rules 自动转换（源：rules/{rel}）"]
            total = 0
            for sec, rs in grouped.items():
                out = [c for t, v in rs if (c := conv(t, v)) is not None]
                if not out: continue
                total += len(out)
                lines.append(f"\n# ── {sec}（{len(out)} 条）──")
                lines += out
            p.write_text("\n".join(lines) + "\n", encoding="utf-8")
            stats[platform] = (total, dropped)
        run("clash", conv_clash)
        run("loon", conv_loon)
        run("shadowrocket", conv_sr)
        policy = QX_POLICY.get(name, name.split("/")[-1].capitalize())
        run("quantumultx", make_qx(policy))
        # v2ray geosite（仅域名类）+ IP 另存
        p = OUT / "v2ray" / rel; p.parent.mkdir(parents=True, exist_ok=True)
        lines = [f"# v2ray/{rel} — geosite 源格式（domain:/full:/keyword:/regexp:），由 surge-rules 自动转换"]
        total = 0; ips = []
        for sec, rs in grouped.items():
            out = []
            for t, v in rs:
                if t == "DOMAIN": out.append(f"full:{v}")
                elif t == "DOMAIN-SUFFIX": out.append(f"domain:{v}")
                elif t == "DOMAIN-KEYWORD": out.append(f"keyword:{v}")
                elif t == "URL-REGEX": out.append(f"regexp:{v}")
                elif t in ("IP-CIDR", "IP-CIDR6"): ips.append(v)
            if out:
                total += len(out)
                lines.append(f"\n# ── {sec}（{len(out)} 条）──"); lines += out
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        if ips:
            (OUT / "v2ray" / (name + "-ip.txt")).write_text("\n".join(sorted(set(ips))) + "\n", encoding="utf-8")
        stats["v2ray"] = (total, len(rows) - total - len(ips))
        # sing-box JSON
        rule = {"domain": [], "domain_suffix": [], "domain_keyword": [], "domain_regex": [], "ip_cidr": [], "process_name": []}
        m = {"DOMAIN": "domain", "DOMAIN-SUFFIX": "domain_suffix", "DOMAIN-KEYWORD": "domain_keyword",
             "URL-REGEX": "domain_regex", "IP-CIDR": "ip_cidr", "IP-CIDR6": "ip_cidr", "PROCESS-NAME": "process_name"}
        dropped = 0
        for _, t, v in rows:
            if t in m: rule[m[t]].append(v)
            else: dropped += 1
        rule = {k: sorted(set(v)) for k, v in rule.items() if v}
        pj = OUT / "singbox" / (name + ".json"); pj.parent.mkdir(parents=True, exist_ok=True)
        pj.write_text(json.dumps({"version": 1, "rules": [rule]}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        stats["singbox"] = (sum(len(v) for v in rule.values()), dropped)
        log.append(f"- {rel}（源 {len(rows)} 条）： " + "；".join(f"{k} {v[0]} 条/丢 {v[1]}" for k, v in stats.items()))
    (ROOT / "PLATFORM-LOG.md").write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"platforms built for {len(all_rows)} lists")

if __name__ == "__main__":
    build()
