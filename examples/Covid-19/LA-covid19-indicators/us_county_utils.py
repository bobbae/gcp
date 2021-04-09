"""
Create a version of processed data
used in our notebooks.

Instead of selecting individual county and then
make chart, we'll clean all counties at once,
then subset.

Save it to `data` to use for our RMarkdown repo:
https://github.com/CityOfLosAngeles/covid19-rmarkdown
"""
import numpy as np
import pandas as pd

import default_parameters
import utils

from IPython.display import Markdown, HTML

start_date = default_parameters.start_date
today_date = default_parameters.today_date
yesterday_date = default_parameters.yesterday_date
one_week_ago = default_parameters.one_week_ago

fulldate_format = default_parameters.fulldate_format


# Clean the JHU county data at once
def clean_jhu(start_date):
    df = utils.prep_us_county_time_series()

    keep_cols = [
        "county",
        "state",
        "state_abbrev",
        "fips",
        "date",
        "Lat",
        "Lon",
        "cases",
        "deaths",
        "new_cases",
        "new_deaths",
    ]

    df = (df[keep_cols]
        .sort_values(["county", "state", "fips", "date"])
        .reset_index(drop=True)
    )
    
    # Merge in population
    pop = (pd.read_csv(utils.CROSSWALK_URL, 
                       dtype={"county_fips": "str", "cbsacode": "str"})
           [["county_fips", "county_pop"]]
           .rename(columns = {"county_fips": "fips"})
          )

    df = pd.merge(df, pop,
                  on = "fips", how = "inner", validate = "m:1"
    )
    
    df = utils.calculate_rolling_average(df, start_date, today_date)
    df = utils.find_tier_cutoffs(df, "county_pop")
    df = utils.doubling_time(df, window=7)
    
    return df


# Clean all CA counties hospitalizations data at once
def clean_hospitalizations(start_date):
    
    df = pd.read_parquet(utils.HOSPITAL_SURGE_URL)
    
    df = (df.assign(
            date = pd.to_datetime(df.date).dt.date,
            date2 = pd.to_datetime(df.date),
        ).rename(columns = {"county_fips": "fips"})
    )
    
    keep_cols = [
        "county",
        "fips",
        "date",
        "date2",
        "hospitalized_covid",
        "all_hospital_beds",
        "icu_covid",
        "all_icu_beds",
    ]

    df = (
        df[keep_cols]
        .sort_values(["county", "fips", "date"])
        .reset_index(drop=True)
    )
    
    # Calculate 7-day average
    df = df.assign(
        hospitalized_avg7 = df.hospitalized_covid.fillna(0).rolling(window=7).mean(),
        icu_avg7 = df.icu_covid.fillna(0).rolling(window=7).mean(),
    )

    df = df[(df.date >= start_date) & (df.date < today_date)]

    df = utils.make_long(df)
    
    return df



