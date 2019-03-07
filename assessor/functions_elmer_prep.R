db.connect <- function(adatabase = c("Sandbox", "Elmer")) {
  elmer_connection <- dbConnect(odbc(),
                                driver = "SQL Server",
                                server = "sql2016\\DSADEV",
                                database = adatabase,
                                trusted_connection = "yes"
  )
}


# Functions ---------------------------------------------------------------


change.colnames.kitsap <- function() {
  colnames.list <- NULL
  for (i in 1:length(filenames)) {
    t <- fread(filenames[i])
    t.cols <- colnames(t)
    t.cols.rep <- str_replace_all(t.cols, "_", " ") %>% str_to_title() %>% str_replace_all(pattern = " ", replacement = "")
    rm(t)
    colnames.list[[files[i]]] <- t.cols.rep
  }
  
  colnames.list.og <- colnames.list
  var <- c("^Mh" = "MobileHome", 
           "Lvg" = "Living", 
           "Bsmt" = "Basement",
           "^Imp(?!rovement)" = "Improvement", 
           "Yr" = "Year", 
           "Blt" = "Built", 
           "Pct" = "Percent",
           "Sf" = "SqFt",
           "Tot" = "Total",
           "Cond" = "Condition", 
           "Qual" = "Quality",
           "STR" = "SectionTownshipRange", "QtrSec" = "QuarterSection", "Nbrhd" = "Neighborhood", "Wf" = "Waterfront",
           "Bedrms" = "Bedrooms", "Remo" = "Remodeled",
           "Uom" = "UnitOfMeasure") 
  
  for (i in 1:length(colnames.list)) {
    for (ii in 1:length(var)) {
      old.var <- names(var)[[ii]]
      new.var <- var[[ii]]
      colnames.list[[i]] <- str_replace_all(colnames.list[[i]], pattern = old.var, replacement = new.var)
    }
  }
}
