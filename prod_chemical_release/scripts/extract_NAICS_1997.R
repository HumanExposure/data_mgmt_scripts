#Script to extract the 1997 NAICS codes from https://www.census.gov/naics/?58967?yearbck=1997
#By: Jonathan Taylor Wall
#Created: 2021-04-22
#Last updated: 2021-04-22

library(dplyr); library(rvest); library(stringr); library(magrittr)

#' @description A function to pull the NAICS code and keyword from the headers found on the
#' input URL's HTML.
#' @param url The URL of interest to pull NAICS codes and keywords from the census.gov website
#' @import dplyr rvest 
#' @return List of NAICS codes and keywords
get_NAICS_code_keyword <- function(url=NULL){
  lapply(c("h2", "h3"), function(x){
    tmp = read_html(url) %>%
      html_nodes(x) %>%
      html_text() %>%
      stringr::str_squish()
    if(x == "h2"){ #Remove Sector from start of strings
      tmp = sub("^Sector ", "", tmp) %>%
        sub("--", " ", .) %>%
        sub(" - NAICS", "",.)
    }
    tmp
    }) %>% 
    unlist() %>% return()
}

#' @description A helpter function to pull the NAICS description found between two extracted NAICS codes
#' found on the census.gov page of interest.
#' @param inputHTML The HTML pulled from the census.gov website.
#' @param start The regex string that marks the start of the NAICS description section
#' @param stop The regex string that marks the end of the NAICS description section
#' @param flip A boolean of whether to remove the start or stop regex string first. Order matters for some NAICS codes
#' due to their start/stop strings occurring in multiple places.
#' @import dplyr stringr
#' @return The NAICS descriptions
get_NAICS_code_description <- function(inputHTML=NULL, start=NULL, stop=NULL, flip=FALSE){
  if(stop == ""){
    inputHTML %>%
      gsub(paste0(".*",start), "", .) %>% #Extract after pattern
      stringr::str_squish() %>% 
      return()
  } else {
    if(flip){
      inputHTML %>%
        gsub(paste0(stop,".*"), "", .) %>% #Extract before pattern
        gsub(paste0(".*",start), "", .) %>% #Extract after pattern
        stringr::str_squish() %>%
        return()
    } else {
      inputHTML %>%
        gsub(paste0(".*",start), "", .) %>% #Extract after pattern
        gsub(paste0(stop,".*"), "", .) %>% #Extract before pattern
        stringr::str_squish() %>%
        return()  
    }
  }
}

#' @description A function to compile a list of NAICS descriptions found on the census.gov page of interest.
#' @param inputHTML The HTML pulled from the census.gov website.
#' @param codes A list of NAICS codes to help navigate the inputHTML to find the NAICS description sections.
#' @import dplyr stringr
#' @return The NAICS descriptions
get_NAICS_code_description_list <- function(inputHTML=NULL, codes=NULL){
  lapply(seq_along(codes), function(x){
    #Escape special characters that mess up regex
    start = ifelse((x == 1), 
                   return("The Sector as a Whole"), 
                   codes[x] %>%
                     gsub("\\(", "\\\\(",.) %>%
                     gsub("\\)", "\\\\)", .) %>%
                     gsub("\r?\n|\r|\t", " ", .) %>%
                     gsub("\\s+"," ",.) %>%
                     #gsub("\'", "\\\\'", .) %>%
                     str_squish()
                   #  gsub("\\,", "\\\\,", .)
                   )
    
    stop = ifelse(!is.na(codes[x+1]), 
                  codes[x+1] %>%
                    str_replace("\\(", "\\\\(") %>%
                    str_replace("\\)", "\\\\)") %>%
                    gsub("\r?\n|\r|\t", " ", .) %>%
                    gsub("\\s+"," ",.) %>%
                    #str_replace_all(., "[\r\n]" , "") %>%
                    #gsub("\'", "\\\\'", .) %>%
                    str_squish(),# %>%
                    #gsub("\\,", "\\\\,", .), 
                  "US—United States industry only")
    desc1 = get_NAICS_code_description(inputHTML=inputHTML, start=start, stop=stop)
    desc1_flip = get_NAICS_code_description(inputHTML=inputHTML, start=start, stop=stop, flip=TRUE)
    #Regex to help in those weird cases with hidden returns/whitespace
    #Ignore whitespace/return/tab, etc. between words
    start = gsub("[[:space:]]", "\\\\s+", start)
    stop = gsub("[[:space:]]", "\\\\s+", stop)
    desc2 = get_NAICS_code_description(inputHTML=inputHTML, start=start, stop=stop)
    desc2_flip = get_NAICS_code_description(inputHTML=inputHTML, start=start, stop=stop, flip=TRUE)
    #Depending on the regex, return the smaller description string
    ifelse(str_length(desc1) < str_length(desc2),
           ifelse(str_length(desc1) < str_length(desc1_flip),
                  return(desc1), return(desc1_flip)),
           ifelse(str_length(desc2) < str_length(desc2_flip),
                             return(desc2), return(desc2_flip)))
  }) %T>% { names(.) <- codes }
}

