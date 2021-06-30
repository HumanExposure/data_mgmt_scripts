
#Re-extract chemical data from the product pages for adhesives and polymer additives (KKI, 6/2021)
#this recreates the %read_all_data SAS macro from the process_product_pages script (KKI, 2015)

#Also extracts function and chemical data from the new coatings data downloaded by KKI 6/2021

library(stringr)
library(dplyr)

getproductdata<-function(indir){

setwd(indir)
files<-list.files(indir,include.dirs=F, recursive = F)


finaldata<-list()
for (j in 1:length(files)) {

  cat("\n","Processing file ",j," of ",length(files))
   #read file 
   thisfile<-data.frame(readLines(files[j]))
   productfile<-files[j]

   #parse file (this reproduces SAS code)
   colnames(thisfile)[1]<-"thisline"
   thisfile$thisline<-as.character(thisfile$thisline)

    if (any(grepl("/product/",thisfile$thisline))==F){
    cat("\n","No products in file ",productfile)
      next
    } 
 CASYES<-0
 compYES<-0
 compline<-0
 casline<-0
   
 product_name<-""
 CAS<-""
 chem_name<-""
 for (i in 1:length(thisfile$thisline)){
      
    thisln<-thisfile$thisline[i]
   
    #products  
    if(grepl("CAS Number", thisln))   CASYES<-1
    if(grepl("Chemical Composition", thisln))   compYES<-1  
 
    #product name
    if(grepl("keywords", thisln)) {
      cat("\n","Found prod name")
      k2<-str_locate(thisln,",")[1]-1
      a<-thisln
      product_name<-substr(a,36,k2)
      #cat("\n",product_name)
      product_name<-gsub("Â","",product_name);
      product_name<-gsub("®","",product_name);
    }

    if (compYES==1) compline<-compline+1;
    if (CASYES==1)  casline<-casline+1;
    if (casline==4)  CAS<-str_trim(thisln);	
    if (compline==4) chem_name<-str_trim(thisln);
 }
 thisdata<- c(product_name,CAS,chem_name,productfile)
 finaldata[[j]]<-thisdata
}
k<-as.data.frame(do.call(rbind, finaldata))
colnames(k)<-c("product_name", "CAS", "reported_chemical_name","product_page_file")

return(k)
}
    
getcoatingdata<-function(indir){
  
  setwd(indir)
  files<-list.files(indir,include.dirs=F, recursive = F)
 
  finaldata<-list()
  for (j in 1:length(files)) {
    
    cat("\n","Processing file ",j," of ",length(files))
    #read file 
    thisfile<-data.frame(readLines(files[j]))
    productfile<-files[j]
    
    #parse file (this reproduces SAS code)
    colnames(thisfile)[1]<-"thisline"
    thisfile$thisline<-as.character(thisfile$thisline)
    
    if (any(grepl("/product/",thisfile$thisline))==F){
      cat("\n","No products in file ",productfile)
      next
    } 
    catYES<-0
    CASYES<-0
    compYES<-0
    compline<-0
    casline<-0
    catline<-0    
        
    product_name<-""
    CAS<-""
    chem_name<-""
    for (i in 1:length(thisfile$thisline)){
      
      thisln<-thisfile$thisline[i]
      
      #products  
      if(grepl("CAS Number", thisln))   CASYES<-1
      if(grepl("Chemical Composition", thisln))   compYES<-1  
      if(grepl("Product Type", thisln))  catYES<-1  
      
      #product name
      if(grepl("properties",thisln) & grepl("name",thisln) & grepl("url",thisln)) {
        cat("\n","Found prod name")
        k1<-str_locate_all(thisln,"name")[[1]][1]+8
        k2<-str_locate_all(thisln,",")[[1]][2]-3
        k3<-str_locate_all(thisln,"url")[[1]][1]+7
        k4<-str_locate_all(thisln,",")[[1]][3]-3
        a<-thisln
        product_name<-substr(a,k1,k2)
        url<-substr(a,k3,k4)
        cat("\n",product_name,url,k1,k2,k3,k4)
        product_name<-gsub("Â","",product_name);
        product_name<-gsub("®","",product_name);
      }

      if (catYES==1) {
        if (!grepl("<",thisln)){
          category<-str_trim(thisln)
          catYES<-0
        }
      }
      if (compYES==1) compline<-compline+1;
      if (CASYES==1)  casline<-casline+1;
      if (casline==3)  CAS<-str_trim(thisln);	
      if (compline==3) chem_name<-str_trim(thisln)

    }
    thisdata<- c(product_name,CAS,category,chem_name,url,productfile)
    finaldata[[j]]<-thisdata
  }
  k<-as.data.frame(do.call(rbind, finaldata))
  colnames(k)<-c("product_name","CAS","category","reported_chemical_name","url","product_page_file")
  
  return(k)
}


setwd("L:/Lab/NERL_Isaacs/kki-21-SPECIALCHEM_FOR_FACTOTUM/kk-15-SPECIALCHEMDATA/")

directory<-"L:/Lab/NERL_Isaacs/kki-21-SPECIALCHEM_FOR_FACTOTUM/kk-15-SPECIALCHEMDATA/adhesives/" 
adhesivedata<-getproductdata(directory)
save(adhesivedata,file="adhesivedata.RData")

