# 模块索引（精选自上游，按需在 Surge 里逐个添加）

模块不打包复制：一是 Rabbit-Spec 未附许可证，二是模块含脚本、直引上游才能及时跟上游修复。

## 去广告 / 重写（blackmatrix7）
- 广告拦截（完整）：`https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rewrite/Surge/Advertising/Advertising_MITM.sgmodule`
- 广告拦截（轻量）：`https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rewrite/Surge/AdvertisingLite/AdvertisingLite_MITM.sgmodule`
- 通用重写：`https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rewrite/Surge/General/General.sgmodule`

> 文件名以仓库实际为准：ios_rule_script 的 rewrite/Surge/<名>/ 目录下 .sgmodule 文件。

## 实用模块（Rabbit-Spec，Module/Spec/）
在 Surge「模块」里粘贴：
`https://raw.githubusercontent.com/Rabbit-Spec/Surge/Master/Module/Spec/<名>.sgmodule`

常用：`Sub-Store`（订阅管理）、`TestFlight`、`Weibo`（微博去广告）、`Bilibili`、`Zhihu`、`Tieba`、`JD_Price`（京东比价）、`DoH`、`DNS-QUIC`、`GoogleRewrite`、`Hide-VPN-Icon`。

## 说明
- 开模块前先在配置里开启 MITM 并安装、信任 CA 证书（需要 MITM 的模块才生效）。
- 模块与规则若同名冲突，以模块为先排查。
