# 分平台规则

同一套合并规则（`rules/` 的 Surge 版为唯一数据源）自动转换到六个平台，每周随主构建一起更新。各平台不支持的规则类型会丢弃，逐份丢弃数见 [PLATFORM-LOG.md](../PLATFORM-LOG.md)。

| 平台目录 | 客户端 | 格式与用法 |
|---|---|---|
| `clash/` | Clash Verge Rev、Mihomo Party、FlClash、Sparkle（Windows/macOS/Android） | mihomo classical 文本：`RULE-SET,<本目录文件地址>,<策略组>,behavior=classical` 或 rule-provider `format: text` |
| `loon/` | Loon（iOS） | 远程规则直接订阅，语法与 Surge 基本一致（IP-CIDR6 已并入 IP-CIDR） |
| `shadowrocket/` | Shadowrocket（iOS） | 远程规则集直接订阅，语法与 Surge 基本一致 |
| `quantumultx/` | Quantumult X（iOS） | filter_remote 格式：`HOST-SUFFIX,域名,策略名`。行尾策略名是占位（AI/Streaming/…/服务名），导入时用资源解析器改成你自己的策略名，或开 force-policy 统一指定 |
| `v2ray/` | v2rayN（Windows）、v2rayNG（Android） | geosite 源格式（`domain:`/`full:`/`keyword:`/`regexp:`），可编译进 geosite.dat 或作自定义路由域名表；IP 段在同名 `-ip.txt` |
| `singbox/` | sing-box、Hiddify、Karing、NekoBox、GUI.for.SingBox | rule-set JSON（version 1），`rule_set` 远程引用即可 |

## Windows 上用什么（2026-11 时点）

- **Clash Verge Rev**（mihomo 内核）：Windows 首选。snell、anytls 节点都原生支持，直接吃 `clash/` 规则。
- **Mihomo Party / FlClash / Sparkle**：同为 mihomo 图形端，界面风格不同，规则通用。
- **v2rayN**：老牌全能，Xray/sing-box 双内核，吃 `v2ray/` 或 `singbox/` 规则；注意其内核**不支持 snell**，snell 节点用不了。
- **Hiddify / Karing**：sing-box 内核、界面现代，吃 `singbox/` 规则；同样不支持 snell。
- 一句话：节点是 snell/anytls 的，Windows 上选 mihomo 系（Clash Verge Rev 等）。
