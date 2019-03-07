library(tidyverse)
library(data.table)
library(odbc)
library(DBI)

curr.dir <- "C:/Users/CLam/Documents"
this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)
source("functions_elmer_prep.R")

setwd(curr.dir)
data.dir <-"AssessorKitsap"
setwd(data.dir)

# vector of files
files <- c("parcels", "dwellings", "mh", "comml_imps", "valuations") # codes may have issue reading
filenames <- paste0(files, ".txt")
db.tblname <- c("Parcel", "Dwelling", "MobileHome", "CommercialImprovement", "Valuation")

# Update Elmer ------------------------------------------------------------

elmer_connection <- db.connect("Elmer")
for (i in 1:length(filenames[1])) {
  working.dbtable <- paste0("tblKitsap_", db.tblname[i])
  dt <- fread(filenames[[i]])
  DBI::dbWriteTable(elmer_connection, Id( schema = "Assessor", table = working.dbtable), as.data.frame(dt), overwrite = TRUE)
  # working.dbtable <- paste0('Assessor.tblKitsap', db.tblname[i])
  # dt <- fread(filenames[[i]])
  # dbWriteTable(elmer_connection, working.dbtable, as.data.frame(dt))
}
dbDisconnect(elmer_connection)

setwd(curr.dir)









