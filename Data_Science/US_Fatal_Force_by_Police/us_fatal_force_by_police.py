import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import os
from matplotlib.ticker import PercentFormatter
from collections import Counter
from census import Census
from us import states

# Create locators for ticks:
register_matplotlib_converters()

# Notebook Presentation:
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 125)
pd.set_option('display.width', None)

df_income = pd.read_csv('csv_files/Median_Household_Income_2015.csv', encoding="windows-1252")
df_poverty = pd.read_csv('csv_files/Pct_People_Below_Poverty_Level.csv', encoding="windows-1252")
df_high_school = pd.read_csv('csv_files/Pct_Over_25_Completed_High_School.csv', encoding="windows-1252")
df_race_shares = pd.read_csv('csv_files/Share_of_Race_By_City.csv', encoding="windows-1252")
df_fatalities = pd.read_csv('csv_files/Deaths_by_Police_US.csv', encoding="windows-1252")


def display_overview(df):
    print(f"Number of Rows (Entries): {df.shape[0]}")
    print(f"Number of Columns (Features): {df.shape[1]}")

    print("\nMissing and Duplicated Entries:")

    if df.isna().values.any():
        na_sum = df.isna().values.any().sum()
        print(f"The Amount of Entries with Missing Values: {na_sum}")
        df = df.dropna()
        print("These missing entries were removed.")
    else:
        print("There is no entry with missing values.")

    if df.duplicated().values.any():
        dup_sum = df.duplicated().values.any().sum()
        print(f"The Amount of Entries with Duplicated Values {dup_sum}")
        df = df.drop_duplicates()
        print("These duplicated entries were removed.")
    else:
        print("There is no entry with duplicated values.")

    print("\nOverview of the DataFrame:")
    print(df.info())

    print("\nRandom five Entries from the DataFrame:")
    print(df.sample(5))



print("\nFatality DataFrame")
display_overview(df_fatalities)

print("\nIncome DataFrame:")
display_overview(df_income)

print("\nPoverty DataFrame:")
display_overview(df_poverty)

print("\nHigh School Graduation DataFrame:")
display_overview(df_high_school)

print("\nRacial Demography DataFrame:")
display_overview(df_race_shares)


# Conversions:
# Fatality dataframe has a little bit differrent structure, we execute the conversions alone here:

# Date Conversion
df_fatalities["date"] = pd.to_datetime(df_fatalities["date"], format="mixed")

# Gender Conversions
# Defining the mapping:
gender_mapping = {"M": "Male", "F": "Female"}
# Applying the mapping
df_fatalities.gender = df_fatalities.gender.map(gender_mapping)


# Race Conversions
# Defining the mapping:
race_mapping = {
    "W": "White",
    "B": "Black",
    "H": "Hispanic",
    "A": "Asian",
    "N": "Native American",
    "O": "Other"
}
# Applying the mapping
df_fatalities.race = df_fatalities.race.map(race_mapping)

# State Conversions
# Sates are held on as abbreviations in the dataset, to get a clearer picture we are going to map them to full_names:
# Defining the mapping:
state_mapping = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

# Appliying the mapping and defining exact place for it:
df_fatalities["State_Full"] = df_fatalities["state"].map(state_mapping)
col = df_fatalities.pop("State_Full")
df_fatalities.insert(10, "State_Full", col)


# State Conversions for the dataframes
# The other 4 dataframes are from the same source thats why, they have the same structure.
def add_full_state(df):
    df.rename(columns={'Geographic Area': 'State'})
    df["State_Full"] = df["Geographic Area"].map(state_mapping)
    col = df.pop("State_Full")
    df.insert(1, "State_Full", col)

add_full_state(df_income)
add_full_state(df_poverty)
add_full_state(df_high_school)
add_full_state(df_race_shares)


# Numeric data conversions for the DataFrames
def convert_str_to_numeric(df, columns=None):
    if columns is None:
        columns = []
    for column in columns:
        df[column] = pd.to_numeric(df[column].str.replace(',', '', regex=False).replace('-', '0', regex=False), errors='coerce')


convert_str_to_numeric(df_income, ["Median Income"])
convert_str_to_numeric(df_poverty, ["poverty_rate"])
convert_str_to_numeric(df_high_school, ["percent_completed_hs"])
convert_str_to_numeric(df_race_shares, ["share_white", "share_black", "share_native_american", "share_asian", "share_hispanic"])




# Adding population to the dataframes:
# WE have just cities and rates for them. For taking average or correct values, we need to have populations of these cities.
# we are going to use cencus for this.

# Api_Key = os.getenv("API_KEY")

# # # Initializing census
# c = Census(Api_Key)
# #
# # Pulling Total Population (B01003_001E) and Name for all "places" (cities/towns) in 2015
# population_data = c.acs5.state_place(('NAME', 'B01003_001E'), Census.ALL, Census.ALL, year=2015)
#
# # Converting population data to a dataframe so that we can perform merging
# df_pop = pd.DataFrame(population_data)
# #
# def add_population(df):
#     # We will use "City name, State name" to retract exact populations (some prefixes are different)
#     # We need to remove the sufficex like " city", " CDP", " town", or " village" from the name of the city.
#     df['Clean_City'] = df['City'].str.replace(r' (city|CDP|town|village)$', '', regex=True)
#
#     # Split the API's 'NAME' column (e.g., "Abbeville city, Alabama") into two new columns
#     df_pop[['Raw_City', 'State_Full']] = df_pop['NAME'].str.split(', ', expand=True)
#
#     # again, we need to clean the city name:
#     df_pop['Clean_City'] = df_pop['Raw_City'].str.replace(r' (city|CDP|town|village)$', '', regex=True)
#
#     # Now perform the merge, we have identical combination at both dataframe
#     df = pd.merge(df, df_pop, on=['State_Full', 'Clean_City'], how='left')
#
#     # Column Arrangements: (many columns we dont need)
#     df = df.rename(columns={'B01003_001E': 'Population'})
#     df = df.drop(columns=['Clean_City', 'NAME', 'state', 'place', 'Raw_City' ])
#     return df

# df_poverty = add_population(df_poverty)
# df_high_school = add_population(df_high_school)
# df_race_shares = add_population(df_race_shares)
# df_income = add_population(df_income)


# Defining dataframes
dataframes = {
    "df_poverty" : df_poverty,
    "df_high_school": df_high_school,
    "df_race_shares" : df_race_shares,
    "df_income": df_income,
}


# # Writing and Retriveing the dataframes:
# for name, df in dataframes.items():
#     df.to_csv(f"csv_files/new_files/{name}.csv_files", index=False)
#     pd.read_csv(f"csv_files/new_files/{name}.csv_files", encoding="windows-1252")


