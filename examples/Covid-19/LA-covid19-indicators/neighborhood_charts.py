"""
Functions to clean up neighborhood data
and feed into interactive charts
"""
import altair as alt
import pandas as pd

import default_parameters
import make_charts
import neighborhood_utils

from datetime import timedelta
from IPython.display import display_html, Markdown, HTML, Image

S3_FILE_PATH = "s3://public-health-dashboard/jhu_covid19/"

CROSSWALK_URL = f"{S3_FILE_PATH}la_neighborhoods_population_crosswalk.parquet"

yesterday_date = default_parameters.yesterday_date
two_days_ago = default_parameters.two_days_ago
two_weeks_ago = default_parameters.two_weeks_ago
one_week_ago = default_parameters.one_week_ago
one_month_ago = default_parameters.one_month_ago

# Chart parameters
title_font_size = 9
font_name = make_charts.font_name
grid_opacity = make_charts.grid_opacity
domain_opacity = make_charts.domain_opacity
stroke_opacity = make_charts.stroke_opacity
chart_width = make_charts.chart_width
chart_height = make_charts.chart_height
time_unit = make_charts.time_unit

fulldate_format = default_parameters.fulldate_format
monthdate_format = default_parameters.monthdate_format

navy = make_charts.blue
light_gray = make_charts.light_gray
gray = make_charts.gray


crosswalk = (pd.read_parquet(CROSSWALK_URL)
             [["aggregate_region", "neighborhood", "in_two_aggregate_regions"]]
            )
la_neighborhoods = sorted(list(crosswalk
                               [crosswalk.neighborhood.str.contains("Los Angeles - ")]
                        .aggregate_region.unique()
                       ))

unincorporated_neighborhoods = sorted(list(crosswalk
                               [crosswalk.neighborhood.str.contains("Unincorporated - ")]
                        .aggregate_region.unique()
                       ))

incorporated_neighborhoods = sorted(list(crosswalk
                                         [(~crosswalk.aggregate_region.isin(la_neighborhoods)) & 
                                          (~crosswalk.aggregate_region.isin(unincorporated_neighborhoods))]
                        .aggregate_region.unique()
                       ))


# Prepare neighborhood case data, testing data, and merge
def prep_data(start_date):
    df1 = neighborhood_utils.clean_data()

    df1 = (df1[(df1.date >= start_date) & (df1.aggregate_region != "Long Beach")]
          .sort_values(["aggregate_region", "date"])
          .reset_index(drop=True)
         )

    df2 = neighborhood_utils.clean_testing_data()

    df = pd.merge(df1, df2.drop(columns = "region_num"), 
                  on = ["aggregate_region", "population", "date", "date2"], 
                  how = "left", validate = "1:1")
    
    
    # Drop the neighborhoods where they don't have data anymore
    # Some have data in early months, and not reported anymore
    df = df.assign(
        max_date = df.groupby("aggregate_region")["date"].transform("max")
    )

    df = (df[df.max_date >= one_week_ago]
          .drop(columns = "max_date")
          .sort_values(["aggregate_region", "date"])
          .reset_index(drop=True)
         )
    
    def tag_groups(row):
        if row.aggregate_region in la_neighborhoods:
            return "City of LA"
        elif row.aggregate_region in unincorporated_neighborhoods:
            return "Unincorporated"
        elif row.aggregate_region in incorporated_neighborhoods:
            return "Incorporated"
    
    df = df.assign(
        group_name = df.apply(tag_groups, axis=1),
        aggregate_region = df.aggregate_region.str.replace("/", "-")
    )
    
    return df



def setup_chart(df, neighborhood, chart_type):
    if chart_type == "cases":
        plot_col = "cases_avg7"
        p25_col = "cases_p25"
        p75_col = "cases_p75"
        chart_title = f"{neighborhood}: Cases"
    
    if chart_type == "new_cases":
        plot_col = "new_cases_avg7"
        p25_col = ""
        p75_col = ""
        chart_title = f"{neighborhood}: New Cases"
    
    if chart_type == "normalized_cases":
        plot_col = "cases_per100k_avg7"
        chart_title = f"{neighborhood}: Cases per 100k"
        p25_col = "ncases_p25"
        p75_col = "ncases_p75"
        
    
    base = (
        alt.Chart(df.drop(columns = "date"))
        .encode(
            x=alt.X("date2:T", #timeUnit = time_unit,
                    title="date", axis=alt.Axis(format=fulldate_format)
                   )
        )
    )
    
    base_2weeks = (
        alt.Chart(df[df.date >= two_weeks_ago].drop(columns = "date"))
        .encode(
            x=alt.X("date2:T", #timeUnit = time_unit,
                    title="date", axis=alt.Axis(format=fulldate_format)
                   )
        )
    )
    
    # Make cases charts
    cases_line = (base
        .mark_line()
        .encode(
            y=alt.Y(plot_col, title="7-day avg"),
            color=alt.value(navy),
        )
    )
    
    cases_shaded = (base_2weeks
        .mark_area()
        .encode(
            y=alt.Y(plot_col, title="7-day avg"),
            color=alt.value(light_gray)
        )
    )
    
    ptile25_line = (base
        .mark_line()
        .encode(
            y=alt.Y(p25_col, title="7-day avg"),
            color=alt.value(gray),
        )
    )
    
    ptile75_line = (base
        .mark_line()
        .encode(
            y=alt.Y(p75_col, title="7-day avg"),
            color=alt.value(gray),
        )
    )
    
    if (chart_type == "cases") or (chart_type == "normalized_cases"):
        chart =  ((cases_shaded + cases_line + ptile25_line + ptile75_line)
                  .properties(title=chart_title, height=chart_height, width=chart_width)
                 )
                
    
    if chart_type == "new_cases":
        chart = ((cases_shaded + cases_line)
                .properties(title=chart_title, height=chart_height, width=chart_width)
                )
    
    return chart
    

