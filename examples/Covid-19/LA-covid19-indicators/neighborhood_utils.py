"""
Functions to clean up neighborhood data
and feed into interactive charts
"""
import numpy as np
import pandas as pd

from datetime import date, timedelta

S3_FILE_PATH = "s3://public-health-dashboard/jhu_covid19/"

NEIGHBORHOOD_URL = f"{S3_FILE_PATH}la-county-neighborhood-time-series.parquet"

CROSSWALK_URL = f"{S3_FILE_PATH}la_neighborhoods_population_crosswalk.parquet"

NEIGHBORHOOD_APPENDED_URL = f"{S3_FILE_PATH}la-county-neighborhood-testing-appended.parquet"

def clean_data():
    df = pd.read_parquet(NEIGHBORHOOD_URL)
    crosswalk = pd.read_parquet(CROSSWALK_URL)
    
    # Get rid of duplicates
    # We keep the incorporated and unincorporated labels because     
    # If there are duplicate dates, but diff values for cases and deaths, let's keep the max
    df = (df[df.Region != "Long Beach"]
          .assign(
              # Had to convert date to string to write to parquet, but we want it as datetime/object
              date = pd.to_datetime(df.date).dt.date,
              cases = df.groupby(["Region", "date", "date2"])["cases"].transform("max"),
              deaths = df.groupby(["Region", "date", "date2"])["deaths"].transform("max"),
          ).drop_duplicates(subset = ["Region", "date", "date2", "cases", "deaths"])
          .drop(columns = ["LCITY", "COMMUNITY", "LABEL"])
    )

    
    # Our crosswalk is more extensive, get rid of stuff so we can have a m:1 merge
    crosswalk = (crosswalk[crosswalk.Region.notna()]
                 [["Region", "aggregate_region", "population"]]
                 .drop_duplicates()
            )
    
    # Merge in pop
    df = pd.merge(df, crosswalk, on = "Region", how = "inner", validate = "m:1")
    
    # Be explicit about which missing values to fill in
    # Add new lines if more missing data appears later
    df = interpolate_linearly(df, "11/18/20", "11/20/20")
    df = interpolate_linearly(df, "12/19/20", "12/22/20")
    df = interpolate_linearly(df, "1/21/21", "1/30/21")
    df = interpolate_linearly(df, "3/29/21", "4/3/21")
    
    # Aggregate 
    keep_cols = ["aggregate_region", "population", "date", "date2"]
    aggregated = (df.groupby(keep_cols)
                  .agg({"cases": "sum", "deaths": "sum"})
                  .reset_index()
                 )    
    
    sort_cols = ["aggregate_region", "date", "date2"]
    group_cols = ["aggregate_region"]
    
    final = derive_columns(aggregated, sort_cols, group_cols)
    
    return final


def interpolate_linearly(df, start_date, end_date):
    """
    Interpolate and fill in missing data
    df: pandas.DataFrame
    start_date: inclusive, provide the date where there is case/death numbers,
                right before the set of missing values.
    end_date: inclusive, provide the date where there is case/death numbers, 
                right after the set of missing values.
                
    Ex: if 12/20 and 12/21 are missing, start_date is 12/19 and end_date is 12/22.
    """
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    days_in_between = (end_date - start_date).days - 1 

    # Now interpolate, but do it just around where the missing area is
    starting_df = df.loc[df.date2==start_date]
    ending_df = df.loc[df.date2 == end_date]
    
    sort_cols = ["Region", "date2"]
    group_cols = ["Region"]

    df2 = starting_df.copy()
    for i in range(1, days_in_between + 1):
        df2 = (df2.append(starting_df)
                        .reset_index(drop=True)
                       )

        df2["obs"] = df2.groupby(group_cols).cumcount() + 1

        df2 = df2.assign(
                date2 = df2.apply(lambda x: x.date2 + timedelta(days = i) if x.obs==i 
                                           else x.date2, axis=1),
                cases = df2.apply(lambda x: np.nan if x.obs==i else x.cases, axis=1),
                deaths = df2.apply(lambda x: np.nan if x.obs==i else x.deaths, axis=1),
        )
        df2["date"] = df2.date2.dt.date

        if i == days_in_between:  
            df2 = (df2.append(ending_df)
                   .sort_values(sort_cols)
                    .drop(columns = "obs")
                    .reset_index(drop=True)
                   )

    # Find our start / end points to calculate change
    for col in ["cases", "deaths"]:
        df2 = (df2.sort_values(sort_cols)
                    .assign(
                        start = df2.groupby(group_cols)[col].transform("min"),
                        change = (df2.groupby(group_cols)[col].transform("max") - 
                                  df2.groupby(group_cols)[col].transform("min")),
                )
            )

        df2 = (df2.assign(
                    daily_change = (df2.change / (days_in_between + 1))
                ).rename(columns = {"daily_change": f"change_{col}", 
                                   "start": f"start_{col}"})
            )
    
    df2 = df2.assign(
            days_since = df2.sort_values(sort_cols).groupby(group_cols).cumcount(),
        )
    
    for col in ["cases", "deaths"]:
        start_col = f"start_{col}"
        change_col = f"change_{col}"
        
        df2[col] = (df2[col].fillna(
                    df2[start_col] + (df2[change_col] * df2.days_since))
                 .astype(int)
                )

    # Append it back to original df
    full_df = (df[(df.date2 != start_date) & (df.date2 != end_date)]
               .append(df2.drop(
                   columns = ["days_since", "change", 
                              "start_cases", "start_deaths", 
                              "change_cases", "change_deaths"]), sort=False)
               .sort_values(sort_cols)
               .reset_index(drop=True)
              )

    return full_df


