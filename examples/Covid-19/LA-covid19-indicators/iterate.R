library(rmarkdown)
library(stringr)
library(tidyverse)

#setwd("GitHub/covid19-indicators)

# create an index
neighborhoods <- c("Echo Park", "Koreatown")

# create a data frame with parameters and output file names
reports <- tibble(
  filename = str_c(neighborhoods, "-trends", ".html"),
  params = map(neighborhoods, ~list(neighborhood = .))
)


# iterate render() along the tibble of parameters and file names
reports %>%
  select(output_file = filename, params) %>%
  pwalk(rmarkdown::render, input = "notebooks/r-neighborhood.Rmd", 
        output_dir = "notebooks")