library(tidyverse)
library(data.table)
library(openxlsx)
library(odbc)
library(DBI)

data.dir <- "C:/Users/CLam/Documents/AssessorSnohomish"
this.dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(this.dir)
source("functions_elmer_prep.R")

setwd(data.dir)

files <- list.files(pattern = "^SnohCo.+\\d+AV")
db.tblname <- str_extract(files, "(?<=\\s)\\w+")


# Update Elmer ------------------------------------------------------------

elmer_connection <- db.connect("Elmer")

for (i in 1:length(files)) {
  working.dbtable <- paste0("tblSnohomish_", db.tblname[i]) # DBI 1.0.0 "_" quirk
  print(paste("Reading", db.tblname[i], "file"))
  dt <- read.xlsx(files[i], startRow = 2)
  print(paste("Writing to", elmer_connection@info$dbname))
  if (elmer_connection@info$dbname == "Elmer") {
    dbWriteTable(elmer_connection, Id(schema = "Assessor", table = working.dbtable), as.data.frame(dt), overwrite = TRUE)
  } else if (elmer_connection@info$dbname == "Sandbox") {
    dbWriteTable(elmer_connection, Id(table = working.dbtable), as.data.frame(dt), overwrite = TRUE)
  }
}

dbDisconnect(elmer_connection)
