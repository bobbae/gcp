"""
Functions to create charts.
"""
import altair as alt
import altair_saver
import os
import pandas as pd
import utils
import default_parameters

from IPython.display import display, SVG

alt.renderers.enable('altair_saver', fmts=['svg'])

def show_svg(image_name):
    image_path = f"../notebooks/{image_name}.svg"
    altair_saver.save(image_name, image_path)
    display(SVG(filename = image_path))
    os.remove(image_path)

    
#---------------------------------------------------------------#
# Chart parameters
#---------------------------------------------------------------#
navy = "#0A4C6A"
maroon = "#F3324C"
green = "#32D486"
orange = "#FCA800"
blue = "#1696D2"
gray = "#797C7C"
purple = "#6B1F84"
orange = "#F7AE1D"
yellow = "#D0E700"

# These colors are used for the shading on cases/deaths
light_gray = "#EAEBEB"
navy_outline = "#052838"
blue_outline = "#1277A5"


title_font_size = 10
font_name = "Arial"
grid_opacity = 0.4
domain_opacity = 0.4
stroke_opacity = 0
time_unit = "monthdate"
chart_width = 300
chart_height = 200
bin_spacing = 100
fulldate_format = "%-m/%-d/%y"
monthdate_format = "%-m/%-d"

two_weeks_ago = default_parameters.two_weeks_ago


#---------------------------------------------------------------#
# Case Data (County, State, MSA, City of LA)
#---------------------------------------------------------------#
def setup_cases_deaths_chart(df, geog, name):
    # Define chart titles
    if geog == "county":
        chart_title = f"{name} County"
    if geog == "state":
        chart_title = f"{name}"
    if geog == "msa":
        chart_title = f"{name} MSA"
    # Add City of LA to this geog
    if geog == "lacity":
        chart_title = f"{name}"
    
    # Set up base charts
    base = (alt.Chart(
        df.drop(columns = "date"))
        .mark_line()
        .encode(
            x=alt.X("date2", 
                   title="date", axis=alt.Axis(format=fulldate_format))
        )
    )
    
    base_2weeks = (
        alt.Chart(df[df.date >= two_weeks_ago].drop(columns = "date"))
        .mark_line()
        .encode(
            x=alt.X("date2", 
                    title="date", axis=alt.Axis(format=fulldate_format))
        )
    )
    
    
    tier_base = (base.mark_line(strokeDash=[2,3], clip=True))
        
    # Make cases charts    
    cases_line = (
        base
        .encode(
            y=alt.Y("cases_avg7:Q", title="7-day avg"),
            color=alt.value(navy),
        )
    )
    
    cases_shaded = (
        base_2weeks
        .mark_area()
        .encode(
            y=alt.Y("cases_avg7:Q", title="7-day avg"),
            color=alt.value(light_gray)
        )
    )
    
    cases_extra_outline = (
        base_2weeks
        .mark_line()
        .encode(
            y=alt.Y("cases_avg7:Q", title="7-day avg"),
            color=alt.value(navy_outline)
        )
    )
    

    tier1_hline = (
        tier_base
        .encode(y=alt.Y("tier1_case_cutoff:Q"),
               color=alt.value(orange))
    )

    tier2_hline = (
        tier_base
        .encode(y=alt.Y("tier2_case_cutoff:Q"),
               color=alt.value(maroon))
    )
    
    tier3_hline = (
        tier_base
        .encode(y=alt.Y("tier3_case_cutoff:Q"),
               color=alt.value(purple))
    )


    cases_chart = (
        (cases_line + cases_shaded + cases_extra_outline + 
         tier1_hline + tier2_hline + tier3_hline)
        .properties(
              title=f"{chart_title}: New Cases", width=chart_width, height=chart_height
            )
        )
    
    
    # Make deaths chart
    deaths_line = (
        base
        .encode(
            y=alt.Y("deaths_avg7:Q", title="7-day avg"),
            color=alt.value(blue),
        )
    )

    deaths_shaded = (
        base_2weeks
        .mark_area()
        .encode(
            y=alt.Y("deaths_avg7:Q", title="7-day avg"),
            color=alt.value(light_gray)
        )
    )
    
    deaths_extra_outline = (
        base_2weeks
        .encode(
            y=alt.Y("deaths_avg7:Q", title="7-day avg"),
            color=alt.value(blue_outline)
        )
    )    
    

    deaths_chart = (
        (deaths_line + deaths_shaded + deaths_extra_outline)
              .properties(
                  title=f"{chart_title}: New Deaths", width=chart_width, height=chart_height
                )
        )    
    
    return cases_chart, deaths_chart


