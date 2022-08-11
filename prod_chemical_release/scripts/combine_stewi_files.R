# Script to read needed StEWI output files from data product list, download the files
# combine StEWI files to push to prod_chemical_release database
# Created by: Jonathan Taylor Wall, Wesley Ingwersen
# Created: 2022-07-13
# Last Updated: 2022-08-10
# R version 4.2.1 (2022-06-23 ucrt)
# curl_4.3.2 arrow_8.0.0 rappdirs_0.3.3 read.so_0.1.1  devtools_2.4.4 usethis_2.1.6  purrr_0.3.4    DBI_1.1.3      magrittr_2.0.3
# jsonlite_1.8.0 tidyr_1.2.0 dplyr_1.0.9  
# Data product tables: https://github.com/USEPA/standardizedinventories/wiki/DataProductLinks

##INSTRUCTIONS
#The 'prod_chemical_release' MySQL database needs to be setup first by importing the MySQL workbench files in database_model
#or using the sql script to create them
##An .Renviron file needs to be created with values for the following:
#mysql_user
#mysql_pass
#mysql_host (probably will be set to localhost if using local database)
#The given myseql_user must have admin privledges
#Set working directory to prod_chemical_release
# Example is setwd("C:/%YOURPATH%/data_mgmt_scripts/prod_chemical_release")
#Make sure the following libraries are installed 
library(dplyr); library(tidyr); library(jsonlite); library(magrittr); library(DBI); library(purrr);library(devtools);
library(rappdirs); library(arrow); library(curl)
#If not installed, install the read.so package for reading markdown tables
if (!"read.so"%in%installed.packages()[, "Package"]) {
  devtools::install_github("alistaire47/read.so")
}
library(read.so)
#Modify any global parameter values in the next section

######################################################################
#Global Parameters
######################################################################
stewi_version <- "v1.0.5" # version of StEWI
stewi_local_store <-  file.path(rappdirs::user_data_dir(), "stewi") #local directory for stewi output files
data_products_url <- "https://raw.github.com/wiki/USEPA/standardizedinventories/DataProductLinks.md"
db_name <- "prod_chemical_release"
stewi_output_formats <- c("flow", "facility", "flowbyfacility") #flowbyprocess and validation not currently included
#db_schema <- "database_models/prod_chemical_release.sql"
######################################################################
#Functions
######################################################################
#'@description A function to make a connection to the database
#'@param con_type Whether to connect to postgres, mysql, or sqlite version
#'@import DBI RMySQL RSQLite
#'@return Database connection pointer object
connect_to_db <- function(con_type){
  switch(con_type,
         "postgres" = dbConnect(RPostgreSQL::PostgreSQL(), 
                                user = Sys.getenv("postgres_user"), 
                                password = Sys.getenv("postgres_pass"), #
                                host = Sys.getenv("postgres_host"), #
                                dbname = db_name),
         "mysql" = dbConnect(RMySQL::MySQL(), #Connect to database with .Renviron parameters
                             username = Sys.getenv("mysql_user"), 
                             password = Sys.getenv("mysql_pass"),
                             host = Sys.getenv("mysql_host"), 
                             port = 3306,
                             dbname = db_name),
         'sqlite' = dbConnect(RSQLite::SQLite(), "prod_chemical_release.sqlite")
  ) %>% return()
}

#'@description A helper function to query database and receive the results. 
#'Handles errors/warnings with tryCatch.
#'@param query A SQL query string to query the database with
#'@param con_type Whether to connect to postgres, mysql, or sqlite version
#'@param schema The schema name to use if using a postgresql connection
#'@import DBI dplyr
#'@return Dataframe of database query results
query_db <- function(query=NULL, con_type, schema){
  if(is.null(query)) return(message("Must provide a query to send"))
  con = connect_to_db(con_type)
  query_result = tryCatch({
    if(con_type == "postgres"){#Add schema tag
      return(dbGetQuery(con, query %>% gsub("FROM ", paste0("FROM ",schema,"."), .)))
    } else {
      return(dbGetQuery(con, query))
    }
  },
  error=function(cond){ message("Error message: ", cond); return(NULL) },
  finally={ dbDisconnect(con) })
  return(query_result)
}

