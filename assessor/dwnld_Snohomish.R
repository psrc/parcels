library(rvest)
library(RCurl)
library(tidyverse)

default.dir <- getwd()
out.dir <-"AssessorSnohomish"
setwd(out.dir)

# assessor_roll currently excluded from download, it is a very generalized & limited dataset with no impr/building records

webpg <- read_html("https://snohomishcountywa.gov/3183/FTP-Data-Downloads")

scrape.main.links <- function() {
  key.dirs <- c("property_characteristics", "documents")
  
  links <- webpg %>%
    html_nodes("#page .Hyperlink") %>% 
    html_attr("href")
  sellinks <- links[str_which(links, paste(key.dirs, collapse = "|"))]
  
  paths <- c()
  for (link in sellinks) {
    base <- basename(link)
    link <- paste0(link, "/") 
    filenames <- getURL(link, ftp.use.epsv = FALSE, dirlistonly = TRUE)
    filenames <- strsplit(filenames, "\r*\n")[[1]]
    if (base == "documents") filenames <- filenames[str_which(filenames, "^Property|Assessment")]
    filenames.path <- paste0(link, filenames)
    paths <- c(paths, filenames.path)
  } 
  return(paths)
}

create.filename <- function(links) {
  fnames <- links %>%
    map(basename) %>%
    unlist
}

main.links <- scrape.main.links()
main.fnames <- create.filename(main.links)
download.files <- partial(download.file, mode = "wb")
walk2(main.links, main.fnames, download.files)

setwd(default.dir)