directory<-"L:/Lab/NERL_Isaacs/kki-21-SPECIALCHEM_FOR_FACTOTUM/kk-15-SPECIALCHEMDATA/Coatings/" 
polymerdata<-getproductdata(directory)
save(polymerdata,file="polymerdata.RData")

#coatings
directory<-"L:/Lab/NERL_Isaacs/kki-21-SPECIALCHEM_FOR_FACTOTUM/kk-15-SPECIALCHEMDATA/Coatings/" 
coatingdata<-getcoatingdata(directory)
save(coatingdata,file="allcoatingdata.RData")


#clean up coating data and remove duplications
coatingdata$reported_chemical_name<-gsub("â"¢","",coatingdata$reported_chemical_name)
coatingdata$reported_chemical_name<-gsub("<sub>","",coatingdata$reported_chemical_name)
coatingdata$reported_chemical_name<-gsub("&reg;","",coatingdata$reported_chemical_name)
coatingdata$reported_chemical_name<-gsub("</sub>","",coatingdata$reported_chemical_name)
coatingdata$product_name<-gsub("&reg;","",coatingdata$product_name)
coatingdata$reported_chemical_name<-gsub("â???T", "'",coatingdata$reported_chemical_name)
coatingdata$reported_chemical_name<-gsub("â???"", "-",coatingdata$reported_chemical_name)
coatingdata$raw_function_category<-coatingdata$category
coatingdata<-coatingdata[,!(colnames(coatingdata) =="category")]
coatingdata2<-coatingdata[which(!duplicated(coatingdata[,c("CAS","reported_chemical_name","raw_function_category")])),]


#Load function data previously extracted for polymers and adhesives
load("L:/Lab/NERL_Isaacs/kki-21-SPECIALCHEM_FOR_FACTOTUM/kk-15-SPECIALCHEMDATA/allcategorydata_06032021.Rdata")

#merge categories other than coatings with their supplier file data (including categories) and save
categories$product_page_file<-categories$product_name
categories<-categories[,!colnames(categories)=="product_name"]

polymerdatafinal<-left_join(polymerdata,categories)
polymerdatafinal<-polymerdatafinal[which(!is.na(polymerdatafinal$supplierfile)),]#there were just a few supplier files mising

#Clean up strange characters in names, get rid of any documents without CAS or chemical names, and since these are uploaded as functional use
#documents, we can drop duplicate combinations of name CAS (i.e. multiple documents from same supplier) with the same functional use
polymerdatafinal$product_name<-gsub("â"¢","",polymerdatafinal$product_name)
polymerdatafinal$product_name<-gsub("<sub>","",polymerdatafinal$product_name)
polymerdatafinal$product_name<-gsub("&reg;","",polymerdatafinal$product_name)

polymerdatafinal2<-polymerdatafinal[which(polymerdatafinal$CAS!="" | polymerdatafinal$reported_chemical_name!=""),]

polymerdatafinal3<-polymerdatafinal2[which(!duplicated(polymerdatafinal2[,c("CAS","reported_chemical_name","raw_function_category")])),]
polymerdatafinal3$reported_chemical_name<-gsub("â???T", "'",polymerdatafinal3$reported_chemical_name)
polymerdatafinal3$reported_chemical_name<-gsub("â???"", "-",polymerdatafinal3$reported_chemical_name)
polymerdatafinal3$supplier<-gsub("&amp;", "&",polymerdatafinal3$supplier)
polymerdatafinal3$fromwhere<-"polymer"

adhesivedatafinal<-left_join(adhesivedata,categories)

adhesivedatafinal$product_name<-gsub("â"¢","",adhesivedatafinal$product_name)
adhesivedatafinal$product_name<-gsub("<sub>","",adhesivedatafinal$product_name)
adhesivedatafinal$product_name<-gsub("&reg;","",adhesivedatafinal$product_name)
adhesivedatafinal<-adhesivedatafinal[which(!is.na(adhesivedatafinal$supplierfile)),]#there were a few supplier files mising

adhesivedatafinal2<-adhesivedatafinal[which(adhesivedatafinal$CAS!="" | adhesivedatafinal$reported_chemical_name!=""),]

adhesivedatafinal3<-adhesivedatafinal2[which(!duplicated(adhesivedatafinal2[,c("CAS","reported_chemical_name","raw_function_category")])),]
adhesivedatafinal3$reported_chemical_name<-gsub("â???T", "'",adhesivedatafinal3$reported_chemical_name)
adhesivedatafinal3$reported_chemical_name<-gsub("â???"", "-",adhesivedatafinal3$reported_chemical_name)
adhesivedatafinal3$supplier<-gsub("&amp;", "&",adhesivedatafinal3$supplier)

adhesivedatafinal3$fromwhere<-"adhesive"

#now combine adhesives and polymers and remove duplicate chemical -function pairs that may have been in both sets because some products were
aandpfinaldata<-rbind(adhesivedatafinal3,polymerdatafinal3)
aandpfinaldata2<-aandpfinaldata[which(!duplicated(aandpfinaldata[,c("CAS","reported_chemical_name","raw_function_category")])),]


setwd("L:/Lab/NERL_Isaacs/kki-21-SPECIALCHEM_FOR_FACTOTUM/FINAL_FOR_FACTOTUM/")
write.csv(aandpfinaldata2,"polymerandadhesivedata_06112021.csv",row.names = F)
write.csv(coatingdata2,"coatingdata_06112021.csv",row.names = F)
