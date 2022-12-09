# Goedge Telegram Bot

> Goedge 是一個開源的 CDN 集羣管理套件：https://github.com/TeaOSLab/EdgeAdmin

這是一個適用 Goedge API 的 Telegram Bot，它可以用於查詢數據，和一些簡單管理。

## 開始

### 1. 配置 GoEdge API

請閱讀官方 Docs 啓用 HTTP API: https://goedge.cn/docs/API/Settings.md

### 2. 創建 GoEdge AccessKey / AccessKeyId

- 創建新系統用戶（可選）
- 配置必要權限（可選）
    - 看板
    - 網站服務
    - 邊緣節點
- 創建 API AccessKey

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