library(XML)
library(RCurl)

## Root webpage
pgroot <- "http://www.pgproductsafety.com"

## SDS search pages
pgpage <- "http://www.pgproductsafety.com/productsafety/search_results.php?submit=Search&searchtext=%2A&category=SDS&start=1&num=2400"
pgurl <- getURL(url = pgpage)
pghtml <- htmlParse(pgurl)

## Links to either look at SDS or add SDS to download queue
pglinks <- unlist(xpathApply(pghtml,"//div[@class='result-data']/p/a",xmlGetAttr,"href"))

## Get rid of "add to download queue" links
pglinks <- pglinks[which(grepl("queue",pglinks)==FALSE)]

## Construct working links
pglinks <- paste(pgroot,pglinks,sep="")
pglinks <- gsub(" ","%20",pglinks)

## Wget executable name
execname <- "wget.exe"

## Write batch file to download all links
Names <- paste(execname,unique(pglinks),sep=" ")
fileConn <- file("Download_All_ProcterGamble_Links.bat")
writeLines(Names,fileConn)
close(fileConn)