# prod_chemical_release

Files and scripts to push [Standardized Emission and Waste Inventories (StEWI)](https://github.com/USEPA/standardizedinventories) output data into a relational database. This works for a selected version of StEWI output (e.g. v1.0.5) and currently stores `flow`, `flowbyfacility`, and `facilty` data outputs from StEWI.

StEWI Output files are automatically downloaded and stored in the same local data directory as used by StEWI software. See [Local Data Storage](https://github.com/USEPA/standardizedinventories/wiki/Data-Storage#local-storage) for more information.

## Requirements
1. R > 3.6 along with a number of publicly available packages specified in the main R script (see Usage).
2. Admin credentials for a running local or remote MySQL database server.
3. ~6 GB of available disk space (5+ for MySQL and 1 for output file storage) 

## Setup and Usage
The [combine_stewi_files.R](scripts/combine_stewi_files.R) script performs the work. Before the script can be run, a MySQL database called 'prod_chemical_release' must be created using an existing database schema - either .sql or .mwb files can be used to set up the database with the required tables. See the database_models below under Associated files. An .Renviron file must be create and put into the same folder in which this directory resideswith keys and values for the database connection including `mysql_user`, `mysql_pass`, and `mysql_host`. See the main R script for more instructions.

## Associated Files
- StEWI output files are retrieved from the Data Commons and are in Apache parquet format. Output files specific to a version of StEWI are listed in a markdown table in a StEWI Wiki page. 

- [database_models](database_models/) with MySQL Workbench .mwb and .sql files of the models used to create the database

- [facility_field_map.csv](facility_field_map.csv) is a mapping file to select columns/fields within data sources and harmonize their names for the database

- [NAICS code sets](naics_codes) with keyword descriptions, pulled from the [US Census website's](https://www.census.gov/naics/?48967) downloadable files. NAICS codes listed as ranges (e.g. 31-33, 44-45, 48-49) were edited to be separate rows (same keyword and description).
  - "naics_codes/2017 NAICS Descriptions"
  - "naics_codes/2-digit_2012_Codes.xls" = "2-6 digit 2012 Code File"
  - "naics_codes/6-digit_2012_Codes.xls" = "6-digit 2012 Code File"
  - "naics_codes/naics07.xls" = "2-6 digit 2007 Code Files"
  - "naics_codes/naics07_6.xls" = "6-digit 2007 Code Files"
  - "naics_codes/naics_2_6_02.txt" = "2-6 digit 2002 Code File"
  - "naics_codes/naics_6_02.txt" = "6-digit 2002 Code File"
  - "naics_codes/NAICS_1997_2021-04-23.xls" = NAICS codes extracted from the US Census website for 1997, using "scripts/extract_NAICS_1997.R"


# Disclaimer
The United States Environmental Protection Agency (EPA) GitHub project code is provided on an "as is" basis and the user assumes responsibility for its use. EPA has relinquished control of the information and no longer has responsibility to protect the integrity , confidentiality, or availability of the information. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by EPA. The EPA seal and logo shall not be used in any manner to imply endorsement of any commercial product or activity by EPA or the United States Government.
