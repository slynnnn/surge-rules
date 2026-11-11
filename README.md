# surge-rules — Ochiai 自用 Surge 规则仓（多源合一）

把各生态的公开规则项目按各自最擅长的部分合并成一套自己用的 Surge 配置。主集合并源：

| 上游 | 许可证 | 在本仓的角色 |
|---|---|---|
| [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | GPL-2.0 | 主力分应用规则 + 广告域名集 + 重写模块 |
| [Loyalsoldier/surge-rules](https://github.com/Loyalsoldier/surge-rules) | GPL-3.0 | 基础分流骨架（reject/apple/google/proxy/direct/gfw 等，每日更新、配置直引） |
| [LceAn/proxy-filter-rules](https://github.com/LceAn/proxy-filter-rules) | Apache-2.0 | 细分应用规则补充（与 blackmatrix7 高度同源，国内应用有增量） |
| [Rabbit-Spec/Surge](https://github.com/Rabbit-Spec/Surge) | 未声明 | 配置参考 + AIGC/GlobalMedia/China 规则补充 + 模块库索引（只索引、不复制） |
| [SukkaW/Surge](https://github.com/SukkaW/Surge)（ruleset.skk.moe） | AGPL-3.0 | 高质量精选集：AI/流媒体/全球/国内/Telegram 增量并入主集 |
| [privacy-protection-tools/anti-AD](https://github.com/privacy-protection-tools/anti-AD) | MIT | 中文去广告大表，域名并入 ads.txt |
| [Cats-Team/AdRules](https://github.com/Cats-Team/AdRules) | 0BSD | 中国区去广告/PCDN/HTTPDNS，域名集并入 ads.txt、全量 typed 进扩展集 |

全量数据库型大表（StevenBlack、GoodbyeAds、AdGuard SDNS、217heidai、GFWList、ACL4SSR、Johnshall、MetaCubeX geosite）单独进[扩展集](rules/extended/README.md)，不灌主配置。无许可证的优质源（KOP-XIAO、zqzess、LOWERTOP 等）只索引不复制，清单见 [sources.yaml](sources.yaml)。

## 一键使用

Surge → 配置 → 从 URL 下载配置：

```
https://raw.githubusercontent.com/slynnnn/surge-rules/main/Surge/Ochiai.conf
```

下载后只做一件事：在配置的「节点选择」策略组里加入你自己的节点或订阅，其余开箱即用。

策略组：`节点选择 / AI / 流媒体 / 社交 / 国内直连 / 广告拦截 / 漏网之鱼`

### 细粒度版（按服务 / 按企业单独选节点）

总版之外另有一套细粒度版，规则内容相同、只是分得更细：

```
https://raw.githubusercontent.com/slynnnn/surge-rules/main/Surge/Ochiai-Detailed.conf
```

多出的独立策略组：
- **按服务**：YouTube、Netflix、Disney、Spotify、TikTok、X、Telegram、GitHub（AI 内部再按 OpenAI/Claude/Gemini/Copilot 分文件、同走 AI 组）
- **按企业**：Google（搜索+YouTube+Gemini 打包）、Meta（Facebook+Instagram+WhatsApp+Threads）、Microsoft（本体+Copilot）、Apple

对应的规则文件在 `rules/service/*.list`（21 个服务）与 `rules/company/*.list`（4 家企业），同样由构建脚本生成，想只引用其中某一份也可以。

## 合并规则（本地生成、自包含）

由 `scripts/build.py` 抓各源指定清单、规范化（去策略后缀与注释）、跨源去重后生成，明细见 [BUILD-LOG.md](BUILD-LOG.md)：

| 文件 | 用途 | 条数（2026-11-11 构建） |
|---|---|---|
| `rules/merged/ai.list` | OpenAI/Claude/Gemini 等 AI 服务 | 143 |
| `rules/merged/streaming.list` | Netflix/YouTube/Disney/Spotify/TikTok 等 | 5,099 |
| `rules/merged/social.list` | Telegram/Twitter/Facebook/Instagram/WhatsApp | 705 |
| `rules/merged/global.list` | Apple/Google/Microsoft/GitHub/PayPal/Steam 等 | 7,736 |
| `rules/merged/china.list` | 国内应用与站点直连 | 6,980 |
| `rules/merged/ads.txt` | 广告域名集（DOMAIN-SET 引用，三源合并：BM7 + anti-AD + Cats-Team） | 426,939 个域名 |

细分类条数（同次构建）：服务——YouTube 195、Netflix 1,630、Disney 251、Spotify 43、TikTok 67、Bilibili 140、Telegram 58、Twitter/X 33、Facebook 593、Instagram 76、WhatsApp 30、Google 1,201、Apple 4,172、Microsoft 856、GitHub 31、PayPal 249、Steam 69、OpenAI 35、Claude 3、Gemini 14、Copilot 51；企业——Google 1,399、Meta 617、Microsoft 906、Apple 4,172。

## 扩展集（rules/extended/）

全量 / 数据库型大表单独产出（20 份，约 125 万条），**不进 Ochiai.conf 默认引用链**，按需单独引用：StevenBlack hosts（77,859）、GoodbyeAds（277,779）、AdGuard SDNS 域名（189,412）、217heidai 域名集（241,657）、GFWList（4,380）、Cats-Team 全量 typed（208,513）、Johnshall 小火箭去广告 typed（52,696）、ACL4SSR BanAD（1,596）、MetaCubeX geosite 12 类（category-ads-all / geolocation-cn / geolocation-!cn / gfw 等）。逐份来源、许可证与引用方式见 [rules/extended/README.md](rules/extended/README.md)，各平台转换版在 `platforms/<平台>/extended/`。

Loyalsoldier 的基础集不在本地合并：其 release 分支每日自动更新，配置里直引原仓地址，新鲜度更好。

## 分平台版本

除 Surge 外，另有 Clash(mihomo) / Loon / Shadowrocket / Quantumult X / v2ray(v2rayN·NG) / sing-box 六个平台的转换版，目录在 `platforms/`，同一数据源自动转换、每周同步更新。导入方法与 Windows 客户端选型见 [platforms/README.md](platforms/README.md)。

## 模块

见 [modules/INDEX.md](modules/INDEX.md)（由 [modules.yaml](modules.yaml) 生成）：37 条精选模块按用途分类——去广告 12 / 重写增强 5 / 应用解锁 6 / 其他 14，来源含 blackmatrix7、Rabbit-Spec、Sukka、app2smile、Maasea、NobyDa 及 Shadowrocket/QX 生态入口。一律只索引、直引上游（跟随上游修复），不复制脚本本体。

## 维护

- 维护者：Lady（Ochiai 的助手）长期负责。
- 合并规则定期重跑 `scripts/build.py` 刷新并提交；上游结构变化时同步修订构建脚本与配置引用。
- 机器可读的来源与用法清单：[sources.yaml](sources.yaml)。

## 许可证

GPL-3.0（取合并源中最严格者）。各上游内容版权归原作者所有、按各自许可证使用（AGPL-3.0 / CC-BY-SA-4.0 等已在来源表与文件头逐项标注），见上表链接与 [sources.yaml](sources.yaml)。
