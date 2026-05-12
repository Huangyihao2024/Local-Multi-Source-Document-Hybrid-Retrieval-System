import os
import jieba
import chromadb

from sentence_transformers import SentenceTransformer, CrossEncoder
from whoosh import index as whoosh_index
from whoosh.qparser import MultifieldParser

# -----------------------------
# Whoosh
# -----------------------------
whoosh_ix = whoosh_index.open_dir("indexdir")

# -----------------------------
# embedding
# -----------------------------
model = SentenceTransformer("./m3e-small")

# -----------------------------
# reranker（本地模型，需提前下载）
# -----------------------------
reranker = CrossEncoder("./reranker_model")   # 改为本地路径

# -----------------------------
# chroma
# -----------------------------
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="file_chunks"
)

# -----------------------------
# stopwords（安全写法）
# -----------------------------
stop_path = "stopwords.txt"

if os.path.exists(stop_path):
    with open(stop_path, "r", encoding="utf-8") as f:
        STOPWORDS = set([x.strip() for x in f if x.strip()])
else:
    STOPWORDS = set()

# -----------------------------
# query clean
# -----------------------------
def clean(q):
    ws = jieba.lcut(q)
    return " ".join([w for w in ws if w.strip() and w not in STOPWORDS])

# -----------------------------
# normalize
# -----------------------------
def norm(scores):
    if not scores:
        return []
    mn, mx = min(scores), max(scores)
    if mn == mx:
        return [0.5] * len(scores)
    return [(x - mn) / (mx - mn) for x in scores]

# -----------------------------
# BM25
# -----------------------------
def bm25_search(query, top_k=30):
    with whoosh_ix.searcher() as s:
        parser = MultifieldParser(
            ["filename", "content"],
            schema=whoosh_ix.schema
        )

        q = parser.parse(query)
        res = s.search(q, limit=top_k)

        return [
            {
                "path": r["path"],
                "score": r.score,
                "text": r["summary"]
            }
            for r in res
        ]

# -----------------------------
# vector
# -----------------------------
def vector_search(query, top_k=30):
    qv = model.encode([query]).tolist()

    res = collection.query(
        query_embeddings=qv,
        n_results=top_k
    )

    out = []

    for i in range(len(res["ids"][0])):
        out.append({
            "path": res["metadatas"][0][i]["path"],
            "score": 1 / (1 + res["distances"][0][i]),
            "text": res["documents"][0][i]
        })

    return out

# -----------------------------
# hybrid + rerank（核心）
# -----------------------------
def hybrid_search(query, top_k=10, alpha=0.6):

    query = clean(query)

    bm = bm25_search(query)
    vec = vector_search(query)

    bm_s = norm([x["score"] for x in bm])
    vec_s = norm([x["score"] for x in vec])

    score_map = {}

    for x, s in zip(bm, bm_s):
        score_map[x["path"]] = score_map.get(x["path"], 0) + alpha * s

    for x, s in zip(vec, vec_s):
        score_map[x["path"]] = score_map.get(x["path"], 0) + (1 - alpha) * s

    candidates = list(score_map.items())[:20]

    pairs = [(query, c[0]) for c in candidates]
    rerank_scores = reranker.predict(pairs)

    final = []

    for (path, _), r in zip(candidates, rerank_scores):
        final.append({
            "path": path,
            "score": float(r)
        })

    final.sort(key=lambda x: x["score"], reverse=True)

    return final[:top_k]