# surge-rules — Ochiai 自用 Surge 规则仓（四源合一）

把四个公开项目按各自最擅长的部分合并成一套自己用的 Surge 配置：

| 上游 | 许可证 | 在本仓的角色 |
|---|---|---|
| [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | GPL-2.0 | 主力分应用规则 + 29 万广告域名集 + 重写模块 |
| [Loyalsoldier/surge-rules](https://github.com/Loyalsoldier/surge-rules) | GPL-3.0 | 基础分流骨架（reject/apple/google/proxy/direct/gfw 等，每日更新、配置直引） |
| [LceAn/proxy-filter-rules](https://github.com/LceAn/proxy-filter-rules) | Apache-2.0 | 细分应用规则补充（与 blackmatrix7 高度同源，国内应用有增量） |
| [Rabbit-Spec/Surge](https://github.com/Rabbit-Spec/Surge) | 未声明 | 配置参考 + AIGC/GlobalMedia/China 规则补充 + 模块库索引（只索引、不复制） |

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

由 `scripts/build.py` 抓四源指定清单、规范化（去策略后缀与注释）、跨源去重后生成，明细见 [BUILD-LOG.md](BUILD-LOG.md)：

| 文件 | 用途 | 条数（2026-11-11 构建） |
|---|---|---|
| `rules/merged/ai.list` | OpenAI/Claude/Gemini 等 AI 服务 | 107 |
| `rules/merged/streaming.list` | Netflix/YouTube/Disney/Spotify/TikTok 等 | 4,993 |
| `rules/merged/social.list` | Telegram/Twitter/Facebook/Instagram/WhatsApp | 704 |
| `rules/merged/global.list` | Apple/Google/Microsoft/GitHub/PayPal/Steam 等 | 6,574 |
| `rules/merged/china.list` | 国内应用与站点直连 | 6,803 |
| `rules/merged/ads.txt` | 广告域名集（DOMAIN-SET 引用，Surge 字典树加载） | 290,392 个域名 |

细分类条数（同次构建）：服务——YouTube 195、Netflix 1,630、Disney 251、Spotify 43、TikTok 67、Bilibili 140、Telegram 57、Twitter/X 33、Facebook 593、Instagram 76、WhatsApp 30、Google 1,201、Apple 4,172、Microsoft 856、GitHub 31、PayPal 249、Steam 69、OpenAI 35、Claude 3、Gemini 14、Copilot 51；企业——Google 1,399、Meta 617、Microsoft 906、Apple 4,172。

Loyalsoldier 的基础集不在本地合并：其 release 分支每日自动更新，配置里直引原仓地址，新鲜度更好。

## 模块

见 [modules/INDEX.md](modules/INDEX.md)：精选 blackmatrix7 重写模块与 Rabbit-Spec 模块库，按需逐个在 Surge 里添加（直引上游，跟随上游修复）。

## 维护

- 维护者：Lady（Ochiai 的助手）长期负责。
- 合并规则定期重跑 `scripts/build.py` 刷新并提交；上游结构变化时同步修订构建脚本与配置引用。
- 机器可读的来源与用法清单：[sources.yaml](sources.yaml)。

## 许可证

GPL-3.0（取四源中最严格者）。各上游内容版权归原作者所有，见上表链接。
