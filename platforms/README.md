# 分平台规则

同一套合并规则（`rules/` 的 Surge 版为唯一数据源）自动转换到六个平台，每周随主构建一起更新。各平台不支持的规则类型会丢弃，逐份丢弃数见 [PLATFORM-LOG.md](../PLATFORM-LOG.md)。

| 平台目录 | 客户端 | 格式与用法 |
|---|---|---|
| `clash/` | Clash Verge Rev、Mihomo Party、FlClash、Sparkle（Windows/macOS/Android） | mihomo classical 文本：`RULE-SET,<本目录文件地址>,<策略组>,behavior=classical` 或 rule-provider `format: text` |
| `loon/` | Loon（iOS） | 远程规则直接订阅，语法与 Surge 基本一致（IP-CIDR6 已并入 IP-CIDR） |
| `shadowrocket/` | Shadowrocket（iOS） | 远程规则集直接订阅，语法与 Surge 基本一致（差异见下方专节）；小火箭原生大表另见 `extended/johnshall-adblock.list` 的 shadowrocket 转换版 |
| `quantumultx/` | Quantumult X（iOS） | filter_remote 格式：`HOST-SUFFIX,域名,策略名`。行尾策略名是占位（AI/Streaming/…/服务名），导入时用资源解析器改成你自己的策略名，或开 force-policy 统一指定 |
| `v2ray/` | v2rayN（Windows）、v2rayNG（Android） | geosite 源格式（`domain:`/`full:`/`keyword:`/`regexp:`），可编译进 geosite.dat 或作自定义路由域名表；IP 段在同名 `-ip.txt` |
| `singbox/` | sing-box、Hiddify、Karing、NekoBox、GUI.for.SingBox | rule-set JSON（version 1），`rule_set` 远程引用即可 |

## 扩展集（extended/）

`rules/extended/` 的全量大表（hosts 大表、geosite 分类、GFWList 等）同样自动转换到各平台的 `extended/` 子目录，用法与主集相同、按需单独引用，不进主配置默认链。各份来源与条数见 [rules/extended/README.md](../rules/extended/README.md)。

## Shadowrocket 兼容性说明

- 转换口径（`conv_sr`）：丢弃 `PROCESS-NAME` 与逻辑复合规则（`AND/OR/NOT`）——小火箭不支持进程规则，复合规则支持也不完整；其余类型（DOMAIN / DOMAIN-SUFFIX / DOMAIN-KEYWORD / IP-CIDR / IP-CIDR6 / IP-ASN / GEOIP / USER-AGENT / URL-REGEX / DEST-PORT / HOSTNAME-TYPE / SRC-IP-CIDR）原样保留，逐份丢弃数见 PLATFORM-LOG.md。
- `USER-AGENT`、`URL-REGEX` 在小火箭里仅对 HTTP/HTTPS 流量生效（需开 MITM 才全量），与 Surge 行为一致，不是转换缺陷。
- 小火箭对超大规则集（如 extended 的 20 万级 typed 表）加载较慢且占内存，iOS 设备上建议优先用域名集型（`.txt` 的 DOMAIN-SET 等价引用）或主集 ads.txt，不要整表 typed 引用。
- Shadowrocket 原生来源：去广告大表源 Johnshall（CC-BY-SA-4.0）已并入 extended；其懒人配置（lazy.conf 系列）与 LOWERTOP 模块聚合只做索引，见 modules/INDEX.md 与 sources.yaml。

## Windows 上用什么（2026-11 时点）

- **Clash Verge Rev**（mihomo 内核）：Windows 首选。snell、anytls 节点都原生支持，直接吃 `clash/` 规则。
- **Mihomo Party / FlClash / Sparkle**：同为 mihomo 图形端，界面风格不同，规则通用。
- **v2rayN**：老牌全能，Xray/sing-box 双内核，吃 `v2ray/` 或 `singbox/` 规则；注意其内核**不支持 snell**，snell 节点用不了。
- **Hiddify / Karing**：sing-box 内核、界面现代，吃 `singbox/` 规则；同样不支持 snell。
- 一句话：节点是 snell/anytls 的，Windows 上选 mihomo 系（Clash Verge Rev 等）。
