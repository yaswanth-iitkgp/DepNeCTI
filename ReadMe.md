Official code for the paper `"NeCTIS: Nested Compound Type Identification for Sanskrit - Introducing a Novel Task, Datasets and Framework"`

## Requirements

* Python 3.7 
* cuda  11.7
* torch              1.13.0
* torchaudio         0.13.0
* torchvision        0.14.0
* And the rest of the dependencies can be installed by simply creating a new environment using the `environment.yml` file.

We assume that you have installed conda beforehand. 

```
conda env create -f environment.yml
```
And then activate this environment and you are good to go now !!

## Where is the dataset 
* Datasets are given in the `Datasets` folder.
* Datasets include - with context (fine grain + coarse) and without context (fine grain + coarse)


## How to generate the data format used in this model
* transfer the `.csv` files from the respective Datasets folder to `Datasets/data_format`
* Use the `.ipynb` file in the  `Datasets/data_format` folder and follow the instructions mentioned there to generate the required data format.


## Pretrained embeddings for NeCTIS datasets
* Pretrained FastText embeddings for NeCTIS can be obtained from [here](https://drive.google.com/drive/folders/1dM4u3cb1XDF_Z866t6VQmn2NeyK4nirW?usp=drive_link).
* Make sure that `cc.NeCTIS.300.txt` file is placed at `data/`. And place the rest of the files in `word_vectors` folder.
* The main results are reported on the systems trained by combining train and dev splits. 


## If you want to get your own Pretrained embeddings for any dataset
* First place all the files in the `word_vectors` folder as mentioned above.
* Use the `.ipynb` file in `word_vectors` folder and generate your own fasttext embeddings.


## How to train Proposed model for NeCTIS
* To run proposed system: simply run bash script `run_NeCTIS.sh` and place the respective dataset similar to those files in the data. With these scripts you will be able to reproduce our results for proposed model reported in Table 2.

## How to Know F1, Precision, Recall scores
* Use the script provided in `Evaluation` folder to get the scores.


## How to reproduce the results shown for other baselines
* Download the dataset from this [link](https://drive.google.com/drive/folders/1nr5keSzfeQuNWabX4CcWEHn9269RWNNB?usp=sharing) which are in the required format for each baseline.
* Go to the respective folders in the `Baselines` folder and follow the readme files given there.
* If you face problem in using this dataset from this link you can generate your data format using the `data_format.ipynb` in `Datasets/data_format`
* Note: for using any baseline the data will have names like "genia", "GENIA" etc but that data is NeCTIS data only, the names are left unchanged to avoid creating trouble when running the model.



## How to Use this NeCTIS model for getting compounds with labels, useful for Machine Translation task
* First you have to place the pretrained models folders in saved_models, download them [here](https://drive.google.com/drive/folders/1rHoRCxu94KeXhBXHMfb0_qDWpXYz-agT?usp=sharing) and unzip them into `saved_models` folder.
* Now place your input file that has sentences with compounds in them (see the `input.txt` in `data_MT` folder) in data_MT with renaming the file to `input.txt`
* open the file run_NeCTIS_for_MT.sh and then set 
* * the `label_type` flag to `Coarse` / `Finegrain` 
* * the `input_format` to `IAST` / `DEVANAGIRI` / `SLP1` 
* The Predictions will be saved in `/saved_models/$label_type/domain_san_test_model_domain_san_data_domain_san_pred.txt` and also in `/data_MT/pred_file.txt`
* To run the system do this
```
bash run_NeCTIS_for_MT.sh
```
* Ignore the UAS, LAS scores given while inference.