# df_poverty = df_poverty.rename(columns={'Geographic Area': 'State'})
# df_high_school = df_high_school.rename(columns={'Geographic Area': 'State'})
# df_race_shares = df_race_shares.rename(columns={'Geographic Area': 'State'})
# df_income = df_income.rename(columns={'Geographic Area': 'State'})

# df_poverty.to_csv(f"csv_files/new_files/df_poverty.csv_files", index=False)
# df_high_school.to_csv(f"csv_files/new_files/df_high_school.csv_files", index=False)
# df_race_shares.to_csv(f"csv_files/new_files/df_race_shares.csv_files", index=False)
# df_income.to_csv(f"csv_files/new_files/df_income.csv_files", index=False)

df_poverty = pd.read_csv(f"csv_files/new_files/df_poverty.csv", encoding="windows-1252")
df_high_school = pd.read_csv(f"csv_files/new_files/df_high_school.csv", encoding="windows-1252")
df_race_shares = pd.read_csv(f"csv_files/new_files/df_race_shares.csv", encoding="windows-1252")
df_income = pd.read_csv(f"csv_files/new_files/df_income.csv", encoding="windows-1252")
df_state_pop = pd.read_csv(f"csv_files/new_files/df_state_population.csv", encoding="windows-1252")




# Population fix:

# Population values at the end of the calculations can be skewed because of a very common pitfall in geospatial data science:
# summing up city data does not equal state data.
# Here are the two specific reasons our methodology can be resulting in an undercount:
# The "Unincorporated Area" Trap
# In our Census API call, we used c.acs5.state_place.
# In Census terminology, a "place" usually refers to an incorporated city, town, village, or a Census Designated Place (CDP).
# But, some Americans live in unincorporated areas—rural regions or suburban sprawls that sit outside official city limits.
# Because these people don't technically live in a "place," they are completely excluded from the population_data variable we pulled.
# When we sum the cities, we are leaving out everyone who lives in the countryside.
# That's why we are going to create another dataframe for state population to add at the last step for our calculations.
# This will just because of the reliability and accuracy our data.
# For example would have median poverty rate for 2 million people in one state but city has 2,2 million population,
# then we are going to fix the population after we calculated this median poverty rate. (0.2 million people does not skew the value too much.)


# Writing all state-population:

# # Pulling Total Population (B01003_001E) for STATES instead of places
# state_population_data = c.acs5.state(('NAME', 'B01003_001E'), Census.ALL, year=2015)
#
# # Converting JSON to a Dataframe:
# df_state_pop = pd.DataFrame(state_population_data)
#
# # Renaming and Dropping same columns
# df_state_pop.drop(columns=['state'], inplace=True)
# df_state_pop = df_state_pop.rename(columns={'B01003_001E': 'total_state_population', 'NAME': 'State_Full'})
#
# # Saving and exporting the datafile:
# df_state_population = df_state_pop.to_csv(f"csv_files/csv_files/new_files/df_state_population.csv_files", index=False)



def fix_population(df):
    # You can now merge this directly with a dataframe of state abbreviations
    df.drop(columns=['total_state_population'], inplace=True)
    df = df.merge(df_state_pop, how='left', on='State_Full')
    col = df.pop("total_state_population")
    df.insert(2, "total_state_population", col)
    return df


# Reachist Cities:
df_income = df_income.sort_values("Median Income", ascending=False)
# Filtering small and unincorporated communities out:
wealthiest_cities = df_income.query("Population > 1000")
print(wealthiest_cities.head(10))




# Analysis for Poverty:
# Adding exact amount of people in poverty at every city:
df_poverty['people_in_poverty'] = ((df_poverty['poverty_rate'] / 100)
                                   * df_poverty['Population'])

# State-wise poverty data:
df_poverty_by_state = (df_poverty
                       .groupby(['State', 'State_Full'], as_index=False)
                       .agg(total_state_population=('Population', 'sum'),
                            total_state_poverty=('people_in_poverty', 'sum')))

# calculating of poverty rate for each state:
df_poverty_by_state['Poverty_Rate'] = (df_poverty_by_state['total_state_poverty'] / df_poverty_by_state['total_state_population']) * 100

# Round the number
df_poverty_by_state['Poverty_Rate'] = df_poverty_by_state['Poverty_Rate'].round(2)

# Sort by poverty rate:
df_poverty_by_state = df_poverty_by_state.sort_values('Poverty_Rate', ascending=False)

# Fixing population:
df_poverty_by_state = fix_population(df_poverty_by_state)

# Dropping the value for total number of people on poverty would be good, since we performed an improvement on exact population:
df_poverty_by_state = df_poverty_by_state.drop(columns=['total_state_poverty'])

# print("df_poverty_by_state :")
# print(df_poverty_by_state)


poverty_colorscale = [
    [0.00, "#F6F4D2"],
    [0.10, "#DCE8B2"],
    [0.22, "#A8D5A2"],
    [0.30, "#6DBFA6"],
    [0.40, "#4FA3A5"],
    [0.50, "#417D9C"],
    [0.70, "#465C9E"],
    [0.85, "#3F3C7A"],
    [1.00, "#24152E"]
]


fig = px.choropleth(
    df_poverty_by_state,
    locations='State',
    locationmode='USA-states',
    color='Poverty_Rate',
    scope="usa",
    color_continuous_scale=poverty_colorscale, # 'Teal' or 'Blues' offers a very corporate/elegant look
    custom_data=['State_Full', 'total_state_population', 'Poverty_Rate']
)


fig.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]} (%{location})</b><br>"
        "<span style='font-size:10px;'>────────────────────────</span><br>"
        "<b>Poverty Rate:</b> %{customdata[2]:.2f}%<br>"
        "<b>Total Population:</b> %{customdata[1]:,.0f}<br>"
        "<extra></extra>"
    ),
    marker_line_width=0.5,   # Thinner state borders
    marker_line_color='white' # Crisp white borders separate
)


fig.update_layout(
    title=dict(
        text='<b>Poverty Rates by US State</b>',
        font=dict(family="Arial, Helvetica, sans-serif", size=22, color="#333333"),
        x=0.5, y=0.95),
    geo=dict(
        bgcolor='rgba(0,0,0,0)',
        lakecolor='#E0EAF5',
        landcolor='#F4F4F4',
        showlakes=True,
        showcoastlines=False,     # Removes the harsh outline around the entire country
        projection_type='albers usa'
    ),
    coloraxis_colorbar=dict(
        title=dict(
            text="Poverty Rate (%)",
            font=dict(size=13, color="#555555")
        ),
        thicknessmode="pixels", thickness=12,
        lenmode="pixels", len=300,
        yanchor="middle", y=0.5,
        ticks="outside",
        ticksuffix="%",
        tickfont=dict(color="#555555")
    ),
    paper_bgcolor='white',
    margin=dict(l=0, r=0, t=60, b=10)
)

