Official code for the paper ["NeCTIS: Nested Compound Type Identification for Sanskrit - Introducing a Novel Task, Datasets and Framework"]
If you use this code please cite our paper.

## Requirements

* Python 3.7 

And the rest of the dependencies can be installed by simply creating a new environment using the environment.yml file.

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
* Pretrained FastText embeddings for NeCTIS can be obtained from [here](https://drive.google.com/drive/folders/1dM4u3cb1XDF_Z866t6VQmn2NeyK4nirW?usp=sharing). 
* Make sure that `cc.NeCTIS.300.txt` file is placed at `data/`. And place the rest of the files in `word_vectors` folder.
* The main results are reported on the systems trained by combining train and dev splits. 


## If you want to get your own Pretrained embeddings for any dataset
* First place all the files in the `word_vectors` folder as mentioned above.
* Use the `.ipynb` file in `word_vectors` folder and generate your own fasttext embeddings.


## How to train Proposed model for NeCTIS
* To run proposed system: simply run bash script `run_NeCTIS.sh` and place the respective dataset similar to those files in the data. With these scripts you will be able to reproduce our results for proposed model reported in Table 2.


## How to reproduce the results shown for other baselines
* Go to the respective folders in the `Baselines` folder and follow the readme files given there.
* Note: for using any baseline the data will have names like "genia", "GENIA" etc but that data is NeCTIS data only, the names are left unchanged to avoid creating trouble when running the model.
