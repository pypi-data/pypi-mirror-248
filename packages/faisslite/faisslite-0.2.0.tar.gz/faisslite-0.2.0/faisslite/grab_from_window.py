def grab_from_window(docs, results, window_size=4):
    Result = list(results)
    for result in Result:
        source = result['source']
        pages = sorted(list(result['pages']))
        paras = docs[source]['paras']
        left = 0
        for i in range(len(pages)):
            right = pages[i+1] if i+1 < len(pages) else len(paras)
            page = pages[i]
            for j in range(page-1, left, -1):
                para = paras[j]
                if 'text' not in para: break
                if para['end']-para['start'] > 1: break
                if page-j > window_size: break
                result['pages'].add(j)
            for j in range(page, right):
                result['pages'].add(j)
                para = paras[j]
                if 'text' not in para: break
                if para['end']-para['start'] > 1: break
                if j-page >= window_size: break
            left = j+1
    return Result
