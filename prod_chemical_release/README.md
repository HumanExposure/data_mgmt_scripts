# prod_chemical_release

The following are files and scripts associated with an effort to push Standardized Emission and Waste Inventories (StEWI) output data into a database.

## Associated Files
- A copy of the latest StEWI output can be found on [GitHub](https://github.com/USEPA/standardizedinventories).
- database_models subfolder with MySQL .mwb files of the models used to create the database
- "facility_field_map.csv" is a mapping file to select columns/fields within data sources and harmonize their names for the database
- List of NAICS codes with keyword descriptions, pulled from the [US Census website's](https://www.census.gov/naics/?48967) downloadable files. NAICS codes listed as ranges (e.g. 31-33, 44-45, 48-49) were edited to be separate rows (same keyword and description).
  - "naics_codes/2017 NAICS Descriptions"
  - "naics_codes/2-digit_2012_Codes.xls" = "2-6 digit 2012 Code File"
  - "naics_codes/6-digit_2012_Codes.xls" = "6-digit 2012 Code File"
  - "naics_codes/naics07.xls" = "2-6 digit 2007 Code Files"
  - "naics_codes/naics07_6.xls" = "6-digit 2007 Code Files"
  - "naics_codes/naics_2_6_02.txt" = "2-6 digit 2002 Code File"
  - "naics_codes/naics_6_02.txt" = "6-digit 2002 Code File"
  - "naics_codes/NAICS_1997_2021-04-23.xls" = NAICS codes extracted from the US Census website for 1997, using "scripts/extract_NAICS_1997.R"

