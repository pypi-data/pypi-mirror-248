from faisslite.encode import encode
# https://zhuanlan.zhihu.com/p/629393766
import os, json, pickle
# https://www.codenong.com/58602494/
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html
# https://cloud.tencent.com/developer/article/1487562
from sklearn.cluster import DBSCAN

class DBscan:
    save_dir = '.'
    def __init__(self, name):
        self.dbscan_path = f'{DBscan.save_dir}/{name}.index'
        if not os.path.exists(self.dbscan_path):
            self.predicts = []
            self.vectors = []
            self.sents = []
            self.docs = {}
        else:
            self.load()

    def add(self, source, page, para):
        Vector, Text = encode(para)
        if not Vector.shape[0]: return
        self.vectors.extend(Vector)
        self.sents.extend([{
            'source': source,
            'page': page,
            'text': text
        } for text in Text])

    def add_doc(self, source, doc):
        if source in self.docs: return
        for page, para in enumerate(doc['paras']):
            if 'text' not in para: continue
            self.add(source, page, para['text'])
        assert len(self.sents) == len(self.vectors)
        self.docs[source] = doc

    def load(self):
        with open(self.dbscan_path+'/index.predicts', 'r', encoding='utf-8') as f:
            self.predicts = json.load(f)
        with open(self.dbscan_path+'/index.vectors', 'rb') as f:
            self.vectors = pickle.load(f)
        with open(self.dbscan_path+'/index.sents', 'r', encoding='utf-8') as f:
            self.sents = json.load(f)
        with open(self.dbscan_path+'/index.docs', 'r', encoding='utf-8') as f:
            self.docs = json.load(f)

    def dump(self):
        if not os.path.exists(self.dbscan_path): os.mkdir(self.dbscan_path)
        with open(self.dbscan_path+'/index.predicts', 'w', encoding='utf-8') as f:
            json.dump(self.predicts, f, ensure_ascii=False, indent=2)
        with open(self.dbscan_path+'/index.vectors', 'wb') as f:
            pickle.dump(self.vectors, f)
        with open(self.dbscan_path+'/index.sents', 'w', encoding='utf-8') as f:
            json.dump(self.sents, f, ensure_ascii=False, indent=2)
        with open(self.dbscan_path+'/index.docs', 'w', encoding='utf-8') as f:
            json.dump(self.docs, f, ensure_ascii=False, indent=2)

    def fit_predict(self, **kwargs):
        clustering = DBSCAN(metric='cosine', **kwargs)
        self.predicts = clustering.fit_predict(self.vectors).tolist()
