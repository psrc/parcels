# tabularize pdfs
library(tabulizer)
library(purrr)
library(data.table)
library(openxlsx)

# default.dir <- getwd()
# new.dir <-"AssessorKitsap"
# setwd(new.dir)

# vector of pdfs
files <- c("parcels", "dwellings", "mh", "codes", "comml_imps", "valuations")
filenames <- paste0(files, ".pdf")

# read through and store lists in list
pdf.list <- NULL
for (i in 1:length(filenames)) {
  out.list <- extract_tables(filenames[i], method = "stream", output = "data.frame")
  pdf.list[[files[i]]] <- out.list
}

# create list of compiled data.tables
dfs <- NULL
for (i in 1:length(pdf.list)) {
  len <- length(pdf.list[[i]])
  sub.list <- pdf.list[[i]]
  if (len >= 2) {
    gen.colnames <- colnames(sub.list[[1]])
    for (ii in seq(2, length(sub.list))) {
      colnames(sub.list[[ii]]) <- gen.colnames
    }
    sub.list <- map(sub.list, setDT)
    dfs[[files[i]]] <- rbindlist(sub.list, use.names = T)
  } else {
    setDT(sub.list[[1]])
    dfs[[files[i]]] <- sub.list[[1]] 
  }
}

# rows where all columns are blank 
remove.blank.rows <- function(table) {
  table[!apply(table == "", 1, all),]
}

dfs.clean <- map(dfs, remove.blank.rows)

write.xlsx(dfs.clean, "kitsap_metadata.xlsx")