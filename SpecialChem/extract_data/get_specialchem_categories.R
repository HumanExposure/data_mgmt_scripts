
#Rescrape product categories from supplier pages (KKI, 6/2021)

#this recreates the %read_all_data SAS macro from the process_supplier_pages script (KKI, 2015)

library(stringr)

getsupplierdata<-function(indir){

setwd(indir)
files<-list.files(indir)

numrec<-0

finaldata<-list()
for (j in 1:length(files)) {

  cat("\n","Processing file ",j," of ",length(files))
   #read file 
   thisfile<-data.frame(readLines(files[j]))
   supplierfile<-files[j]

   #parse file (this reproduces SAS code)
   colnames(thisfile)[1]<-"thisline"
   thisfile$thisline<-as.character(thisfile$thisline)

   if (any(grepl("href='/product/",thisfile$thisline))==F){
    # cat("\n","No products in file ",supplierfile)
     next
   } 

 for (i in 1:length(thisfile$thisline)){
      
    #products  
    if(grepl("href='/product/", thisfile$thisline[i]) & grepl("overtitle", thisfile$thisline[i])) {
      addressstr<-thisfile$thisline[i]

      k1<-str_locate(addressstr,"href='")[1]+15
      k2<-str_locate(addressstr,"'>")[1]-1
      product_name<-substr(addressstr,k1,k2)
    }
    if(grepl("</h1>", thisfile$thisline[i])) {
      supplierstr<-thisfile$thisline[i]
      
      #get the supplier
      k1<-str_locate(supplierstr,">")[1]+1   
      k2<-str_locate(supplierstr,"</h1>")[1]-1  
     suppliername<-substr(supplierstr,k1,k2)
#     cat("\n","found a supplier")
    }    
    #categories
    if(grepl("/product-categories/", thisfile$thisline[i])) {
     numrec<-numrec+1
     #cat("\n","found a category")
     catstr<-thisfile$thisline[i]
     #get the current category
     k1<-str_locate(catstr,"'>")[1]+2
     k2<-str_locate(catstr,"</a>")[1]-1
     category<-substr(catstr,k1,k2)

       thisdata<- c(product_name, supplierfile, suppliername, category)
     finaldata[[numrec]]<-thisdata
   }
  }
}
k<-as.data.frame(do.call(rbind, finaldata))
colnames(k)<-c("product_name", "supplierfile", "supplier", "raw_function_category")

return(k)
}
    
directory<-"L:/Lab/NERL_Isaacs/kki-21-SPECIALCHEM_FOR_FACTOTUM/kk-15-SPECIALCHEMDATA/AllSupplierFilesWithProducts"

allcategorydata<-getsupplierdata(directory)
setwd("L:/Lab/NERL_Isaacs/kki-21-SPECIALCHEM_FOR_FACTOTUM/kk-15-SPECIALCHEMDATA/")
write.csv(allcategorydata,"allcategorydata_06032021.csv")
save(allcategorydata, file="allcategorydata.RData")
