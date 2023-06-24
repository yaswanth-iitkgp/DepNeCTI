# pointer-net-for-nested
The official implementation of ACL2022: [Bottom-Up Constituency Parsing and Nested Named Entity Recognition with Pointer Networks](https://arxiv.org/pdf/2110.05419.pdf)


## Setup
python = 3.7
create environment using `environment.yml`

## Data
Put the data in the `data/genia` folder
 
# Run
```
python train.py +exp=ft_10 datamodule=genia model=pointer model.use_prev_label=True
```

evaluation:
```
python evaluate.py +load_from_checkpoint=your/checkpoint/dir
```   


# Citation
```
@misc{yang2021bottomup,
      title={Bottom-Up Constituency Parsing and Nested Named Entity Recognition with Pointer Networks}, 
      author={Songlin Yang and Kewei Tu},
      year={2021},
      eprint={2110.05419},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

# Credits
The code is based on [lightning+hydra](https://github.com/ashleve/lightning-hydra-template) template. I use [FastNLP](https://github.com/fastnlp/fastNLP) for loading data. I use lots of built-in modules (LSTMs, Biaffines, Triaffines, Dropout Layers, etc) from [Supar](https://github.com/yzhangcs/parser/tree/main/supar).  



