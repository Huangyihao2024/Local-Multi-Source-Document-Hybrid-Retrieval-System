# Local Multi-Source Document Hybrid Retrieval System

## 项目简介

本项目实现了一套本地多源文档混合检索系统（Local Multi-Source Document Hybrid Retrieval System），支持对 PDF、DOCX、TXT 等多种格式文件进行统一解析、索引构建与语义检索。

系统结合：

- BM25 稀疏检索（Whoosh）
- 稠密向量检索（SentenceTransformer + ChromaDB）
- Cross-Encoder 重排序
- Streamlit 可视化界面

实现了兼顾关键词匹配与语义理解的本地混合检索框架。

整个系统支持离线运行，无需云端服务，可用于：

- 本地知识库检索
- 课程项目
- 文档管理
- RAG 前置检索系统
- 私有化文档搜索

---

# 系统架构

系统整体流程如下：

1. 文件解析
2. 文本分块
3. Whoosh BM25 索引构建
4. ChromaDB 向量索引构建
5. 混合检索
6. Cross-Encoder 重排序
7. Streamlit 前端展示

---

# 项目结构

```text
.
├── app.py
├── search.py
├── file_parser.py
├── tokenizer.py
├── utils.py
├── build_whoosh_index.py
├── build_chroma_index.py
├── stopwords.txt
├── test_files/
├── indexdir/
├── chroma_db/
├── m3e-small/
├── reranker_model/
└── README.md
```

---

# 核心模块说明

## 1. file_parser.py

负责解析本地文件。

支持：

- PDF
- DOCX
- TXT
- Markdown

功能：

- 自动识别文件类型
- 提取文本内容
- 异常处理
- 返回统一文本格式

---

## 2. tokenizer.py

实现 Whoosh 中文分词器。

系统使用 Jieba 分词，并桥接 Whoosh Tokenizer 接口，实现中文 BM25 检索。

---

## 3. build_whoosh_index.py

构建 BM25 倒排索引。

功能：

- 遍历 test_files
- 调用 file_parser 解析文件
- 使用 JiebaTokenizer 分词
- 建立 Whoosh 索引

生成目录：

```text
indexdir/
```

---

## 4. build_chroma_index.py

构建 ChromaDB 向量索引。

功能：

- 文本分块
- SentenceTransformer 向量编码
- 向量写入 ChromaDB

生成目录：

```text
chroma_db/
```

---

## 5. search.py

系统核心模块。

实现：

- 查询清洗
- BM25 检索
- 向量检索
- 分数归一化
- 混合检索
- Cross-Encoder 重排序

检索流程：

```text
用户查询
    ↓
BM25 检索
    ↓
向量检索
    ↓
分数融合
    ↓
CrossEncoder 重排序
    ↓
返回最终结果
```

---

## 6. app.py

Streamlit 前端。

提供：

- 搜索输入框
- top_k 滑块
- 结果展示
- 文本预览

---

# 使用模型

## Embedding Model

```text
m3e-small
```

下载地址：

https://huggingface.co/moka-ai/m3e-small

---

## Reranker Model

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

下载地址：

https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2

---

# 环境配置

## Python 版本

推荐：

```text
Python 3.10+
```

---

## 安装依赖

```bash
pip install streamlit
pip install sentence-transformers
pip install chromadb
pip install whoosh
pip install jieba
pip install pymupdf
pip install python-docx
pip install tqdm
```

---

# 模型准备

下载模型后：

```text
m3e-small/
reranker_model/
```

放在项目根目录。

---

# 如何运行项目

## 第一步：准备测试文件

将需要检索的文件放入：

```text
test_files/
```

例如：

```text
test_files/
├── report.pdf
├── note.docx
├── data.txt
```

---

## 第二步：构建 BM25 索引

```bash
python build_whoosh_index.py
```

成功后生成：

```text
indexdir/
```

---

## 第三步：构建向量索引

```bash
python build_chroma_index.py
```

成功后生成：

```text
chroma_db/
```

---

## 第四步：启动系统

```bash
streamlit run app.py
```

浏览器会自动打开。

---

# 系统特点

## 1. 本地离线运行

所有模型与数据库均本地运行。

不依赖云端 API。

---

## 2. 中文优化

使用：

- Jieba 中文分词
- m3e-small 中文向量模型

适合中文语义检索。

---

## 3. 混合检索

结合：

- BM25 精确匹配
- 向量语义召回
- CrossEncoder 精排

提升检索质量。

---

## 4. 多格式支持

支持：

- PDF
- DOCX
- TXT
- Markdown

---

# 未来优化方向

后续可以继续扩展：

- 增量索引更新
- FAISS 向量加速
- 多线程检索
- GPU 推理
- RAG 问答系统
- OCR 图片文本识别
- 多语言支持
- Web API 服务化

---

# 作者

黄奕浩

Nankai University

Information Retrieval System Project

---

# License

This project is for educational and research purposes only.