#'@description A helper function to send a statement to the database to update table entries. 
#'Handles errors/warnings with tryCatch.
#'@param statement A SQL query string to send to the database
#'@param con_type Whether to connect to postgres, mysql, or sqlite version
#'@param schema The schema name to use if using a postgresql connection
#'@import DBI dplyr magrittr
#'@return None. A SQL statement is passed to the database to make changes to the database.
send_statement_db <- function(statement=NULL, con_type=NULL, schema){
  if(is.null(statement)) return(message("Must provide a statement to send"))
  con = connect_to_db(con_type=con_type)
  tryCatch({
    if(con_type == "postgres"){#Add schema tag
      return(dbSendStatement(con, statement %>% 
                               gsub("FROM ", "FROM ",schema,".", .) %>%
                               gsub("INTO ", "INTO ",schema,".", .) %>%
                               gsub("UPDATE ", "UPDATE ",schema,".", .) %>%
                               gsub("EXISTS ", "EXISTS ",schema,".", .)
      ) %>% dbClearResult())
    } else {
      return(dbSendStatement(con, statement) %>% dbClearResult())
    }
  },
  error=function(cond){ message("Error message: ", cond); return(NA) },
  warning=function(cond){ message("Warning message: ", cond); return(NULL) },
  finally={ dbDisconnect(con) })
}

#'@description A helper function to write a table to the datbase. Note, if it already exists, 
#'the table will be overwritten.
#'@param name The name of the table to write to the database
#'@param data The data to push into the new database table
#'@param con_type Whether to connect to postgres, mysql, or sqlite version
#'@param schema The schema name to use if using a postgresql connection
#'@import DBI
#'@return None. A table is written (or overwritten) on the database with a given 'name' and 'data'.
write_table_db <- function(name=NULL, data=NULL, con_type=NULL){
  if(is.null(name)) return(message("Must provide a name for the database table"))
  if(is.null(data)) return(message("Must provide data to push to the database table"))
  con = connect_to_db(con_type)
  tryCatch({
    if(con_type == "postgres"){
      dbWriteTable(con, name =c(schema, name), value = data, row.names = FALSE, overwrite = TRUE)
    } else {
      #Make sure use of local files to write data is allowed
      dbSendQuery(con, "SET GLOBAL local_infile = true;")
      dbWriteTable(con, name = name, value = data, row.names = FALSE, overwrite = TRUE)
    }
  },
  error=function(cond){ message("Error message: ", cond); return(NA) },
  warning=function(cond){ message("Warning message: ", cond); return(NULL) },
  finally={ dbDisconnect(con) })
}

########################################

#'@description A function to derive the data source type of a filename from StEWI output files
#'@param filename The filename (full or relative path) that contains the data source type
#'@return The data source type for the filename passed
get_source_type <- function(filename=""){
  #Could use switch, but need grepl()
  if(grepl("eGRID", filename)) return("eGRID")
  if(grepl("NEI", filename)) return("NEI")
  if(grepl("TRI", filename)) return("TRI")
  if(grepl("RCRAInfo", filename)) return("RCRAInfo")
  if(grepl("DMR", filename)) return("DMR")
  if(grepl("GHGRP", filename)) return("GHGRP")
  return(NA)
}

