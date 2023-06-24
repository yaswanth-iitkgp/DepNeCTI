import chardet
with open('data/genia/train_utf8.data', 'rb') as f:
    data = f.read()
result = chardet.detect(data)
print(result['encoding'], result['confidence'])