def derive_columns(df, sort_cols, group_cols):
    # Derive columns
    POP_DENOM = 100_000
    
    df = (df.assign(
            new_cases = (df.sort_values(sort_cols).groupby(group_cols)["cases"]
                         .diff(periods=1)
                        ),
            cases_per100k = df.cases / df.population * POP_DENOM,
        ).sort_values(sort_cols)
        .reset_index(drop=True)
    )
    
    df = df.assign(
        new_cases = df.new_cases.fillna(0)
    )
    
    # Calculate rolling averages
    df = (df.assign(
            cases_avg7 = df.cases.rolling(window=7).mean(),
            new_cases_avg7 = df.new_cases.rolling(window=7).mean(),
            cases_per100k_avg7 = df.cases_per100k.rolling(window=7).mean(),
        )   
    )
    
    # Calculate quartiles
    case_quartiles = (df.groupby("date")["cases_avg7"].describe()[["25%", "50%", "75%"]]
                 .rename(columns = {"25%": "cases_p25",
                                    "50%": "cases_p50",
                                    "75%" :"cases_p75"})
                 .reset_index()
                )
    
    normalized_case_quartiles = (df.groupby("date")["cases_per100k_avg7"].describe()[["25%", "50%", "75%"]]
                 .rename(columns = {"25%": "ncases_p25",
                                    "50%": "ncases_p50",
                                    "75%" :"ncases_p75"})
                 .reset_index()
                )
    
    
    df2 = pd.merge(df, case_quartiles, on = "date", how = "left", validate = "m:1")
    df3 = pd.merge(df2, normalized_case_quartiles, on = "date", how = "left", validate = "m:1")
    
    # Add rankings
    df3["rank"] = df3.groupby("date")["cases_per100k"].rank("dense", ascending=False).astype("Int64")
    df3["max_rank"] = df3.groupby("date")["rank"].transform("max").astype(int)
    
    return df3


def clean_testing_data():
    df = pd.read_parquet(NEIGHBORHOOD_APPENDED_URL)

    keep_cols = ["neighborhood", "persons_tested_final", 
                "persons_tested_pos_final", "date"]
    
    df = (df[keep_cols]
            .assign(
                date = df.date.dt.date,
                date2 = pd.to_datetime(df.date)
            )
        )
    
    def clean_up_city(row):
        if "City of " in row.neighborhood:
            return row.neighborhood.replace("City of", "")
        if "Los Angeles - " in row.neighborhood:
            return row.neighborhood.replace("Los Angeles - ", "")
        if "Unincorporated - " in row.neighborhood:
            return row.neighborhood.replace("Unincorporated - ", "")

    df["Region"] = df.apply(clean_up_city, axis=1).str.strip() 
    
    # For every Region, aggregate, so that these match how the historical data was parsed
    df = (df.assign(
            persons_tested = (df.groupby(["Region", "date"])["persons_tested_final"]
                            .transform("sum")),
            persons_tested_pos = (df.groupby(["Region", "date"])["persons_tested_pos_final"]
                                .transform("sum")),
        ).drop(columns = ["persons_tested_final", "persons_tested_pos_final"])
          .drop_duplicates()
    )
    
    # Merge in population crosswalk (cleaned up)
    crosswalk = pd.read_parquet(CROSSWALK_URL)

    df2 = pd.merge(df.drop(columns = "neighborhood"), crosswalk, 
                   on = "Region", how = "inner")
    
    # Aggregate to aggregate_region
    df3 = (df2.groupby(["region_num", "aggregate_region", "population", "date", "date2"])
       .agg({"persons_tested": "sum", "persons_tested_pos": "sum"})
       .reset_index()
      )
    
    POP_DENOM = 1_000
    
    df3 = (df3.assign(
            pct_positive = df3.persons_tested_pos / df3.persons_tested,
            positive_per1k = df3.persons_tested_pos / df3.population * POP_DENOM
        )
    )

    integrify_me = ["region_num", "population", "persons_tested", "persons_tested_pos"]

    df3[integrify_me] = df3[integrify_me].astype("Int64")
    
    df3 = df3.sort_values(["aggregate_region", "date"]).reset_index(drop=True)
    
    df3.to_parquet(f"{S3_FILE_PATH}la-county-neighborhood-testing-time-series.parquet")
    
    return df3