#!/usr/bin/env python3
"""模块索引生成：读 modules.yaml -> 写 modules/INDEX.md（按用途分类的表格）。
模块一律只索引直引、不复制本体；本脚本由 build.py 在构建末尾调用，也可单独跑。
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load():
    try:
        import yaml
        return yaml.safe_load((ROOT / "modules.yaml").read_text(encoding="utf-8"))
    except ImportError:
        raise SystemExit("需要 pyyaml 才能生成模块索引")


def main():
    data = load()
    cats = data["categories"]
    mods = data["modules"]
    lines = ["# 模块索引（精选自上游，按需在客户端里逐个添加）", "",
             "本文件由 `scripts/build_modules.py` 从 [modules.yaml](../modules.yaml) 生成，勿手改。",
             "模块不打包复制：一律直引上游原仓链接（多数模块仓无许可证或含脚本，直引才能跟随上游修复）。", ""]
    total = 0
    for key in ["ads", "rewrite", "unlock", "other"]:
        rows = [m for m in mods if m["category"] == key]
        if not rows:
            continue
        total += len(rows)
        lines += [f"## {cats[key]}（{len(rows)}）", "",
                  "| 名称 | 作用 | 适用软件 | MITM 主机名 | 链接 | 来源 |",
                  "|---|---|---|---|---|---|"]
        for m in rows:
            lines.append(f"| {m['name']} | {m['desc']} | {m['software']} | {m['mitm']} | [直引]({m['url']}) | {m['source']} |")
        lines.append("")
    lines += ["## 说明", "",
              "- 开模块前先在配置里开启 MITM 并安装、信任 CA 证书（需要 MITM 的模块才生效）。",
              "- 模块与规则若同名冲突，以模块为先排查。",
              "- 链接存活由 `scripts/verify.py` 每周巡检，失效项记入 VERIFY-LOG.md。"]
    (ROOT / "modules" / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"modules index: {total} entries")


if __name__ == "__main__":
    main()
