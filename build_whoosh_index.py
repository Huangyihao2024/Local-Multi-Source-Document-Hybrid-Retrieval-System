import os
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from file_parser import parse_file
from tqdm import tqdm
from tokenizer import JiebaTokenizer

schema = Schema(
    path=ID(stored=True, unique=True),
    filename=TEXT(stored=True),
    content=TEXT(analyzer=JiebaTokenizer(), stored=True),
    summary=TEXT(stored=True)   # 必须添加这个字段
)

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = index.create_in("indexdir", schema)
writer = ix.writer()

root_dir = "test_files"
all_files = []
for dirpath, _, filenames in os.walk(root_dir):
    for fn in filenames:
        all_files.append(os.path.join(dirpath, fn))

for file_path in tqdm(all_files):
    text = parse_file(file_path)
    if not text:
        continue
    writer.add_document(
        path=file_path,
        filename=os.path.basename(file_path),
        content=text,
        summary=text[:300]  # 写入前300字作为摘要
    )
writer.commit()
print("Whoosh index built with summary field.")