#Script to combine StEWI files to push to prod_chemical_release database
#Created by: Jonathan Taylor Wall
#Created: 2020-12-31
#Last Updated: 2021-4-12

library(dplyr); library(tidyr); library(jsonlite); library(magrittr); library(DBI); library(purrr)

#'@description A function to create a connection to the prod_factotum database using .Renviron parameters
#'@import DBI
#'@return A mysql connection object
connect_to_db <- function(){
  return(dbConnect(RMySQL::MySQL(), 
                   username = Sys.getenv("user"), password = Sys.getenv("pass"), 
                   host = Sys.getenv("host"), port = 3306, dbname = Sys.getenv("dbname")))
}

#'@description A function to derive the data source type of a filename from STeWI output files
#'@param filename The filename (full or relative path) that contains the data source type
#'@return The data source type for the filename passed
get_source_type <- function(filename=""){
  if(grepl("eGRID", filename)) return("eGRID")
  if(grepl("NEI", filename)) return("NEI")
  if(grepl("TRI", filename)) return("TRI")
  if(grepl("RCRAInfo", filename)) return("RCRAInfo")
}

#'@description A function to load STeWI output JSON metadata files and push to the prod_chemical_release database.
#'Fills the datasource and datadocument tables in the database.
#'@import jsonlite dplyr tidyr
#'@return None.
fill_datasource_document_table <- function(){
  #standardizedinventories-0.9.4\stewi\output\eGRID_2014_metadata.json"
  #Get list of JSON metadata files
  files <- list.files("standardizedinventories-0.9.4/stewi/output", 
                      pattern=".json", 
                      full.names = TRUE)
  metadata <- lapply(files, function(x){
    message("Pulling: ", x)
    jsonlite::fromJSON(x) %>% #Load JSON file
      as.data.frame() %>% 
      mutate(filename=basename(x)) #Add base filename
  }) %>% 
    dplyr::bind_rows() %>%# jsonlite::rbind_pages() %>% #Combine all files into dataframe
    mutate(SourceName = gsub("_metadata.json", "", filename)) %>% #Get sourcename from filename
    separate(SourceName, c("SourceName","SourceYear"), sep="_") #Separate into source and year
  #Select distinct datasources to push to datasource table
  datasource <- metadata %>%
    select(SourceName) %>%
    distinct()
  #Select datadocuments (and metadata) to push to datadocuments table
  datadocument <- metadata %>%
    select(SourceName,
           SourceFileName,
           SourceType,
           SourceYear,
           SourceURL,
           SourceVersion,
           StEWI_versions_version,
           SourceAquisitionTime)
  
  con = connect_to_db()
  #Write temp_table in database
  dbWriteTable(con, name = 'temp_table', value = datasource, row.names = F, overwrite = T)
  #Insert temp_table data into datasource table
  dbSendStatement(con, paste0("INSERT INTO datasource (SourceName)
                                           SELECT SourceName
                                           FROM temp_table")) 
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
                              SourceURL, SourceVersion, StEWI_versions_version, SourceAquisitionTime)
                                           SELECT datasource_id, SourceFileName, SourceType, SourceYear, SourceURL, 
                                            SourceVersion, StEWI_versions_version, SourceAquisitionTime
                                           FROM temp_table")) 
  #Disconnect from database
  dbDisconnect(con)
  message("Done...pushed data to datasource and datadocument table")
}

#'@description A function to pull all file paths for datadocuments in each STeWI output subfolder, grouped by datadocument.
#'@import dplyr magrittr jsonlite
#'@return A dataframe of filepaths grouped by STeWI datadocument
get_file_list <- function(){
  #Get complete list of output files grouped by datadocument
  return(lapply(c("flow", "facility", "flowbyfacility", "validation"), #Subfolder list
                function(x){ list.files(paste0("standardizedinventories-0.9.4/stewi/output/", x),
                                        pattern=".csv",
                                        full.names=TRUE) %>% #Loopthrough each subfolder
                    as.data.frame() %T>% { 
                      names(.) <- "filename" } %>% #Add dataframe name
                    mutate(type = x) #Add type of datadocument
                }) %>% dplyr::bind_rows() %>%#jsonlite::rbind_pages() %>% #Combine dataframes
           mutate(filename=as.character(filename),
                  datadocument=gsub(".csv", "", basename(filename))) #Get datadocument name
  )
}

#'@description A function to load datadocument data from all STeWI output subfolders into named list of dataframes
#'@param files The output of get_file_list() function
#'@param x The datadocument SourceName and Year (e.g. TRI_1998, eGRID_2014)
#'@import dplyr magrittr readr
#'@return A named dataframe list of data from each STeWI output file for a datadocument
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
    readr::read_csv(y, col_types=readr::cols())
  }) %T>% { names(.) <- typeList }
  
  #Filter facility file to mapped fields
  facility_map = readr::read_csv("facility_field_map.csv", col_types=readr::cols())
  toMap = facility_map %>%
    filter(sourceName == get_source_type(sub("\\_.*", "", x)), !is.na(to))
  fileList$facility = fileList$facility %>%
    select(all_of(toMap$from)) %T>% {
      names(.) <- toMap$to
    }
  
  #Join all the dataframes in the list together
  #Some datasources don't have the validation file, so don't join
  #Don't include "by" argument in joins so duplicate columns aren't created with suffixes
  if(!"validation" %in% names(fileList)){
    output = fileList$flowbyfacility %>%
      left_join(fileList$facility) %>%
      left_join(fileList$flow) 
  } else {
    output = fileList$flowbyfacility %>%
      left_join(fileList$facility) %>%
      left_join(fileList$flow) %>%
      left_join(fileList$validation)  
  }
  return(output)
}

