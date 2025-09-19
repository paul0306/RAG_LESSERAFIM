import os
import requests
import json
import numpy as np
import faiss
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from rapidfuzz import process
import google.generativeai as genai

# ========= 初始化 =========
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ========= STEP 1: 抓 Wiki HTML =========
def get_wiki_html(title, lang="zh"):
    url = f"https://{lang}.wikipedia.org/zh-tw/{title}"
    headers = {"User-Agent": "Mozilla/5.0 (RAG Project Script)"}
    res = requests.get(url, headers=headers, timeout=10)
    if res.status_code != 200:
        raise ValueError(f"抓取失敗: HTTP {res.status_code}")
    return res.text

# ========= STEP 2: 解析 Wiki =========
def parse_wiki_content(title, lang="zh"):
    html = get_wiki_html(title, lang)
    soup = BeautifulSoup(html, "html.parser")

    paragraphs = [p.get_text(strip=True) for p in soup.select("p") if p.get_text(strip=True)]
    infobox = soup.find("table", {"class": "infobox vcard plainlist"})
    infobox_text = []
    if infobox:
        for row in infobox.find_all("tr"):
            cells = row.find_all(["th", "td"])
            row_text = [c.get_text(strip=True) for c in cells if c.get_text(strip=True)]
            if row_text:
                infobox_text.append(" | ".join(row_text))

    return {"paragraphs": paragraphs, "infobox": infobox_text}

# ========= STEP 3: 本地 JSON =========
file_map = {
    "團體": "lesserafim.json",
    "金采源": "chaewon.json",
    "宮脇咲良": "sakura.json",
    "許允真": "yunjin.json",
    "中村一葉": "kazuha.json",
    "洪恩採": "eunchae.json",
}

keywords = {
    "團體": ["團體", "LE SSERAFIM", "fim寶"],
    "金采源": ["金采源", "采源", "醃蘿蔔混混", "Chaewon", "隊長"],
    "宮脇咲良": ["宮脇咲良", "櫻花", "Sakura", "大姐"],
    "許允真": ["許允真", "允真", "Jennifer", "美國女人", "Yunjin"],
    "中村一葉": ["中村一葉", "一葉", "Kazuha", "耶耶", "薩摩耶耶"],
    "洪恩採": ["洪恩採", "恩採", "妹寶", "忙內", "Eunchae", "忙採"],
}

# 展開 keyword -> label 對應表
all_keywords = {w: label for label, words in keywords.items() for w in words}

def choose_file(question: str) -> str:
    best_match, score, _ = process.extractOne(question, all_keywords.keys())
    if score > 70:
        label = all_keywords[best_match]
        return os.path.join("data", file_map[label])
    else:
        return os.path.join("data", file_map["團體"])

def load_json_data(file_name):
    all_documents = []
    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
        if data:
            if "paragraphs" in data:
                all_documents.extend(data["paragraphs"])
            if "infobox" in data:
                all_documents.extend(data["infobox"])
    return all_documents

# ========= STEP 4: 向量資料庫 =========
def build_vectorstore(documents):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(documents)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index, model

# ========= STEP 5: RAG 查詢 =========
def rag_query(query, index, model, documents, k=100):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k)
    context = [documents[i] for i in I[0]]

    prompt = f"""根據以下的資料回答問題：\n{context}\n\n問題：{query}
已經有事先根據問題描述挑選出最適合的資料，如果問題中有看到不認識的詞或名字出現就默認那些資料就是屬於那個人的再回答問題
回覆的答案中請不要有'根據提供的資料'等類似冗餘的話"""

    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    response = gemini_model.generate_content(prompt)
    return response.text
