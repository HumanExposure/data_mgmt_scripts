from dotenv import load_dotenv
import pymysql.cursors
import os
import sys
import csv
import logging
import time

# This script takes a tsv file from prod_dsstox with this query:

#  select cl.name, ss.external_id, ss.dsstox_record_id, gs.dsstox_substance_id
#  from chemical_lists cl
#  join source_substances ss on ss.fk_chemical_list_id = cl.id
#  left join source_generic_substance_mappings sgm on sgm.fk_source_substance_id = ss.id
#  left join generic_substances gs on gs.id = sgm.fk_generic_substance_id
#  where cl.name like 'Factotum_chemicals01';

# It reads through the file and inserts new records as needed and updates records as needed.
# Set up enviroment variables
load_dotenv()

mhost = os.getenv("HOST")
muser = os.getenv("MSQL_USER")
mpasswd = os.getenv("PASSWD")
mdb = os.getenv("DB")

# Set up MySQL database
db = pymysql.connect(host=mhost,
                     user=muser,
                     db=mdb,
                     passwd=mpasswd)

cursor = db.cursor()

# Check for arguments to grab the filename/path

if len(sys.argv) < 1:
    print("Add path to csv and filename as argument")
else:
    fname = sys.argv[1]
    logname = os.path.basename(fname) + ".log"
    logging.basicConfig(filename=logname,
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

# set up / initialize counters
external_id_not_in_factotum = 0
external_id_in_factotum = 0
chemical_with_sid = 0
chemical_with_rid = 0


# Start the main program
# Open the file and start reading
with open(sys.argv[1], newline='', ) as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for row in reader:
        external_id = row['external_id']
        dsstox_rid = row['dsstox_record_id']
        dsstox_sid = row['dsstox_substance_id']
        preferred_name = row['preferred_name']
        casrn = row['casrn']
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        # Does the external id exist in Factotum?
        sql = "SELECT * FROM dashboard_rawchem WHERE id = '%s'" % external_id
        cursor.execute(sql)
        data = cursor.fetchone()
        # If there is a row in factotum in the raw_chem table check for rid
        if data:
            logging.info("%s processing" % row['external_id'])
            external_id_in_factotum += 1
            factotum_id = data[0]
            raw_cas = data[1]
            raw_chem_name = data[2]
            rid = data[5]

            if rid:
                logging.info("%s already has rid %s assigned." % (factotum_id, rid))
            else:
                logging.info("Checking if SID already exists")
                sql = "SELECT * FROM dashboard_dsstoxlookup WHERE sid = '%s'" % dsstox_sid
                print(sql)
                cursor.execute(sql)
                lookup = cursor.fetchone()
                if lookup:
                    logging.info("Entry exists in dsstox_lookup, linking to rawchem")
                    sql = "UPDATE dashboard_rawchem SET dsstox_id = '%i', rid = '%s' " \
                          "WHERE id = '%i'" % (lookup[0], dsstox_rid, factotum_id)
                    print(sql)
                    print("data = %s" % data)
                    print("row = %s" % row)
                    cursor.execute(sql)
                    db.commit()
                else:
                    logging.info("%s : adding rid and sid to factotum")
                    sql = "INSERT INTO dashboard_dsstoxlookup (created_at, sid, true_cas, true_chemname) " \
                          "VALUES ('%s', '%s', '%s', '%s')" % (now, dsstox_sid, casrn, preferred_name)
                    print(sql)
                    cursor.execute(sql)
                    db.commit()
                    sql = "SELECT * FROM dashboard_dsstoxlookup WHERE sid = '%s'" % dsstox_sid
                    print(sql)
                    cursor.execute(sql)
                    link = cursor.fetchone()
                    sql = "UPDATE dashboard_rawchem (dsstox_id, rid, updated_at) " \
                          "values (%i, '%s', '%s') WHERE id = %i" % (link[0], rid, now, factotum_id)
                    print(sql)
                    cursor.execute(sql)
                    db.commit()
        else:
            logging.info("%s does not exist in Factotum.dashboard_dsstox" % row['external_id'])
            external_id_not_in_factotum += 1

db.close()
print("Added %s" % external_id_not_in_factotum)
print("Skipped %s" % external_id_in_factotum)