# fig.write_html("interactive_graphs/usa_poverty.html")

# fig.show()








# Analysis of High-school Completion
# Percentage of Adults (25+) with a High School Diploma:
# This measures the total adult population that has completed high school at some point in their lives,
# regardless of when or where they did it.


df_graduation_by_state = df_high_school.copy()

# Adding exact amount of people in poverty at every city:
df_graduation_by_state['people_completed_hs'] = (df_graduation_by_state['percent_completed_hs'] / 100) * df_graduation_by_state['Population']

# State-wise poverty data:
df_graduation_by_state = df_graduation_by_state.groupby(['State', 'State_Full'], as_index=False).agg(
    total_state_population=('Population', 'sum'),
    total_state_graduates=('people_completed_hs', 'sum')
)

# calculating of poverty rate for each state:
df_graduation_by_state['HS_Graduation_Rate'] = (df_graduation_by_state['total_state_graduates'] / df_graduation_by_state['total_state_population']) * 100

# Round the number
df_graduation_by_state['HS_Graduation_Rate'] = df_graduation_by_state['HS_Graduation_Rate'].round(2)

# Sort by poverty rate:
df_graduation_by_state = df_graduation_by_state.sort_values('HS_Graduation_Rate', ascending=False)

# Fixing population:
df_graduation_by_state = fix_population(df_graduation_by_state)

df_graduation_by_state = df_graduation_by_state.drop(columns=['total_state_graduates'])


# print("\States by High-school graduation rate:")
# print(df_graduation_by_state)

graduation_colorscale = [
    [0.00, '#9E5344'], [0.11, '#B25D4D'], [0.22, '#CE8456'], [0.33, '#E2AB67'],
    [0.44, '#EDD488'], [0.55, '#DCE0A6'],  [0.66, '#A9C68E'],[0.77, '#71AC7A'],
    [0.88, '#3A8F66'], [1.00, '#0F6B4C']
    ]

fig = px.choropleth(
    df_graduation_by_state,
    locations='State',
    locationmode='USA-states',
    color='HS_Graduation_Rate',
    scope="usa",
    color_continuous_scale=graduation_colorscale,
    custom_data=['State_Full', 'total_state_population', 'HS_Graduation_Rate']
)


fig.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]} (%{location})</b><br>"
        "<span style='font-size:10px;'>───────────────────────────────────────</span><br>"
        "<b>High-School Graduation Rate:</b> %{customdata[2]:.2f}%<br>"
        "<b>Total Population:</b> %{customdata[1]:,.0f}<br>"
        "<extra></extra>"
    ),
    marker_line_width=0.5,   # Thinner state borders
    marker_line_color='white', # Crisp white borders separate
    hoverlabel=dict(bgcolor="#1A6143", font_size=14, font_family="Arial", bordercolor="#F7F5EB")
)


fig.update_layout(
    title=dict(
        text='<b>Percentage of Adults (25+) with a High School Diploma by US State</b>',
        font=dict(family="Arial, Helvetica, sans-serif", size=22, color="#333333"),
        x=0.5, y=0.95),
    geo=dict(
        bgcolor='rgba(0,0,0,0)',
        lakecolor='#E0EAF5',
        landcolor='#F4F4F4',
        showlakes=True,
        showcoastlines=False,     # Removes the harsh outline around the entire country
        projection_type='albers usa'
    ),
    coloraxis_colorbar=dict(
        title=dict(
            text="Graduation Rate (%)",
            font=dict(size=13, color="#555555")
        ),
        thicknessmode="pixels", thickness=12,
        lenmode="pixels", len=300,
        yanchor="middle", y=0.5,
        ticks="outside",
        ticksuffix="%",
        tickfont=dict(color="#555555")
    ),
    paper_bgcolor='white',
    margin=dict(l=0, r=0, t=60, b=10)
)

# fig.write_html("interactive_graphs/usa_hs_graduation.html")

# fig.show()





# Analysis of poverty and high-school graduation rate:
# Visualizing the Relationship between Poverty Rates and High School Graduation Rates

# Now we are going to perform analysis between these two datasets, so it is better to merge them as we desire:
df_poverty_graduation = df_poverty_by_state.merge(df_graduation_by_state, how='left', on=['State', 'State_Full','total_state_population'])

print("\ndf_poverty_graduation:")
print(df_poverty_graduation)

# Creating the Plot:
fig = px.scatter(
    df_poverty_graduation,
    x='HS_Graduation_Rate',
    y='Poverty_Rate',
    hover_name='State_Full',
    custom_data=['total_state_population'],
    trendline='ols',           # Automatically plots the line of best fit
    trendline_color_override='crimson',
)

# Professional Styling and Hover Templates
fig.update_traces(
    marker=dict(
        size=17,
        color='#0A7C6E',
        opacity=0.6,
        line=dict(width=1, color='rgba(50, 50, 50, 0.8)') # Crisp, dark borders around dots
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "<span style='font-size:10px;'>────────────────────────</span><br>"
        "<b>Graduation Rate:</b> %{x:.1f}%<br>"
        "<b>Poverty Rate:</b> %{y:.1f}%<br>"
        "<b>State Population:</b> %{customdata[0]:,.0f}"
        "<extra></extra>"
    ),
    selector=dict(mode='markers')
)

trendline_trace = fig.data[1]
# Trendlines
trendline_trace.line.color = '#DC3545'
trendline_trace.line.dash = 'dash'
trendline_trace.line.width = 5


fig.update_layout(
    title=dict(
        text='<b>The Relationship Between High School Graduation and Poverty</b><br>'
             '<span style="font-size: 14px; color: gray;">Higher graduation rates strongly correlate with lower poverty rates across US States.</span>',
        font=dict(family="Arial, Helvetica, sans-serif", size=20, color="#333333"),
        x=0.05,
        y=0.95
    ),
    xaxis=dict(
        title=dict(
            text="<b>High School Graduation Rate</b>",
            font=dict(size=13, color="#E03F4F")
        ),
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        tickfont=dict(color="#555555"),
        ticksuffix="%"
    ),
    yaxis=dict(
        title=dict(
            text="<b>Poverty Rate </b>",
            font=dict(size=13, color="#E03F4F")
        ),
        showgrid=True,
        gridcolor='#E5E5E5',
        zeroline=False,
        tickfont=dict(color="#555555"),
        ticksuffix="%"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=100, b=60),
    hoverlabel=dict(
        bgcolor="white",
        font_size=13,
        font_family="Arial"
    )
)

# fig.write_html("interactive_graphs/relationship_poverty_graduation.html")