def make_cases_deaths_chart(df, geog, name):  
    cases_chart, deaths_chart = setup_cases_deaths_chart(df, geog, name)
    
    # Cases and deaths chart to display side-by-side
    combined_chart = (
        alt.hconcat(cases_chart, deaths_chart)
        .configure_title(
            fontSize=title_font_size, font=font_name, anchor="middle", color="black"
        )
        .configure_axis(gridOpacity=grid_opacity, domainOpacity=domain_opacity)
        .configure_view(strokeOpacity=stroke_opacity)
    )
        
    show_svg(combined_chart)

    
#---------------------------------------------------------------#
# Testing Data (LA County and City of LA)
#---------------------------------------------------------------#
def make_la_testing_chart(df, plot_col, chart_title, lower_bound, upper_bound):
    
    chart_width = 650
    
    bar = (
        alt.Chart(df)
        .mark_bar(color=navy)
        .encode(
            x=alt.X(
                "date2:T",
                title="date",
                axis=alt.Axis(format=fulldate_format),
            ),
            y=alt.Y(plot_col, title="# Tests"),
        )
    )

    line1 = (
        alt.Chart(pd.DataFrame({"y": [lower_bound]}))
        .mark_rule(color=maroon, strokeDash=[6, 3])
        .encode(y="y")
    )
    line2 = (
        alt.Chart(pd.DataFrame({"y": [upper_bound]}))
        .mark_rule(color=maroon, strokeDash=[6, 3])
        .encode(y="y")
    )

    testing_chart = (
        (bar + line1 + line2)
        .properties(title=chart_title, width=chart_width)
        .configure_title(
            fontSize=title_font_size, font=font_name, anchor="middle", color="black"
        )
        .configure_axis(
            gridOpacity=grid_opacity, domainOpacity=domain_opacity, ticks=False
        )
        .configure_view(strokeOpacity=stroke_opacity)
    )

    show_svg(testing_chart)   
 

    
#---------------------------------------------------------------#
# Share of Positive Tests by Week (LA County)
#---------------------------------------------------------------#
def make_la_positive_test_chart(df, positive_lower_bound, positive_upper_bound, 
                                testing_lower_bound, testing_upper_bound, 
                                chart_title1, chart_title2): 
    num_weeks = len(df.week2.unique())  
    chart_width = num_weeks * 10
    
    base = (alt.Chart(df)
            .mark_bar(binSpacing = bin_spacing)
            .encode(
                x=alt.X("week2", title="date", sort=None)
            )
    )
    
    positive_bar = (
        base
        .mark_bar(color = navy)
        .encode(
            y=alt.Y("pct_positive", title="Percent",
                axis=alt.Axis(format="%")
            ),
        )

    )
    
    positive_lower_line = (
        alt.Chart(pd.DataFrame({"y": [positive_lower_bound]}))
        .mark_rule(color=maroon, strokeDash=[6, 3])
        .encode(y="y")
    )  
    
    positive_upper_line = (
        alt.Chart(pd.DataFrame({"y": [positive_upper_bound]}))
        .mark_rule(color=maroon, strokeDash=[6, 3])
        .encode(y="y")
    ) 
    
    positive_chart = (
        (positive_bar + positive_lower_line + positive_upper_line)
            .properties(title=chart_title1, width = chart_width)
         )

    test_bar = (
        base
        .mark_bar(color = blue)
        .encode(
            y=alt.Y("weekly_tests", title="# Weekly Tests",),
        )
    )
    
    num_positive_bar  = (
        base
        .mark_bar(color = gray)
        .encode(
            y=alt.Y("weekly_cases", title="# Weekly Tests",),
        )
    )
    
    weekly_test_lower_line = (
        alt.Chart(pd.DataFrame({"y": [testing_lower_bound * 7]}))
        .mark_rule(color=maroon, strokeDash=[6, 3])
        .encode(y="y")
    )  
    
    weekly_test_upper_line = (
        alt.Chart(pd.DataFrame({"y": [testing_upper_bound * 7]}))
        .mark_rule(color=maroon, strokeDash=[6, 3])
        .encode(y="y")
    )
    
    
    test_chart = (
        (test_bar + num_positive_bar + weekly_test_lower_line + weekly_test_upper_line)
            .properties(title=chart_title2, width = chart_width)
         )
    
    
    combined_weekly_chart = (
        alt.hconcat(positive_chart, test_chart)
        .configure_title(
            fontSize=title_font_size, font=font_name, anchor="middle", color="black"
        )
        .configure_axis(gridOpacity=grid_opacity, domainOpacity=domain_opacity)
        .configure_view(strokeOpacity=stroke_opacity)
    )
        
    show_svg(combined_weekly_chart)
    
    
