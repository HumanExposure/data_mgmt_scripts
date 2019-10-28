# PUC Prediction
The purpose of this set of scripts is to use a product name to predict a PUC. Below are instructions for running the code.

## How to Use
### Generate model data
As a perquisite for using this model, a few pieces need to be generated. Both of these scripts will take a while to run, but only need to be run once. I would also recommend using a computer that has a decent amount of ram and free storage space (i.e. not your laptop).
* Run `data_processing.py`. This script pulls every product name and PUC from factotum and cleans them up. `mysql.json` needs to be filled out for this to work. Two CSV files will be created containing the data that was retrieved, with `clean.csv` being the important one.
* Run `puc_model.py`. This script will take a while to run. Here is a list of important files that will be generated:
  * `xdata.joblib`: A file containing the result of converting every product name to a vector.
  * `PUC_doc_embeddings.joblib`: The model used for generating the above data. If this is lost, any saved models become useless.
  * `PUD_key.csv`: A key for converting predicted PUCs back into their respective categories. This can easily be regenerated.
If you ever want to refresh the model with new data from factotum, you will need to run both of these scripts again.

### Building a model
The script `model_helper.py` contains functions to make building a model straightforward. The function you will want to use is called `model_build`. If you need more control of the model, you can directly use `build_model` in `puc_model.py`. Multiple files are saved after running this method; these are the actual trained models. After training these models once, they do not need to be trained again.

`model_build` takes the following as inputs:
* `df`: The entire dataset used to generate the model data (i.e. clean.csv).
* `df_train`: A subset of the dataset that is used for training the models. Should be a DataFrame, and can be the same as `df`.
* `num_runs`: Number of times to fit the model before aggregating it.
* `bootstrap`: Whether to sample `df_train` with replacement or not (recommended to be set to `True` if `num_runs` is more than 1).
* `sample_size`: Size of the training set for each run (sampled from the training set). If there are multiple runs, each sample from the training set will be this large. Can be a number, or `all` (recommended).
* `label`: A label for the saved models. This label is used for running model predictions, as well. Any models with the same label will be overwritten.

```python
from model_helper import model_build
import pandas as pd

df = pd.read_csv('clean.csv', index_col='key')
model_build(df, df, bootstrap=True, num_runs=5, label='boot')
```

### Making predictions
`model_helper.py` also contains a function to help with predictions, `model_run`. It takes a list of product names as the input. The list should be in the form `[['brand1', 'title1'], ['brand2', 'title2']]`, but can also just be a list of names. This script will clean and vectorize the product names before using the model to make a prediction. There is also a label field; this field needs to be the same as when training the model. The output will be an array of PUCs in the form `[['gen_cat', 'prod_fam', 'prod_type'], ...]`.

```python
from model_helper import model_run
import pandas as pd

prod_names = [['clorox', 'extra fancy bleach'], ['crayola', 'purple crayons']]
puclist = model_run(prod_names, 'boot')
```

## Requirements
Unless otherwise notes, packages are on the main Anaconda channel. Many packages exist as dependencies to Flair.
* Python (tested on 3.7)
* Pandas
* SQLAlchemy
* NLTK
* PyMySQL
* scikit-learn
* joblib
* spaCy (conda-forge)
* spaCy-lookups-data (conda-forge)
* Flair (pip, **see below**)

Before installing Flair, install `pytorch` via the following command: `conda install pytorch torchvision cpuonly -c pytorch`. Also, the following are all dependencies to Flair that are available via Anaconda. If you want to install these via Anaconda, do it before installing Flair. If you just want to use `pip`, you don't need to do anything with the packages below. See [Flair's requirements](https://github.com/zalandoresearch/flair/blob/master/requirements.txt) for more details.
* matplotlib (Flair dependency)
* mpld3=0.3 (Flair dependency)
* pymongo (Flair dependency)
* pytest (Flair dependency)
* regex (Flair dependency)
* cython (Flair dependency)
* sortedcontainers (Flair dependency)
* urllib3=1.24.2 (Flair dependency)
* ipython=7.6.1 (Flair dependency)
* ipython_genutils=0.2.0 (Flair dependency)
* transformers (conda-forge; Flair dependency)
* langdetect (conda-forge; Flair dependency)
* sqlitedoct (conda-forge; Flair dependency)
* tabulate (conda-forge; Flair dependency)
* hyperopt (conda-forge; Flair dependency)
* deprecated (conda-forge; Flair dependency)
* gensim (conda-forge; Flair dependency)

Finally, you will need to run this in the command line: `python -m spacy download en_core_web_sm`.
