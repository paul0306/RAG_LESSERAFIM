# LE SSERAFIM RAG Line Bot  

一個結合 **LINE Messaging API** 與 **Retrieval-Augmented Generation (RAG)** 技術的聊天機器人 🤖，能夠回答關於韓國女團 **LE SSERAFIM** 以及各個成員的相關問題。  
所有知識資料均來自 **維基百科 (Wikipedia)**，並透過向量檢索與大型語言模型進行整合。  

---

## ✨ 功能特色  

- 📖 **LE SSERAFIM 資訊查詢**：回答團體與各成員的背景、經歷、作品等問題。  
- 🔍 **RAG 技術支援**：結合向量資料庫與大語言模型，提升回答的準確性與可解釋性。  
- 💬 **LINE Bot 整合**：用戶可以直接在 LINE 上與機器人互動。

---

## 🛠 技術架構  

- **語言**：Python  
- **框架**：LINE Messaging API SDK  
- **RAG**：  
  - Embedding 模型（例：OpenAI / Sentence Transformers）  
  - 向量資料庫（例：FAISS / Chroma）  
- **資料來源**：Wikipedia  
- **部署**：可於本地或雲端（Heroku / Vercel / Railway / GCP / AWS 等）運行  

---

## 🚀 安裝與使用  

### 1. 環境需求  
- Python 3.9+  
- LINE 開發者帳號與 Channel Access Token  
- OpenAI API Key（或其他 LLM 提供商 API Key）  

### 2. 安裝套件  
```bash
git clone https://github.com/your-username/lesserafim-rag-linebot.git
cd lesserafim-rag-linebot
pip install -r requirements.txt
