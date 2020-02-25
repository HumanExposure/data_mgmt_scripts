# PUC Prediction
The purpose of this set of scripts is to use a product name to predict a PUC. Below are instructions for running the code.

## How to Use
All of the following methods can be imported from `model_helper.py`. See this file for more info about the parameters.

### Generate model data
As a perquisite for using this model, a few pieces need to be generated. This takes a while to do, but only needs to be done once as long as the training data doesn't change. If you ever want to refresh the model with new data from factotum, you will need to run this function again. I would also recommend using a computer that has a decent amount of RAM and free storage space (i.e. not your laptop). Many files ending in `.joblib` are saved by running this function; do not delete them.

`model_initialize` is the required function and takes the following inputs:
* `add_groups`: List of data groups with additional products to add. These products should be ones that have no PUCs and should not have PUCs. The purpose of adding these groups is to train the model on products that shouldn't be assigned PUCs. This argument is optional if you don't want to add any data groups.
* `label`: A label for the saved data. This label lets you run and save multiple models at the same time. This label should be used for building and running the model, as well.

```python
from model_helper import model_initialize
model_initialize([47])
```
**Important:** If you run this again after building a model, that model will no longer work because the file containing the word embedding information will overwritten. 

### Building a model
The script `model_helper.py` contains functions to make building a model straightforward. The function you will want to use is called `model_build`. Multiple files are saved after running this method; these are the actual trained models. After training these models once, they do not need to be trained again.

`model_build` takes the following as inputs:
* `df_train`: A subset of the dataset that is used for training the models. Should be a DataFrame, can also be a string to use the whole training set.
* `num_runs`: Number of times to fit the model before aggregating it.
* `bootstrap`: Whether to sample `df_train` with replacement or not (recommended to be set to `True` if `num_runs` is more than 1).
* `sample_size`: Size of the training set for each run (sampled from the training set). If there are multiple runs, each sample from the training set will be this large. Can be a number, or `all`. Since SVMs can be slow with many samples, this parameter is designed to allow for fitting subets of the data in different runs to speed up computation time.
* `label`: A label for the saved models. This label is used for running model predictions, as well. Any models with the same label will be overwritten.
* `probab`: Whether to calculate probabilities for the classes. Enabling this will increase computation time.

```python
from model_helper import model_build
model_build(df_train='all', bootstrap=True, num_runs=5, label='boot')
```

### Making predictions
`model_helper.py` also contains a function to help with predictions, `model_run`. It takes a list of product names as the input. The list should be in the form `[['brand1', 'title1'], ['brand2', 'title2']]`, but can also just be a list of names. This script will clean and vectorize the product names before using the model to make a prediction. There is also a label field; this field needs to be the same as when training the model. The output will be an array of PUCs in the form `[['gen_cat', 'prod_fam', 'prod_type'], ...]`.

`model_run` takes the following as inputs:
* `sen_itr`: List of product names in the form `['brand', 'title']`
* `label`: Model label, should match the label used when building the model
* `mode`: Whether to take the mode of the different runs or just output the results of all runs
* `proba`: Whether to output probabilities (need to enable the flag when building the model, as well)

There are three lists that are returned by the function:
* A list of predicted PUCs (form depending on `mode` flag)
* A list of probabilities (blank if `proba=False`)
* A list of predicted PUC names for each level based on the probability (used for formatting the list of probabilities, blank if `proba=False`)

```python
from model_helper import model_run

prod_names = [['clorox', 'extra fancy bleach'], ['crayola', 'purple crayons']]
puclist, problist, probnames = model_run(prod_names, 'boot')
```

## Requirements

### TLDR: Run these commands in a new conda environment
This will install all the required packages, getting them using `conda` before `pip`.

```bash
conda install python pandas sqlalchemy nltk pymysql scikit-learn joblib

conda install -c conda-forge spacy spacy-lookups-data

conda install pytorch torchvision cpuonly -c pytorch  # can install the cuda version if you have an nvidia gpu, see https://pytorch.org/get-started/locally/

flair_version="$(echo "$(curl -sS https://github.com/flairNLP/flair/releases/latest)" | sed -n -E "s@.*https://github.com/flairNLP/flair/releases/tag/v(([0-9]+\.?)+).*@\1@p")"

wget "https://github.com/flairNLP/flair/archive/v"$flair_version".tar.gz"

tar -xvzf "v"$flair_version".tar.gz" "flair-"$flair_version"/requirements.txt" --strip-components=1

while read requirement || [ -n "$requirement" ]; do conda install --yes $requirement || conda install -c conda-forge --yes $requirement; done < requirements.txt > /dev/null 2>&1

rm requirements.txt "v"$flair_version".tar.gz"

# fix a few things up
conda install networkx==2.2 filelock  # needs older version
conda install -c conda-forge transformers # install an older version to get dependencies before replacing with pip version

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

Finally, you will need to run this in the command line: `python -m spacy download en_core_web_sm`.
