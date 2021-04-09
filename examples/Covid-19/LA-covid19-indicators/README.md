From: https://github.com/CityOfLosAngeles/covid19-indicators


Scripts and Notebooks
------------

## Scripts
* `default_parameters.py`: Default parameters used in the notebooks, which default to Los Angeles County, California, and the Los Angeles-Long Beach-Anaheim metropolitan area. One can visualize the trend in cases and deaths for any other US county, metropolitan area, or state, since we use Johns Hopkins University data. Indicators specific to coronavirus testing, test results, and hospital capacity are specific to LA County or the City of LA. 
* `utils.py`: Functions for a high-level daily report of the situation within the county. 
    * `make_charts.py`: Use the `altair` package to create charts with some standardized formatting.
    * `meet_indicators.py`: Functions to spit out the indicator for the prior day. The daily report gives a high-level summary of indicators for yesterday, due to a slight lag in the data.
    * `useful_dict.py`: Dictionary of US state abbreviations and state names and time zone options to use in `default_parameters.py`

## Notebooks
* `sample-indicators`: Notebook demonstrating how to apply the indicators to other US counties, metropolitan areas, and states.
* `county-city-indicators.ipynb`: LA County and City of LA specific notebook for our daily reporting.
* `state-msa-indicators.ipynb`: California and Los Angeles-Long Beach-Anaheim indicators for daily reporting.
* `neighborhood-charts.ipynb`: LA County neighborhood trends with case data.
* `conversions.ipynb`: Conversions to get New York and Chicago testing benchmarks into the same unit. Apply it to LA by scaling according to population.
