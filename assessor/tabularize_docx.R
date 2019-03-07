# This script will extract tables embedded in .docx files (e.g. Snohomish County metadata)

library(docxtractr)
library(openxlsx)

dir <- "C:/Users/CLam/Documents/AssessorSnohomish"
setwd(dir)

doc <- read_docx("Property Characteristics Extract.docx")
num.tbls <- docx_tbl_count(doc)

# clean tables
tbls.list <- NULL
for (i in 1:num.tbls) {
  tb <- docx_extract_tbl(doc, i)
  desc.data <- colnames(tb)[1]
  name.data <- str_extract(desc.data, "(?<=\\.{3})\\w+(?!\\s)")
  colnames(tb) <- unname(unlist(as.list(tb[1, ])))
  tb <- tb[2:nrow(tb),]
  tbls.list[[name.data]] <- tb
}

# export to excel
wb <- createWorkbook()
for (i in 1:length(tbls.list)) {
  addWorksheet(wb, names(tbls.list)[[i]])
  modifyBaseFont(wb, fontSize = 10, fontName = "Segoe UI Semilight")
  writeData(wb, names(tbls.list)[[i]], tbls.list[[i]])
  saveWorkbook(wb, file = "snohomish_metadata.xlsx", overwrite = T)
}
