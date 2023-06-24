
# Nested NER as Latent Lexicalized Parsing

The code of our ACL2022 paper: [Nested Named Entity Recognition as Latent Lexicalized Constituency Parsing](https://aclanthology.org/2022.acl-long.428/). 

## How to run this baseline for NeCTIS experiments
* Simply create a conda enviroment using `environment.yml` file
* The code was implemented in Python 3.9 with anaconda environment. 
* The experiment configurations assume at least 30GB GPU memory.


## Data
* Don't change any names from 'genia' to 'NeCTIS'
* Place the train.data, dev.data, test.data in the `data/GENIA` folder and run the following command to generate brat files.
* Download the `bio_nlp_vec` , `biobert-large-cased-v1.1 `, from this [link](https://drive.google.com/drive/folders/1cP_cuKRsikCfQhbS4y2-3LKyvTmCO5aj?usp=sharing) and `glove` from this [link](https://nlp.stanford.edu/projects/glove/)

```
C3<hft anta sTa>C3 C2<saMkawa boDa>C2
0,2 Tatpurusha|0,3 Tatpurusha|3,5 Tatpurusha

...
```

Next we will convert the data to the brat standoff format. See [its document](https://brat.nlplab.org/standoff.html) for more information. We provide a script for the conversion in the `data` folder.
Run it with command
```shell
python raw2brat.py -o brat/genia/brat/train GENIA/train.data
python raw2brat.py -o brat/genia/brat/test GENIA/test.data
python raw2brat.py -o brat/genia/brat/dev GENIA/dev.data
```

## Train
* Don't change the name from genia (the contents inside is NeCTIS data only.)
```
python train.py model=genia
```


## Test

```
python test.py runner.load_from_checkpoint=<path_to_ckpt>
```
It will report scores and write the predictions on the test set to the `predict_on_test` file.

## Citation

```
@inproceedings{lou-etal-2022-nested,
    title = "Nested Named Entity Recognition as Latent Lexicalized Constituency Parsing",
    author = "Lou, Chao  and
      Yang, Songlin  and
      Tu, Kewei",
    booktitle = "Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = may,
    year = "2022",
    address = "Dublin, Ireland",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.acl-long.428",
    pages = "6183--6198",
    abstract = "Nested named entity recognition (NER) has been receiving increasing attention. Recently, Fu et al. (2020) adapt a span-based constituency parser to tackle nested NER. They treat nested entities as partially-observed constituency trees and propose the masked inside algorithm for partial marginalization. However, their method cannot leverage entity heads, which have been shown useful in entity mention detection and entity typing. In this work, we resort to more expressive structures, lexicalized constituency trees in which constituents are annotated by headwords, to model nested entities. We leverage the Eisner-Satta algorithm to perform partial marginalization and inference efficiently.In addition, we propose to use (1) a two-stage strategy (2) a head regularization loss and (3) a head-aware labeling loss in order to enhance the performance. We make a thorough ablation study to investigate the functionality of each component. Experimentally, our method achieves the state-of-the-art performance on ACE2004, ACE2005 and NNE, and competitive performance on GENIA, and meanwhile has a fast inference speed.",
}
```