#' @description A function to convert a list of NAICS codes/keywords and descriptions into a dataframe.
#' @param codes A list of NAICS codes (returned from get_NAICS_code_keyword())
#' @param descriptions A list of NAICS descriptions (returned from get_NAICS_code_description_list())
#' @import dplyr stringr
#' @return The NAICS descriptions
convert_NAICS_to_table <- function(codes=NULL, descriptions=NULL){
  data.frame(codes = codes) %>%
    left_join(descriptions %>%
                bind_rows() %>%
                tidyr::pivot_longer(cols=names(.), names_to="codes", values_to="description"),
              by="codes") %>%
    mutate(codes = stringr::str_replace(codes, "\\s", "|")) %>%
    tidyr::separate(codes, into = c("NAICS_code", "keyword"), sep = "\\|") %>%
    return()
}

#' @description A function to run all the above functions to extract NAICS information from 
#' the census.gov website.
#' @param section The section number to pull NAICS data from (based on the census.gov website URLss)
#' @import dplyr rvest
#' @return The NAICS descriptions
extract_NAICS <- function(section=NULL){
  message("Extracting for section ", section)
  url <- paste0("https://www.census.gov/naics/resources/archives/sect",section,".html")
  #https://www.census.gov/naics/resources/archives/sect31-33.html
  message("...Extracting NAICS Codes...")
  NAICS_codes <- get_NAICS_code_keyword(url=url)
  message("...Pulling HTML for descriptions...")
  node = ifelse(!section %in% c(23, "31-33"),
                "section.col-sm-10.col-sm-offset-1", 
                "div.col-sm-10.col-sm-offset-1")
  htmlExtract = read_html(url) %>%
    html_nodes(node) %>%
    html_text()
  Sys.sleep(0.25)#Rest between request so no more than 4/second
  message("...Extracting ",length(NAICS_codes)," descriptions...")
  NAICS_descriptions <- get_NAICS_code_description_list(inputHTML=htmlExtract, codes=NAICS_codes)
  message("...Converting to table...")
  NAICS_table <- convert_NAICS_to_table(codes=NAICS_codes, descriptions=NAICS_descriptions)
  return(NAICS_table)
}

####################################################################################################
###Run the extraction
sectionList = c(11, 21, 22, 23, "31-33", 42, "44-45", 
                "48-49", 51, 52, 53, 54, 55, 56, 61,
                62, 71, 72, 81, 92)
#problemList = c("31-33", 42, 53, 62, 72, 81, 92)
#problemList = c(339914, 72233, 71132)
#problemList = c(72233)
#problemList = c(32611)
#Problem with weird character return or extra space or something inhibiting regex for 92, code 38 (92313)
message("Starting extraction...", Sys.time())
NAICS_tables <- lapply(sectionList, function(x) { extract_NAICS(section=x) }) %>% bind_rows()
#Character limit check (typically they should be < 10000)
#NAICS_tables = NAICS_tables %>%
#  mutate(nchar = str_length(description))
#NAICS_tables$description[NAICS_tables$nchar > 10000] <- NA
#NAICS_tables = NAICS_tables %>% select(-nchar)
message("Saving output...")
writexl::write_xlsx(x=list(NACIS_1997=NAICS_tables), path=paste0("naics_codes/NAICS_1997_",Sys.Date(), ".xlsx"))
message("Done...", Sys.time())
