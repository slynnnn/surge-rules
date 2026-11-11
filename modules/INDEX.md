# 模块索引（精选自上游，按需在客户端里逐个添加）

本文件由 `scripts/build_modules.py` 从 [modules.yaml](../modules.yaml) 生成，勿手改。
模块不打包复制：一律直引上游原仓链接（多数模块仓无许可证或含脚本，直引才能跟随上游修复）。

## 去广告（12）

| 名称 | 作用 | 适用软件 | MITM 主机名 | 链接 | 来源 |
|---|---|---|---|---|---|
| 广告拦截（完整） | blackmatrix7 全量去广告重写（MITM） | Surge | 模块自带大名单 | [直引](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rewrite/Surge/Advertising/Advertising.sgmodule) | blackmatrix7/ios_rule_script |
| 广告拦截（轻量） | blackmatrix7 轻量去广告，规则量小、误杀少 | Surge | 模块自带名单 | [直引](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rewrite/Surge/AdvertisingLite/AdvertisingLite.sgmodule) | blackmatrix7/ios_rule_script |
| Sukka 增强去广告 | Sukka 的去广告增强模块，配合其 reject 规则集 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/SukkaW/Surge/master/Modules/sukka_enhance_adblock.sgmodule) | SukkaW/Surge |
| 通用去广告（adsense） | app2smile 通用广告清理模块 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/app2smile/rules/master/module/adsense.sgmodule) | app2smile/rules |
| Bilibili 去广告/增强 | app2smile 哔哩哔哩去广告与功能增强 | Surge | app.bilibili.com, grpc.biliapi.net | [直引](https://raw.githubusercontent.com/app2smile/rules/master/module/bilibili.sgmodule) | app2smile/rules |
| Bilibili Helper | Maasea 的 B 站辅助模块（去广告/增强） | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/Maasea/sgmodule/master/Bilibili.Helper.sgmodule) | Maasea/sgmodule |
| 微博去广告 | Rabbit-Spec 微博去广告模块 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/Rabbit-Spec/Surge/Master/Module/Spec/Weibo/Moore/Weibo.sgmodule) | Rabbit-Spec/Surge |
| 知乎去广告（Loon 插件） | app2smile 知乎去广告插件（Rabbit-Spec 的 Surge 版已被上游删除，改收此条） | Loon | 随插件声明 | [直引](https://raw.githubusercontent.com/app2smile/rules/master/plugin/zhihu.plugin) | app2smile/rules |
| 贴吧去广告 | Rabbit-Spec 百度贴吧去广告模块 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/Rabbit-Spec/Surge/Master/Module/Spec/Tieba/Moore/Tieba.sgmodule) | Rabbit-Spec/Surge |
| 贴吧 Mini | app2smile 贴吧精简去广告 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/app2smile/rules/master/module/tieba-mini.sgmodule) | app2smile/rules |
| QQ 新闻去广告 | app2smile 腾讯新闻去广告 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/app2smile/rules/master/module/qqnews.sgmodule) | app2smile/rules |
| YouTube 去广告（Loon 插件） | app2smile 的 YouTube 去广告插件 | Loon | 随插件声明 | [直引](https://raw.githubusercontent.com/app2smile/rules/master/plugin/youtube.plugin) | app2smile/rules |

## 重写增强（5）

| 名称 | 作用 | 适用软件 | MITM 主机名 | 链接 | 来源 |
|---|---|---|---|---|---|
| 通用重写 | blackmatrix7 通用 URL 重写集合 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rewrite/Surge/General/General.sgmodule) | blackmatrix7/ios_rule_script |
| URL Rewrite 增强 | Maasea 的常用重写合集 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/Maasea/sgmodule/master/URLRewrite.sgmodule) | Maasea/sgmodule |
| Google CN 307 跳转 | Sukka：google.cn/g.cn 强制 307 到国际版 | Surge | g.cn, www.g.cn, google.cn, www.google.cn | [直引](https://raw.githubusercontent.com/SukkaW/Surge/master/Modules/google_cn_307.sgmodule) | SukkaW/Surge |
| 百度不重定向 | app2smile：百度搜索结果去跳转跟踪 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/app2smile/rules/master/module/baidu-no-redirect.sgmodule) | app2smile/rules |
| Google 重写 | Rabbit-Spec 的 Google 相关重写 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/Rabbit-Spec/Surge/Master/Module/Spec/GoogleRewrite/Moore/GoogleRewrite.sgmodule) | Rabbit-Spec/Surge |

## 应用解锁（6）

