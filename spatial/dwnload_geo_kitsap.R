# This script will download spatial data and extract from zipped file

library(rvest)
library(data.table)
library(tidyverse)

out.dir <-"J:/Projects/Geocoding/19GEOCODING/Setup/1Raw/Kitsap"
setwd(out.dir)

webpg <- read_html("https://www.kitsapgov.com/dis/Pages/resources.aspx")
cssselector <- ".ms-rteTableEvenCol-4 a" # css selector found via https://selectorgadget.com/

filenms <- c("roadcl", "parcels", "siteaddr")

scrape.links <- function(cssselector) {
  links <- webpg %>%
    html_nodes(cssselector) %>% 
    html_attr("href")
}

create.filename <- function(links) {
  fnames <- links %>%
    map(basename) %>%
    unlist
}

execute.process <- function(cssselector) {
  download.files <- partial(download.file, mode = "wb")
  unzip.files <- partial(unzip, junkpaths = TRUE)
  
  data.links <- scrape.links(cssselector) %>% str_subset(paste0(filenms, collapse = "|"))
  data.fnames <- create.filename(data.links)
  
  walk2(data.links, data.fnames, download.files)
  walk(data.fnames, unzip.files)
}
  
walk(cssselector, execute.process)