#---------------------------------------------------------------#
# Hospital Equipment Availability (LA County)
#---------------------------------------------------------------#
def make_lacounty_hospital_chart(df):
    chart_width = 350
    acute_color = green
    icu_color = navy
    ventilator_color = orange

    base = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(
                "date2:T",
                title="date",
                axis=alt.Axis(format=fulldate_format),
            ),
            y=alt.Y("pct_available_avg3", title="3-day avg", 
                    axis=alt.Axis(format="%")
            ),
            color=alt.Color(
                "equipment",
                scale=alt.Scale(
                    domain=["Acute Care Beds", "ICU Beds", "Ventilators"],
                    range=[acute_color, icu_color, ventilator_color],
                ),
            ),
        )
    )

    line1 = (
        alt.Chart(pd.DataFrame({"y": [0.3]}))
        .mark_rule(color=maroon, strokeDash=[6, 3])
        .encode(y="y")
    )

    hospital_pct_chart = (
        (base + line1)
        .properties(
            title="Percent of Available Hospital Equipment by Type",
            width=chart_width,
        )
        .configure_title(
            fontSize=title_font_size, font=font_name, anchor="middle", color="black"
        )
        .configure_axis(
            gridOpacity=grid_opacity, domainOpacity=domain_opacity, ticks=False
        )
        .configure_view(strokeOpacity=stroke_opacity)
    )

    hospital_num_chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(
                "date2:T",
                title="date",
                axis=alt.Axis(format=fulldate_format),
            ),
            y=alt.Y("n_available_avg3", title="3-day avg"),
            color=alt.Color(
                "equipment",
                scale=alt.Scale(
                    domain=["Acute Care Beds", "ICU Beds", "Ventilators"],
                    range=[acute_color, icu_color, ventilator_color],
                ),
            ),
        ).properties(
            title="Number of Available Hospital Equipment by Type", width=chart_width
        ).configure_title(
            fontSize=title_font_size, font=font_name, anchor="middle", color="black"
        ).configure_axis(
            gridOpacity=grid_opacity, domainOpacity=domain_opacity, ticks=False
        ).configure_view(strokeOpacity=stroke_opacity)
    )

    hospital_covid_chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(
                "date2:T",
                title="date",
                axis=alt.Axis(format=fulldate_format),
            ),
            y=alt.Y("n_covid_avg7", title="7-day avg"),
            color=alt.Color(
                "equipment",
                scale=alt.Scale(
                    domain=["Acute Care Beds", "ICU Beds", "Ventilators"],
                    range=[acute_color, icu_color, ventilator_color],
                ),
            ),
        ).properties(
            title="Number of COVID-Occupied / Under Investigation Equipment Use by Type",
            width=chart_width,
        )
        .configure_title(
            fontSize=title_font_size, font=font_name, anchor="middle", color="black"
        )
        .configure_axis(
            gridOpacity=grid_opacity, domainOpacity=domain_opacity, ticks=False
        )
        .configure_view(strokeOpacity=stroke_opacity)
    )

    show_svg(hospital_pct_chart) 
    show_svg(hospital_num_chart)
    show_svg(hospital_covid_chart)


#---------------------------------------------------------------#
# COVID Hospitalizations (CA data portal)
#---------------------------------------------------------------#
def setup_county_covid_hospital_chart(df, county_name):
    hospitalizations_color = green
    icu_color = navy
    
    covid_hospitalizations_chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(
                "date2:T",
                title="date",
                axis=alt.Axis(format=fulldate_format),
            ),
            y=alt.Y("num:Q", title="7-day avg"),
            color=alt.Color(
                "type",
                scale=alt.Scale(
                    domain=["All COVID-Hospitalized", "COVID-ICU"],
                    range=[hospitalizations_color, icu_color],
                ),
            )
        ).properties(
            title=f"{county_name} County: COVID Hospitalizations", 
            width=chart_width, height=chart_height
        )
    )
        
    return covid_hospitalizations_chart


def make_county_covid_hospital_chart(df, county_name):
    
    chart = setup_county_covid_hospital_chart(df, county_name)
    
    covid_hospitalizations_chart = (
        chart.configure_title(
            fontSize=title_font_size, font=font_name, anchor="middle", color="black"
        ).configure_axis(
            gridOpacity=grid_opacity, domainOpacity=domain_opacity, ticks=False
        ).configure_view(strokeOpacity=stroke_opacity)
    )
    
    show_svg(covid_hospitalizations_chart)
