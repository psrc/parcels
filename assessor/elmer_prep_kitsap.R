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
files <- c("parcels", "dwellings", "mh", "comml_imps", "valuations", "codes") # codes may have issue reading, needs to be converted to UTF-8 beforehand
filenames <- paste0(files, ".txt")
db.tblname <- c("Parcel", "Dwelling", "MobileHome", "CommercialImprovement", "Valuation", "Codes")

clean.codes.dt <- function(filename) {
  dt <- fread(filename)
  colname2rm <- str_subset(colnames(dt), "^V\\d*")
  new.colnames <- setdiff(colnames(dt), colname2rm)
  col2rm <- colnames(dt)[apply(dt, 2, function(x) all(is.na(x)))]
  cols <- setdiff(colnames(dt), col2rm)
  t <- dt[, ..cols]
  setnames(t, colnames(t), new.colnames)
  print("Tidied table, ignore warning")
  return(t)
}


# Update Elmer ------------------------------------------------------------

elmer_connection <- db.connect("Elmer")

for (i in 1:length(filenames)) {
  working.dbtable <- paste0("tblKitsap_", db.tblname[i]) # DBI 1.0.0 "_" quirk
  if (db.tblname[i] == "Codes") {
    dt <- clean.codes.dt(filenames[[i]])
  } else {
    dt <- fread(filenames[[i]])
  }
  if (elmer_connection@info$dbname == "Elmer") {
    dbWriteTable(elmer_connection, Id(schema = "Assessor", table = working.dbtable), as.data.frame(dt), overwrite = TRUE)
  } else if (elmer_connection@info$dbname == "Sandbox") {
    dbWriteTable(elmer_connection, Id(table = working.dbtable), as.data.frame(dt), overwrite = TRUE)
  }
}

dbDisconnect(elmer_connection)

setwd(curr.dir)









