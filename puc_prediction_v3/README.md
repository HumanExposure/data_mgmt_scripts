# PUC Prediction
The purpose of this set of scripts is to use a *product name* to predict a *Product Use Category* (PUC). Below are instructions for running the code.

# Environment Set-up

### TL;DR: Run these commands in a new conda environment
This will install all the required packages, getting them using `conda` before `pip`.
```bash
#Create a new environment (name can be anything)
conda create --name pucModel_3.7 python=3.7
#Activate the environment
conda activate pucModel_3.7
#Install packages
conda install python pandas sqlalchemy nltk pymysql scikit-learn joblib openpyxl
#conda forge
conda install -c conda-forge spacy spacy-lookups-data boruta_py
#spacy package
python -m spacy download en_core_web_sm
```
`pytorch` install command changes depending on NVIDIA GPU or CPU usage
#Before installing Flair, install `pytorch` by copying the command [here](https://pytorch.org/get-started/locally/). 
```bash
#Linux install pytorch with CPU example
conda install pytorch torchvision torchaudio cpuonly -c pytorch
#Install flair last
pip install flair
```

### Details
Unless otherwise noted, packages are on the main Anaconda channel. `Flair` has many dependencies, which you may want to install via `conda` rather than `pip`. See below for details.

Package versions listed are the latest the code has been tested on. Older version may still work.
* `python` (tested on 3.6 and 3.7)
* `pandas` 1.3.1
* `SQLAlchemy` 1.4.22
* `NLTK` 3.6.2
* `PyMySQL` 1.0.2
* `scikit-learn` 0.24.2
* `joblib` 1.0.1
* `openpyxl` 3.0.7
* `spacy` 3.1.1 (conda-forge)
* `spacy-lookups-data` 1.0.0 (conda-forge)
* `boruta_py` 0.3.0 (conda-forge)
* `Flair` 0.8.0.post1 (pip, **see below**)

