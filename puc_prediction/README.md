# PUC Prediction
The purpose of this set of scripts is to use a product name to predict a PUC. Below are instructions for running the code.

## How to Use
All of the following methods can be imported from `model_helper.py`. See this file for more info about the parameters.

### Generate model data
As a perquisite for using this model, a few pieces need to be generated. This takes a while to do, but only needs to be done once as long as the training data doesn't change. If you ever want to refresh the model with new data from factotum, you will need to run this function again. I would also recommend using a computer that has a decent amount of RAM and free storage space (i.e. not your laptop). Many files ending in `.joblib` are saved by running this function; do not delete them.

`model_initialize` is the required function and takes the following inputs:
* `add_groups`: List of data groups with additional products to add. These products should be ones that have no PUCs and should not have PUCs. The purpose of adding these groups is to train the model on products that shouldn't be assigned PUCs. This argument is optional if you don't want to add any data groups. Defailts to `[]`.
* `label`: A label for the saved data. This label lets you run and save multiple models at the same time. This label should be used for building and running the model, as well. Defaults to `''`.

```python
from model_helper import model_initialize
model_initialize([47])
```
**Important:** If you run this again wwith the same label after building a model, that model will no longer work because the file containing the word embedding information will overwritten. 

### Building a model
The script `model_helper.py` contains functions to make building a model straightforward. The function you will want to use is called `model_build`. Multiple files are saved after running this method; these are the actual trained models. After training these models once, they do not need to be trained again.

`model_build` takes the following as inputs:
* `df_train`: A subset of the dataset that is used for training the models. Should be a DataFrame, can also be a string to use the whole training set. Defaults to `'all'`.
* `bootstrap`: Whether to sample `df_train` with replacement or not (recommended to be set to `True` if `num_runs` is more than 1). Defailts to `False`.
* `num_runs`: Number of times to fit the model before aggregating it. Defaults to `1`.
* `sample_size`: Size of the training set for each run (sampled from the training set). If there are multiple runs, each sample from the training set will be this large. Can be a number, or `all`. Since SVMs can be slow with many samples, this parameter is designed to allow for fitting subets of the data in different runs to speed up computation time. If `bootstrap` is not `True`, do not make this larger than the length of `df_train`. Defaults to `'all'`.
* `label`: A label for the saved models. This label is used for running model predictions, as well. Any models with the same label will be overwritten. Defaults to `''`.
* `probab`: Whether to calculate probabilities for the classes. Enabling this will increase computation time. Defaults to `False`.

```python
from model_helper import model_build
model_build(df_train='all', bootstrap=True, num_runs=5, label='boot')
```

### Making predictions
`model_helper.py` also contains a function to help with predictions, `model_run`. It takes a list of product names as the input. The list should be in the form `[['brand1', 'title1'], ['brand2', 'title2']]`, but can also just be a list of names. This script will clean and vectorize the product names before using the model to make a prediction. There is also a label field; this field needs to be the same as when training the model. The output will be an array of PUCs in the form `[['gen_cat', 'prod_fam', 'prod_type'], ...]`. I recommend you put all the products you need to predict in the same list, as calling the function multiple times is slow because it has to load the models each time.

`model_run` takes the following as inputs:
* `sen_itr`: List of product names in the form `['brand', 'title']`. Required.
* `label`: Model label, should match the label used when building the model. Defaults to `''`.
* `mode`: Whether to take the mode of the different runs or just output the results of all runs. If you set to `False`, you will need to aggregate the runs yourself. Defaults to `True`.

There are three lists that are returned by the function:
* A list of predicted PUCs (form depending on `mode` flag)
* A list of products that were removed during cleaning
* A list of probabilities (blank no probabilities found)
* A list of predicted PUC names for each level based on the probability (used for formatting the list of probabilities)

```python
from model_helper import model_run

prod_names = [['clorox', 'extra fancy bleach'], ['crayola', 'purple crayons']]
puclist, removed, problist, probnames = model_run(prod_names, label='boot')
```

### Organizing the results

There is also a function for formatting the predictions and probabilities and outputting them into a dataframe. This function is called `results_df`. The parameters are listed below. It is important to run this function because it makes the the output is the same length as `sen_itr` by adding blank rows where predictions were not made.
* `sen_itr`: List of product names in the form `['brand', 'title']`. Same as input into `model_run`.
* `all_list`: List of predicted PUCs, first output from `model_run`.
* `removed`: List of removed values, second output from `model_run`.
* `proba_pred`: List of probabilities, third output from `model_run`.
* `puc_list`: List of PUC names, fourth output from `model_run`.
* `proba_limit`: Bool for whether to include probabilites in output DF (if available). Can be a float to use a probability cutoff.
* `label`: Model label, should match the label used when building the model. Defaults to `''`.

```python
from model_helper import results_df
results = results_df(sen_test, puclist, removed, problist,
                     probnames, proba_limit=0.8, label='boot')
```

There is a file called `run.py` included in this repo that has an example of how to run all of these commands together.

## Requirements

### TLDR: Run these commands in a new conda environment
This will install all the required packages, getting them using `conda` before `pip`.

```bash
conda install python pandas sqlalchemy nltk pymysql scikit-learn joblib

conda install -c conda-forge spacy spacy-lookups-data

python -m spacy download en_core_web_sm

pip install flair
```

### Details
Unless otherwise noted, packages are on the main Anaconda channel. Flair has many dependencies, which you may want to install via `conda` rather than `pip`. See below for details.
* Python (tested on 3.7)
* Pandas
* SQLAlchemy
* NLTK
* PyMySQL
* scikit-learn
* joblib
* spaCy (conda-forge)
* spacy-lookups-data (conda-forge)
* Flair (pip, **see below**)

Before installing Flair, install `pytorch` by copying the command [here](https://pytorch.org/get-started/locally/). If you don't have an Nvidia GPU , select 'None' for CUDA. Also, there are many flair dependencies that are available via Anaconda. If you want to install these via Anaconda, do it before installing Flair, or else they will be automatically installed via `pip`. If you just want to use `pip`, you don't need to do anything with the other packages. See [Flair's requirements](https://github.com/zalandoresearch/flair/blob/master/requirements.txt) for more details.

This script was recently updated to work on flair version 0.5.1. This package changes frequently so future versions may not be compatible.

Finally, you will need to run this in the command line: `python -m spacy download en_core_web_sm`.