#'@description A function to filter facility ID values to only those not already in the database
#'@param x A list of facility ID values
#'@import DBI dplyr
#'@return A unique list of facility ID values not already in the database
filter_to_unique_facility <- function(x=NULL){
  con = connect_to_db()
  tmp = anti_join(x %>% mutate(FacilityID = as.character(FacilityID)), #Filter to those not in the database
                  tbl(con, "facility") %>% 
                    collect())
  dbDisconnect(con)
  return(tmp)
}

#'@description A function that uses all helper functions to pull STeWI output data by datasource_year (datadocument),
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
    dbSendQuery(con, paste0("SELECT dd.id, ds.SourceName, dd.SourceYear, dd.uploadComplete ",
                            "FROM datadocument dd LEFT JOIN datasource ds ON dd.datasource_id = ds.id")) %T>%
    { dbFetch(., -1) ->> datadocuments } %>% #save intermediate variable, critical tee-operator
      dbClearResult() #clear result
    datadocuments = datadocuments %>% 
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
    #Break STeWI data into database tables
    facility = dat %>% 
      select(FacilityID) %>% 
      unique() %>%
      filter_to_unique_facility() #Filter to unique FacilityID not in database
    dbWriteTable(con, name = 'temp_table', value = facility, row.names = F, overwrite = T)
    dbSendStatement(con, paste0("INSERT INTO facility (FacilityID)
                                SELECT FacilityID
                                FROM temp_table"))
    rm(facility)
    facility_info = dat %>% select(FacilityName, CompanyName, State, County,
                                   Latitude, Longitude, Address, City, Zip,
                                   NAICS, facility_id=FacilityID, datadocument_id) %>%
      distinct()
    dbWriteTable(con, name = 'temp_table', value = facility_info, row.names = F, overwrite = T)
    dbSendStatement(con, paste0("INSERT INTO facility_info (FacilityName, CompanyName, State, County,
                                Latitude, Longitude, Address, City, Zip,
                                NAICS, facility_id, datadocument_id)
                                SELECT FacilityName, CompanyName, State, County,
                                Latitude, Longitude, Address, City, Zip,
                                NAICS, facility_id, datadocument_id
                                FROM temp_table"))
    rm(facility_info)
    flow = dat %>% select(FlowName, FlowID, datadocument_id, CAS) %>%
      distinct()
    dbWriteTable(con, name = 'temp_table', value = flow, row.names = F, overwrite = T)
    dbSendStatement(con, paste0("INSERT INTO flow (FlowName, FlowID, datadocument_id, CAS)
                                SELECT FlowName, FlowID, datadocument_id, CAS
                                FROM temp_table"))
    rm(flow)
    #Get Flow IDs to add to flowbyfacility table
    dbSendQuery(con, paste0("SELECT * FROM flow")) %T>%
    { dbFetch(., -1) ->> flowIDs } %>% #save intermediate variable, critical tee-operator
      dbClearResult() #clear result
    flowIDs = dplyr::rename(flowIDs, flow_id = id)
    flowbyfacility = dat %>% select(FlowAmount, ReliabilityScore, Compartment,
                                    Unit, facility_id=FacilityID, datadocument_id, 
                                    FlowName, FlowID, CAS) %>%
      left_join(flowIDs) %>%
      select(-FlowName, -FlowID, -CAS) %>%
      distinct()
    dbWriteTable(con, name = 'temp_table', value = flowbyfacility, row.names = F, overwrite = T)
    dbSendStatement(con, paste0("INSERT INTO flowbyfacility (FlowAmount, ReliabilityScore, flow_id, Compartment,
                               Unit, facility_id, datadocument_id)
                               SELECT FlowAmount, ReliabilityScore, flow_id, Compartment,
                               Unit, facility_id, datadocument_id
                               FROM temp_table"))
    rm(flowbyfacility)
    validation = dat %>% 
      left_join(flowIDs) %>% #Add flowIDs to validation table
      select(Inventory_Amount, Reference_Amount, Percent_Difference,
             Conclusion, flow_id) %>%
      distinct()
    dbWriteTable(con, name = 'temp_table', value = validation, row.names = F, overwrite = T)
    dbSendStatement(con, paste0("INSERT INTO validation (Inventory_Amount, Reference_Amount, Percent_Difference,
                               Conclusion, flow_id)
                               SELECT Inventory_Amount, Reference_Amount, Percent_Difference,
                               Conclusion, flow_id
                               FROM temp_table"))
    rm(validation, flowIDs)
    dbSendStatement(con, paste0("UPDATE datadocument SET uploadComplete = 1 WHERE id = ", 
                                unique(dat$datadocument_id)))
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
  dbSendStatement(con, "SET FOREIGN_KEY_CHECKS = 0")
  lapply(tblList, function(x){
    dbSendStatement(con, paste0("TRUNCATE ", x))
  })
  dbSendStatement(con, "SET FOREIGN_KEY_CHECKS = 0")
  dbDisconnect(con)
  message("Done...all desired tables Truncated")
}