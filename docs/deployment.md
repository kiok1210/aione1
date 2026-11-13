# AIONE1 部署说明

作者：姚毛毛。目标域名：aione1.com / www.aione1.com。

## Linux 生产目录

- /opt/aione1/current：指向最新版本的 dist。
- /opt/aione1/releases/：发布历史，保留回滚。
- /opt/aione1/downloads/：实际安装包、数字人源码包、SHA-256 校验值。
- /opt/aione1/routes.conf：管理器生成的工具路由，包含在 Nginx server 块内。
- /opt/aione1/private/：口令哈希与路由数据，仅 root 可读，不在静态目录内。
- /opt/budayang-comics/current：原有六宝作品与漫画资源，通过 /liubao/ 访问。
- /opt/budayang-comics/nginx.conf：实际运行的 Nginx 配置，部署前自动备份。

网页全部由 Nginx 托管，无 Node 常驻服务。可视化管理员使用一个监听 127.0.0.1:9180 的 Python 标准库服务 aione1-admin.service。

## 页面与真实能力

| 路径 | 能力 |
| --- | --- |
| / | 工具目录、搜索与筛选 |
| /about.html | 关于姚毛毛与建站初衷 |
| /tools/{id}/ | 8 个独立宣传页 |
| /apps/music/ | 预置 9 条音乐与有声书，分类、搜索、收藏、续听、倍速 |
| /apps/podcast/ | 预置 5 条播客，搜索、收藏、续听、倍速 |
| /apps/video/ | 网页基础录屏：共享、可选麦克风、暂停、预览、下载 |
| /liubao/ | 完整在线文学漫画故事馆 |
| /use/{id}/ | 实际下载与部署步骤 |
| /admin/ | 口令保护的可视化 Nginx 管理 |

网页播放器使用已有下载曲库，打开即可播放；不是本地上传播放器。YouTube 搜索、新增缓存、歌词和字幕等完整能力仍由客户端提供。基础录屏使用原生 MP4 编码，浏览器不支持时明确提示而不改后缀伪装。录屏要求 HTTPS 或 localhost。

数字人口播提供原有完整工作台前端与一个 Python 后端，静态页面由 Nginx 提供，API 转发到 7860。Linux VPS 尚未安装模型与推理引擎，工作台如实展示环境缺项并禁用生成。本机预览接入原有已安装的本机后端。lumen remote、渡口和青灯等待作者从其他机器上传源码。

曲库音频与封面独立存储于 /opt/aione1/media，当前版本 dist/media 指向它；媒体不提交 GitHub。仅导出 library.json 中引用的文件，不导出 Cookie、账号配置或个人播放历史。同步命令为 python scripts/sync_media.py --key <SSH私钥路径>。前端 dist 压缩包不包含大体积媒体，需同时保留媒体目录。

完整本地预览使用 python scripts/preview.py，映射六宝、实际下载文件及数字人后端；直接使用普通静态服务器不具备这些外部目录映射。

## DNS 与 HTTPS

本次检查未取得 aione1.com 的有效 A 记录。需要在 DNS 管理台设置：

| 类型 | 主机记录 | 值 |
| --- | --- | --- |
| A | @ | 8.133.244.26 |
| A | www | 8.133.244.26 |

Nginx 已包含两个域名。DNS 生效后还需安装有效 TLS 证书并配置 443；当前不宣称 HTTPS 上线。

实际公网 Host 测试中，aione1.com 返回阿里云 Beaver 的 403 页面，标题为 Non-compliance ICP Filing。服务器内用该 Host 访问 Nginx 正常；域名还存在云端备案接入拦截，不能仅凭 Nginx 配置宣称域名已经上线。当前可用入口是 http://8.133.244.26/ 。

管理操作只允许 HTTPS 或 SSH 隧道访问。公网 HTTP 可看到登录页，但不能提交口令、修改配置。当前使用：

    ssh -i C:\Users\Administrator\.ssh\vinylbox_server -L 18082:127.0.0.1:80 root@8.133.244.26

随后访问 http://127.0.0.1:18082/admin/ 。随机口令在本机 local-admin-credentials.md，已被 Git 排除；服务器只保存 PBKDF2-SHA256 哈希。

## 可视化配置

8 个工具均可选择宣传页或本机后端端口；有静态构建的项目可选静态 dist。代理端口限本机 1024–65535，排除管理服务自身，不接受任意配置文本或文件路径。

先预览，再应用。服务端执行 nginx -t，通过后重载，失败恢复原配置。登录失败限速，使用 HttpOnly / SameSite Cookie，修改需要 CSRF Token。推理后端等资源型服务应自行设置访问控制后再对外转发。

## Linux 更新

    python scripts/build_site.py
    python scripts/test_admin.py
    python scripts/package.py
    python scripts/deploy.py --key C:\Users\Administrator\.ssh\vinylbox_server

仅更新页面加 --skip-downloads。已有口令与路由不会被后续发布覆盖。

## Windows / 其他 Linux

dist 无平台相关运行时，可复制到任意 Nginx 服务器。本地预览：

    python -m http.server 5178 --directory dist

Windows 安装 Nginx 后，将生成文件放在其 conf 目录，便于 include mime.types：

    python scripts/generate_nginx.py --root C:\aione1\dist --output C:\nginx\conf\aione1.conf --port 8080
    C:\nginx\nginx.exe -p C:\nginx\ -c conf\aione1.conf

Linux 同样可用生成器，或在虚拟主机中设置 root 为 dist。此便携静态配置不包含 Linux 专用的 systemd 管理后端、漫画高清原图和安装包，这些需单独接入。

本机执行 build_content.py 后，dist 内也有完整漫画与下载目录；build_media.py 接入原有音频与封面。package.py --with-content 可另外输出包含这些内容的 aione1-complete-dist.zip，供 Windows / Linux 静态迁移。该内容包与媒体不提交 GitHub。

当前 VPS 为 2 核、约 1.6 GB 内存，检查时可用内存约 399 MB，同时承担既有服务。数字人 Python API 已启动，但完整模型推理环境尚未安装；本次未在该服务器强行安装和运行大型推理模型。工作台会显示真实缺项并禁用生成，本机已安装引擎的工作台仍可使用。

## 回滚

将 current 切回 releases 下旧版本的 dist，执行 nginx -t -c /opt/budayang-comics/nginx.conf 后重载 budayang-comics。完整配置备份为 nginx.conf.before-aione1-<版本>。不要删除现有漫画目录。

## 青灯与阅读体验更新

已确认现有青灯源码位于 /home/ymm/qingdeng，入口 server.mjs，另有 server 与 public 目录。现有服务使用根路径登录，因此站内 /apps/qingdeng/ 跳转到原有 http://8.133.244.26:4317/，保留登录、Cookie 和资源路径。原服务未重装或改动，源码尚未同步到 GitHub 预留仓库。

字体统一为正文 16px、说明与标签最小 14px，并加深浅色文字；手机导航换行。博客园已加入导航和关于页面。

原本机 18081 端口现被其他下载服务占用，管理隧道改为只绑定 127.0.0.1:18082；已核验其 session 接口返回 transportAllowed=true。
