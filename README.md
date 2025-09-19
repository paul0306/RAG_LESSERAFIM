# LE SSERAFIM Line Bot (RAG-powered)

本專案是一個基於 **LINE Messaging API** 與 **RAG (Retrieval-Augmented Generation)** 技術的聊天機器人。  
機器人能回答關於 **LE SSERAFIM** 以及各成員的相關問題，所有資料皆從 **維基百科** 自動抓取、解析與建立向量資料庫。  

---

## ✨ 功能特色
- 🤖 LINE Bot 即時回覆使用者訊息  
- 📚 自動從維基百科抓取團體與成員資料  
- 🔎 使用 **SentenceTransformers + FAISS** 建立向量資料庫  
- 🧠 透過 **RAG 技術**讓 Gemini API 產生更準確的回答  
- 🌐 支援關鍵字模糊匹配（rapidfuzz），可辨識暱稱、別稱  

---

<!--
## 📸 Demo
以下為 Bot 回答示範（輸入問題 → Bot 回覆）：

![Demo Screenshot](assets/demo.png)

> 💡 請將圖片放在 `assets/` 資料夾，或修改路徑連結。

---
-->

## 🛠️ 技術架構
- **Python 3.10+**
- **LINE Messaging API**
- **SentenceTransformers** (`all-MiniLM-L6-v2`)
- **FAISS**（向量檢索）
- **Gemini API (Google Generative AI)**
- **BeautifulSoup4**（維基百科爬取解析）
- **RapidFuzz**（關鍵字模糊比對）
- **Flask**（LINE Bot Webhook 伺服器）

---

## 🚀 安裝與執行

### 1. Clone 專案
```bash
git clone https://github.com/paul0306/lesserafim-linebot.git
cd lesserafim-linebot
```

### 2. 建立虛擬環境並安裝套件
```bash
python -m venv venv
source venv/bin/activate   # Mac / Linux
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

### 3. 設定環境變數 `.env`
建立 `.env` 檔，內容如下：
```bash
LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 4. 運行程式
```bash
python app.py
```

### 5. 部署（Heroku / Railway / Render）
- 將程式碼推到 GitHub
- 部署至雲端平台，設定環境變數
- 在 LINE Developers 後台設定 Webhook URL