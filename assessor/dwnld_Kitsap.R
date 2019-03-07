library(rvest)
library(data.table)
library(tidyverse)

out.dir <-"C:/Users/CLam/Documents/AssessorKitsap"
setwd(out.dir)

domain <- "https://www.kitsapgov.com/"
webpg <- read_html("https://www.kitsapgov.com/assessor/Pages/DataDownload.aspx") 

scrape.links <- function(cssselector) {
  links <- webpg %>%
    html_nodes(cssselector) %>% 
    html_attr("href") %>%
    map(function(x) paste0(domain, x)) %>%
    unlist
}

create.filename <- function(links) {
  fnames <- links %>%
    map(basename) %>%
    unlist
}

execute.process <- function(cssselector) {
  download.files <- partial(download.file, mode = "wb")
  data.links <- scrape.links(cssselector)
  data.fnames <- create.filename(data.links)
  walk2(data.links, data.fnames, download.files)
}

# css selector found via https://selectorgadget.com/
# data, pdfs
css.selectors <- list(".ms-rteTableEvenCol-2:nth-child(1) a", ".ms-rteTableOddCol-2+ .ms-rteTableEvenCol-2 a")

walk(css.selectors, execute.process)
