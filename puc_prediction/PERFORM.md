## Model Performance

### Accuracy
The following code was run to test for model accuracy. For this test, 11 runs were aggregated, but the difference between 11 runs and something like 5 runs is not very large.
```python
from model_helper import model_build, model_run
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split

df = pd.read_csv('clean.csv', index_col='key')
df_train, df_test = train_test_split(df, test_size=0.2)
sen_test = df_test['name'].to_list()
model_build(df, df_train, bootstrap=True, num_runs=11, label='perform')
puclist = model_run(sen_test, 'perform')

PUC_act = df_test[['gen_cat', 'prod_fam', 'prod_type']].fillna('').apply(
    lambda x: x.to_list(), axis=1).to_list()
ct = np.array([0] * 3)
for i in range(len(puclist)):
    if puclist[i] == PUC_act[i]:
        ct += 1
    else:
        for n in range(3):
            if puclist[i][:n+1] == PUC_act[i][:n+1]:
                ct[n] += 1
ct = ct / len(puclist)
print(ct)
```
Results are as follows:
* **gen_cat accuracy:** 98.9%
* **prod_fam accuracy:** 97.9%
* **prod_type accuracy:** 97.2%

### Data Breakdown
We obtained a high accuracy using this model, but it would be helpful to break down the results a little bit more. One thing we can do is look at the accuracy of each category. This is important because some categories are very large, while others are very small.

Below we have a table showing the different classifications in `gen_cat`.

![gen_cat table](images/gen_cat_table.PNG)
