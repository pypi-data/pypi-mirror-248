# About
一个用于中文文本向量化和相似度搜索的Python包。它可以将中文段落表征为向量矩阵,并构建向量搜索索引,用于快速准确检索文本中的相似句子。

# Install
`$ pip3 install -U faisslite`

# Director 
+ faisslite 
    + document.py
    + DBscan.py
    + Faiss.py
    + grab\_from\_window.py

## document.py
对输入文本进行规范化处理，并将输入文本拆分成段落。
- parse函数
  将文本拆分为由文本段落和分隔符构成的字典数组，为后续向量化处理文本提供了基础。
- stringify函数
  将字典数组表示的文章序列化为文本。

## DBscan.py
对文本进行向量化处理，对向量化后文本聚类。
- DBscan类
  - add\_doc函数
    将完整文档向量化，同时记录各段落和文档的信息，包括偏移、起止、页码等。
  - fit\_predict函数
    向量聚类

## Faiss.py
用DBscan.py处理后的数据建立Faiss索引。实现语义相似句检索。
- Faiss类
  - search\_doc函数
    优先选择完整文档相似度最大的，并且过滤掉低于阈值的结果。

## grab\_from\_window.py
合并多个向量库的检索结果，在指定的窗口内选取返回的文字。

# Usage
将预处理好的文本向量化
```python3
from faisslite.document import parse
from faisslite.DBscan import DBscan

source = "预处理好的文本的唯一ID"
paras = parse("预处理好的文本字符串")

DBscan.save_dir = "向量数据库存放目录"
db = DBscan("向量数据库名字")
db.add_doc(source, {'paras': paras})
db.dump()
```
将向量化后文本聚类
```python3
from faisslite.DBscan import DBscan

DBscan.save_dir = "向量数据库存放目录"
db = DBscan("向量数据库名字")
db.fit_predict()
db.dump()
```
建立向量数据库
```python3
from faisslite.Faiss import Faiss

Faiss.save_dir = "向量数据库存放目录"
db = Faiss("向量数据库名字", exclude=[-1])
```
查询向量数据库，输出查询结果
```python3
from faisslite.Faiss import Faiss

Faiss.save_dir = "向量数据库存放目录"
db = Faiss("向量数据库名字")
results = db.search_doc("与这段文字进行相似匹配")
for result in results:
    source = result['source'] # 预处理好的文本的唯一ID
    score  = result['score']  # 相似度
    texts  = result['texts']  # 匹配的语句

    print(f"{source}: {score}")
    print(texts)

from faisslite.grab_from_window import grab_from_window
from faisslite.document import stringify
import json

with open(Faiss.save_dir+'/index.docs', 'r', encoding='utf-8') as f:
    docs = json.load(f)
results = grab_from_window(docs, results)
for result in results:
    source = result['source'] # 预处理好的文本的唯一ID
    score  = result['score']  # 相似度
    pages  = result['pages']  # 匹配的段落下标

    print(f"{source}: {score}")
    doc = docs[source]
    print(stringify(doc['paras'], pages))
```

# Contact us
<may.xiaoya.zhang@gmail.com>