# fig.show()





# Analysis of Incomes:

df_income_by_state = df_income.copy()

# Adding exact amount of people in poverty at every city:
df_income_by_state['total_income'] = df_income_by_state['Median Income'] * df_income_by_state['Population']

# State-wise poverty data:
df_income_by_state = df_income_by_state.groupby(['State', 'State_Full'], as_index=False).agg(
    total_state_population=('Population', 'sum'),
    total_state_income=('total_income', 'sum')
)

# calculating of poverty rate for each state:
df_income_by_state['Median_Income'] = df_income_by_state['total_state_income'] / df_income_by_state['total_state_population']

# Round the number
df_income_by_state['Median_Income'] = df_income_by_state['Median_Income'].round(2)

# Sort by poverty rate:
df_income_by_state = df_income_by_state.sort_values('Median_Income', ascending=False)

# Fixing population:
df_income_by_state = fix_population(df_income_by_state)

df_income_by_state = df_income_by_state.drop(columns=['total_state_income'])


# print("\nStates by median incomes")
# print(df_income_by_state)



income_colorscale = [
    [0.00, "#7A1F2B"],
    [0.10, "#BA444F"],
    [0.22, "#EBB7B8"],
    [0.25, "#F3EFEC"],
    [0.28, "#C6DCCB"],
    [0.60, "#80AE8E"],
    [0.75, "#579772"],
    [0.90, "#1F5A3D"],
    [1.00, "#1A4A32"]
]

fig = px.choropleth(
    df_income_by_state,
    locations='State',
    locationmode='USA-states',
    color=np.log10(df_income_by_state['Median_Income']),
    scope="usa",
    color_continuous_scale=income_colorscale,
    custom_data=['State_Full', 'total_state_population', 'Median_Income']
)


fig.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]} (%{location})</b><br>"
        "<span style='font-size:10px;'>────────────────────────</span><br>"
        "<b>Median Income:</b> $%{customdata[2]:,.0f}<br>" # Added $, commas, and removed decimals
        "<b>Total Population:</b> %{customdata[1]:,.0f}<br>"
        "<extra></extra>"
    ),
    marker_line_width=0.7,
    marker_line_color='white',
    hoverlabel=dict(
        bgcolor="rgba(255,255,255,0.96)",
        bordercolor="rgba(0,0,0,0)",
        font_size=15,
        font_family="Source Sans Pro",
        font_color="#2B2B2B",
        align="left"
    )
)


fig.update_layout(
    title=dict(
        text='<b>Yearly Median Income by US State</b><br>'
             '<span style="font-size: 14px; color: gray;">Geographic distribution of well-estimated median household earnings in 2015.</span>',
        font=dict(family="Arial, Helvetica, sans-serif", size=20, color="#333333"),
        x=0.05, y=0.95
    ),
    geo=dict(
        bgcolor='rgba(0,0,0,0)',
        lakecolor='#FFFFFF',
        landcolor='#F4F4F4',
        showlakes=True,
        showcoastlines=False,
        projection_type='albers usa'
    ),
    coloraxis_showscale=False,
    paper_bgcolor='white',
    margin=dict(l=0, r=0, t=80, b=0) # Tight margins so the map fills the vertical space
)

# fig.write_html("interactive_graphs/median_income_by_state.html")

# fig.show()


# Median incomes and racial demographics were engineered by calculating a population-weighted average of city-level data.
# While the Census provides true state medians, this approach was chosen to demonstrate advanced data manipulation,
# merging, and aggregation techniques in Pandas."








# Analysis for Race Distribution Among States
# Visualizing the share of the white, black, hispanic, asian and native american population in each US State

df_race = df_race_shares.copy()

# Defining the columns
race_cols = ['share_white', 'share_black', 'share_native_american', 'share_asian', 'share_hispanic']

# Multiplying shares by the population (vectorized weight calculation)
df_race[race_cols] = df_race[race_cols].multiply(df_race['Population'], axis="index")

# Grouping by state and sum everything up
df_race_by_state = df_race.groupby(['State', 'State_Full'], as_index=False)[race_cols + ['Population']].sum()

# Dividing by the new total state population to convert back to true percentages
df_race_by_state[race_cols] = df_race_by_state[race_cols].divide(df_race_by_state['Population'], axis="index")

# Renaming the population columns
df_race_by_state = df_race_by_state.rename(columns={'Population': 'total_state_population'})

df_race_by_state[race_cols] = df_race_by_state[race_cols].round(2)


# In the U.S. Census (and the Washington Post dataset), sometimes hispanic people were also identified as both "White" AND "Hispanic".
# Because these groups overlap, the total sum of the race distributions sums to more than 100.
# We are going to extract hispanic people from "white" people category to come up with a clearer picture.

# Defining new share_white values:
# By this way, the people in "white" category will only be in that category.
df_race_by_state.share_white = 100.00 - (df_race_by_state.share_black + df_race_by_state.share_native_american + df_race_by_state.share_asian + df_race_by_state.share_hispanic)

# Fixing total state population:
df_race_by_state = fix_population(df_race_by_state)

# Sort by poverty rate:
df_race_by_state = df_race_by_state.sort_values('share_white', ascending=False)


# print("\nStates by Races:")
# print(df_race_by_state)


race_labels = {
    'share_white': 'White',
    'share_black': 'Black',
    'share_hispanic': 'Hispanic',
    'share_asian': 'Asian',
    'share_native_american': 'Native American'
}

race_colors = {
    'share_white': '#1A5F7A',
    'share_hispanic': '#F3A712',
    'share_black': '#D9534F',
    'share_asian': '#5CB85C',
    'share_native_american': '#8E6CBE'
}


r_bar = px.bar(
    df_race_by_state,
    x='State_Full',
    y=race_cols,
    barmode='stack',
    color_discrete_map=race_colors,
    custom_data=['total_state_population'],
    labels={"value": "Percentage (%)", "variable": "Demographic", "State_Full": "State"}
)


r_bar.for_each_trace(lambda t: t.update(
    name=race_labels.get(t.name, t.name),
    hovertemplate="<b>%{x}</b><br>%{data.name}: %{y:.1f}%<br><br>"
                  "<span>State Population:</b> %{customdata[0]:,.0f}<br>"
                  "<extra></extra>"
))


