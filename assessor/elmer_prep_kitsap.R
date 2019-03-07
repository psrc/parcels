library(tidyverse)
library(data.table)
library(odbc)
library(DBI)

# curr.dir <- getwd()
curr.dir <- "C:/Users/CLam/Documents"
this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)
source("functions_elmer_prep.R")

setwd(curr.dir)
new.dir <-"AssessorKitsap"
setwd(new.dir)

# vector of files
files <- c("parcels", "dwellings", "mh", "comml_imps", "valuations") # codes may have issue reading
filenames <- paste0(files, ".txt")
db.tblname <- c("Parcel", "Dwelling", "MobileHome", "CommercialImprovement", "Valuation")

# Update Elmer ------------------------------------------------------------

elmer_connection <- db.connect("Elmer")
for (i in 1:length(filenames[[i]])) {
  working.dbtable <- paste0("Assessor.tblKitsap", db.tblname[i])
  dt <- fread(filenames[[i]])
  dbWriteTable(elmer_connection, working.dbtable, as.data.frame(dt))
}
dbDisconnect(elmer_connection)

setwd(curr.dir)









