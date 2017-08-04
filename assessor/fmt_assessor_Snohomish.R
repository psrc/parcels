library(openxlsx)
library(magrittr)

rootDir <- 'J:/Projects/UrbanSim/NEW_DIRECTORY/Databases/Access/Parcels/Snohomish/2016/downloads/March_10_2016/prop_characteristics'
setwd(rootDir)
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
                        fill = TRUE, 
                        sep = '\t', 
                        quote = "", 
                        comment.char = "", 
                        row.names = NULL,
                        col.names = c("building_id", headers[[a]])
    )
  } else {
    table <- read.table(paste0('SnohomishCo ', attributes[a], ' Records_', year, 'AV.txt'), 
                        header = FALSE, 
                        fill = TRUE, 
                        sep = '\t', 
                        quote = "", 
                        comment.char = "", 
                        col.names = headers[[a]])
  }
  write.table(table, file.path('data_formatted', paste0('SnohomishCo_', attributes[a], '_Records_', year, 'AV.txt')), row.names = FALSE, quote = FALSE, sep = "\t")
  print(paste("Exported", attributes[a]))
}

print("Exporting Completed")