# Layout Formatting
r_bar.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text='<b>Racial and Ethnic Composition by State</b><br>'
             '<span style="font-size: 14px; color: gray;">Breakdown of demographic shares across major US states.</span>',
        font=dict(family="Arial, sans-serif", size=24, color='#2E2E2E'),
        x=0.053,
        y=0.91
    ),
    xaxis=dict(title="", tickfont=dict(size=12, color='#555555'), showgrid=False),
    yaxis=dict(
        title=dict(
            text="<b>Percentage (%)</b>",
            font=dict(size=13, color='#555555'),
            standoff=20  # Keeps the title a little bit pushed away from the numbers
        ),
        tickfont=dict(size=12, color='#555555'),
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False,
        ticks="outside",  # Adding padding to y axis
        ticklen=5,
        tickcolor="white"
    ),
    legend=dict(
        title="",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=12, color='#555555')
    ),
    margin=dict(t=110, l=80, r=40, b=50)
)


# r_bar.write_html("interactive_graphs/race_distribution_by_state.html")

# r_bar.show()




# Analysis of racial distribution of the fatlieites that killed by police:

df_fatalities_race_dist = df_fatalities.groupby(['race'], as_index=False).agg(Total_Death=('id', 'count'))

# USA race Distribution in 2015:
pop_mapping = {
    'White': 61.5,
    'Black': 12.5,
    'Hispanic': 17.6,
    'Asian': 5.3,
    'Native American': 1.0,
    'Other': 2.1
}

df_fatalities_race_dist['US_Pop_Pct'] = df_fatalities_race_dist['race'].map(pop_mapping)

# print("\ndf_fatalities_race_dist:")
# print(df_fatalities_race_dist)

custom_colors = {
    'White': '#2A3F54',
    'Black': '#1ABB9C',
    'Hispanic': '#E74C3C',
    'Asian': '#F39C12',
    'Native American': '#9B59B6',
    'Other': '#95A5A6'
}


fig = px.pie(
    df_fatalities_race_dist,
    values='Total_Death',
    names='race',
    hole=0.4,
    color='race',
    color_discrete_map=custom_colors,
    custom_data=['US_Pop_Pct']
)

# Hover template
fig.update_traces(
    textposition='outside',
    textinfo='percent+label',
    textfont=dict(size=13, color='#555555'),
    marker=dict(line=dict(color='white', width=2)),
    pull=[0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
    hovertemplate=(
        "<b>%{label}</b><br>"
        "<span style='font-size:10px;'>────────────────────</span><br>"
        "<b>Fatalities:</b> %{value:,.0f}<br>"
        "<b>Share of Fatalities:</b> %{percent:.1%}<br>"
        "<span style='font-size:10px;'>────────────────────</span><br>"
        "<b>US Population Share: </b> %{customdata[0][0]}%<br>"
        "<extra></extra>"
    )
)

# Layout Formatting
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text="<b>Proportion of Individuals Killed by Police by Race</b><br>"
             "<span style='font-size: 13px; color: gray;'>Comparing total fatalities alongside 2015 baseline US demographics.</span>",
        font=dict(size=18, color='#333333'),
        x=0.05, y=0.95
    ),
    showlegend=False,
    margin=dict(t=100, b=40, l=40, r=40)
)

# fig.write_html("interactive_graphs/fatalities_by_race.html")

# fig.show()









# Analysis of Sex of the fatalities:
# we are going to create a Chart Comparing the Total Number of Deaths of Men and Women
# we are going to use df_fatalities to illustrate how many more men are killed compared to women.

df_fatalities_sex = df_fatalities.groupby('gender', as_index=False).agg(Total_Death=('id', 'count'))

# USA race Distribution in 2015:
gender_mapping = {'Female': 51.1, 'Male': 48.9}

df_fatalities_sex['US_Gender_Pct'] = df_fatalities_sex['gender'].map(gender_mapping)

gender_colors = {'Female': '#D14D72', 'Male': '#355C7D'}

fig = px.pie(
    df_fatalities_sex,
    values='Total_Death',
    names='gender',
    hole=0.4,
    color='gender',
    color_discrete_map=gender_colors,
    custom_data=['US_Gender_Pct']
)

# Hover template
fig.update_traces(
    textposition='outside',
    textinfo='percent+label',
    textfont=dict(size=13, color='#555555'),
    marker=dict(line=dict(color='white', width=2)),
    pull=[0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
    hovertemplate=(
        "<b>%{label}</b><br>"
        "<span style='font-size:10px;'>────────────</span><br>"
        "<b>Fatalities:</b> %{value:,.0f}<br>"
        "<b>Share of Fatalities:</b> %{percent:.1%}<br>"
        "<span style='font-size:10px;'>───────────────────────</span><br>"
        "<b>US Population Share: </b> %{customdata[0][0]}%<br>"
        "<extra></extra>"
    )
)

# Layout Formatting
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text="<b>Sex Distribution of Individuals Killed by Police by Race</b><br>"
             "<span style='font-size: 13px; color: gray;'>Comparing total fatalities alongside 2015 baseline US demographics.</span>",
        font=dict(size=22, color='#333333'),
        x=0.05, y=0.95
    ),
    showlegend=False,
    margin=dict(t=100, b=40, l=40, r=40)
)

# fig.write_html("interactive_graphs/fatalities_by_sex.html")

# fig.show()







# Analysis of number of fatalities by gender by race

# We won't include the entries with no race data:
df_fatalities_filtered = df_fatalities.query("race != 'Other'")

# Counting by gender and by race:
df_fatalities_by_gender_race = df_fatalities_filtered.groupby(['race', 'gender'], as_index=False).agg(Total_Death=('id', 'count'))

# Sorting by total number of individiuals
df_fatalities_by_gender_race = df_fatalities_by_gender_race.sort_values('Total_Death', ascending=False)


fig = px.bar(
    df_fatalities_by_gender_race,
    x='race',
    y='Total_Death',
    color='gender',
    barmode='group', # bars side by side
    text='Total_Death',
    color_discrete_map=gender_colors,
    category_orders={'Race': df_fatalities_by_gender_race} # Orders the X-axis by largest total demographic
)

# desigining the graph
fig.update_traces(
    textposition='outside', # Pushes the labels above the bars
    textfont=dict(size=12, color='#333333'),
    marker_line_width=0,    # no borders from bars
    hovertemplate=(
        "<b>%{x} (%{data.name})</b><br>"
        "<b>Individuals:</b> %{y}<br>"
        "<extra></extra>"
    )
)


fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text='<b>Fatalities by Race and Gender</b><br>'
             '<span style="font-size: 14px; color: gray;">Male fatalities drastically outnumber female fatalities across all demographic groups.</span>',
        font=dict(family="Arial, sans-serif", size=20, color='#333333'),
        x=0.05,
        y=0.93
    ),
    xaxis=dict(
        title="",
        tickfont=dict(size=12, color='#555555'),
        showgrid=False
    ),
    yaxis=dict(
        title=dict(
            text="<b>Number of Individuals</b>",
            font=dict(size=15, color='#555555'),
            standoff=20
        ),
        tickfont=dict(size=12, color='#555555'),
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False,
        range=[0, 1300]
    ),
    legend=dict(
        title="",
        orientation="h",
        yanchor="bottom",
        y=0.95,
        xanchor="right",
        x=1,
        font=dict(size=13, color='#555555')
    ),
    margin=dict(t=120, l=80, r=40, b=50)
)