# Caption to include under each county
def county_caption(df, county_name):
    df = df[df.county == county_name]
    
    '''
    This changes the columns to string...which shows up incorrectly in Markdown.
    
    cols_to_format = ["cases", "deaths", "new_cases", "new_deaths"]
    for c in cols_to_format:
        df[c] = df[c].map("{:,g}".format)
    '''
    np.seterr(divide='ignore', invalid='ignore')

    extract_col = "cases"    
    cumulative_cases = df[df.date == yesterday_date].iloc[0][extract_col]
    
    extract_col = "cases_avg7"
    new_cases_1week = df[df.date == one_week_ago].iloc[0][extract_col]
    new_cases_yesterday = df[df.date == yesterday_date].iloc[0][extract_col]
    tier3_cutoff = df[df.date == yesterday_date].iloc[0]["tier3_case_cutoff"]
    pct_change_new_cases = (((new_cases_yesterday - new_cases_1week) / new_cases_1week) * 100).round(1)
    new_cases_tier4_proportion = (new_cases_yesterday / tier3_cutoff).round(1)
    
    extract_col = "deaths"
    cumulative_deaths = df[df.date == yesterday_date][extract_col].iloc[0]

    
    extract_col = "deaths_avg7"
    new_deaths_1week = df[df.date == one_week_ago].iloc[0][extract_col]
    new_deaths_yesterday = df[df.date == yesterday_date].iloc[0][extract_col]      
    pct_change_new_deaths = (((new_deaths_yesterday - new_deaths_1week) / new_deaths_1week) * 100).round(1)

    extract_col = "doubling_time"
    doubling_time_1week = df[df.date == one_week_ago].iloc[0][extract_col].round(0).astype(int)
    doubling_time_yesterday = df[df.date == yesterday_date].iloc[0][extract_col].round(0).astype(int)      
    
    # Add condition for small numbers; report 7-day rolling average instead of percent change
    threshold = 10
    cases_under = ((new_cases_1week <= threshold) or (new_cases_yesterday <= threshold))
    cases_over = ((new_cases_1week > threshold) and (new_cases_yesterday > threshold))
    
    deaths_under = ((new_deaths_1week <= threshold) or (new_deaths_yesterday <= threshold))
    deaths_over = ((new_deaths_1week > threshold) and (new_deaths_yesterday > threshold))
    
    if cases_under and deaths_over:
        display(
            Markdown(
                f"As of {yesterday_date.strftime(fulldate_format)}, there were **{cumulative_cases:,}** total cases "
                f"and **{cumulative_deaths:,}** total deaths. "
                f"<br>In the past week, new cases went from **{new_cases_1week:.1f}** to **{new_cases_yesterday:.1f}**; "
                f"new deaths grew by **{pct_change_new_deaths}%**. " 
                f"<br>New cases are **{new_cases_tier4_proportion:.1f}x** higher than the Tier 4 cut-off. <i><span style='color:#797C7C'>(1 = Tier 4 widespread cut-off; 2 = new cases are 2x higher than the Tier 4 cut-off)</span></i>."
                f"<br>In the past week, the doubling time went from **{doubling_time_1week} days** to "
                f"**{doubling_time_yesterday} days** <i><span style='color:#797C7C'>(longer doubling time is better)</span></i>. "
            )
        )

    elif cases_over and deaths_under:
        display(
            Markdown(
                f"As of {yesterday_date.strftime(fulldate_format)}, there were **{cumulative_cases:,}** total cases "
                f"and **{cumulative_deaths:,}** total deaths. "
                f"<br>In the past week, new cases grew by **{pct_change_new_cases}%**; "
                f"new deaths went from **{new_deaths_1week:.1f}** to **{new_deaths_yesterday:.1f}**. " 
                f"<br>New cases are **{new_cases_tier4_proportion:.1f}x** higher than the Tier 4 cut-off. <i><span style='color:#797C7C'>(1 = Tier 4 widespread cut-off; 2 = new cases are 2x higher than the Tier 4 cut-off)</span></i>."
                f"<br>In the past week, the doubling time went from **{doubling_time_1week} days** to "
                f"**{doubling_time_yesterday} days** <i><span style='color:#797C7C'>(longer doubling time is better)</span></i>. "
            )
        )
    
    elif cases_under and deaths_under:
        display(
            Markdown(
                f"As of {yesterday_date.strftime(fulldate_format)}, there were **{cumulative_cases:,}** total cases "
                f"and **{cumulative_deaths:,}** total deaths. "
                f"<br>In the past week, new cases went from **{new_cases_1week:,.1f}**  to **{new_cases_yesterday:,.0f}**; "
                f"new deaths went from **{new_deaths_1week:.1f}** to **{new_deaths_yesterday:.1f}**. " 
                f"<br>New cases are **{new_cases_tier4_proportion:.1f}x** higher than the Tier 4 cut-off. <i><span style='color:#797C7C'>(1 = Tier 4 widespread cut-off; 2 = new cases are 2x higher than the Tier 4 cut-off)</span></i>."
                f"<br>In the past week, the doubling time went from **{doubling_time_1week} days** to "
                f"**{doubling_time_yesterday} days** <i><span style='color:#797C7C'>(longer doubling time is better)</span></i>. "
            )
        )        
    
    else:   
        display(
            Markdown(
                f"As of {yesterday_date.strftime(fulldate_format)}, there were **{cumulative_cases:,}** total cases "
                f"and **{cumulative_deaths:,}** total deaths. "
                f"<br>In the past week, new cases grew by **{pct_change_new_cases}%**; "
                f"new deaths grew by **{pct_change_new_deaths}%**. " 
                f"<br>New cases are **{new_cases_tier4_proportion:.1f}x** higher than the Tier 4 cut-off. <i><span style='color:#797C7C'>(1 = Tier 4 widespread cut-off; 2 = new cases are 2x higher than the Tier 4 cut-off)</span></i>."
                f"<br>In the past week, the doubling time went from **{doubling_time_1week} days** to "
                f"**{doubling_time_yesterday} days** <i><span style='color:#797C7C'>(longer doubling time is better)</span></i>. "
            )
        )

