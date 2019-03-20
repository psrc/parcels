library(rvest)
library(RCurl)
library(tidyverse)


out.dir <- "J:/Projects/Geocoding/19GEOCODING/Setup/1Raw/Snohomish"
setwd(out.dir)

webpg <- read_html("https://snohomishcountywa.gov/3183/FTP-Data-Downloads")

key.dirs <- list(shapefiles = list(filenames = c("parcels")),
                 addressing = list(filenames = c("situsaddr")))

cssselector <- "#page .Hyperlink"

scrape.ftp.dirs <- function(cssselector) {
  links <- webpg %>%
    html_nodes(cssselector) %>% 
    html_attr("href")
  ftp.dirs <- names(key.dirs)
  dir.links <- links[str_which(links, paste(ftp.dirs, collapse = "|"))]
}

scrape.ftp.files <- function(ftp.dirs) {
  paths <- c()
  for (dir in ftp.dirs) {
    base <- basename(dir)
    filenames <- key.dirs[[base]]$filenames
    link <- paste0(dir, "/")
    all.filenames <- getURL(link, ftp.use.epsv = FALSE, dirlistonly = TRUE)
    clean.filenames <- strsplit(all.filenames, "\r*\n")[[1]]
    for (filename in filenames) {
      afilename <- str_subset(clean.filenames, paste0("^", filename))
      filename.path <- paste0(link, afilename)
      paths <- c(paths, filename.path)
    }
  }
  return(paths)
}

create.filename <- function(links) {
  fnames <- links %>%
    map(basename) %>%
    unlist
}


ftp.dirs <- scrape.ftp.dirs(cssselector)

file.links <- scrape.ftp.files(ftp.dirs)
file.names <- create.filename(file.links)

download.files <- partial(download.file, mode = "wb")
unzip.files <- partial(unzip, junkpaths = TRUE)

walk2(file.links, file.names, download.files)
walk(file.names, unzip.files)

