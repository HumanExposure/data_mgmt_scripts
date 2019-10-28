## How this Script Works
This document will breifly go though the steps that the script takes to make its predictions.

### Obtaining and cleaning training data
Product names and PUCS are pulled from factotum with the following query:
```sql
SELECT puc_id, product_id, brand_name, title, gen_cat, prod_fam, prod_type, description FROM ( SELECT brand_name, title, puc_id, product_id FROM (select id, brand_name, title from dashboard_product) as product INNER JOIN (select puc_id, product_id from dashboard_producttopuc) as prod_to_puc ON product.id = prod_to_puc.product_id ) as product_match INNER JOIN (select * from dashboard_puc) as puc ON product_match.puc_id = puc.id;
```
Cleaning is done using regular expressions to remove symbols and other irregularities, including some numbers and stopwords. The PUCs are also lemmatized and stopwords are removed.
