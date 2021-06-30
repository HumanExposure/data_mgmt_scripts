
#Make bat file for product pages (KKI, 6/2021)


library(stringr)


getcoatingsdata<-function(indir){

setwd(indir)
files<-list.files(indir)

numrec<-0

finaldata<-list()
#for (j in 1:1){
for (j in 1:length(files)) {

  cat("\n","Processing file ",j," of ",length(files))
   #read file    
   cat("\n","readinglines")
   thisfile<-data.frame(readLines(files[j]))
   supplierfile<-files[j]
   #cat("\n","readinglines",colnames(thisfile))
   
   #parse file (this reproduces SAS code)
   colnames(thisfile)[1]<-"thisline"
   thisfile$thisline<-as.character(thisfile$thisline)

   
    if (any(grepl("/product/",thisfile$thisline))==F){
      cat("\n","No products in file ",supplierfile)
      next
    } 

 for (i in 1:length(thisfile$thisline)){

    #category
    if(grepl("<title>Additives ", thisfile$thisline[i])) {
      k1<-str_locate(thisfile$thisline[i],"additives ")[1]+9
      k2<-str_locate(thisfile$thisline[i],"</title>")[1]-1
      k3<-str_locate(thisfile$thisline[i],"SpecialChem - ")[1]+14
      k4<-str_locate(thisfile$thisline[i],"- additives")[1]-1
            
      category<-substr(thisfile$thisline[i],k1,k2)
      supplier<-substr(thisfile$thisline[i],k3,k4)
      
      cat("\n","found category",k1, category)
    }
    #products  
    if(grepl("/product/", thisfile$thisline[i]) & grepl("view more", thisfile$thisline[i])) {
      addressstr<-thisfile$thisline[i]
      numrec<-numrec+1
      prefix="https://coatings.specialchem.com/product/"
      
     #get the current product name
      #product_name<-addressstr

      k1<-str_locate(addressstr,"/product/")[1]+11
      k2<-str_locate(addressstr," rel=")[1]-2
      product_name<-substr(addressstr,k1,k2)
      docname<-substr(addressstr,k1-2,k2)
      URL<-paste0(prefix,docname)
      cat("\n","found a product",k1,k2,product_name)
      thisdata<- c(product_name,category,docname,URL,supplierfile,supplier)
      finaldata[[numrec]]<-thisdata
    }

  }
}
k<-as.data.frame(do.call(rbind, finaldata))
colnames(k)<-c("product_name", "category", "document", "URL","supplierfile","supplier")

return(k)
}
    
directory<-"L:/Lab/NERL_Isaacs/kki-21-SPECIALCHEM_FOR_FACTOTUM/kk-15-SPECIALCHEMDATA/coatings_supplier_pages/"

#directory<-"L:/Lab/NERL_Isaacs/kki-21-SPECIALCHEM_FOR_FACTOTUM/Adhesives_final"

allcategorydata<-getcoatingsdata(directory)
setwd("L:/Lab/NERL_Isaacs/kki-21-SPECIALCHEM_FOR_FACTOTUM/kk-15-SPECIALCHEMDATA/")
allcategorydata$wget<-paste0("wget ", allcategorydata$URL)
write.csv(allcategorydata$wget,"getcoatingproductpages.bat",row.names = F,quote=F)
