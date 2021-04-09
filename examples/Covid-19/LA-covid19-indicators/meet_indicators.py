"""
Functions to see if indicators are met for yesterday.
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
two_weeks_ago = default_parameters.two_weeks_ago
two_days_ago = default_parameters.two_days_ago
three_days_ago = default_parameters.three_days_ago
eight_days_ago = default_parameters.eight_days_ago
nine_days_ago = default_parameters.nine_days_ago


#---------------------------------------------------------------#
# Case Indicators (County, State, MSA, City of LA)
#---------------------------------------------------------------#    
def meet_case(geog, name, start_date):
    df = meet_case_death_prep(geog, name, start_date)
    extract_col = "days_fewer_cases"
    try:
        indicator = df.iloc[0][extract_col]
        return indicator
    except IndexError:
        return np.nan

def meet_death(geog, name, start_date):
    df = meet_case_death_prep(geog, name, start_date)
    
    extract_col = "days_fewer_deaths"
    try:
        indicator = df.iloc[0][extract_col]
        return indicator
    except IndexError:
        return np.nan


"""
Sub-functions for cases / deaths
"""
def meet_case_death_prep(geog, name, start_date):
    if geog == "county":
        county_state_name = name
        df = utils.prep_county(county_state_name, start_date)
        name = df.county.iloc[0]
        group_cols = ["county", "state"]
        
    if geog == "state":
        state_name = name
        df = utils.prep_state(state_name, start_date)
        name = df.state.iloc[0]
        group_cols = ["state"]
        
    if geog == "msa":
        msa_name = name
        df = utils.prep_msa(msa_name, start_date)
        name = df.msa.iloc[0]
        group_cols = ["msa"]
    
    if geog=="lacity":
        name = "City of LA"
        df = utils.prep_lacity_cases(start_date)
        df = df.assign(name = "City of LA")
        group_cols = ["name"]
        
    df = df[(df.date < today_date) & (df.date >= two_weeks_ago)]
    df = past_two_weeks(df, group_cols)  
    
    return df


def past_two_weeks(df, group_cols):
    """
    Count number of times in past 14 days where
    we had drop in cases / deaths from prior day.
    We will use 7-day rolling average for BOTH cases and deaths.
    Date two weeks ago is 15 days ago because
    we need 14 change-from-prior-day observations.
    """
    
    df = df.assign(
        delta_cases_avg7=(
            df.sort_values("date")
            .groupby(group_cols)["cases_avg7"]
            .diff(periods=1)
        ),
        delta_deaths_avg7=(
            df.sort_values("date")
            .groupby(group_cols)["deaths_avg7"]
            .diff(periods=1)
        )
    )

    df = df.assign(
        days_fewer_cases = df.apply(lambda row: 1 if row.delta_cases_avg7 < 0 
                                    else 0, axis=1),
        days_fewer_deaths = df.apply(lambda row: 1 if row.delta_deaths_avg7 < 0 
                                     else 0, axis=1),
    )

    two_week_totals = (df.groupby(group_cols)
                        .agg({"days_fewer_cases": "sum", 
                            "days_fewer_deaths": "sum"})
                        .reset_index()
                        )

    return two_week_totals


#---------------------------------------------------------------#
# Daily Testing (LA County and City of LA)
#---------------------------------------------------------------#  
def meet_daily_testing(yesterday_date, city_or_county, lower_bound, upper_bound):
    df = utils.prep_testing(start_date)
    
    """
    7/20: can't understand why county's persons tested and city tests 
    (tests and persons tested) don't pass sanity checks.
    Allow county's results to lag; it updates only after ___ days (3? 5? 7?).
    Start with 3.
    """
    yesterday_date = three_days_ago

    if city_or_county == "county":
        extract_col = "County_Performed"
        
    if city_or_county == "city":
        extract_col = "City_Site_Performed"
    
    try:
        indicator = df[df.date==yesterday_date].iloc[0][extract_col]
        return indicator
    except IndexError:
        return np.nan

    
# Share of Positive Results
def meet_positive_share(yesterday_date, city_or_county, lower_bound, upper_bound):
    """
    Returns red/green depending on if benchmark was met last week
    """
    if city_or_county == "county":
        df = utils.prep_la_positive_test(start_date, "county")
        
    if city_or_county == "city":
        df = utils.prep_la_positive_test(start_date, "city")
    
    extract_col = "pct_positive"
    try:
        indicator = df[df.week == df.week.max()].iloc[0][extract_col].round(2)
        return indicator
    except IndexError:
        return np.nan

    
# WHO recommendation of less than 5% positive for 2 weeks     
def meet_positive_share_for_two_weeks(yesterday_date, city_or_county):
    """
    Returns red/green depending on if benchmark was met last week
    """
    if city_or_county == "county":
        df = utils.prep_la_positive_test(start_date, "county")
        
    if city_or_county == "city":
        df = utils.prep_la_positive_test(start_date, "city")
    
    df = df.assign(
        week = df.week.astype(int),
        group = 1,
    )

    df = (df[df.week >= df.week.max() - 1]
          .groupby("group")
          .agg({"weekly_cases": "sum", 
                "weekly_tests": "sum"})
          .reset_index()
         )

    df = df.assign(
        pct_positive = df.weekly_cases / df.weekly_tests
    )
    
    extract_col = "pct_positive"

    try:        
        indicator = df.iloc[0][extract_col].round(2)
        return indicator
    except IndexError:
        return np.nan    
    

#---------------------------------------------------------------#
# COVID-Hospitalizations (LA County)
#---------------------------------------------------------------#
# Data from CA open data portal
def meet_all_hospitalization(county_state_name, yesterday_date):
    df = meet_hospitalization(county_state_name, yesterday_date)
    extract_col = "avg_pct_change_hospitalized"
    try:
        indicator = df.iloc[0][extract_col].round(2)
        return indicator
    except IndexError:
        return np.nan

    
def meet_icu_hospitalization(county_state_name, yesterday_date):
    df = meet_hospitalization(county_state_name, yesterday_date)
    extract_col = "avg_pct_change_icu"
    try:
        indicator = df.iloc[0][extract_col].round(2)
        return indicator
    except IndexError:
        return np.nan
    
"""
Sub-functions for hospitalization data.
"""
def meet_hospitalization(county_state_name, yesterday_date):
    df = utils.prep_hospital_surge(county_state_name, start_date)
    
     # Calculate change from prior day
    df = df.assign(
        change_hospitalized = df.sort_values("date")["hospitalized_covid"].diff(periods=1),
        change_icu = df.sort_values("date")["icu_covid"].diff(periods=1),
        prior_date = df.date2 + pd.Timedelta(days=-1)
    )

    # Guideline says that there either it's downward trending or a percent change of less than 5%.
    # Denominator for percent change is the prior day's # hospitalizations.
    cols = ["date2", "hospitalized_covid", "icu_covid"]
    yesterday_df = (df[cols]
                    .rename(columns = {"date2": "prior_date", 
                                      "hospitalized_covid": "prior_hospitalized",
                                      "icu_covid": "prior_icu"})
                   )

    df = pd.merge(df, yesterday_df, on = "prior_date", how = "left", validate = "1:1")

    # Calculate percent change
    df = df.assign(
        pct_change_hospitalized = df.change_hospitalized / df.prior_hospitalized,
        pct_change_icu = df.change_icu / df.prior_icu,
    )    
    
    # The past week, up through yesterday. Grab [-8 days to -1 day]    
    # Now, subset to the past 7 days and calculate the average pct change.
    if df.date.max() == yesterday_date:
        df = df[(df.date >= eight_days_ago)]
    
    # The value will be constant for the past 7 days, so let's grab just yesterday's date
    # Data lags...so let's grab two days ago
    if df.date.max() == two_days_ago:
        df = df[(df.date >= nine_days_ago)]
        yesterday_date = two_days_ago
    
    df = df.assign(
        avg_pct_change_hospitalized = df.pct_change_hospitalized.mean(),
        avg_pct_change_icu = df.pct_change_icu.mean()
    )
    
    df = df[df.date == yesterday_date]
    return df 