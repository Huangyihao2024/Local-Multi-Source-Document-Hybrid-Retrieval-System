import os
import chromadb
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from file_parser import parse_file
from utils import chunk_text

# 加载本地向量模型
model = SentenceTransformer("./m3e-small")

# 连接 ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# 先删除旧集合（如果存在），确保全量重建
try:
    client.delete_collection("file_chunks")
except Exception:
    pass

collection = client.create_collection("file_chunks")

root_dir = "test_files"
ids, docs, metas = [], [], []

# 遍历所有文件，解析并分块
for dirpath, _, filenames in os.walk(root_dir):
    for fn in filenames:
        fpath = os.path.join(dirpath, fn)
        text = parse_file(fpath)
        if not text:
            continue
        for i, chunk in enumerate(chunk_text(text)):
            ids.append(f"{fpath}_{i}")
            docs.append(chunk)
            metas.append({"path": fpath, "chunk": i})

# 分批向量化并写入
batch_size = 64
for i in tqdm(range(0, len(ids), batch_size)):
    b_ids = ids[i:i+batch_size]
    b_docs = docs[i:i+batch_size]
    b_metas = metas[i:i+batch_size]
    emb = model.encode(b_docs).tolist()
    collection.add(
        ids=b_ids,
        documents=b_docs,
        metadatas=b_metas,
        embeddings=emb
    )

print("Chroma vector index rebuilt successfully.")