def ca_hospitalizations_caption(df, county_name):
    df = df[df.county == county_name]
    
    if df.date.max() == default_parameters.two_days_ago:
        yesterday_date = default_parameters.two_days_ago
        one_week_ago = default_parameters.nine_days_ago
    else:
        yesterday_date = default_parameters.yesterday_date
        one_week_ago = default_parameters.one_week_ago

    np.seterr(divide='ignore', invalid='ignore')

    extract_col = "COVID-ICU"
    icu_1week = df[(df.date == one_week_ago) & (df["type"]==extract_col)].iloc[0]["num"]
    icu_yesterday = df[(df.date == yesterday_date) & (df["type"]==extract_col)].iloc[0]["num"]      
    pct_change_icu = (((icu_yesterday - icu_1week) / icu_1week) * 100).round(1)
    
    extract_col = "All COVID-Hospitalized"
    hosp_1week = df[(df.date == one_week_ago) & (df["type"]==extract_col)].iloc[0]["num"]
    hosp_yesterday = df[(df.date == yesterday_date) & (df["type"]==extract_col)].iloc[0]["num"]      
    pct_change_hosp = (((hosp_yesterday - hosp_1week) / hosp_1week) * 100).round(1)
    
    # Add condition for small numbers; report 7-day rolling average instead of percent change
    threshold = 10
    icu_under = ((icu_1week <= threshold) or (icu_yesterday <= threshold))
    icu_over = ((icu_1week > threshold) and (icu_yesterday > threshold))
    
    hosp_under = ((hosp_1week <= threshold) or (hosp_yesterday <= threshold))
    hosp_over = ((hosp_1week > threshold) and (hosp_yesterday > threshold))
    
    if icu_under and hosp_over: 
        display(
            Markdown(
                f"In the past week, all COVID hospitalizations grew by **{pct_change_hosp}%**.; "
                f"COVID ICU hospitalizations went from **{icu_1week:.1f}** to **{icu_yesterday:.1f}**. "
            )
        )
        
    elif icu_over and hosp_under:
        display(
            Markdown(
                f"In the past week, all COVID hospitalizations went from **{hosp_1week:.1f}** to **{hosp_yesterday:.1f}**.; "
                f"COVID ICU hospitalizations grew by **{pct_change_icu}%**. "
            )
        )
        
    elif icu_under and hosp_under:
        display(
            Markdown(
                f"In the past week, all COVID hospitalizations went from **{hosp_1week:.1f}** to **{hosp_yesterday:.1f}**.; "
                f"COVID ICU hospitalizations went from **{icu_1week:.1f}** to **{icu_yesterday:.1f}**. "
            )
        )
        
    else:
        display(
            Markdown(
                f"In the past week, all COVID hospitalizations grew by **{pct_change_hosp}%**.; "
                f"COVID ICU hospitalizations grew by **{pct_change_icu}%**. "
            )
        )