# fig.write_html("interactive_graphs/deaths_by_race_and_gender.html")

# fig.show()






# Analysis for the Age of the Fatalities
df_age_distribution = df_fatalities.groupby('age', as_index=False).agg(Total_Fatality=('id', 'count'))

df_age_distribution = df_age_distribution.sort_values("Total_Fatality", ascending=False)

# print("\ndf_age_distribution:")
# print(df_age_distribution[:40])
# print(df_age_distribution[40:])


sns.set_theme(style="white", context="notebook")
plt.figure(figsize=(12, 6), dpi=300)

ax = sns.histplot(
    data=df_fatalities,
    x='age',
    bins=73,
    color="#3465a4",
    edgecolor="white",
    linewidth=1.5,
    alpha=0.9
)

plt.title('Age distribution of the Suspects who killed by police',
          fontsize=22, pad=20, fontweight='bold', color='#F05454')
plt.xlabel('Age', fontsize=15, labelpad=15, fontweight='bold', color='#F05454')
plt.ylabel('Number of Individuals', fontsize=15,fontweight='bold', labelpad=15, color='#F05454')

ax.grid(axis='y', color='#dddddd', linestyle='--', alpha=0.8)
ax.tick_params(axis='both', which='major', labelsize=13, colors='#555555', length=0)
ax.set_axisbelow(True)

sns.despine(left=True, bottom=False)
plt.tight_layout()

# plt.show()
# plt.close()




# Getting the Children under 15 killed by police in the USA:

# Filtering for under 15 and sorting ascendingly by age:
fatalities_under_15 = df_fatalities.query('age <= 15')
fatalities_under_15 = fatalities_under_15.sort_values("age", ascending=True)

# Since there are too many features here, we need to plot what features we would like to see here:
display_columns = ['name','date','manner_of_death','armed','age', 'gender', 'race', 'State_Full']

# print(fatalities_under_15[display_columns])






# Analysis of age distribution by Race

fig = px.box(
    df_fatalities_filtered,
    x="race",
    y="age",
    color="race",
    title='Age Distribution of Fatalities by Race',
    labels={"race": "Race", "age": "Age at Time of Death"},
    color_discrete_sequence=px.colors.qualitative.Bold,
    template="plotly_white"
)

fig.update_layout(
    font_family="Inter, Helvetica, Arial, sans-serif",
    title_font_size=24, title_font_color="#008695", title_font_family="Arial Black",
    title_x=0.5, # Center the title
    showlegend=False, # No need to show legend
    xaxis=dict(showgrid=False, zeroline=False, title_font_size=18, tickfont=dict(size=14), title_font_color="#008695"),
    yaxis=dict(showgrid=True, gridcolor='#E5E7EB', zeroline=False, title_font_size=18, title_font_color="#008695"),
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=80, b=40, l=40, r=40)
)

# Polish the boxes themselves (line width and outlier styling)
fig.update_traces(
    marker=dict(size=6, opacity=1, line=dict(width=1, color='DarkSlateGrey')),
    line=dict(width=1.5)
)

# fig.write_html("interactive_graphs/age_distribution_by_race.html")

# fig.show()









# Analysis of wether the fatalities armed or not
# In what percentage of police killings were people armed?
# How many of the people killed by police were armed with guns versus unarmed?

df_killed_armed = df_fatalities.copy()

# Filtering the dataframe and creating new through an existing column
df_killed_armed['armed_or_not'] = np.where(df_killed_armed.armed == 'unarmed', 'no', 'yes')

# Grouping and counting
df_killed_armed_or_not = df_killed_armed.groupby('armed_or_not', as_index=False).agg(Total_Death=('id', 'count'))

armed_colors = {'no': '#F0E9B6', 'yes': '#4B2E2B'}

fig = px.pie(
    df_killed_armed_or_not,
    values='Total_Death',
    names=['Not Armed', 'Armed'],
    hole=0.4,
    color='armed_or_not',
    color_discrete_map=armed_colors,
)

# Hover template
fig.update_traces(
    textposition='outside',
    textinfo='percent+label',
    textfont=dict(size=15, color='#555555'),
    marker=dict(line=dict(color='white', width=2)),
    pull=[0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
    hovertemplate=(
        "<b>%{label}</b><br>"
        "<span style='font-size:10px;'>────────────</span><br>"
        "<b>Fatalities:</b> %{value:,.0f}<br>"
        "<b>Share of Fatalities:</b> %{percent:.1%}<br>"
        "<extra></extra>"
    )
)

# Layout Formatting
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text="<b>Were the Fatalities Armed ?</b><br>"
             "<span style='font-size: 13px; color: gray;'>Comparison of the total number of deaths with the U.S. baseline from 2015.</span>",
        font=dict(size=22, color='#333333'),
        x=0.05, y=0.95
    ),
    showlegend=False,
    margin=dict(t=100, b=40, l=40, r=40)
)

# fig.write_html("interactive_graphs/distribution_of_fatalities_by_arming.html")

# fig.show()






# Analysis of the type of arms which are possessed by fatalities

# Filtering for the armed
df_killed_arm_type = df_killed_armed[df_killed_armed['armed'] != 'unarmed']

# Renaming the column
df_killed_arm_type = df_killed_arm_type.rename(columns={'armed': 'Arm_Type'})

# Grouping by arm type to get their total numbers and percentages:
df_killed_arm_type = (
    df_killed_arm_type
    .groupby('Arm_Type', as_index=False)
    .agg(Total_Individuals=('id', 'count'))
    .assign(
        Arm_Share=lambda x: x['Total_Individuals'] / x['Total_Individuals'].sum() * 100
    ))

# Only more than 2 (otherwise there are too many options)
df_killed_arm_type = df_killed_arm_type.query("Total_Individuals > 2")

df_killed_arm_type = df_killed_arm_type.sort_values("Total_Individuals", ascending=False)

# print("df_killed_arm_type:")
# print(df_killed_arm_type)

arm_bar = px.bar(
    df_killed_arm_type,
    x='Total_Individuals',
    y='Arm_Type',
    orientation='h',
    custom_data=['Arm_Share'],
    text='Total_Individuals',
    color=np.log10(df_killed_arm_type['Total_Individuals']),
    color_continuous_scale='Matter',
)

