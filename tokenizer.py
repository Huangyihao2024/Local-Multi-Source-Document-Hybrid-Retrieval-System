import jieba
from whoosh.analysis import Tokenizer, Token

class JiebaTokenizer(Tokenizer):
    def __call__(self, value, **kwargs):
        pos = 0
        for w in jieba.lcut(value):
            t = Token()
            t.text = w
            t.pos = pos
            pos += 1
            yield t