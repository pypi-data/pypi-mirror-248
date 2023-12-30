from faisslite.encode import encode
# https://zhuanlan.zhihu.com/p/107241260
# https://zhuanlan.zhihu.com/p/350957155
# https://ispacesoft.com/85864.html
# https://zhuanlan.zhihu.com/p/530958094
import faiss, numpy
# https://zhuanlan.zhihu.com/p/629393766
import os, json, pickle

faiss_gpu = faiss.get_num_gpus()
print("faiss_gpu=", faiss_gpu)

class Faiss:
    save_dir = '.'
    def __init__(self, name, include=None, exclude=None):
        self.faiss_path = f'{Faiss.save_dir}/{name}.index'
        self.faiss_name = 'index'
        if include:
            self.faiss_name += '_'
            self.faiss_name += '_'.join(map(str, include))
        if exclude:
            self.faiss_name += '_exclude_'
            self.faiss_name += '_'.join(map(str, exclude))
        self.name_sents = self.faiss_path+'/'+self.faiss_name+'.sents'
        self.name_faiss = self.faiss_path+'/'+self.faiss_name+'.faiss'
        if not os.path.exists(self.name_faiss):
            with open(self.faiss_path+'/index.vectors', 'rb') as f:
                vectors = pickle.load(f)
            with open(self.faiss_path+'/index.sents', 'r', encoding='utf-8') as f:
                sents = json.load(f)

            if include or exclude:
                with open(self.faiss_path+'/index.predicts', 'r', encoding='utf-8') as f:
                    predicts = json.load(f)
                _vectors = []
                _sents = []
                for i, cls in enumerate(predicts):
                    if include and cls not in include: continue
                    if exclude and cls in exclude: continue
                    _vectors.append(vectors[i])
                    _sents.append(sents[i])
                with open(self.name_sents, 'w', encoding='utf-8') as f:
                    json.dump(_sents, f, ensure_ascii=False, indent=2)
                vectors = _vectors
                sents = _sents

            self.sents = sents
            vectors = numpy.array(vectors)
            # L2 欧几里得距离（空间距离）
            # IP 内积算法（Inner Product）
            self.faiss_index = faiss.IndexFlatIP(vectors.shape[1])
            self.faiss_index.add(vectors)
            assert len(self.sents) == self.faiss_index.ntotal
            faiss.write_index(self.faiss_index, self.name_faiss)
            if faiss_gpu > 0: self.cpu_to_gpu()
        else:
            with open(self.name_sents, 'r', encoding='utf-8') as f:
                self.sents = json.load(f)
            self.faiss_index = faiss.read_index(self.name_faiss)
            if faiss_gpu > 0: self.cpu_to_gpu()

    def cpu_to_gpu(self):
        res = faiss.StandardGpuResources()
        self.faiss_index = faiss.index_cpu_to_gpu(res, 0, self.faiss_index)

    def gpu_to_cpu(self):
        self.faiss_index = faiss.index_gpu_to_cpu(self.faiss_index)

    def search(self, para, top_k=100, threshold=0.6):
        Vector, Text = encode(para)
        if not Vector.shape[0]: return []

        Score, Index = self.faiss_index.search(Vector, top_k)
        Result = []
        for i in range(Index.shape[0]):
            result = []
            for j in range(Index.shape[1]):
                if Index[i, j] < 0 or Score[i, j] < threshold: break
                result.append((Score[i, j], Index[i, j]))
            Result.append(result)
        return Result

    def search_doc(self, para, closely=0.05, nearly=0.001, **kwargs):
        Result = self.search(para, **kwargs)
        Docs = {}
        for result in Result:
            docs = {}
            for score, index in result:
                p = self.sents[index]
                source = p['source']
                if source not in docs:
                    docs[source] = {
                        'score': score,
                        'pages': set(),
                        'texts': set()
                    }
                if docs[source]['score']-score < closely:
                    docs[source]['pages'].add(p['page'])
                    docs[source]['texts'].add(p['text'])
            for source in docs:
                if source not in Docs:
                    Docs[source] = {
                        'score': 0.0,
                        'pages': set(),
                        'texts': set()
                    }
                Docs[source]['score'] += docs[source]['score']
                Docs[source]['pages'] |= docs[source]['pages']
                Docs[source]['texts'] |= docs[source]['texts']

        Result = [{
            'source': source,
            'score': Docs[source]['score'],
            'pages': Docs[source]['pages'],
            'texts': Docs[source]['texts']
        } for source in Docs]
        Result = sorted(Result, key=lambda x:x['score'], reverse=True)
        return list(filter(lambda x:Result[0]['score']-x['score'] < nearly, Result))
