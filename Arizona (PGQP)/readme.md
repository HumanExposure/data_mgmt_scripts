# Arizona Department of Environmental Quality Pesticide Groundwater Quality Protection Annual Reports

Reports contain information regarding the use of pesticides in the State of Arizona.  Occasionally, the function of the chemical pesticide is also given.  Each report was extracted with a customized script to account for formatting changes from report to report.

## Requirements

All scripts were run using Spyder in a Python 3.8.5 environment using the packages:
* Pandas
* Camelot


To reproduce the environment, run the following commands in Anaconda Powershell
```bash
conda create --name py385 python=3.8.5
conda activate py385
conda install -c anaconda pandas
conda install -c conda-forge camelot-py
```

## Usage

1. Manually create new Data group for each report.
2. Write and upload Registered Records CSV
3. Get new Registered Records document from Factotum, and use to get Data Document IDs
4. Run script and upload extracted data CSV
