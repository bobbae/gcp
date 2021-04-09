"""
Functions to see how CA counties are meeting the
CA Department of Public Health's reopening metrics

https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/COVID19CountyMonitoringOverview.aspx

"""
import numpy as np
import pandas as pd

import default_parameters
import utils

fulldate_format = default_parameters.fulldate_format
time_zone = default_parameters.time_zone
start_date = default_parameters.start_date
yesterday_date = default_parameters.yesterday_date
today_date = default_parameters.today_date
one_week_ago = default_parameters.one_week_ago
two_weeks_ago = default_parameters.two_weeks_ago
three_weeks_ago = default_parameters.three_weeks_ago
two_days_ago = default_parameters.two_days_ago
three_days_ago = default_parameters.three_days_ago
eight_days_ago = default_parameters.eight_days_ago
nine_days_ago = default_parameters.nine_days_ago

S3_FILE_PATH = "s3://public-health-dashboard/jhu_covid19/"

# Units for case rates are per 100k
POP_RATE = 100_000

# LA County population (using ca_county_pop_crosswalk)
LA_POP = 10_257_557

#---------------------------------------------------------------#
# Case Rate (CA counties)
#---------------------------------------------------------------#  
# Case Rate (per 100k) is calculated as 7-day average with 7-day lag
# Calculated off of daily new cases
def case_rate(county_state_name, start_date, time_period):
    df = prep_case_rate(county_state_name, start_date, time_period)
    
    pop = (pd.read_parquet(f'{S3_FILE_PATH}ca_county_pop_crosswalk.parquet')
       .rename(columns = {"county_fips": "fips"})
        [["fips", "county_pop2020"]]
      )
    
    df = pd.merge(df, pop, on = "fips", how = "left", validate = "m:1")
    
    # Calculate 7-day average of new cases
    extract_col = ["new_cases"]
    county_pop = df.county_pop2020.iloc[0]
    new_cases_avg7 = df[extract_col].mean()
    
    # Convert to cases per 100k
    cases_per100k = (new_cases_avg7 / county_pop * POP_RATE).round(2).iloc[0]
    
    return cases_per100k

    
"""
Sub-functions for case rate
"""
def prep_case_rate(county_state_name, start_date, time_period):
    df = utils.prep_county(county_state_name, start_date)    
    
    if time_period == "today":
        df = df[(df.date <= yesterday_date) & (df.date > one_week_ago)]
    
    if time_period == "one_week_ago":
        df = df[(df.date <= one_week_ago) & (df.date > two_weeks_ago)]

    if time_period == "two_weeks_ago":       
        df = df[(df.date <= two_weeks_ago) & (df.date > three_weeks_ago)]
    
    return df 



#---------------------------------------------------------------#
# Test Positivity Rate (LA County)
#---------------------------------------------------------------#  
# Test Positivity is calculated as 7-day average with 7-day lag
# Testing particularly is lagged; we know this to be true for LA County's data
def positive_rate(start_date, time_period):
    df = prep_test_rate(start_date, time_period)  
    
    # Calculate 7-day average of test positivity
    extract_col1 = ["County_Positive"]
    extract_col2 = ["County_Performed"]
    
    positivity_rate = (df[extract_col1].sum().iloc[0]) / (df[extract_col2].sum().iloc[0])    
    positivity_rate = positivity_rate.round(3)
    
    return positivity_rate


"""
Sub-functions for testing and test positivity rates
"""
def prep_test_rate(start_date, time_period):
    df = utils.prep_testing(start_date)
    
    if time_period == "one_week_ago":
        df = df[(df.date <= one_week_ago) & (df.date > two_weeks_ago)]

    if time_period == "two_weeks_ago":       
        df = df[(df.date <= two_weeks_ago) & (df.date > three_weeks_ago)]
    
    return df


#---------------------------------------------------------------#
# Test Rate (LA County)
#---------------------------------------------------------------#  
# Test Rate is calculated as 7-day average with 7-day lag
# It is per 100k. It's only used to adjust for test positivity rate.
# Testing particularly is lagged; we know this to be true for LA County's data
def test_rate(start_date, time_period):
    df = prep_test_rate(start_date, time_period)  
        
    # Calculate 7-day average of tests conducted
    extract_col = ["County_Performed"]
    tests_avg7 = df[extract_col].mean()
    
    tests_per100k = (tests_avg7 / LA_POP * POP_RATE).round(2).iloc[0]
    
    return tests_per100k