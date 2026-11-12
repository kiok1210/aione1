# AIONE1 · 姚毛毛的工具与创作

让好用的工具，安静地陪你创造。

个人工具目录，暖白与深绿配色，响应式设计。包含工具分类、实时搜索、项目状态与关于自己。主站使用静态 HTML / CSS / JavaScript，无外部字体、CDN 和追踪脚本。管理接口与数字人口播后端使用 Python，前端由 Nginx 统一托管。

## 工具目录

| 分类 | 项目 | 入口 |
| --- | --- | --- |
| 声音与影像 | musicForYou | https://github.com/kiok1210/musicForYou |
| 声音与影像 | bokeForYou | https://github.com/kiok1210/bokeForYou |
| 声音与影像 | videoForYou | https://github.com/kiok1210/videoForYou |
| 声音与影像 | 数字人口播 | https://github.com/kiok1210/digital-human |
| 文字与创作 | 青灯 | https://github.com/kiok1210/qingdeng |
| 文字与创作 | 六宝 | https://github.com/kiok1210/liubao |
| 连接与效率 | lumen remote | https://github.com/kiok1210/lumen-remote |
| 连接与效率 | 渡口 | https://github.com/kiok1210/dukou |

青灯、lumen remote、渡口为预留仓库，源码由作者后续在其他机器上传。网页如实标注状态，不提供虚假下载。

## 本地预览

```powershell
python scripts/build_site.py
python scripts/preview.py
```

访问 http://127.0.0.1:5178 。工具数据与文案在 `scripts/build_site.py`，生成 `dist/index.html`、`dist/about.html` 和 `dist/tools.json`。样式与交互分别在 `dist/assets/site.css`、`dist/assets/site.js`。

六宝阅读入口 `/liubao/` 在生产 Nginx 中映射到已部署的故事馆，普通静态预览没有完整漫画资源。

## 更新

每个工具先进入站内独立宣传页。音乐、播客和录屏另有基础网页版本，完整 Electron 功能由客户端提供。网页由 Nginx 托管，无 Node 常驻服务；数字人口播模型与推理服务需另行部署。

管理入口为 `/admin/`：口令验证后，可预览并应用各工具的宣传页、静态页面或本机后端转发。一个 Python 管理服务负责口令校验、`nginx -t` 和重载，失败自动回滚。公网 HTTP 管理操作关闭；使用 HTTPS 或 SSH 隧道。

Windows / Linux 静态配置生成器：`python scripts/generate_nginx.py --root <dist绝对路径> --output <nginx配置文件>`。完整说明见 [部署文档](docs/deployment.md)。

修改内容后运行构建脚本，将 `dist/` 部署到静态服务器。当前服务器使用版本目录与 `current` 软链接，发布脚本见 `scripts/deploy.py`。SSH 私钥通过本机路径参数提供，不写入仓库。

域名与部署状态见 `docs/deployment.md`。三个预留项目上传源码后，更新构建脚本中的项目状态、说明与入口，再重新构建和部署。

## 已接入曲库与工具

音乐与有声书共 9 条、播客 5 条，默认从服务器曲库播放，支持分类、搜索、收藏和浏览器续听。录屏原生输出 MP4；六宝接入完整故事馆；数字人使用原有工作台和 Python API，生成能力取决于后端模型状态。

本地预览会映射真实下载文件、漫画资源及口播 API。Linux 架构、模型缺项、DNS 与管理口令使用方式见 docs/deployment.md。