arm_bar.update_traces(
    # marker_color='#2A3F54',
    marker_line_width=0,
    textposition='outside',
    texttemplate='%{x:,.0f}',
    textfont=dict(size=12, color='#333333'),
    cliponaxis=False,
    hovertemplate=(
        "<b>%{y}</b><br>"
        "<span style='font-size:10px;'>────────────────────</span><br>"
        "<b>Total Individuals:</b> %{x:,.0f}<br>"
        "<b>Share of Total:</b> %{customdata[0]:.1f}%<br>" 
        "<extra></extra>"
    )
)

arm_bar.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text='<b>Weapons Possessed by Fatalities in Police Encounters</b><br>'
             '<span style="font-size: 14px; color: gray;">Note: The X-axis is displayed on a logarithmic scale.</span>',
        font=dict(family="Arial, sans-serif", size=20, color='#9f2561'),
        x=0.115, y=0.95
    ),
    xaxis=dict(
        title=dict(
            text="<b>Number of Individuals (Log Scale)</b>",
            font=dict(size=13, color='#555555'),
            standoff=15
        ),
        type='log',
        # customized x-axis labels:
        tickvals=[3, 5, 10, 20, 50, 100, 200, 500, 1000],
        ticktext=['3', '5', '10', '20', '50', '100', '200', '500', '1,000'],
        tickfont=dict(size=12, color='#555555'),
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False
    ),
    yaxis=dict(
        title="",
        categoryorder='total ascending',
        tickfont=dict(size=13, color='#333333'),
        showgrid=False,
        zeroline=False,
        # Y-axis Padding:
        ticks="outside", ticklen=4, tickcolor="white"
    ),
    margin=dict(t=100, l=120, r=60, b=60),
    coloraxis_showscale=False,
)


# arm_bar.write_html("interactive_graphs/distribution_of_weapons_by_fatalities.html")

# fig.show()







# Analysis of Mental Illness in Police Killings
# What percentage of people killed by police have been diagnosed with a mental illness?


df_killed_mental_illness = df_killed_armed.groupby('signs_of_mental_illness', as_index=False).agg(Total_Death=('id', 'count'))

mentally_ill = {False: '#35858E', True: '#E03F4F'}

fig = px.pie(
    df_killed_mental_illness,
    values='Total_Death',
    names=['Not Mentally ill', 'Mentally ill'],
    hole=0.4,
    color='signs_of_mental_illness',
    color_discrete_map=mentally_ill,
)

# Hover template
fig.update_traces(
    textposition='outside',
    textinfo='percent+label',
    textfont=dict(size=15, color='#555555'),
    marker=dict(line=dict(color='white', width=2)),
    pull=[0.02, 0.02, 0.02, 0.02, 0.02, 0.02],
    hovertemplate=(
        "<b>%{label}</b><br>"
        "<span style='font-size:10px;'>────────────</span><br>"
        "<b>Fatalities:</b> %{value:,.0f}<br>"
        "<b>Share of Fatalities:</b> %{percent:.1%}<br>"
        "<extra></extra>"
    )
)

# Layout Formatting
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text="<b>Percentage of People Killed by Police with Mental Illness</b><br>",
        font=dict(size=22, color='#333333'),
        x=0.5, y=0.95
    ),
    showlegend=False,
    margin=dict(t=100, b=40, l=40, r=40)
)

# fig.write_html("interactive_graphs/distribution_of_fatalities_by_mentality.html")

# fig.show()






# Analysis of the Cities
# In Which Cities Do the Most Police Killings Take Place?
# Which cities are the most dangerous?

df_top_cities = df_fatalities.copy()

# Remove the entries wih undefined race:
df_top_cities = df_top_cities.query("race != 'Other'")

# Gather NYC boroughs
nyc_boroughs = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'New York']
df_top_cities['city'] = df_top_cities['city'].replace(nyc_boroughs, 'New York City')

# Group by city and count total killings
df_city_counts = df_top_cities.groupby('city').size().reset_index(name='total_killings')

# Get top 20 cities with most killings
top_cities = df_city_counts.sort_values(by='total_killings', ascending=False).head(20)['city']

# Filter original data for only those top 20 cities
df_top_cities = df_top_cities[df_top_cities['city'].isin(top_cities)]

# Group by city and race for visualization
df_top_cities = df_top_cities.groupby(['city','State_Full', 'race']).size().reset_index(name='killings')

# Calculate total Deaths by City:
df_top_cities['city_total'] = df_top_cities.groupby('city')['killings'].transform('sum')

# Now we calculate the percentage of that specific race within that specific city
df_top_cities['city_race_pct'] = (df_top_cities['killings'] / df_top_cities['city_total']) * 100

# df_top_cities = df_top_cities.sort_values("city_total", ascending=False)

# print("df_top_cities")
# print(df_top_cities[:40])
# print(df_top_cities[40:])

race_colors = {
    'White': '#2A3F54',
    'Black': '#1ABB9C',
    'Hispanic': '#E74C3C',
    'Asian': '#F39C12',
    'Native American': '#9B59B6'
}


fig = px.bar(
    df_top_cities,
    x='killings',
    y='city',
    orientation='h',
    color='race',
    color_discrete_map=race_colors,
    # Passing the calculated hover data:
    custom_data=['State_Full', 'killings', 'city_race_pct']
)


fig.update_traces(
    marker_line_width=0,
    hovertemplate=(
        "<b>%{y}, %{customdata[0]}</b><br>"
        "<span style='font-size:10px;'>────────────────────</span><br>"
        "<b>Demographic:</b> %{data.name}<br>"
        "<b>Individuals:</b> %{customdata[1]}<br>"
        "<b>Share of City Total:</b> %{customdata[2]:.1f}%<br>"
        "<extra></extra>"
    ),
    hoverlabel=dict(font_size=15)
)


fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text='<b>Top Cities by Police Fatalities</b><br>'
             '<span style="font-size: 14px; color: gray;">Demographic breakdown of individuals within the most affected cities.</span>',
        font=dict(family="Arial, sans-serif", size=20, color='#333333'),
        x=0.05,
        y=0.95
    ),
    xaxis=dict(title=dict(text="<b>Number of Individuals</b>", font=dict(size=13, color='#555555'), standoff=15),
        tickfont=dict(size=12, color='#555555'),
        showgrid=True,
        gridcolor='#EAEAEA', # Vertical subtle grids
        zeroline=False,
        # Padding:
        ticks = "outside", ticklen = 8, tickcolor = "white"
    ),
    yaxis=dict(
        title="",
        categoryorder='total ascending',
        tickfont=dict(size=12, color='#333333'),
        showgrid=False,
        # Padding:
        ticks="outside", ticklen=6, tickcolor="white"
    ),
    legend=dict(
        title="",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=12, color='#555555')
    ),
    margin=dict(t=110, l=120, r=40, b=60), # Extra left margin for long city names
    height=700 # Gives the 20 cities enough vertical room to breathe
)

