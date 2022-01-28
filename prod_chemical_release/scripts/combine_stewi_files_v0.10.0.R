#Script to combine StEWI files to push to prod_chemical_release database (v0.10.0)
#Created by: Jonathan Taylor Wall
#Created: 2021-09-10
#Last Updated: 2021-09-10

library(dplyr); library(tidyr); library(jsonlite); library(magrittr); library(DBI); library(purrr)

#'@description A function to create a connection to the prod_factotum database using .Renviron parameters
#'@import DBI
#'@return A mysql connection object
connect_to_db <- function(){
  return(dbConnect(RMySQL::MySQL(), 
                   username = Sys.getenv("user"), password = Sys.getenv("pass"), 
                   host = "mysql-ip-m.epa.gov", port = 3306, dbname = "prod_chemical_release"))
}

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
  return(NA)
}

#'@description A function to load StEWI output JSON metadata files and push to the prod_chemical_release database.
#'Fills the datasource and datadocument tables in the database.
#'@import jsonlite dplyr tidyr
#'@return None.
fill_datasource_document_table <- function(){
  #standardizedinventories-0.9.4\stewi\output\eGRID_2014_metadata.json"
  #Get list of JSON metadata files
  files <- list.files("/home/jwall01/prod_chemical_release/StEWI_0.10/StEWI/", 
                      pattern=".json", 
                      full.names = TRUE)
  metadata <- lapply(files, function(x){
    message("Pulling: ", x)
    jsonlite::fromJSON(x, flatten=TRUE) %>% #Load JSON file
      as.data.frame() %T>% {
        message(names(x))
      } %>% 
      select(starts_with("tool_meta")) %>%
      #Add base filename
      mutate(filename=basename(x)) %T>%{ #Important T-operator
        colnames(.) = sub('.*\\.', '', colnames(.)) #Remove Prefixes
      } 
  }) %>% 
    dplyr::bind_rows() %>%# jsonlite::rbind_pages() %>% #Combine all files into dataframe
    #select(SourceType, SourceFileName, SourceURL, SourceVersion, SourceAcquisitionTime,
    #       StEWI_Version, filename) %>%
    mutate(SourceName = gsub("_metadata.json", "", filename)) %>% #Get sourcename from filename
    separate(SourceName, c("SourceName","SourceYear"), sep="_") #Separate into source and year
  #Select distinct datasources to push to datasource table
  datasource <- metadata %>%
    select(SourceName) %>%
    distinct()
  #Select datadocuments (and metadata) to push to datadocuments table
  datadocument <- metadata %>%
    select(SourceName,
           #SourceFileName,
           SourceType,
           SourceYear,
           SourceURL,
           SourceVersion,
           StEWI_Version,
           SourceAcquisitionTime) %>%
    distinct() %>%
    mutate(SourceFileName = NA) #Filling NA for now (avoid duplicate source/year)
  #Date fix (filter to most recent acquisition time)
  dates <- datadocument$SourceAcquisitionTime %>%
    stringr::str_squish() %>%
    strsplit(., " ") %>% lapply(., function(x){ paste(x[5], x[2], x[3], sep="-") })
  datadocument$dateFix <- dates %>% unlist() %>% lubridate::ymd()
  datadocument <- datadocument %>% #Filter to only the most recently uploaded Clowder documents
    mutate(SourceID = paste0(SourceName, SourceYear, sep="_")) %>%
    group_by(SourceID) %>% 
    slice(which.max(dateFix)) %>%
    ungroup() %>%
    select(-dateFix, -SourceID)
  
  con = connect_to_db()
  #Write temp_table in database
  dbWriteTable(con, name = 'temp_table', value = datasource, row.names = F, overwrite = T)
  #Insert temp_table data into datasource table
  dbSendStatement(con, paste0("INSERT INTO datasource (SourceName)
                              SELECT SourceName
                              FROM temp_table")) %>% dbClearResult()
  #Get datasource ID values
  dbSendQuery(con, paste0("SELECT id, SourceName FROM datasource")) %T>%
  { dbFetch(., -1) ->> datasource_id } %>% #save intermediate variable, critical tee-operator
    dbClearResult() #clear result
  
  datadocument = datadocument %>%
    left_join(datasource_id, by="SourceName") %>% #Add datasource IDs to datadocuments table
    dplyr::rename(datasource_id = id) %>%
    select(-SourceName)
  #Write temp_table to database
  dbWriteTable(con, name = 'temp_table', value = datadocument, row.names = F, overwrite = T)
  #Insert temp_table into datadocument table
  dbSendStatement(con, paste0("INSERT INTO datadocument (datasource_id, SourceFileName, SourceType, SourceYear,
                              SourceURL, SourceVersion, StEWI_Version, SourceAcquisitionTime)
                              SELECT datasource_id, SourceFileName, SourceType, SourceYear, SourceURL, 
                              SourceVersion, StEWI_Version, SourceAcquisitionTime
                              FROM temp_table")) %>% dbClearResult()
  #Disconnect from database
  dbDisconnect(con)
  message("Done...pushed data to datasource and datadocument table")
}

#'@description A function to pull all file paths for datadocuments in each StEWI output subfolder, grouped by datadocument.
#'@import dplyr magrittr jsonlite
#'@return A dataframe of filepaths grouped by StEWI datadocument
get_file_list <- function(){
  #Get complete list of output files grouped by datadocument
  lapply(c("flow", "facility", "flowbyfacility", "validation", "flowbyprocess"), #Subfolder list
         function(x){ 
           list.files(paste0("StEWI_0.10/StEWI/", x),
                      pattern=".parquet|.csv",
                      full.names=TRUE) %>% #Loopthrough each subfolder
             as.data.frame() %T>% { 
               names(.) <- "filename" } %>% #Add dataframe name
             mutate(type = x) #Add type of datadocument
           }) %>% dplyr::bind_rows() %>% #jsonlite::rbind_pages() %>% #Combine dataframes
    mutate(filename=as.character(filename),
           datadocument=gsub(".parquet|.csv", "", basename(filename))) %>% #Get datadocument name
    separate(datadocument, c("Source", "Year", "version", "hash"), sep="_") %>%
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
  facility_map = readr::read_csv("facility_field_map_v0100.csv", col_types=readr::cols())
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
  if("validation" %in% names(fileList)){
    output = output %>%
      left_join(fileList$validation)  
  }
  return(output)
}

#'@description A function to filter facility ID values to only those not already in the database
#'@param x A list of facility ID values
#'@import DBI dplyr
#'@return A unique list of facility ID values not already in the database
filter_to_unique_facility <- function(x=NULL){
  db_facility=query_prod_chemical_release("SELECT DISTINCT FacilityID FROM facility")
  tmp = x$FacilityID[!x$FacilityID %in% db_facility$FacilityID]
  # tmp = anti_join(x %>% mutate(FacilityID = as.character(FacilityID)), #Filter to those not in the database
  #                 db_facility)
  # con = connect_to_db()
  # tmp = anti_join(x %>% mutate(FacilityID = as.character(FacilityID)), #Filter to those not in the database
  #                 tbl(con, "facility") %>% 
  #                   collect())
  # dbDisconnect(con)
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
  con = connect_to_db()
  dbWriteTable(con, name = 'temp_table', value = NAICS_list, row.names = F, overwrite = T)
  dbSendStatement(con, paste0("INSERT INTO naics_info (NAICS_code, keyword, description)
                              SELECT NAICS_code, keyword, description
                              FROM temp_table")) %>% dbClearResult()
  dbSendStatement(con, "DROP TABLE temp_table") %>% dbClearResult()
  dbDisconnect(con)
}

#'@description A function to pull corresponding NAICS_info table ID based on input NAICS_code
#'@param input_NAICS A single NAICS or list of NAICS codes to pull ID values for
#'@return A list of NAICS codes with associated NAICS_info table ID values
get_NAICS_id <- function(input_NAICS=NULL){
  con = connect_to_db()
  input_NAICS = input_NAICS[!is.na(input_NAICS) & 
                              !is.nan(input_NAICS) & 
                              input_NAICS != "NaN" & 
                              input_NAICS != "NA"]
  dbSendQuery(con, paste0("SELECT id AS NAICS_id, NAICS_code FROM NAICS_info WHERE NAICS_code IN (",
                          paste0(input_NAICS, collapse = ", "),")")) %T>%
                          { dbFetch(., -1) ->> tmp } %>% #save intermediate variable, critical tee-operator
    dbClearResult()
  #See what matches
  tmp = left_join(data.frame(NAICS_code = input_NAICS, stringsAsFactors = FALSE),
                  tmp, 
                  by="NAICS_code")
  #Filter to NAICS not found in database and push/pull to get ID
  tmp2 = tmp %>% 
    select(NAICS_code) %>% 
    filter(is.na(tmp$NAICS_id)) %>% 
    unique() %>%
    mutate(keyword = "NEED TO CURATE KEYWORD",
           description = "NEED TO CURATE DESCRIPTION")
  #Push missing NAICS to get IDs
  dbWriteTable(con, name = 'temp_table', value = tmp2, row.names = F, overwrite = T)
  dbSendStatement(con, paste0("INSERT INTO naics_info (NAICS_code, keyword, description)
                              SELECT NAICS_code, keyword, description
                              FROM temp_table")) %>% dbClearResult()
  #Pull all matching NAICS again
  dbSendQuery(con, paste0("SELECT id As NAICS_id, NAICS_code FROM NAICS_info WHERE NAICS_code IN (",
                          paste0(input_NAICS, collapse = ", "),")")) %T>%
                          { dbFetch(., -1) ->> tmp } %>% #save intermediate variable, critical tee-operator
    dbClearResult()
  dbSendStatement(con, "DROP TABLE temp_table") %>% dbClearResult()
  dbDisconnect(con)
  #Match ID's again
  tmp = left_join(data.frame(NAICS_code = input_NAICS, stringsAsFactors = FALSE),
                  tmp, 
                  by="NAICS_code") %>%
    distinct()
  return(tmp)
}

#'@description A helper function to query prod_chemical_samples and receive the results. 
#'Handles errors/warnings with tryCatch.
#'@param query A SQL query string to query the database with
#'@import DBI dplyr magrittr
#'@return Dataframe of database query results
query_prod_chemical_release <- function(query=NULL){
  if(is.null(query)) return(message("Must provide a query to send"))
  con = connect_to_db()
  query_result = tryCatch({
    dbSendQuery(con, query) %T>% #run query
      
    { dbFetch(., -1) ->> tmp } %>% #save intermediate variable, critical tee-operator
      dbClearResult() #clear result
    tmp #return query results
  },
  error=function(cond){ message("Error message: ", cond); return(NA) },
  #warning=function(cond){ message("Warning message: ", cond); return(NULL) },
  finally={ dbDisconnect(con) })
  return(query_result)
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
    con = connect_to_db()
    #Pull datadocuments table
    datadocuments = query_prod_chemical_release(paste0("SELECT dd.id, ds.SourceName, dd.SourceYear, dd.uploadComplete ",
                                                       "FROM datadocument dd LEFT JOIN datasource ds ON dd.datasource_id = ds.id")) %>% 
      unite("SourceName", SourceName, SourceYear, sep="_") %>%
      filter(SourceName == x) #Filter to datadocument
    #Check if file already uploaded
    if(datadocuments$uploadComplete){
      dbDisconnect(con)
      message("File already uploaded...next...")
      return(NULL)
    }
    #Loop through docList docs and push to database
    dat = load_datadocument(files, x) %>% #Load data
      mutate(SourceName = x) %>%
      left_join(datadocuments, #Get source name
                by="SourceName") %>%
      dplyr::rename(datadocument_id = id)
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
      dbWriteTable(con, name = 'temp_table', value = facility, row.names = F, overwrite = T)
      dbSendStatement(con, paste0("INSERT INTO facility (FacilityID)
                                  SELECT FacilityID
                                  FROM temp_table")) %>% dbClearResult()
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
    
    dbWriteTable(con, name = 'temp_table', value = facility_info, row.names = F, overwrite = T)
    dbSendStatement(con, paste0("INSERT INTO facility_info (FacilityName, CompanyName, State, County,
                                Latitude, Longitude, Address, City, Zip,
                                NAICS_id, facility_id, datadocument_id)
                                SELECT FacilityName, CompanyName, State, County,
                                Latitude, Longitude, Address, City, Zip,
                                NAICS_id, facility_id, datadocument_id
                                FROM temp_table")) %>% dbClearResult()
    rm(facility_info)
    flow = dat %>% select(FlowName, FlowID, datadocument_id, CAS)# %>%
    #distinct() #Removed distinct because we want all chemical records for RID assignment
    dbWriteTable(con, name = 'temp_table', value = flow, row.names = F, overwrite = T)
    dbSendStatement(con, paste0("INSERT INTO flow (FlowName, FlowID, datadocument_id, CAS)
                                SELECT FlowName, FlowID, datadocument_id, CAS
                                FROM temp_table")) %>% dbClearResult()
    rm(flow)
    #Get Flow IDs to add to flowbyfacility table
    flowIDs = query_prod_chemical_release(paste0("SELECT id, FlowName, FlowID, CAS FROM flow where datadocument_id = ", 
                                                 dat$datadocument_id %>% unique()))
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
    dbWriteTable(con, name = 'temp_table', value = flowbyfacility, row.names = F, overwrite = T)
    dbSendStatement(con, paste0("INSERT INTO flowbyfacility (FlowAmount, ReliabilityScore, flow_id, Compartment,
                                Unit, facility_id, datadocument_id)
                                SELECT FlowAmount, ReliabilityScore, flow_id, Compartment,
                                Unit, facility_id, datadocument_id
                                FROM temp_table")) %>% dbClearResult()
    rm(flowbyfacility)
    validation = dat %>% 
      cbind(flow_id=flowIDs$flow_id) %>% #Uncertain if best practice to just cbind...but memory issues...
      #left_join(flowIDs, by = c("FlowName", "FlowID", "CAS")) %>%
      select(Inventory_Amount, Reference_Amount, Percent_Difference,
             Conclusion, flow_id) %>%
      distinct()
    dbWriteTable(con, name = 'temp_table', value = validation, row.names = F, overwrite = T)
    dbSendStatement(con, paste0("INSERT INTO validation (Inventory_Amount, Reference_Amount, Percent_Difference,
                                Conclusion, flow_id)
                                SELECT Inventory_Amount, Reference_Amount, Percent_Difference,
                                Conclusion, flow_id
                                FROM temp_table")) %>% dbClearResult()
    rm(validation, flowIDs)
    dbSendStatement(con, paste0("UPDATE datadocument SET uploadComplete = 1 WHERE id = ", 
                                unique(dat$datadocument_id))) %>% dbClearResult()
    dbSendStatement(con, "DROP TABLE temp_table") %>% dbClearResult()
    dbDisconnect(con)
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
  con = connect_to_db()
  tblList = dbListTables(con)
  if(notDataSource){#Only remove flow facility info, not datasource/document
    tblList = tblList[!tblList %in% c("datasource", "datadocument")]
  }
  dbSendStatement(con, "SET FOREIGN_KEY_CHECKS = 0")  %>% dbClearResult()
  lapply(tblList, function(x){
    dbSendStatement(con, paste0("TRUNCATE ", x)) %>% dbClearResult()
    dbSendStatement(con, paste0("ALTER TABLE ",x," AUTO_INCREMENT = 1")) %>% dbClearResult()
  })
  dbSendStatement(con, "SET FOREIGN_KEY_CHECKS = 1") %>% dbClearResult()
  dbDisconnect(con)
  message("Done...all desired tables Truncated")
}

#'@description Function to run all necessary functions in their appropriate order to build the database
#'@import DBI dplyr
#'@return None.
build_prod_chemical_release <- function(){
  reset_prod_chemical_release(notDataSource = FALSE)
  push_NAICS_table()
  fill_datasource_document_table()
  push_to_prod_chemical_release()
}
