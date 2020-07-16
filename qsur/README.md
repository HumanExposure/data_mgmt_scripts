# QSUR Scripts
This set of scripts uses training data to create a model that maps a chemical's raw functional use to a harmonized functional use.

An example of how to run the scripts is located in `run.py`. The important details are below. For additional information, check the docstrings in the scripts.

## Before you start
### Preparation
All of the scripts should be in the same folder. Additionally, you need a sub-folder named `store`. This is where intermediate and cached files will be stored. The word embeddings models will need to be a folder called `bert`. Instructions on how to download the models are in the Other Info section. A few packages need to be installed. Instructions for this are also in Other Info.

### Training Data
The training data needs to be prepared before running. The training data consists of two parts: the default OECD functions and mappings, and user supplied data.

The default mappings are derived from the information contained in `oecd.py`. There is a dictionary of the OECD functional uses and their definitions `oecd_def`. This dictionary is important, and the keys represent the classes the model will use. This dictionary should not need to be changed, save updating the functional uses to match those the OECD ones. 
`oecd_ont` contains other names for the OECD functional uses as defined in the definitions. `map` contains a manual mapping of various functional uses to the harmonized ones. You could add synonyms here to improve classification. Additionally, there's another dictionary called `manual_fix`. The model uses the keys of `oecd_def` as classes. Some training data, including `oecd_ont` and `maps`, have classes that don't quite match these harmonized ones, so fuzzy matching is used to align them. If fuzzy matching to a class in `oecd_def` doesn't work, you can add an entry to `manual_fix` to directly map a functional use to a harmonized one (this is for training data only). Once everything is mapped correctly, the dictionaries in `oecd.py` are used to create a basic training set.

The user can also supply training data. All of this data should be added to the `get_training_set` function in `make_training_data.py`. Here you can load and format whatever dataset you want. In the end, it must be a DataFrame with the following columns: `report_funcuse`, `harmonized_funcuse`, and `raw_chem_name` (can be NAN). There are a few helper functions too. Below is an example of how they are used when importing data. Ideally, new training data will have a 1 to 1 match between reported functional use and harmonized functional use. The script can deal with multiple functional uses in one line, but it's not ideal. See the doctring for `format_splits` for details.

```python
df2 = pd.read_csv(
    'fudc_7-15-20.csv', index_col=0) \
    .reset_index(drop=True) \
    .rename(columns={'reported_functional_use': 'report_funcuse',
                     'technical_function': 'harmonized_funcuse'})
df2 = df2[['report_funcuse', 'harmonized_funcuse']]
df2_split = format_splits(df2, df_default, strict=False)
df2_split['raw_chem_name'] = np.nan
df2_formatted = format_training_set(df2_split)
```

The above code loads data that is in a CSV file, and renames the columns to match what was stated above. If there's no `raw_chems_name` column, you can create one and make it NAN. The other important part of this code is the `format_training_set` function. This takes the DataFrame and matches the functional uses to the necessary classes. It's not necessary if these are already matched in the first place. There is also a function called `format_splits`. If there are multiple harmonized functional uses, this function looks to see if there is a corresponding reported functional use. It also removed lists formatted into strings in the training set.

You can load multiple datasets like this. Make sure to add it to the list in `pd.concat` at the end of the function.