#'@description A function to load StEWI output JSON metadata files and push to the prod_chemical_release database.
#'Fills the datasource and datadocument tables in the database.
#'@param metadata Input dataframe of metadata Wiki
#'@import jsonlite dplyr tidyr
#'@return None.
fill_datasource_document_table <- function(metadata=NULL){
  #Get list of JSON metadata files
  #Select distinct datasources to push to datasource table
  datasource <- metadata %>%
    select(SourceName=Source) %>%
    distinct()
  #Select datadocuments (and metadata) to push to datadocuments table
  datadocument <- metadata %>%
    select(SourceName=Source,
           SourceYear=Year,
           StEWI_Version=version) %>%
    distinct() %>%
    mutate(SourceFileName = NA) #Filling NA for now (avoid duplicate source/year)
  
  # Check for already loaded datasources
  d_check = query_db(query="SELECT * FROM datasource",
                     con_type="mysql")
  
  #Write temp_table in database - only load new datasources
  write_table_db(name="temp_table",
                 data = datasource %>%
                   filter(!SourceName %in% d_check$SourceName),
                 con_type = "mysql")
  #Insert temp_table data into datasource table
  send_statement_db(statement=paste0("INSERT INTO datasource (SourceName)
                              SELECT SourceName
                              FROM temp_table"),
                    con_type = "mysql")
  
  #Get datasource ID values
  datasource_id = query_db(query="SELECT id, SourceName FROM datasource",
                           con_type="mysql")
  
  datadocument = datadocument %>%
    left_join(datasource_id, by="SourceName") %>% #Add datasource IDs to datadocuments table
    dplyr::rename(datasource_id = id) %>%
    select(-SourceName)
  
  d_check = query_db(query="SELECT b.SourceYear, a.id FROM datasource a
                     LEFT JOIN datadocument b on a.id=b.datasource_id",
                     con_type="mysql") %>%
    mutate(check = paste(id, SourceYear, sep="_"))
  #Write temp_table to database
  write_table_db(name="temp_table",
                 data = datadocument %>%
                   mutate(check = paste(datasource_id, SourceYear, sep="_")) %>%
                   filter(!check %in% d_check$check) %>%
                   select(-check),
                 con_type = "mysql")
  #Insert temp_table into datadocument table
  send_statement_db(statement=paste0("INSERT INTO datadocument (datasource_id, SourceFileName, SourceYear, StEWI_Version)
                              SELECT datasource_id, SourceFileName, SourceYear, StEWI_Version
                              FROM temp_table"),
                    con_type="mysql")
  message("Done...pushed data to datasource and datadocument table")
}

#'@description A function to pull all file paths for datadocuments in each StEWI output subfolder, grouped by datadocument.
#'@import dplyr magrittr jsonlite
#'@return A dataframe of filepaths grouped by StEWI datadocument
get_file_list <- function(){
  #Get complete list of output files grouped by datadocument
  lapply(stewi_output_formats, #Subfolder list
         function(x){ 
           list.files(file.path(stewi_local_store, x),
                      pattern=paste0(stewi_version,".*.parquet"),
                      full.names=TRUE) %>% #Loopthrough each subfolder getting files from specified version
             as.data.frame() %T>% { 
               names(.) <- "filename" } %>% #Add dataframe name
             mutate(type = x) #Add type of datadocument
         }) %>% dplyr::bind_rows() %>% #jsonlite::rbind_pages() %>% #Combine dataframes
    mutate(filename=as.character(filename),
           datadocument=gsub(".parquet|.csv", "", basename(filename))) %>% #Get datadocument name
    separate(datadocument, c("Source", "Year", "version"), sep="_") %>%
    unite("datadocument", c("Source", "Year"), sep="_") %>%
    return()
}

#'@description A function to load datadocument data from all StEWI output subfolders into named list of dataframes
#'@param files The output of get_file_list() function
#'@param x The datadocument SourceName and Year (e.g. TRI_1998, eGRID_2014)
#'@import dplyr magrittr readr
#'@return A named dataframe list of data from each StEWI output file for a datadocument
load_datadocument <- function(files=NULL, x=NULL){
  message("Joining files for: ", x)
  #Get list of files to pull by datadocument name
  tmp = files %>% 
    filter(datadocument == x) %>% #Filter to datadocument
    arrange(type) %T>% {#Order by type
      .$type ->> typeList #Get list of types
    } %>%
    select(filename) %>% unlist() %>% unname() #Get list of file paths
  #Load in datadocument types in named list to join
  fileList = lapply(tmp, function(y){#Load all files into named list by type
    if(grepl(".csv", y)){
      d = readr::read_csv(y, col_types=readr::cols())
      
    } else if(grepl(".parquet", y)){
      d = arrow::read_parquet(y) %>%
        as.data.frame(., stringsAsFactors=FALSE)
    } else {
      message("...unsupported file type: ", y)
      return(NULL)
    }
    d["__index_level_0__"] = NULL
    return(d)
  }) %T>% { names(.) <- typeList }
  
  #Filter facility file to mapped fields
  facility_map = readr::read_csv("facility_field_map.csv", col_types=readr::cols())
  toMap = facility_map %>%
    filter(sourceName == get_source_type(sub("\\_.*", "", x)), !is.na(to))
  if(!nrow(toMap)){
    stop("No facility fields mapped for: ", get_source_type(sub("\\_.*", "", x)))
  }
  fileList$facility = fileList$facility %>%
    select(all_of(toMap$from)) %T>% {
      names(.) <- toMap$to
    }
  
  #Join all the dataframes in the list together
  #Some datasources don't have the validation file, so don't join
  #Don't include "by" argument in joins so duplicate columns aren't created with suffixes
  output = fileList$flowbyfacility %>%
    left_join(fileList$facility#, by="FacilityID"
    ) %>%
    left_join(fileList$flow#,by=c("FlowName", "Compartment", "Unit")
    )
#  if("validation" %in% names(fileList)){
#    output = output %>%
#      left_join(fileList$validation)  
#  }
  return(output)
}

#'@description A function to filter facility ID values to only those not already in the database
#'@param x A list of facility ID values
#'@import DBI dplyr
#'@return A unique list of facility ID values not already in the database
filter_to_unique_facility <- function(x=NULL){
  db_facility=query_db(query="SELECT DISTINCT FacilityID FROM facility", con_type="mysql")
  tmp = x$FacilityID[!x$FacilityID %in% db_facility$FacilityID]
  return(data.frame(FacilityID = tmp))
}

#'@description A function to push NAICS codes from input file to the NAICS_info table
#'@imort DBI dplyr readxl stringr readr tidyr
#'@return None.
push_NAICS_table <- function(){
  #Pull NAICS 2017 Codes
  NAICS_2017 = readxl::read_xlsx("naics_codes/2017_NAICS_Descriptions.xlsx", col_types = "text") %>%
    select(NAICS_code = Code, keyword = Title, description = Description) %>%
    mutate(across(names(.), stringr::str_squish))
  #Pull NAICS 2007 and 2012 Codes (Filter out repeats from 2017)
  NAICS_2007_2012 = lapply(c("naics_codes/2-digit_2012_Codes.xls", 
                             "naics_codes/6-digit_2012_Codes.xls", 
                             "naics_codes/naics07.xls", 
                             "naics_codes/naics07_6.xls"), 
                           function(x){
                             readxl::read_xls(x, col_types = c("text")) %T>% {
                               names(.) <- stringr::str_squish(names(.))
                             } %>%
                               select(NAICS_code = colnames(.)[grepl("Code", colnames(.))], 
                                      keyword = colnames(.)[grepl("Title", colnames(.))])
                           }) %>% bind_rows() %>% 
    distinct() %>%
    filter(!is.na(NAICS_code), 
           !NAICS_code %in% unique(NAICS_2017$NAICS_code)) %>%
    mutate(description = NA) %>%
    mutate(across(names(.), stringr::str_squish))
  #Pull NAICS 2002 Codes (Filter out repeats from 2017, 2012, and 2007)
  NAICS_2002 = lapply(c("naics_codes/naics_2_6_02.txt", 
                        "naics_codes/naics_6_02.txt"),
                      function(x){
                        readr::read_delim(x, delim=",", skip=5, col_names=c("NAICS")) %>%
                          mutate(NAICS = stringr::str_replace(NAICS, "\\s", "|")) %>%
                          tidyr::separate(NAICS, into = c("NAICS_code", "keyword"), sep = "\\|") %>%
                          filter(!NAICS_code %in% c("Code", "NAICS"), 
                                 !grepl("-", NAICS_code))
                      }) %>% bind_rows() %>% 
    distinct() %>%
    filter(!is.na(NAICS_code), 
           !NAICS_code %in% unique(NAICS_2007_2012$NAICS_code),
           !NAICS_code %in% unique(NAICS_2017$NAICS_code)) %>%
    mutate(description = NA) %>%
    mutate(across(names(.), stringr::str_squish))
  #Temp fix to force NAICS_2002 to same 3 cols as other tables
  NAICS_2002 <- NAICS_2002[,c("NAICS_code","keyword","description")]  
  #Pull NAICS 1997 (Extracted usingg scripts/extract_NAICS.R)
  NAICS_1997 = readxl::read_xlsx("naics_codes/NAICS_1997_2021-04-23.xlsx") %>%
    filter(!is.na(NAICS_code), 
           !NAICS_code %in% unique(NAICS_2002$NAICS_code),
           !NAICS_code %in% unique(NAICS_2007_2012$NAICS_code),
           !NAICS_code %in% unique(NAICS_2017$NAICS_code)) %>%
    mutate(across(names(.), stringr::str_squish))
  
  NAICS_list = rbind(NAICS_2017, NAICS_2007_2012, NAICS_2002, NAICS_1997) %>% 
    filter(!grepl("-", NAICS_code)) %>%
    distinct()
  
  write_table_db(name="temp_table", data = NAICS_list, con_type="mysql")
  #dbWriteTable(con, name = 'temp_table', value = NAICS_list, row.names = F, overwrite = T)
  send_statement_db(statement = paste0("INSERT INTO naics_info (NAICS_code, keyword, description)
                              SELECT NAICS_code, keyword, description
                              FROM temp_table"),
                    con_type = "mysql")
  send_statement_db(statement = "DROP TABLE temp_table", con_type = "mysql")
}

#'@description A function to pull corresponding NAICS_info table ID based on input NAICS_code
#'@param input_NAICS A single NAICS or list of NAICS codes to pull ID values for
#'@return A list of NAICS codes with associated NAICS_info table ID values
get_NAICS_id <- function(input_NAICS=NULL){
  input_NAICS = input_NAICS[!is.na(input_NAICS) & 
                              !is.nan(input_NAICS) & 
                              input_NAICS != "NaN" & 
                              input_NAICS != "NA"]
  tmp = query_db(query=paste0("SELECT id AS NAICS_id, NAICS_code FROM NAICS_info WHERE NAICS_code IN (",
                              paste0(input_NAICS, collapse = ", "),")"),
                 con_type = "mysql") %>%
    #See what matches
    left_join(data.frame(NAICS_code = input_NAICS, stringsAsFactors = FALSE),
              by="NAICS_code")
  #Filter to NAICS not found in database and push/pull to get ID
  tmp2 = tmp %>% 
    select(NAICS_code) %>% 
    filter(is.na(tmp$NAICS_id)) %>% 
    unique() %>%
    mutate(keyword = "NEED TO CURATE KEYWORD",
           description = "NEED TO CURATE DESCRIPTION")
  #Push missing NAICS to get IDs
  write_table_db(name="temp_table",
                 data = tmp2,
                 con_type = "mysql")
  send_statement_db(statement = paste0("INSERT INTO naics_info (NAICS_code, keyword, description)
                              SELECT NAICS_code, keyword, description
                              FROM temp_table"),
                    con_type = "mysql")
  send_statement_db(statement="DROP TABLE temp_table", con_type = "mysql")
  #Pull all matching NAICS again and return
  query_db(query=paste0("SELECT id As NAICS_id, NAICS_code FROM NAICS_info WHERE NAICS_code IN (",
                        paste0(input_NAICS, collapse = ", "),")"),
           con_type = "mysql") %>%
    #Match ID's again
    left_join(data.frame(NAICS_code = input_NAICS, stringsAsFactors = FALSE),
              by="NAICS_code") %>%
    distinct() %>%
    return()
}

#'@description A function that uses all helper functions to pull StEWI output data by datasource_year (datadocument),
#'combine across subfolders, and push data to corresponding prod_chemical_release database tables.
#'@import DBI dplyr magrittr
#'@return None.
push_to_prod_chemical_release <- function(){
  files = get_file_list() #Get list of all SteWI output files
  docList <- unique(files$datadocument) #Unique list of datadocuments
  lapply(docList, function(x){ #Loop through all datadocuments
    #Add datadocument IDs
    #Pull datadocuments table
    datadocuments = query_db(query=paste0("SELECT dd.id, ds.SourceName, dd.SourceYear, dd.uploadComplete ",
                                          "FROM datadocument dd LEFT JOIN datasource ds ON dd.datasource_id = ds.id"),
                             con_type="mysql") %>% 
      unite("SourceName", SourceName, SourceYear, sep="_") %>%
      filter(SourceName == x) #Filter to datadocument
    #Check if file already uploaded
    if(nrow(datadocuments)){
      if(datadocuments$uploadComplete){
        message("File already uploaded...next...")
        return(NULL)
      }  
    }
    
    #Loop through docList docs and push to database
    dat = load_datadocument(files, x) %>% #Load data
      mutate(SourceName = x) %>%
      left_join(datadocuments, #Get source name
                by="SourceName") %>%
      dplyr::rename(datadocument_id = id) %>%
      filter(!is.na(datadocument_id))
    
    if(!nrow(dat)){
      message("Error: no datadocuments associated with input datadocument...")
      return(NULL)
    }
    #List of all database fields
    tblNames = c("FacilityName", "CompanyName", "State", "County",
                 "Latitude", "Longitude", "Address", "City", "Zip",
                 "NAICS", "FacilityID", "datadocument_id", "FlowName", 
                 "CAS", "FlowAmount", "ReliabilityScore", "FlowID",
                 "Compartment", "Unit", "Inventory_Amount", "Reference_Amount", 
                 "Percent_Difference", "Conclusion")
    #Fill in missing columns (some datadocuments don't have all columns)
    dat[, tblNames[!tblNames %in% names(dat)]] <- NA
    #Break StEWI data into database tables
    facility = dat %>% 
      select(FacilityID) %>% 
      unique() %>%
      filter_to_unique_facility() #Filter to unique FacilityID not in database
    if(nrow(facility)){#Only send if any new facilityID values present
      write_table_db(name="temp_table",
                     data = facility,
                     con_type="mysql")
      send_statement_db(statement = paste0("INSERT INTO facility (FacilityID)
                                  SELECT FacilityID
                                  FROM temp_table"),
                        con_type="mysql")
    }
    rm(facility)
    facility_info = dat %>% select(FacilityName, CompanyName, State, County,
                                   Latitude, Longitude, Address, City, Zip,
                                   NAICS, facility_id=FacilityID, datadocument_id) %>%
      distinct() %>% #Add 0's to end of NAICS that aren't 6 digits long
      mutate(NAICS=as.character(NAICS))
    #mutate(NAICS = stringr::str_pad(NAICS, width=6, side="right", pad="0"))
    #Get NAICS_id map
    if(!all(is.na(facility_info$NAICS))) {
      tmp = get_NAICS_id(facility_info$NAICS)
      #Match NAICS_id and remove NAICS field
      facility_info = facility_info %>%
        left_join(tmp, by=c("NAICS"="NAICS_code")) %>%
        select(-NAICS)  
    } else {
      facility_info = facility_info %>% dplyr::rename(NAICS_id=NAICS)
    }
    
    write_table_db(name="temp_table",
                   data = facility_info,
                   con_type = "mysql")
    send_statement_db(statement = paste0("INSERT INTO facility_info (FacilityName, CompanyName, State, County,
                                Latitude, Longitude, Address, City, Zip,
                                NAICS_id, facility_id, datadocument_id)
                                SELECT FacilityName, CompanyName, State, County,
                                Latitude, Longitude, Address, City, Zip,
                                NAICS_id, facility_id, datadocument_id
                                FROM temp_table"),
                      con_type = "mysql")
    rm(facility_info)
    flow = dat %>% select(FlowName, FlowID, datadocument_id, CAS)# %>%
    #distinct() #Removed distinct because we want all chemical records for RID assignment
    write_table_db(name="temp_table",
                   data = flow,
                   con_type = "mysql")
    send_statement_db(statement = paste0("INSERT INTO flow (FlowName, FlowID, datadocument_id, CAS)
                                SELECT FlowName, FlowID, datadocument_id, CAS
                                FROM temp_table"),
                      con_type = "mysql")
    rm(flow)
    #Get Flow IDs to add to flowbyfacility table
    flowIDs = query_db(query=paste0("SELECT id, FlowName, FlowID, CAS FROM flow where datadocument_id = ", 
                                    dat$datadocument_id %>% unique()),
                       con_type = "mysql")
    # dbSendQuery(con, paste0("SELECT id, FlowName, FlowID, CAS FROM flow where datadocument_id = ", dat$datadocument_id %>% unique())) %T>%
    # { dbFetch(., -1) ->> flowIDs } %>% #save intermediate variable, critical tee-operator
    #   dbClearResult() #clear result
    flowIDs = dplyr::rename(flowIDs, flow_id = id)
    flowbyfacility = dat %>% select(FlowAmount, ReliabilityScore, Compartment,
                                    Unit, facility_id=FacilityID, datadocument_id, 
                                    FlowName, FlowID, CAS) %>%
      cbind(flow_id=flowIDs$flow_id) %>% #Uncertain if best practice to just cbind...but memory issues...
      #left_join(flowIDs, by = c("FlowName", "FlowID", "CAS")) %>%
      #left_join(flowIDs, by = c("FlowID", "FlowName", "CAS")) %>%
      select(-FlowName, -FlowID, -CAS) %>%
      distinct() #Should we also remove distinct here, like with flow?
    unmatched_flow = flowbyfacility %>% filter(is.na(flow_id))
    if(nrow(unmatched_flow)){
      stop("Unmatched flow_id for ", x, ": ", nrow(unmatched_flow), " rows")
    }
    
    write_table_db(name="temp_table",
                   data = flowbyfacility,
                   con_type = "mysql")
    send_statement_db(statement =  paste0("INSERT INTO flowbyfacility (FlowAmount, ReliabilityScore, flow_id, Compartment,
                                Unit, facility_id, datadocument_id)
                                SELECT FlowAmount, ReliabilityScore, flow_id, Compartment,
                                Unit, facility_id, datadocument_id
                                FROM temp_table"),
                      con_type = "mysql")
    rm(flowbyfacility)
    # validation = dat %>% 
    #   cbind(flow_id=flowIDs$flow_id) %>% #Uncertain if best practice to just cbind...but memory issues...
    #   #left_join(flowIDs, by = c("FlowName", "FlowID", "CAS")) %>%
    #   select(Inventory_Amount, Reference_Amount, Percent_Difference,
    #          Conclusion, flow_id) %>%
    #   distinct()
    # 
    # write_table_db(name="temp_table",
    #                data = validation,
    #                con_type = "mysql")
    # send_statement_db(statement =  paste0("INSERT INTO validation (Inventory_Amount, Reference_Amount, Percent_Difference,
    #                             Conclusion, flow_id)
    #                             SELECT Inventory_Amount, Reference_Amount, Percent_Difference,
    #                             Conclusion, flow_id
    #                             FROM temp_table"),
    #                   con_type = "mysql")
    # rm(validation, flowIDs)
    send_statement_db(statement=paste0("UPDATE datadocument SET uploadComplete = 1 WHERE id = ", 
                                       unique(dat$datadocument_id)),
                      con_type="mysql")
    send_statement_db(statement="DROP TABLE temp_table",
                      con_type="mysql")
    message("Done...datadocument added to all database tables")
    })
  message("Done...", Sys.time())
  }

#'@description A function to reset the prod_chemical_release database by TRUNCATING all tables
#'@param notDataSource A logical or whether to Truncate the datasource and datadocument table or not
#'@import DBI
#'@return None.
reset_prod_chemical_release <- function(notDataSource=TRUE){
  message("Resetting prod_chemical_release...")
  # Get list of tables in prod_chemical_release
  tblList = query_db(query = paste0("SHOW TABLES FROM ",Sys.getenv("mysql_dbname")),
                     con_type = "mysql") %>% unlist() %>% unname()
  if(notDataSource){#Only remove flow facility info, not datasource/document
    tblList = tblList[!tblList %in% c("datasource", "datadocument")]
    # Reset document uploadComplete to 0 so they'll be reprocessed after reset
    send_statement_db(statement="UPDATE datadocument set uploadComplete = 0",
                      con_type = "mysql")
  }
  
  # Turn off foreign key checks before truncation
  # Truncate and reset autoincrement to 1
  # Must use same connection or foreign key checks will be reset to 1
  con = connect_to_db(con_type="mysql")
  dbSendStatement(con, "SET FOREIGN_KEY_CHECKS=0") %>% dbClearResult()
  lapply(tblList, function(x){
    dbSendStatement(con, paste0("TRUNCATE ", x)) %>% dbClearResult()
    dbSendStatement(con, paste0("ALTER TABLE ",x," AUTO_INCREMENT = 1")) %>% dbClearResult()
  })
  dbDisconnect(con)
  message("Done...all desired tables Truncated")
}

#'@title Extract Wiki Docs
#'@param overwrite Boolean to re-download files or not
#'@description Extract stewi document information from wiki and download files
extract_wiki_docs <- function(version = "StEWI_1.0.5"){
  wiki = read.so::read.md(file(data_products_url),skip=3) %>%
    #https://statisticsglobe.com/extract-characters-between-parantheses-r
    mutate(across(!c("Year", "Source"), ~gsub("\\(([^()]+)\\)", # Extract characters within parentheses
                                          "\\1",
                                          stringr::str_extract(.,
                                                               "\\(([^()]+)\\)")))) %>%
    # Drop flow-by-process column
    select(-"Flow.By.Process") %>%
    # Pivot to list of URLs
    tidyr::pivot_longer(!c("Year", "Source"), names_to="parent", values_to = "url") %>%
    filter(!is.na(url)) %>%
    # https://stevencarlislewalker.wordpress.com/2013/02/13/remove-or-replace-everything-before-or-after-a-specified-character-in-r-strings/
    # Get folder and file names to organize download
    mutate(path = sub('.*\\.com/', '', url),
           file = basename(path),
           folders = dirname(path),
           version = strsplit(file, "_")[[1]][3] %>%
             gsub(".parquet", "", .))


    # Define paths to all files, check if they exist, download if not
    
    lapply(seq_len(nrow(wiki)), function(r){
      f_name = file.path(rappdirs::user_data_dir(), wiki$folders[r], wiki$file[r])
      if(!file.exists(f_name)){
        Sys.sleep(0.25)
        try(curl::curl_download(wiki$url[r],
                          destfile=f_name,quiet=FALSE, mode="wb"))
      }
    }) %>% invisible() 
  return(wiki)
}

#'@description Function to create tables in db if they don't exist
#'@return None.
# setup_db <- function() {
#   #load schema
#   schema <- readLines(db_schema)
#   result <- query_db(query=schema, con_type="mysql")
#   return(result)
# }

#'@description Function to run all necessary functions in their appropriate order to build the database
#'@param reset Boolean of whether to reset the database (truncate all and repopulate)
#'@import DBI dplyr
#'@return None.
build_prod_chemical_release <- function(reset = FALSE, notDataSource = TRUE){
  wiki <- extract_wiki_docs(stewi_version)
  
  # Before downloading data, check for and create stewi local storage
  if(!file.exists(stewi_local_store)){
    dir.create(stewi_local_store, recursive = TRUE)
  }
  
  #Set up table schema automaically - NOT WORKING
  #setup_db()
  
  if(reset){
    reset_prod_chemical_release(notDataSource = notDataSource)
    push_NAICS_table()
    fill_datasource_document_table(metadata=wiki)
  }
  push_to_prod_chemical_release()
}

build_prod_chemical_release(reset=TRUE, notDataSource = FALSE)
