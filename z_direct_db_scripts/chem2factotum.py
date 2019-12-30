from dotenv import load_dotenv
import pymysql.cursors
import os

# This script takes a tsv file from prod_dsstox with this query:

#  select cl.name, ss.external_id, ss.dsstox_record_id, gs.dsstox_substance_id
#  from chemical_lists cl
#  join source_substances ss on ss.fk_chemical_list_id = cl.id
#  left join source_generic_substance_mappings sgm on sgm.fk_source_substance_id = ss.id
#  left join generic_substances gs on gs.id = sgm.fk_generic_substance_id
#  where cl.name like 'Factotum_chemicals01';

# It reads through the file and inserts new records as needed and updates records as needed.

load_dotenv()

mhost = os.getenv("HOST")
muser = os.getenv("MSQL_USER")
mpasswd = os.getenv("PASSWD")
mdb = os.getenv("DB")

db = pymysql.connect(host=mhost,
                     user=muser,
                     db=mdb,
                     passwd=mpasswd)

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print(data)
db.close()
