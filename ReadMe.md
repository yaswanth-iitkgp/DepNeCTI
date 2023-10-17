Official code for the paper [DepNeCTI: Dependency-based Nested Compound Type Identification for Sanskrit](http://arxiv.org/abs/2310.09501)

## Requirements for running DepNeCTI-LSTM model

* Python 3.7 
* cuda  11.7
* torch              1.13.0
* torchaudio         0.13.0
* torchvision        0.14.0
* And the rest of the dependencies can be installed by simply creating a new environment using the `environment.yml` file.

We assume that you have installed conda beforehand. 

```
conda env create -f DepNeCTI-LSTM_environment.yml
conda env create -f DepNeCTI-XLMR_environment.yml
```
And then activate this environment and you are good to go now !!

## Where is the dataset 
* Datasets are given in the `Datasets` folder.
* Datasets include - with context (fine grain + coarse) and without context (fine grain + coarse)


## How to generate the data format used in this model(DepNeCTI-LSTM)
* transfer the `.csv` files from the respective Datasets folder to `Datasets/data_format`
* Use the `.ipynb` file in the  `Datasets/data_format` folder and follow the instructions mentioned there to generate the required data format.


## Pretrained embeddings for DepNeCTI datasets
* Pretrained FastText embeddings for DepNeCTI can be obtained from [here](https://drive.google.com/drive/folders/1dM4u3cb1XDF_Z866t6VQmn2NeyK4nirW?usp=drive_link).
* Make sure that `cc.NeCTIS.300.txt` file is placed at `data/`. And place the rest of the files in `word_vectors` folder.
* The main results are reported on the systems trained by combining train and dev splits. 


## If you want to get your own Pretrained embeddings for any dataset
* First place all the files in the `word_vectors` folder as mentioned above.
* Use the `.ipynb` file in `word_vectors` folder and generate your own fasttext embeddings.


## How to train Proposed model for DepNeCTI-LSTM and DepNeCTI-XLMR
* To run proposed system: simply run bash script `run_DepNeCTI_LSTM.sh` or `run_DepNeCTI_XLMR.sh`and place the respective dataset similar to those files in the data. With these scripts you will be able to reproduce our results for proposed model reported in Table 2.

* To run the system do this
```
bash run_DepNeCTI_LSTM.sh
```

## How to Know F1, Precision, Recall scores
* Use the script (`eval_f1.py`) provided in `Evaluation` folder to get the scores.

## How to Know USS, LSS scores
* Use the script (`eval_USS_LSS.py`) provided in `Evaluation` folder to get the scores.

## How to reproduce the results shown for other baselines
* Download the dataset from this [link](https://drive.google.com/drive/folders/1nr5keSzfeQuNWabX4CcWEHn9269RWNNB?usp=sharing) which are in the required format for each baseline.
* Go to the respective folders in the `Baselines` folder and follow the readme files given there.
* If you face problem in using this dataset from this link you can generate your data format using the `data_format.ipynb` in `Datasets/data_format`
* Note: for using any baseline the data will have names like "genia", "GENIA" etc but that data is DepNeCTI data only, the names are left unchanged to avoid creating trouble when running the model.


## Citing DepNeCTI
If you use DepNeCTI in your research, please consider citing our work:

```
@misc{sandhan2023depnecti,
      title={DepNeCTI: Dependency-based Nested Compound Type Identification for Sanskrit}, 
      author={Jivnesh Sandhan and Yaswanth Narsupalli and Sreevatsa Muppirala and Sriram Krishnan and Pavankumar Satuluri and Amba Kulkarni and Pawan Goyal},
      year={2023},
      eprint={2310.09501},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```