# fig.write_html("interactive_graphs/most_dangerous_cities.html")

# fig.show()






# Analysis of Dangerous states
# Which states are the most dangerous?
# Are these the same states with high degrees of poverty?

df_fatalities_by_state = df_fatalities.copy()

df_fatalities_by_state = df_fatalities_by_state.groupby(['state', 'State_Full']).size().reset_index(name='killings')

df_fatalities_by_state = df_fatalities_by_state.merge(df_state_pop, on='State_Full', how='left')

# Calculating of the State's Share
total_us_fatalities = df_fatalities_by_state['killings'].sum()

df_fatalities_by_state['killing_by_police_usa_share_pct'] = (df_fatalities_by_state['killings'] / total_us_fatalities) * 100


print("df_fatalities_by_state:")
print(df_fatalities_by_state)

fatality_colorscale = [
    [0.00, "#F6E3B4"],   # pale sand
    [0.08, "#EFBA6B"],
    [0.18, "#E57827"],
    [0.32, "#B73123"],
    [0.40, "#BF2F4E"],
    [0.50, "#AB1D56"],
    [0.60, "#7B0F45"],
    [0.70, "#5C0B3A"],
    [0.80, "#870B26"],
    [1.00, "#240014"]    # almost black plum
]

world_map = px.choropleth(
    df_fatalities_by_state,
    locations='state',
    locationmode='USA-states',
    color='killings',
    # color=np.log10(df_fatalities_by_state['killings']),
    scope="usa",
    color_continuous_scale=fatality_colorscale,
    custom_data=['State_Full', 'killings', 'total_state_population', 'killing_by_police_usa_share_pct']
)

world_map.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "<span style='font-size:10px;'>────────────────────────</span><br>"
        "<b>Individuals:</b> %{customdata[1]:,.0f}<br>"
        "<b>Share of US Total:</b> %{customdata[3]:.1f}%<br>"
        "<b>State Population:</b> %{customdata[2]:,.0f}<br>"
        "<extra></extra>"
    ),
    marker_line_width=0.5,
    marker_line_color='white',
    hoverlabel=dict(bgcolor="#831e70", font_size=13),
)


world_map.update_layout(
    title=dict(
        text='<b>Police Fatalities by US State</b><br>'
             '<span style="font-size: 14px; color: gray;">Total individuals per state and their share of the national total.</span>',
        font=dict(family="Arial, sans-serif", size=22, color='#831e70'),
        x=0.05,
        y=0.95
    ),
    geo=dict(
        bgcolor='rgba(0,0,0,0)',
        lakecolor='#FFFFFF',
        landcolor='#F4F4F4',
        showlakes=True,
        showcoastlines=False,
        projection_type='albers usa'
    ),
    coloraxis_colorbar=dict(
        title=dict(text="<b>Total Fatalities</b>", font=dict(size=12, color="#555555")),
        thicknessmode="pixels", thickness=10,
        lenmode="pixels", len=250,
        yanchor="middle", y=0.5,
        xanchor="left", x=1.02,
        ticks="outside",
        tickfont=dict(color="#555555")
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=0, r=0, t=80, b=0)
)


# world_map.write_html("interactive_graphs/police_killing_by_state.html")

# world_map.show()





# Relation Between Income and Crime
df_income_vs_killing = df_income_by_state.merge(df_fatalities_by_state, on='State_Full', how='inner')

# Calculating Per Capita Rate (Killings per 1 Million people)
df_income_vs_killing['killings_per_1m'] = (df_income_vs_killing['killings'] / df_income_vs_killing['total_state_population_x']) * 1000000

# The "Rate per 1M" Metric: By standardizing the data (killings / population) * 1,000,000,
# the chart now genuinely compares the safety and socioeconomic environments of the states,
# rather than just highlighting which states have the largest borders.

# df_income_vs_killing = df_income_vs_killing.sort_values(by='killings_per_1m', ascending=False)
# display_columns = ['State', 'State_Full', 'total_state_population_x', 'Median_Income', 'killings', 'killing_by_police_usa_share_pct', 'killings_per_1m']
# print(df_income_vs_killing[display_columns])

#    State            State_Full  total_state_population_x  Median_Income state  killings  total_state_population_y  killing_by_police_usa_share_pct  killings_per_1m

# Scatter Plot with Ordinary Least Squares (OLS) trendline
fig = px.scatter(
    df_income_vs_killing,
    x='Median_Income',
    y='killings_per_1m',
    hover_name='State_Full',
    trendline='ols',
    trendline_color_override='#c0392b',
    custom_data=['total_state_population_x', 'killings', 'Median_Income']
)


fig.update_traces(
    marker=dict(
        size=20,
        color='#005691',
        opacity=0.6,
        line=dict(width=1, color='rgba(50, 50, 50, 0.8)') # Crisp, dark borders around dots
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "<span style='font-size:10px;'>─────────────────────</span><br>"
        "<b>Median Income:</b> $%{customdata[2]:,.0f}<br>"
        "<b>Rate per 1M Residents:</b> %{y:.1f}<br>"
        "<span style='font-size:10px;'>───────────────────────────</span><br>"
        "<b>Individuals Killed by Police:</b> %{customdata[1]}<br>"
        "<b>Total Population:</b> %{customdata[0]:,.0f}<br>"
        "<extra></extra>"
    ),
    selector=dict(mode='markers') # white borders only apply to the dots.
)

# Customizing the trendline
trendline_trace = fig.data[1]
trendline_trace.line.color = '#DC3545'
trendline_trace.line.dash = 'dash'
trendline_trace.line.width = 5

# Layout Adjustments
fig.update_layout(
    title=dict(
        text='<b>Income vs. Police Fatalities by State</b><br>'
             '<span style="font-size: 14px; color: gray;">Analyzing the relationship between median household income and fatalities per 1M residents.</span>',
        font=dict(family="Arial, Helvetica, sans-serif", size=20, color="#333333"),
        x=0.05, y=0.95
    ),
    xaxis=dict(
        title=dict(text="<b>Median Household Income</b>", font=dict(size=13, color="#555555"), standoff=15),
        tickfont=dict(size=12, color="#555555"),
        tickprefix="$",
        tickformat=",.0f",
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False
    ),
    yaxis=dict(
        title=dict(text="<b>Fatalities (per 1,000,000 residents)</b>", font=dict(size=13, color="#555555"), standoff=15),
        tickfont=dict(size=12, color="#555555"),
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=100, b=60),
    hoverlabel=dict(font_size=13, font_family="Arial", bordercolor="#EAEAEA")
)

# fig.write_html("interactive_graphs/income_vs_killing.html")

# fig.show()