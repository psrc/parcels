library(rvest)
library(data.table)
library(tidyverse)

default.dir <- getwd()
out.dir <-"AssessorKitsap"
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

data.links <- scrape.links(".ms-rteTableEvenCol-2:nth-child(1) a") # css selector found via https://selectorgadget.com/
data.fnames <- create.filename(data.links)
walk2(data.links, data.fnames, download.file)

doc.links <- scrape.links(".ms-rteTableOddCol-2+ .ms-rteTableEvenCol-2 a")
doc.fnames <- create.filename(doc.links)
download.pdf <- partial(download.file, mode = "wb")
walk2(doc.links, doc.fnames, download.pdf)

setwd(default.dir)
