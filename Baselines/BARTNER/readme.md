This is the code for ACL-ICJNLP2021 paper [A Unified Generative Framework for Various NER Subtasks](https://arxiv.org/abs/2106.01223).

## Data
* simply put the data in the `data` folder and train the model.

Install the package in the requirements.txt, then use the following
commands to install two other packages
```text
pip install git+https://github.com/fastnlp/fastNLP@dev
pip install git+https://github.com/fastnlp/fitlog
```

You need to put your data in the parallel folder of this repo
```text
    - BARTNER/
        - train.py
        ...
    - data/
        - conll2003
            - train.txt
            - text.txt
            - dev.txt
        - en-ontonotes
            - ...
        - Share_2013
        - Share_2014
        - CADEC
        - en_ace04
        - en_ace05
        - genia

```

the data should like 
(each line is a jsonline, contains ``ners`` and ``sentences`` keys.)
```text
{"ners": [[[0, 1, "BvS"], [2, 4, "Ds"]], [[10, 11, "T6"], [10, 12, "U"], [13, 14, "T6"]], [[3, 4, "K1"], [3, 5, "U"]], [[1, 2, "T6"], [1, 3, "T7"]], [[2, 3, "K1"], [2, 4, "T7"]], [[1, 2, "T6"], [1, 3, "T6"]]], "sentences": [["C2<sa", "sarzapaM>C2", "C3<tumburu", "DAnya", "vanyaM>C3", "caRqAM", "ca", "cUrRAni", "samAni", "kuryAt"], ["ApAtata", "sAmAnyA", "iva", "pratIyamAnA", "ete", "yadi", "sUkzmam", "nirIkzyeran", "tarhi", "etezAm", "C3<hft", "anta", "sTa>C3", "C2<saMkawa", "boDa>C2"], ["saH", "ca", "na", "C3<viSizwa", "vESizwya", "avagAhI>C3"], ["saH", "C3<SAstra", "arTa", "vicakzaRaH>C3"], ["avadAtike", "kimetad", "C3<vAma", "hasta", "parigfhItam>C3"], ["yatra", "C3<hIbrU", "pracAra", "kAryaM>C3", "samyak", "pracalati", "sma"]]}
{"ners": [[[1, 2, "U"], [3, 4, "T6"], [3, 5, "T6"], [10, 11, "K7"]], [[6, 7, "K1"], [6, 8, "T6"]], [[0, 1, "T6"], [3, 4, "K1"], [3, 5, "Bsu"]], [[1, 2, "U"], [1, 3, "T6"], [5, 6, "T6"], [5, 7, "T7"], [5, 8, "T3"], [9, 10, "T3"]], [[1, 2, "T6"], [4, 5, "T6"], [4, 6, "T3"]], [[3, 4, "T6"], [5, 7, "T6"], [6, 7, "Tp"]]], "sentences": [["kaScit", "C2<kAMsya", "kAraH>C2", "C3<pAtra", "nirmARa", "viDO>C3", "saMlagnaH", "sarvaM", "dinaM", "hastikayA", "C2<KawKaw", "DvaniM>C2", "karoti", "sma"], ["lakzmI", "vakti", "sma", "ahaM", "SikzAM", "prApya", "C3<AdarSa", "gfhiRI", "Darmasya>C3", "pAlanaM", "karizyAmi"], ["C2<pAda", "pIWikAyA>C2", "upari", "C3<rakta", "kamala", "kOmalO>C3", "caraRO", "virAjete"], ["cazakam", "C3<kampamAna", "kara", "dvayena>C3", "AdAya", "C4<sva", "vastu", "saMBAra", "gatam>C4", "C2<SikyA", "sadfSam>C2", "tat", "puwakam", "aspfSat"], ["nanu", "C2<vAkya", "arTaH>C2", "lAkzaRikaH", "C3<pada", "arTa", "boDya>C3", "tvAt"], ["samprati", "na", "kopi", "C2<asmat", "deSe>C2", "C3<parihAsa", "vi", "jalpanam>C3", "kartum", "samarTaH", "Bavizyati"]]}
{"ners": [[[1, 2, "T6"], [1, 3, "T6"]], [[1, 2, "T6"], [1, 3, "Bs6"], [4, 5, "T5"], [4, 6, "T6"], [4, 7, "Bs6"]], [[3, 5, "Bb"], [6, 7, "Bs6"], [8, 11, "Bb"]], [[3, 4, "Tn"], [3, 5, "K1"]], [[3, 4, "T6"], [3, 5, "T6"], [6, 7, "T6"]], [[3, 5, "Di"], [10, 11, "T6"]]], "sentences": [["nirmitAm", "C3<sumanas", "bfnda", "priyAm>C3", "SAbdataraNgiRIm"], ["arTAH", "C3<pAda", "raja", "upamAH>C3", "C4<giri", "nadI", "vega", "upamam>C4", "yOvanam"], ["rUpam", "mahat", "te", "C3<bahu", "vaktra", "netram>C3", "C2<mahat", "bAho>C2", "C4<bahu", "bAhu", "Uru", "pAdam>C4"], ["tasya", "jIvanam", "api", "C3<na", "Agata", "prakASam>C3", "pARqulipiH", "iva", "eva", "pariRatam"], ["vAlI", "sugrIva", "pratigfhyatAm", "C3<asmad", "kula", "Danam>C3", "C2<heman", "mAlA>C2"], ["satyAm", "api", "avidyAyAm", "C3<suKa", "duHKa", "mohezu>C3", "guRezu", "BujyamAnezu", "yaH", "saNgaH", "C2<Atman", "BAvaH>C2", "saMsArasya", "saH", "praDAnam", "kAraRam", "janmanaH"]]}

...
```
## Train
You can run the code by directly using
```shell
python train.py
```

The following output should be achieved
```text
Save cache to caches/data_facebook/bart-large_conll2003_word.pt.                                                                                                        
max_len_a:0.6, max_len:10
In total 3 datasets:
        test has 3453 instances.
        train has 14041 instances.
        dev has 3250 instances.

The number of tokens in tokenizer  50265
50269 50274
input fields after batch(if batch size is 2):
        tgt_tokens: (1)type:torch.Tensor (2)dtype:torch.int64, (3)shape:torch.Size([2, 8]) 
        src_tokens: (1)type:torch.Tensor (2)dtype:torch.int64, (3)shape:torch.Size([2, 11]) 
        first: (1)type:torch.Tensor (2)dtype:torch.int64, (3)shape:torch.Size([2, 11]) 
        src_seq_len: (1)type:torch.Tensor (2)dtype:torch.int64, (3)shape:torch.Size([2]) 
        tgt_seq_len: (1)type:torch.Tensor (2)dtype:torch.int64, (3)shape:torch.Size([2]) 
target fields after batch(if batch size is 2):
        entities: (1)type:numpy.ndarray (2)dtype:object, (3)shape:(2,) 
        tgt_tokens: (1)type:torch.Tensor (2)dtype:torch.int64, (3)shape:torch.Size([2, 8]) 
        target_span: (1)type:numpy.ndarray (2)dtype:object, (3)shape:(2,) 
        tgt_seq_len: (1)type:torch.Tensor (2)dtype:torch.int64, (3)shape:torch.Size([2]) 

training epochs started 2021-06-02-11-49-26-964889
Epoch 1/30:   0%|                                                         | 15/32430 [00:06<3:12:37,  2.80it/s, loss:6.96158
```

Some important python files are listed below
```text
- BartNER
  - data
     - pipe.py # load and process data
  - model
     - bart.py # the model file
  - train.py  # the training file
```

The different ``Loader``s  in the `data/pipe.py` is meant to load data, and the ``data.BartNERPipe`` class 
is to process data, the loader should load data into a DataBundle object,
you can mock the provided Loader to write your own loader, as long as your
dataset has the following four fields, the ``BartNERPipe`` should be able to 
process it
```text
- raw_words  # List[str]
    # ['AL-AIN', ',', 'United', 'Arab', 'Emirates', '1996-12-06']
- entities  # List[List[str]]
    # [['AL-AIN'], ['United', 'Arab', 'Emirates']]
- entity_tags  # List[str], the same length as entities
    # ['loc', 'loc']
- entity_spans # List[List[int]], the inner list must have an even number of ints, means the start(inclusive，闭区间) and end(exclusive，开区间) of an entity segment
    # [[0, 1], [2, 5]] or for discontinous NER [[0, 1, 5, 7], [2, 3, 5, 7],...]
```

In order to help you reproduce the results, we have hardcoded the hyper-parameters
 for each dataset in the code, you can change them based on your need. 
We conduct all experiments in NVIDIA-3090(24G memory). Some known
 difficulties about the reproduction of this code: (1) Some datasets
(nested and discontinous) will drop to 0 or near 0 F1 during training, please drop these
 results; (2) randomness will cause large performance variance for some datasets, please try to 
run multiple times. 

We deeply understand how frustrating it can be 
if the results are hard to reproduce, we tried our best to make sure 
the results were at least reproducible in our equipment (Usually take 
average from at least  five runs).

