# This script will append column headers to Snohomish County Assessors files
# and export as new set of txt files 

library(openxlsx)

rootDir <- 'J:/Projects/UrbanSim/NEW_DIRECTORY/Databases/Access/Parcels/Snohomish/2018/dwnld_2018_02_07'
setwd(rootDir)
outDir <- 'data_formatted'
attributes <- c("Master", "Land", "Improvement")
col.attributes <- c("Master", "Land", "Improvements")
year <- '2016'

headers <- list()

#read headers
for (a in 1:length(col.attributes)) {
  columns <- read.xlsx("ReportTitles.xlsx", sheet = col.attributes[a], startRow = 1)
  c <- colnames(columns)[1:(length(columns)-1)]
  headers[[a]] <- c
}

for (a in 1:length(attributes)) {
  if (attributes[a] == 'Improvement') {
    table <- read.table(paste0('SnohomishCo ', attributes[a], ' Records_', year, 'AV.txt'), 
                        header = FALSE, 
                        sep = '\t', 
                        quote = "", 
                        comment.char = "",
                        colClasses = "character",
                        stringsAsFactors = FALSE,
                        col.names = headers[[a]]
    )
    table$building_id <- 1:nrow(table)
  } else {
    table <- read.table(paste0('SnohomishCo ', attributes[a], ' Records_', year, 'AV.txt'), 
                        header = FALSE, 
                        sep = '\t', 
                        quote = "", 
                        comment.char = "", 
                        colClasses = "character",
                        stringsAsFactors = FALSE,
                        col.names = headers[[a]])
  }
  write.table(table, file.path(outDir, paste0('SnohomishCo_', attributes[a], '_Records_', year, 'AV.txt')), row.names = FALSE, quote = FALSE, sep = "\t")
  print(paste("Exported", attributes[a]))
}

print("Exporting Completed")