| 名称 | 作用 | 适用软件 | MITM 主机名 | 链接 | 来源 |
|---|---|---|---|---|---|
| Spotify 解锁 | app2smile：Spotify 功能解锁（.module 版） | Shadowrocket / Stash | 随模块声明 | [直引](https://raw.githubusercontent.com/app2smile/rules/master/module/spotify.module) | app2smile/rules |
| Spotify 解锁（Loon 插件） | app2smile：Spotify 解锁的 Loon 版 | Loon | 随插件声明 | [直引](https://raw.githubusercontent.com/app2smile/rules/master/plugin/spotify.plugin) | app2smile/rules |
| YouTube Enhance | Maasea：YouTube 功能增强/解锁 | Surge | *.googlevideo.com, youtubei.googleapis.com | [直引](https://raw.githubusercontent.com/Maasea/sgmodule/master/YouTube.Enhance.sgmodule) | Maasea/sgmodule |
| 微信读书解锁 | Maasea：WeRead 解锁/增强 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/Maasea/sgmodule/master/WeRead.sgmodule) | Maasea/sgmodule |
| 起点读书 | app2smile：起点读书去广告/解锁 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/app2smile/rules/master/module/qidian.sgmodule) | app2smile/rules |
| 百度地图 | app2smile：百度地图去广告/增强 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/app2smile/rules/master/module/baidumap.sgmodule) | app2smile/rules |

## 其他（14）

| 名称 | 作用 | 适用软件 | MITM 主机名 | 链接 | 来源 |
|---|---|---|---|---|---|
| Sub-Store | Rabbit-Spec：订阅管理前端模块 | Surge | 不需要 | [直引](https://raw.githubusercontent.com/Rabbit-Spec/Surge/Master/Module/Spec/Sub-Store/Moore/Sub-Store.sgmodule) | Rabbit-Spec/Surge |
| TestFlight 管理 | Rabbit-Spec：TestFlight 相关增强 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/Rabbit-Spec/Surge/Master/Module/Spec/TestFlight/Moore/TestFlight.sgmodule) | Rabbit-Spec/Surge |
| 京东比价 | Rabbit-Spec：京东历史价格显示 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/Rabbit-Spec/Surge/Master/Module/Spec/JD_Price/Moore/JD_Price.sgmodule) | Rabbit-Spec/Surge |
| DoH 增强 | Rabbit-Spec：加密 DNS 模块（Ali-DoH 版） | Surge | 不需要 | [直引](https://raw.githubusercontent.com/Rabbit-Spec/Surge/Master/Module/Spec/DoH/Moore/Ali-DoH.sgmodule) | Rabbit-Spec/Surge |
| DNS over QUIC | Rabbit-Spec：DoQ 支持模块（Ali-DoQ 版） | Surge | 不需要 | [直引](https://raw.githubusercontent.com/Rabbit-Spec/Surge/Master/Module/Spec/DNS-QUIC/Moore/Ali-DoQ.sgmodule) | Rabbit-Spec/Surge |
| 隐藏 VPN 图标 | Rabbit-Spec：状态栏 VPN 图标隐藏 | Surge | 不需要 | [直引](https://raw.githubusercontent.com/Rabbit-Spec/Surge/Master/Module/Spec/Hide-VPN-Icon/Moore/Hide-VPN-Icon.sgmodule) | Rabbit-Spec/Surge |
| Alidns | Maasea：阿里 DNS 相关模块 | Surge | 不需要 | [直引](https://raw.githubusercontent.com/Maasea/sgmodule/master/Alidns.sgmodule) | Maasea/sgmodule |
| SRSS | Maasea：RSS 订阅提醒脚本模块 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/Maasea/sgmodule/master/SRSS.sgmodule) | Maasea/sgmodule |
| 网易云更新检查禁用 | Sukka：禁止网易云音乐检查更新弹窗 | Surge | 随模块声明 | [直引](https://raw.githubusercontent.com/SukkaW/Surge/master/Modules/sukka_disable_netease_music_v2_update_check.sgmodule) | SukkaW/Surge |
| MITM 全主机名（工具） | Sukka：调试用，一键放行全部 MITM 主机名 | Surge | * | [直引](https://raw.githubusercontent.com/SukkaW/Surge/master/Modules/sukka_mitm_all_hostnames.sgmodule) | SukkaW/Surge |
| NobyDa 脚本模块库 | NobyDa 的 Surge 脚本/模块目录（签到、比价等，GPL-3.0） | Surge | 随模块声明 | [直引](https://github.com/NobyDa/Script/tree/master/Surge) | NobyDa/Script |
| Shadowrocket 模块/配置聚合 | LOWERTOP 的小火箭模块与配置导航页（无许可证，仅索引） | Shadowrocket | 随模块声明 | [直引](https://github.com/LOWERTOP/Shadowrocket) | LOWERTOP/Shadowrocket |
| Quantumult X 资源库 | KOP-XIAO 的 QX 规则/重写/脚本资源库（无许可证，仅索引） | Quantumult X | 随资源声明 | [直引](https://github.com/KOP-XIAO/QuantumultX) | KOP-XIAO/QuantumultX |
| QX 规则与重写库 | zqzess 的 Quantumult X 规则/重写集合（无许可证，仅索引） | Quantumult X | 随资源声明 | [直引](https://github.com/zqzess/rule_for_quantumultx) | zqzess/rule_for_quantumultX |

## 说明

- 开模块前先在配置里开启 MITM 并安装、信任 CA 证书（需要 MITM 的模块才生效）。
- 模块与规则若同名冲突，以模块为先排查。
- 链接存活由 `scripts/verify.py` 每周巡检，失效项记入 VERIFY-LOG.md。
