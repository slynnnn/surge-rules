# 验证状态

本仓的验证分三层，诚实标注每一层验到什么程度。最近一轮机器验证结果见 [VERIFY-LOG.md](VERIFY-LOG.md)。

## 第一层：机器验证（常设，每周重建后自动跑 `scripts/verify.py`）

- **链接存活**：两份配置引用的全部远程规则集逐个探活，须返回 200
- **格式合法**：全部生成列表逐行扫描，规则类型与形态须合法、无策略后缀残留
- **抽样命中模拟**：24 个代表域名按 Ochiai.conf 的规则顺序模拟匹配，落点须与预期一致；同时列出被多份列表交叉命中的域名（靠顺序裁决的要心里有数，如 chatgpt.com 同时在 AI 与流媒体列表中，因 AI 在前而正确落 AI）
- **条数对账**：构建条数较上次暴跌（>30%）即报警
- **模块链接软巡检**：modules.yaml 全部索引链接逐个探活，失效只记入 VERIFY-LOG 警告、不硬失败（上游模块下线不拖垮规则构建）

机器层证明的是「文件没坏、Surge 能加载、典型域名分得对」，不证明每个域名都分得对。

## 第二层：社区背书（上游）

| 上游 | 背书强度 | 说明 |
|---|---|---|
| Loyalsoldier/surge-rules | 强 | Surge 圈基础集事实标准，每日自动生成、用户量大 |
| blackmatrix7/ios_rule_script | 强 | 分应用规则最大来源，issue 区活跃 |
| SukkaW/Surge | 强 | 业内公认高质量精选集，构建管线公开、更新活跃 |
| privacy-protection-tools/anti-AD | 强 | 中文去广告命中率导向，★10.9k、多格式自动生成 |
| Cats-Team/AdRules | 中强 | 中国区去广告（含 HTTPDNS/PCDN），每日更新 |
| MetaCubeX/meta-rules-dat | 强 | mihomo/sing-box 两大内核共用的 geo 数据库正典 |
| StevenBlack/hosts | 强 | hosts 大表事实标准，★31k |
| AdguardTeam/AdguardSDNSFilter | 强 | AdGuard 官方 DNS 滤表 |
| Johnshall/Shadowrocket-ADBlock-Rules-Forever | 强 | Shadowrocket 生态最知名去广告源，★32k |
| gfwlist/gfwlist | 强 | GFWList 正典源，★25k |
| 217heidai/adblockfilters | 中 | 聚合型大表（每 8 小时自动更新），质量靠去重与分层隔离控制 |
| ACL4SSR/ACL4SSR | 中 | 老牌 Clash 分流集；与 Loyalsoldier 同源度高，本仓只取 BanAD 两份 |
| LceAn/proxy-filter-rules | 中 | 与 blackmatrix7 高度同源，在本仓只作补充 |
| Rabbit-Spec/Surge | 中弱 | 个人自用仓，在本仓只作补充与模块索引 |
| jerryn70/GoodbyeAds | 中弱 | MIT 大表，但 2024-11 后更新放缓，只进扩展集 |

## 第三层：真机验证（只有用户能完成）

规则在 Surge 真机上的实际命中、模块/脚本的实际运行效果，本仓环境无法验证。状态：**待真机**。
用法：日常使用中发现某应用走错组或打不开，反馈现象即可按域名定位到具体规则与小节修复。

## 组件状态一览

| 组件 | 机器验 | 社区背书 | 真机验 |
|---|---|---|---|
| rules/merged 五大类 | ✓ 每周 | ✓ 强（BM7/Loyalsoldier 为主源） | 待 |
| rules/service 21 份 | ✓ 每周 | ✓ | 待 |
| rules/company 4 份 | ✓ 每周 | ✓ | 待 |
| rules/merged/ads.txt | ✓ 每周（存活+条数+格式） | ✓ 强（三源：BM7/anti-AD/Cats-Team） | 待 |
| rules/extended/*（20 份） | ✓ 每周（格式逐行扫） | ✓ 中~强（见上表） | 待（扩展集按需引用，未真机全量验） |
| Loyalsoldier 基础集（直引） | ✓ 每周（存活） | ✓ 强 | 待 |
| Surge/Ochiai.conf、Ochiai-Detailed.conf | ✓ 每周（引用闭合+抽样落点） | — | 待 |
| modules.yaml / modules/INDEX.md 索引的模块（37 条） | ✓ 每周（链接存活软巡检，失效记入 VERIFY-LOG） | 上游自述 | **未验**（需开 MITM 真机跑） |
