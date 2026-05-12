import os
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from file_parser import parse_file
from tqdm import tqdm
from tokenizer import JiebaTokenizer      # 用你自己写好的分词器

schema = Schema(
    path=ID(stored=True, unique=True),
    filename=TEXT(stored=True),
    content=TEXT(analyzer=JiebaTokenizer(), stored=True)
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
        content=text
    )
writer.commit()
print("Whoosh index built.")