Before installing Flair, install `pytorch` by copying the command [here](https://pytorch.org/get-started/locally/). 
If you don't have an Nvidia GPU , select 'None' for CUDA. Also, there are many flair dependencies that are available via Anaconda. 
If you want to install these via Anaconda, do it before installing Flair, or else they will be automatically installed via `pip`. 
If you just want to use `pip`, you don't need to do anything with the other packages. 
See [Flair's requirements](https://github.com/zalandoresearch/flair/blob/master/requirements.txt) for more details.

The flair package changes frequently so future versions may not be compatible.

# How to Use
All of the following functions can be imported from the `puc_model` module subfolder. 
See these modules for more info about function parameters. All generated model assets are stored in the `models` subfolder using the input `label` parameter.

**Important:** Be sure to match `label` parameter values between scripts and functions to ensure model assets produced from each step is carried through on the same model run name.

### Pull and prepare model data
Model training, test, and validation data are prepared from a direct data pull from the `Factotum` database.

In the root of the model code directory, users must edit the `mysql.json` file with Factotum database credentials:
```json
{
	"mysql": {
		"username": "username",
		"password": "password",
		"server": "Facotum Server host",
		"port": "port number",
		"database": "Factotum database name"
	}
}
```
Preparation steps include download, cleaning, and vectorization. Processing time varies by dataset size. (**Benchmark:** ~100k products in 1.5 hours)

As long as training data doesn't change, this only needs to be performed once. If you ever want to refresh the model with new data from factotum, you will need to run this function again. It is recommended to use a computer that has a decent amount of RAM and free storage space (i.e. not your laptop).

Many files ending in `.joblib` are cached by running this function; do not delete them.

`model_initialize` is the required function and takes the following inputs:
* `add_groups`: List of data groups with additional products to add. Typically used to add negative cases of products without PUCs that should not be categorized. 
This argument is optional if you don't want to add any data groups. Defailts to `[]`.
* `label`: A label for the saved data. This label lets you run and save multiple models at the same time. 
This label should be used for building and running the model, as well. Defaults to `''`.
* `recordMin`: Integer for the minimum records a PUC should have before it will be used to make a PUC model. Default is `30`.
* `pucType`: String filter to certain PUC Kind levels. Default is `all`, with input options of `UN`, `FO`, `AR`, or `OC`.
* `overwrite`: Boolean whether to overwrite a previous model's assets with the same `label`. Default is `False`.

```python
#Example model initialization found in run_model_initialize.py
from puc_model.model_initialize import (model_initialize)
label = 'envTest'
model_initialize(add_groups=[37, 47, 30], label=label, recordMin=100,
                 pucType='all', overwrite=True)
```
Users will be prompted to run `run_xdata_components_dump.py` script once data is pulled and cleaned. This is a script that generates a word embedding model to vectorize input product names.

`run_xdata_components_dump.py` is the script that takes the following inputs:
* `parallel`: A boolean of whether to run the vectorization in parallel. Default is `True`.
* `label`: A label for the saved data. This label lets you run and save multiple models at the same time. 
This label should be used for building and running the model, as well. Defaults to `''`.

```bash
#Remember to match the `label` parameter before running.
python run_xdata_components_dump.py
```
`run_xdata_components_dump.py` will run through the entire preprocessed dataset created from `model_initialize` and create word embedded vectors per product in grouped subsets (n=500 products default - RAM limits may allow increase or require decreased group sizes). Vectors are cached in `models/model_*label*/components/`.

### Building PUC tiered models
Once data has been prepped, the script `run_model_selection_train.py` contains a workflow to build models.

This script will:
1. Split prepared data into 10% validation, 90% building (80% training, 20% testing) datasets.
2. Create `n_models` per PUC level based on `modelType`, with feature selector (if `get_fs` is `True`)
3. Create Voting Classifier (VC) models per PUC level (using generated feature selector if `get_fs` is `True`).
4. Perform Grid Search to find optimal parameters for the selected model type and input training data
5. Log performance metrics for individual and VC models
    * Cross Validation (`get_cv = True`)
    * Domain of Applicability analysis (`get_DA = True`)
    * Generated reports and log files (see `output` folder for a given model `label`)
6. Log validation dataset performance metrics (e.g. accuracy, precision, F1-score)

`run_model_selection_train.py` takes the following parameters:
* `label`: A label for the saved data. This label lets you run and save multiple models at the same time. 
This label should be used for building and running the model, as well. Defaults to `''`.
* `pucType`: String filter to certain PUC Kind levels. Default is `all`, with input options of `UN`, `FO`, `AR`, or `OC`.
`modelType`: String of the type of model to train (e.g. `SVM`, `RF`, `SGD`). Defaults to `SGD`
`n_models`: Integer number of models to train. Defaults to `5`.
`del_models`: Boolean of whether to delete all models for a `label`. Defaults to `False`.
`parallel`: Boolean of whether to run model generation in parallel. Defaults to `True`.
`get_fs`: Boolean of whether to perform feature selection. Defaults to `False`.
`get_cv`: Boolean of whether to perform cross validation on VC models. Defaults to `False`.
`get_DA`: Boolean of whether to perform Domain of Applicability analysis for VC models. Defaults to `False`.
`setName`: String value to set which dataset to use for `run_model_validation` function. Default is `val`.
`predKindBool`: Boolean of whether to predict PUC kind for `run_model_validation` function. Defaults to `False`.
`pred_proba`: Boolean of whether to generate predicted probabilities for `run_model_validation` function. Defaults to `True`.

```bash
#Remember to match the `label` parameter before running.
#Set parameters listed above before running.
python run_model_selection_train.py
```

### Making predictions
To make predictions, input data must be prepared in the same fashion as the models' training data. This includes cleaning, vectorization (using the same embedding model), and scaling (same scaler). All model assets should have been cached in the model's `components` folder.

`model_utils.py` has two functions to help make predictions:
* `format_prediction_input`: Takes prediction input and converts it into the expected DataFrame format (if not already a DataFrame).
* `run_model_prediction`: Prepares the data and makes predictions based on cached model assets.
    * `label`: A label for the saved data. This label lets you run and save multiple models at the same time. 
This label should be used for building and running the model, as well. Defaults to `''`.
    * `pucKind`: String filter to certain PUC Kind levels. Default is `all`, with input options of `UN`, `FO`, `AR`, or `OC`.
    * `modelType`: String of the type of model to train (e.g. `SVM`, `RF`, `SGD`).
    * `pred_proba`: Boolean of whether to generate predicted probabilities for `run_model_validation` function. Defaults to `True`.

See `run_model_prediciton.py` for an example of how to make model predictions from existing models.

Allowed prediction input:
* DataFrame (title, brand_name, manufacturer columns)
* String (title, brand_name, manufacturer concatenated)
* List of strings
* Tuple (title, brand_name, manufacturer)
* List of tuples
* Dictionary (title, brand_name, manufacturer keys)

```bash
#Console run of model predictions
#Set parameters listed above before running.
python run_model_prediciton.py
```

### Running the full workflow
All `run_*.py` files included in this repo provide examples for how to run the full workflow.

1. run_model_initialize.py
2. run_xdata_components_dump.py
3. run_model_selection_train.py
4. run_domain_applicability.py (optional)
5. run_model_prediction.py