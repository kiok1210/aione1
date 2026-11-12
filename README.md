# AIONE1 · 姚毛毛的工具与创作

让好用的工具，安静地陪你创造。

个人工具目录，暖白与深绿配色，响应式设计。包含工具分类、实时搜索、项目状态与关于自己。纯静态 HTML / CSS / JavaScript，无外部字体、CDN、追踪脚本或前端依赖。

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
python -m http.server 5178 --bind 127.0.0.1 --directory dist
```

访问 http://127.0.0.1:5178 。工具数据与文案在 `scripts/build_site.py`，生成 `dist/index.html`、`dist/about.html` 和 `dist/tools.json`。样式与交互分别在 `dist/assets/site.css`、`dist/assets/site.js`。

六宝阅读入口 `/liubao/` 在生产 Nginx 中映射到已部署的故事馆，普通静态预览没有完整漫画资源。

## 更新

修改内容后运行构建脚本，将 `dist/` 部署到静态服务器。当前服务器使用版本目录与 `current` 软链接，发布脚本见 `scripts/deploy.py`。SSH 私钥通过本机路径参数提供，不写入仓库。

域名与部署状态见 `docs/deployment.md`。三个预留项目上传源码后，更新构建脚本中的项目状态、说明与入口，再重新构建和部署。