## Building the Model
### Model Options
Before running the model, you can set a few options.
```python
from model_run_helper import model_opts
opts = model_opts(label='testing', bert='bio', cval=1)
```
As in the example above, you can call `model_opts` and use various parameters to change the defaults. Here is a list of things you can change.
* `bert`: Controls which word embeddings model to use. Values can be `bio` ([model](https://github.com/dmis-lab/biobert)), `sci` ([model](https://github.com/allenai/scibert)), or '' (uses default bert model)
* `reset`: Bool for whether to used cached embeddings if they exist, or make new ones
* `label`: Label for all output and intermediate files. Will overwrite other runs that have the same label.
* `cval`: C value for SVM

There are some other parameters that you should not change (they come from other iterations/uses of parts of the code).
* `ref`: Keep this as `key`.
* `document`: Bool for whether to use document embeddings. Keep to `True`. If it's false it would only use the embeddings for the first subword.
* `flair`: Bool for whether to add flair embeddings. Would make it more accurate but you need a lot of training data.
* `cosine`: An experiment where instead of word vectors, vectors with the distance to each class were created and used to train the model.

### Load Data
Next we have to load the training data, which includes cleaning it and creating the word embeddings. The training data itself should be added as mentioned earlier.

```python
from make_training_data import load_training_data
df_train, data = load_training_data(opts, reset=False)
```
`opts` was created previously, and the `reset` parameter is a bool for whether to use a cached version of the training data. Both of the returned values will be used in future functions.

### Build the Model
```python
from model_run_helper import model_build
model_build(df_train, opts, data,
            bootstrap=True, num_runs=11, probab=True)
```
To build the model, you call `model_build`. The parameters are listed below. This function saves the model to the folder `store`.
* `df_train`: Training data from previous step.
* `opts`: Options dictionary from earlier.
* `data`: List from previous step.
* `bootstrap`: Bool for whether to sample with replacement for each run.
* `num_runs`: Number of times to run the model. Runs are aggregated.
* `sample_size`: Number of times to sample the dataset for each model run. Can be a number or `all`.
* `probab`: Bool for whether to calculate probabilities. Adds run time.

## Making Predictions
### Preparing a Test Set
The test set should be an iterable (like a list or Series) of strings, with each string being a functional use you want to map. It should not be a DataFrame.

### Using the Model
```python
from model_run_helper import predict_values
final_df = predict_values(sen_itr, opts, raw_chems,
                          proba_limit=True, calc_similarity=True)
```
All of the prediction functions are wrapped in `predict_values`. The parameters are listed below.
* `sen_itr`: List-like object of strings to predict.
* `opts`: Options dictionary from earlier.
* `raw_chems`: A list of chemical names. Should be the same length as `sen_itr`, with each chemical having a corresponding functional use. This is optional.
* `proba_limit`: Changes behavior regarding probability. If `True`, probabilities for each prediction will be added to the final DataFrame (if `False`, they will not). If it's a number, a cutoff will be imposed on the predictions (e.g. if it's set to 0.5, only predictions with over 0.5 probability will be returned). You must have set `probab` to `True` when building the model for this to do anything.
* `calc_similarity`: Whether to add text similarities between the input and predicted values.

The output of this function is a DataFrame, which you can then save.

## Other Info
### Requirements
Below is a list of package requirements. You will likely need to run all of this on Linux.
* Python (tested on 3.7)
* Flairn (updated to work with 0.5.1)
* PyTorch
* Pandas
* Numpy
* Joblib
* Scikit-learn
* Spacy
* SQLAlchemy
* PyMySQL
* Fuzzywuzzy
* xlrd

To easilly install all of the requirements, you can run the following in a new conda environment.
```bash
conda install python pandas sqlalchemy nltk pymysql scikit-learn joblib xlrd
conda install -c conda-forge spacy spacy-lookups-data
python -m spacy download en_core_web_sm
pip install fuzzywuzzy[speedup]
pip install flair
```
If you're running on an older operating system, you may get an error about C libraries when you import Flair. To solve this, you can run `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/miniconda3/lib/`. Replace `$HOME/miniconda3` with the path to your Anaconda folder. If you want to undo this, you can run `unset LD_LIBRARY_PATH`. 

### Downloading Models
There are three word embeddings models that you can use by setting the proper value when running `model_opts`. This section details where to download the models for `sci` and `bio`. Any other value will cause the default english language model to be used, which will be automatically downloaded.

To download the SciBERT model, go to [this](https://github.com/allenai/scibert) page and download the `scibert-scivocab-uncased` model under `PyTorch HuggingFace Models`. On download, unpack the `.tar` file. The folder structure, relative to the scripts, should be `bert/scibert_scivocab_uncased`.

The process for BioBERT is more complicated. Download `BioBERT-Base v1.1` from [here](https://github.com/dmis-lab/biobert) (you can download the large one too but everything takes longer). You will need to follow the steps below to transform this model. After you're done, the folder `bert-base-biobert-cased` needs to be in the `bert` folder with `scibert_scivocab_uncased`. 

```bash
conda create --name pytorch-transformers python tensorflow
conda activate pytorch-transformers
conda install pytorch torchvision cpuonly -c pytorch
pip install transformers
export LD_LIBRARY_PATH="$HOME/miniconda3/envs/pytorch-transformers/lib"

wget LINK_TO_BIOBERT_FILE
tar -xzf biobert_v1.1_pubmed.tar.gz
mv biobert_v1.1_pubmed bert-base-biobert-cased
cd bert-base-biobert-cased
transformers-cli convert --model_type bert \
  --tf_checkpoint ./model.ckpt-1000000 \
  --config ./bert_config.json \
  --pytorch_dump_output ./pytorch_model.bin
mv bert_config.json config.json
unset LD_LIBRARY_PATH
conda deactivate
conda remove --name pytorch-transformers --all
```

### Other Data Sources
`data.py` contains two functions to load data. `cpdat_data` can load a file called `functional_uses.xlsx` from CompTox (it's in one of the ZIP files on the downloads page) while `factotum_data` will load all of the functional use data from Factotum. These might be more suited as a test set.

### Notes on Model
Not all model parameters are exposed. They are located in `train_model.py`, and are copied below. The documentation for this model is [here](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html).

```python
clf = svm.SVC(gamma='scale', decision_function_shape='ovo',
              cache_size=20000, kernel='linear', C=cval,
              probability=proba, class_weight='balanced')
```

A note on probability: if you're predicting probability, you'll notice that two seperate prediction values are returned. One is the normal SVM prediction, and the other comes from the probability prediction. They should be the same, but since the probabilities are calculated separately, they could technically be different. I've never encountered an example of when they were different, but they have been included for completeness. More info [here](https://scikit-learn.org/stable/modules/svm.html#scores-probabilities). Also, if you don't have much training data, the probabilities will generally be lower.

### Multiple Funtional Uses
Sometimes, there are multiple functional uses in one field. This is usually from one chemical having multiple uses. This model splits these uses (in `data.py`) and treats them as separate entries. When outputting the test set, split functional uses are reassembled, with ` / ` as a separator (can be changed).

