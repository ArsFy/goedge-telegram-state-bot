# Goedge Telegram Bot

> GoEdge 是一个开源的 CDN 集群管理套件：https://github.com/TeaOSLab/EdgeAdmin

![](https://img.shields.io/badge/license-MIT-blue)
![](https://img.shields.io/badge/Python->=3.7-blue)
![](https://img.shields.io/badge/PRs-welcome-green)

这是一个适用 GoEdge API 的 Telegram Bot，它可以用于查询数据，和一些简单管理。

## 开发进度

- `/start` 关于这个 Bot
- `/goedge` GoEdge 的简要资讯
- `/d15` 15 天流量统计图
- `/h24` 24 小时流量统计图
- `/node_cpu` 集群节点 CPU 占用统计图
- `/node_memory` 集群节点记忆体占用统计图
- `/node_load` 集群节点负载统计图
- `/nodelist` 列出所有节点

## Start

### 1. 配置 GoEdge API

请阅读官方 Docs 启用 HTTP API: https://goedge.cn/docs/API/Settings.md

### 2. 创建 GoEdge AccessKey / AccessKeyId

- 创建新系统用户（可选）
- 创建 API AccessKey

![image](https://user-images.githubusercontent.com/93700457/206788246-a784e297-0b5f-46b6-9416-78b9deb760e1.png)

### 3. 配置 `config.json`

- 重新命名 `config.example.json` 爲 `config.json`

```js
{
    "bot_token": "123456:abcdefgabcdefg",   // Telegram Bot Token
    "host": "http://goedge.test.com:8080",  // HTTP API
    "auth": {
        "type": "admin",      // 毋需修改
        "accessKeyId": "",    // 上面申請的 accessKeyId
        "accessKey": ""       // 上面申請的 accessKey
    }
}
```

### 4. Run

```bash
python3 main.py
```