def make_chart(df, neighborhood):
    
    subset_df = df[df.aggregate_region == neighborhood]
    
    cases_chart = setup_chart(subset_df, neighborhood, "cases")
    ncases_chart = setup_chart(subset_df, neighborhood, "normalized_cases")
    new_cases_chart = setup_chart(subset_df, neighborhood, "new_cases")
    
    combined_chart = (
        alt.hconcat(cases_chart, ncases_chart, new_cases_chart)
        .configure_title(
            fontSize=title_font_size, font=font_name, anchor="middle", color="black"
        )
        .configure_axis(gridOpacity=grid_opacity, domainOpacity=domain_opacity)
        .configure_view(strokeOpacity=stroke_opacity)
    )
    
    group_name = subset_df.group_name.iloc[0]
    
    display(Markdown(f"#### {neighborhood} ({group_name})"))
    summary_sentence(subset_df, neighborhood)

    make_charts.show_svg(combined_chart)
    
        
        
def summary_sentence(df, neighborhood):
    max_date = df.date.max()
    try:
        extract_col = "cases"
        cases_1month = df[df.date == one_month_ago][extract_col].iloc[0]
        cases_2weeks = df[df.date == two_weeks_ago][extract_col].iloc[0]
        cases_1week = df[df.date == one_week_ago][extract_col].iloc[0]
        cases_yesterday = df[df.date == max_date][extract_col].iloc[0]

        pct_positive_2days = (df[df.date == max_date]["pct_positive"].iloc[0] * 100).round(1)
        positive_per1k_2days = df[df.date == max_date]["positive_per1k"].iloc[0].round(2)

        extract_col2 = "cases_per100k"
        n_cases_1week = df[df.date == one_week_ago][extract_col2].iloc[0].round(2)
        # Sometimes cases for yesterday don't show, we'll have to use 2 days ago       
        n_cases_yesterday = df[df.date == max_date][extract_col2].iloc[0].round(2)

        ranking = df[df.date == max_date]["rank"].iloc[0].astype(int)
        max_rank = df[df.date == max_date]["max_rank"].iloc[0].astype(int)

        pct_change = (((n_cases_yesterday - n_cases_1week) / n_cases_1week) * 100).round(1)
        
        extract_col3 = "new_cases"
        new_cases_1week = cases_yesterday - cases_1week
        new_cases_yesterday = df[df.date == max_date][extract_col3].iloc[0]
    
        display(Markdown(
            f"Cumulative cases reported in {neighborhood}: "
            f"<br>1 month ago: {cases_1month:,};  2 weeks ago: {cases_2weeks:,}" 
            f"<br>1 week ago: {cases_1week:,};  yesterday: {cases_yesterday:,}"
            f"<br> New cases past week: {new_cases_1week:,}; new cases yesterday: {new_cases_yesterday:,}"
            f"<br>Percent change over past week: <strong>{pct_change}% </strong>"
            f"<br>Of those tested so far, {pct_positive_2days}% tested positive, with persons testing positive at a "
            f"rate of {positive_per1k_2days:,} per 1k. "
            f"<br>As of {max_date.strftime(fulldate_format)}, "
            f"{neighborhood} ranked <strong> {ranking} out of {max_rank} </strong> neighborhoods "
            "on cases per 100k <i>(1 being the most severely hit)</i>."
            )
        )   
        
    except AttributeError:
         display(Markdown(
            f"Cumulative cases reported in {neighborhood}:"
            f"<br>1 month ago: {cases_1month:,};  2 weeks ago: {cases_2weeks:,}" 
            f"<br>1 week ago: {cases_1week:,};  yesterday: {cases_yesterday:,}"
            f"<br> New cases past week: {new_cases_1week:,}; new cases yesterday: {new_cases_yesterday:,}"
            f"{neighborhood} has missing data; cases per 100k and rankings based on cases per 100k "
             "cannot be calculated. "
            )
        )
    except:
        pass