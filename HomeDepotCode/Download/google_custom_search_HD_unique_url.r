
### combine all CSV files ###
pth_part_1 <- "D:/Dropbox/_ICF_project/WA 2-75/HD/part_1"
setwd(pth_part_1)

filenames_part_1 <- Sys.glob("*.csv")

file_part_1_all <- c()
for (file in filenames_part_1){
	file_temp <- read.csv(file, header=FALSE, sep=",", stringsAsFactors = FALSE)
	file_part_1_all <- rbind(file_part_1_all, file_temp)
}

length(unique(file_part_1_all[,2]))


pth_part_2 <- "D:/Dropbox/_ICF_project/WA 2-75/HD/part_2"
setwd(pth_part_2)

filenames_aprt_2 <- Sys.glob("*.csv")


file_part_2_all <- c()
for (file in filenames_aprt_2){
	file_temp <- read.csv(file, header=FALSE, sep=",", stringsAsFactors = FALSE)
	file_part_2_all <- rbind(file_part_2_all, file_temp)
}


length(unique(file_part_2_all[,2]))


all <- rbind(file_part_1_all, file_part_2_all)
length(unique(all[,2]))

dup_ind <- duplicated(all[,2])

all_final <- all[!dup_ind,]

write.csv(all_final, "all_final.csv", row.names=FALSE)
