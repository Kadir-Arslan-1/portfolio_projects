import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import iso3166
import plotly.graph_objects as go
from iso3166 import countries


# Create locators for ticks:
register_matplotlib_converters()

# Notebook Presentation:
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 125)
pd.set_option('display.width', None)

#Load the Data
df = pd.read_csv('csv_files/mission_launches.csv')



print("\nShape of the DataFrame:")
print(df.shape)

print("\nColumns of the Dataframe:")
print(df.columns)

df = df.drop('Unnamed: 0.1', axis=1)
df = df.drop('Unnamed: 0', axis=1)


print("\nFirst rows of the DataFrame:")
print(df.head())

print("\nIs there any missing values?")
print(df.isna().values.any())
# True
print("\nIs there any duplicated values?")
print(df.duplicated().values.any())

print("\nThe Amount of Duplicated Entries:")
print(df.duplicated().values.any().sum())

# There is just one duplicates, simply drop it.
df.drop_duplicates(keep='last', inplace=True)

print("\nThe Amount of Duplicated Entries:")
print(df.duplicated().values.any().sum())

print("\nOverview of the DataFrame:")
print(df.info())


def parse_date(x):
    try:
        return pd.to_datetime(x, format='%a %b %d, %Y %H:%M UTC', utc=True)
    except:
        try:
            return pd.to_datetime(x, format='%a %b %d, %Y', utc=True)
        except:
            return pd.NaT

df['Date'] = df['Date'].apply(parse_date)
df['Date'] = df['Date'].dt.tz_localize(None)

df['Price'] = pd.to_numeric(
    df['Price'].str.replace(',', '', regex=False),
    errors='coerce'
)

print("\nOverview of the DataFrame:")
print(df.info())


# Descriptive Statistics
print("\nDescriptive Statistics of the Dataframe:")
print(df.Price.describe())


# Plotting County Names:
# We need to use country names and their codes (iso) at the analysis.
# Russia is the Russian Federation
# New Mexico should be USA
# Yellow Sea refers to China
# Shahrud Missile Test Site should be Iran
# Pacific Missile Range Facility should be USA
# Barents Sea should be Russian Federation
# Gran Canaria should be USA


# Define mappings for ambiguous locations
location_mapping = {
    "Russia": "Russian Federation",
    "New Mexico": "USA",
    "Yellow Sea": "China",
    "Shahrud Missile Test Site": "Iran",
    "Pacific Missile Range Facility": "USA",
    "Barents Sea": "Russian Federation",
    "Gran Canaria": "USA"
}

df["Country"] = df["Location"].astype(str).str.split(",").str[-1].str.strip()
# Apply location mapping
df["Country"] = df["Country"].replace(location_mapping)



# Plotting "ISO" names to the data:
# Define missing ISO codes
missing_iso_mapping = {
    "Iran": "IRN",
    "North Korea": "PRK",
    "Pacific Ocean": "PAC",  # Custom code for non-country regions
    "South Korea": "KOR",
    "USA": "USA"
}


# Function to get Alpha-3 country codes
def get_iso_alpha3(country):
    country = country
    if country in missing_iso_mapping:
        return missing_iso_mapping[country]  # Return manually assigned code if available
    try:
        return iso3166.countries_by_name[country.upper()].alpha3
    except KeyError:
        return missing_iso_mapping[country]  # Handle missing cases gracefully

# Convert country names to ISO Alpha-3 codes
df["ISO"] = df["Country"].map(get_iso_alpha3)



# The standard format for that Detail column across the dataset is actually:
# Rocket (Launch Vehicle) | Payload (Mission Name)
# Here is the breakdown of why that is, and how it applies to your examples.
# Saturn V Example
# In Saturn V | Apollo 6:
# Saturn V is the Rocket (specifically called a "Launch Vehicle" in aerospace, which usually refers to a weapon).
# It is the physical machine that does the lifting.
#
# Apollo 6 is the Payload or Mission. It is the spacecraft sitting on top of the rocket.

# Adding Rocket Types to the DataFrame:
# This creates two new columns by splitting the text at the pipe '|' symbol
df['Rocket_Type'] = df['Detail'].str.split(' | ', regex=False, expand=True)[0].str.strip()



print("\nDataframe with countries and Country Codes:")
print(df.head(10))




# Number of Launches per Company

df_by_organisation = (
    df.groupby(['Organisation', 'Country'])
      .size()
      .reset_index(name='Total_Launches')
)

df_first_20 = df_by_organisation.sort_values('Total_Launches', ascending=False).head(20)


h_bar = px.bar(
    df_first_20,
    x='Total_Launches',
    y='Organisation',
    orientation='h',
    text='Total_Launches', color='Organisation',
    color_discrete_sequence=px.colors.qualitative.G10,
    custom_data=['Country'],
    labels={'Organisation': 'Organisation', 'Total_Launches': 'Total Launches'}
)

# Designing the layout
h_bar.update_layout(
    plot_bgcolor='white',paper_bgcolor='white',
    font_family='Arial, Helvetica, sans-serif',
    title=dict(text="Top Space Organizations by Launches",
               font=dict(family='Arial, Helvetica, sans-serif', size=28, color='#D14D72'), x=0.03),

    xaxis_title='', yaxis_title='',
    yaxis=dict(
        categoryorder='total ascending',
        showgrid=False,showline=False,
        ticks='outside', ticklen=5, tickcolor='white',
        tickfont=dict(family='Arial Black', size=12, color='#2c3e50')
    ),
    xaxis=dict(showgrid=True, gridcolor='#f0f0f0', showline=False, zeroline=False, showticklabels=True),
    coloraxis_showscale=False,
    showlegend=False,
    height=750
)

# Alignments for the labels and bars
h_bar.update_traces(
    textposition='outside',
    textfont=dict(size=14, color='#2c3e50'),
    marker_line_width=0,
    cliponaxis=False,
    hovertemplate=(
        '<b style="font-size: 14px;">%{y}</b><br>' +
        '<span style="font-size: 13px;">Total Launches: </span>' +
        '<b style="font-size: 14px;">%{x}</b>' +
        '<br>' +
        '<span style="font-size: 13px;">Country: </span>' +
        '<b style="font-size: 14px;">%{customdata[0]}</b>' +
        '<extra></extra>'
    ),
)

# h_bar.write_html("interactive_graphs/top_20_organizations.html")

# h_bar.show()





# Distribution of Mission Status
# How many missions were successful? How many missions failed?

df_by_mission_status = (df.groupby('Mission_Status', as_index=False)
                        .size().rename(columns={'size': 'Count'}))


color_map = {'Success': '#00B8A9', 'Failure': '#F6416C', 'Partial Failure': '#FFDE7D', 'Prelaunch Failure': '#E4C59E'}

colors = [color_map.get(status, '#CCCCCC') for status in df_by_mission_status['Mission_Status']]

# This dynamically pulls the 'Failure' slice out by 10% (0.1)
pull_values = [0.1 if status == 'Failure' else 0 for status in df_by_mission_status['Mission_Status']]

fig = go.Figure(data=[go.Pie(
    labels=df_by_mission_status['Mission_Status'],
    values=df_by_mission_status['Count'],
    hole=0.35,
    pull=pull_values,
    marker=dict( colors=colors,line=dict(color='#FFFFFF', width=1)),
    textinfo='percent+label',
    textposition='outside',
    textfont=dict(size=14, family="Arial, sans-serif", color='#333333'),
    hoverinfo='label+value+percent'
)])

# 4. Update the layout for a clean, editorial look
fig.update_layout(
    title=dict(
        text='Distribution of Mission Status',
        font=dict(size=30, family="Arial, Helvetica, sans-serif", color='#27496D'),
        x=0.5,y=0.97
    ),
    annotations=[
        dict(
            text='Launch<br>Outcomes',
            x=0.5, y=0.5,
            font_size=16, font_color='#6B7280',
            showarrow=False
        )
    ],
    # showlegend=False,  # Removing the legend makes it cleaner
    margin=dict(t=90, b=40, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)
# fig.write_html("interactive_graphs/distribution_mission_status.html")

# fig.show()



# # Number of Active versus Retired Rockets
# # How many rockets are active compared to those that are decomissioned?

df_by_rocket_status = (
    df.groupby('Rocket_Status', as_index=False)
    .size()
    .rename(columns={'size': 'Count'})
)


color_map = {'StatusActive': '#08CB00', 'StatusRetired': '#D32626'}

colors = [color_map.get(status, '#CCCCCC') for status in df_by_rocket_status['Rocket_Status']]

fig = go.Figure(data=[go.Pie(
    labels=df_by_rocket_status.Rocket_Status,
    values=df_by_rocket_status.Count,
    hole=0.4, # Creates a donut effect
    marker=dict( colors=colors,line=dict(color='#FFFFFF', width=1)),
    textinfo = 'percent+label',
    textposition = 'outside',
    textfont = dict(size=14, family="Arial, sans-serif", color='#333333'),
    hoverinfo = 'label+value+percent'
)])

fig.update_traces(textinfo='percent+label')

fig.update_layout(
    title=dict(
        text='Conditions of Rocket Status',
        font=dict(size=30, family="Arial, Helvetica, sans-serif", color='#2A2F4F'),
        x=0.5,y=0.97
    ),
    annotations=[dict(text='Rocket<br>Condition',x=0.5, y=0.5, font_size=16, font_color='#6B7280',showarrow=False )],
    margin=dict(t=90, b=40, l=40, r=40),
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# fig.write_html("interactive_graphs/rocket_condition.html")

# fig.show()





# we are going to use a Choropleth Map to Show the Number of Launches by Country



# Aggregate mission counts by location
df_country = (df.groupby(['Country', 'ISO'], as_index=False)
              .agg(Total_Missions=('Mission_Status', 'count')))

# Sort the dataframe for better visualization
df_country.sort_values('Total_Missions', ascending=False, inplace=True)

# Plotting the Choropleth
world_map = px.choropleth(
    df_country,
    locations='ISO',
    color='Total_Missions',
    hover_name='Country',
    custom_data=['ISO','Total_Missions'],
    color_continuous_scale='matter',
    title='<b style="color:#152346;">Global Rocket Launches by Country</b>'
)

# Layout adjustments
world_map.update_layout(
    font_family='Arial, Helvetica, sans-serif',
    font_color='#2c3e50',
    title_font_size=24,
    title_font_color='#922062',
    title_x=0.03,
    margin=dict(t=80, l=0, r=0, b=0),
    geo=dict(
        showframe=False,  # remove the border around the world
        showcoastlines=False,  # remove the thick lines
        projection_type='natural earth',  # an earth projection
        bgcolor='rgba(0,0,0,0)',  # transparent background
        lakecolor='#ffffff',  # fill lakes with white to blend in cleanly
    ),

    coloraxis_colorbar=dict(
        title=dict(text="Total Launches", font=dict(size=14, color='#2c3e50')),
        thicknessmode="pixels", thickness=12,
        lenmode="pixels", len=250,
        yanchor="middle", y=0.5,
        xanchor="left", x=0.95,
        tickvals=[0, 1, 2],
        ticktext=['1', '10', '100+'],
        tickfont=dict(size=12, color='#2c3e50')
    )
)

world_map.update_traces(
    marker_line_color='#ffffff',  # a subtle white borders between countries
    marker_line_width=0.4,  # but they must be thin
    # Hover arrangements:
    hovertemplate=(
            '<b style="font-size: 14px; color: #152346;">%{hovertext}</b><br>' +
            '<span style="font-size: 13px; color: #555;">ISO: </span>' +
            '<b style="font-size: 14px; color: #2c3e50;">%{customdata[0]}</b><br>' +
            '<span style="font-size: 13px; color: #555;">Total Launches: </span>' +
            '<b style="font-size: 14px; color: #152346;">%{customdata[1]}</b><br>' +
            '<extra></extra>'
    ),
    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial", bordercolor="#e2e8f0")
)

# world_map.write_html("interactive_graphs/world_map_by_launches.html")

# world_map.show()




# Here we filter all the entries where missiın status is not success
df_failure = df.query("Mission_Status != 'Success'")

# We group this entries by country to get desirable entries
df_failure = df_failure.groupby(["Country"], as_index=False).agg(Total_Failures=("Mission_Status", "count"))

# Adding an additional column for failures to df_country database.
df_success_vs_failure = df_country.merge(df_failure, on="Country", how="left").sort_values('Total_Failures', ascending=False)

# In cast there were no failure
df_success_vs_failure.fillna(0, inplace=True)

# # Creating a new column for failure percentages:
df_success_vs_failure["Success_Rate"] = (df_success_vs_failure.Total_Missions - df_success_vs_failure.Total_Failures) / df_success_vs_failure.Total_Missions * 100

# print("\nMost Successful Countries by Launch Success Rate:")
df_success_vs_failure.sort_values('Success_Rate', ascending=False, inplace=True)


print(df_success_vs_failure.head(20))


bar = px.bar(
    df_success_vs_failure[:10],
    x='Country',
    y='Success_Rate',
    color='Country',
    custom_data=['Total_Missions','Total_Failures', 'Success_Rate'],
    color_discrete_sequence=px.colors.qualitative.Bold,
    text='Success_Rate',  # Display the success rates
)

# Options for styling, text formatting, and hover template
bar.update_traces(
    texttemplate='<b>%{text:,.2f}%</b>', # Formatting success rates to percentages.
    textposition='outside', textfont_size=12, marker_line_width=0,  # Arrangements for bars.
    # customdata=custom_data, # These are the arrangements for hover display
    hovertemplate=(
        "<b>%{x}</b><br>" +
        "Total Missions: %{customdata[0]}<br>" +
        "Total Failures: %{customdata[1]:,.0f}<br>" +
        "Success Rate: %%{customdata[2]:,.0f}" +
        "<extra></extra>"
    )
)


bar.update_layout(
    template='plotly_white',
    title=dict(text='<b>Most Successful Countries by Space Launch Success Rate</b>',
               font=dict(size=26, family='Arial, Helvetica, sans-serif', color='#008695'), x=0.025),
    xaxis_title='',
    yaxis_title='Percentages',
    yaxis_title_font_size=16,
    yaxis_title_font_color="#008695",
    yaxis_range=[30, 100],
    font=dict(family='Arial, sans-serif', size=13, color='#555555'),
    showlegend=False, # No legend
    coloraxis_showscale=False, # No coloraxis
    yaxis=dict(showgrid=True, showticklabels=True, zeroline=False, ticklabelposition="outside", ticklabelstandoff=13, tickfont=dict(size=15, family="Arial", color='black')),
    xaxis=dict(showgrid=False, ticklabelposition="outside", ticklabelstandoff=7, tickfont=dict(size=15, family="Arial", color='black')),
    margin=dict(l=10, r=70, t=70, b=20),

)

# bar.write_html("interactive_graphs/top_10_countries_with_success_rate.html")

# bar.show()






# Most Unsuccessful Countries
print("\nMost Unsuccessful Countries by Launch Success Rate:")
df_success_vs_failure.sort_values('Success_Rate', ascending=True, inplace=True)
print(df_success_vs_failure.head())




# we are going to create a Plotly Sunburst Chart of the countries, organisations, and mission status.

# Grouping and Sorting
country_organisation = (df.groupby(['Country', 'Organisation', 'Mission_Status'], as_index=False)
                        .agg(Launch_Number=('Rocket_Status','count')))

country_organisation.sort_values('Launch_Number', ascending=False)

burst = px.sunburst(
    country_organisation,
    path=['Country', 'Organisation', 'Mission_Status'],
    values='Launch_Number',
    template="plotly_white"
)

status_colors = {
    "Success": "#4CAF50",
    "Failure": "#E53935",
    "Partial Failure": "#FB8C00",
    "Prelaunch Failure": "#1E88E5",
    "Unknown": "#9E9E9E",
}

sequential_palette = px.colors.qualitative.Pastel

# We are going to customize the coloring of the labels here
# Extract the labels generated by Plotly and assign our custom colors to them one by one
labels = burst.data[0].labels
custom_colors = []
seq_index = 0

for label in labels:
    if label in status_colors:
        custom_colors.append(status_colors[label])
    else:
        custom_colors.append(sequential_palette[seq_index % len(sequential_palette)])
        seq_index += 1

burst.update_traces(
    marker=dict(colors=custom_colors, line=dict(color='#FFFFFF', width=1.5)),
    textfont=dict(family="Arial, sans-serif", color="#2C3E50"),
    hovertemplate="<b>%{label}</b><br>Launches: %{value}<extra></extra>"
)

burst.update_layout(
    margin=dict(t=70, l=10, r=10, b=10),
    title=dict(text='<b>Rocket Launches by Country, Organisation, and Mission Status</b>',
               font=dict(size=22, family='Arial, Helvetica, sans-serif', color='#2C3E50'), x=0.5),
    uniformtext=dict(minsize=11, mode="hide"),
)

# burst.write_html("interactive_graphs/sunburst_all_organizations.html")

# burst.show()






# Analyse the Total Amount of Money Spent by Organisation on Space Missions

# Getting the total number of launches and total spending
org_price_with_na = df.groupby(['Organisation'], as_index=False).agg(
    Total_Spending=("Price", "sum"),
    Launch_Count_Total=("Mission_Status", "count")
)

# Some launch data has no price data, so we have to create another colum with dropping the na values
prices_without_na = df.dropna(subset=['Price']).copy()

org_price_without_na = (prices_without_na.groupby(['Organisation'], as_index=False)
                        .agg(Launch_Count_Spending_Accessible=("Mission_Status", "count")))


# Merging two dataframe we have:
org_price_with_na = org_price_with_na.merge(org_price_without_na, on="Organisation", how="left")

# Converting second values to integers: (since it can incluse na values they are held on float numbers:
org_price_with_na["Launch_Count_Spending_Accessible"] = (
    org_price_with_na["Launch_Count_Spending_Accessible"]
    .fillna(0)
    .astype(int)
)

# Adding a ew column to display the average spending by launch:
org_price_with_na["Avr_Spending_by_Launch"] = org_price_with_na.Total_Spending / org_price_with_na.Launch_Count_Spending_Accessible

# Sorting by Total Spending:
org_price_with_na = org_price_with_na.sort_values('Total_Spending', ascending=False)

# Take the most 20 Organizations
org_price_with_na_top_20 = org_price_with_na[:20]


def format_spending_label(val_in_millions):
    if val_in_millions < 1000:
        return f"${val_in_millions:,.0f}M"
    else:
        return f"${val_in_millions / 1000:,.2f}B"

org_price_with_na_top_20['Display_Label'] = org_price_with_na_top_20['Total_Spending'].apply(format_spending_label)

# Since values are in millions, we are going to need formatting:
org_price_with_na_top_20['Total_Spending_B'] = org_price_with_na_top_20['Total_Spending'] / 1000

print(org_price_with_na_top_20)

c_bar = px.bar(
    org_price_with_na_top_20,
    x='Total_Spending_B',
    y='Organisation',
    orientation='h',
    custom_data=[
        'Total_Spending_B',
        'Launch_Count_Spending_Accessible',
        'Avr_Spending_by_Launch',
        'Launch_Count_Total'
    ],
    text='Display_Label',
    color=np.log10(org_price_with_na_top_20['Total_Spending_B']),
    color_continuous_scale='Deep',
)


c_bar.update_traces(
    texttemplate='<b>%{text}</b>',
    textposition='outside',
    textfont=dict(size=12, color='#2C3E50'),
    marker_line_width=0,
    hovertemplate=(
        "<b style='font-size:15px;'>%{y}</b><br><br>" +
        "<span>Total Spending:</span> <b>$%{customdata[0]:,.2f} Billion</b><br>" +
        "<span>Number of Launches accounts for this Amount:</span> <b>%{customdata[1]:,.0f}</b><br>" +
        "<span>Average Cost per Launch:</span> <b>$%{customdata[2]:,.0f}M</b><br>" +
        "<span>Total Number of Launches (General):</span> <b>%{customdata[3]:,.0f}</b>" +
        "<extra></extra>" # Removes the messy secondary trace box
    )
)


c_bar.update_layout(
    template='plotly_white',
    title=dict(
        text='<b>Top 20 Organizations by Total Launch Expenditure</b>',
        font=dict(size=25, family='Helvetica Neue, Arial, sans-serif', color='#3f4b86'),
        x=0.03, xanchor='left'
    ),
    xaxis_title=dict(
        text='<b>Total Expenditure on Launches</b>',
        font=dict(size=14, family='Arial Helvetica, sans-serif', color='#3f4b86')),
    yaxis_title='',
    font=dict(family='Helvetica Neue, Arial, sans-serif', size=13, color='#5F6B78'),
    showlegend=False,
    coloraxis_showscale=False,
    margin=dict(l=10, r=70, t=80, b=30),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

c_bar.update_xaxes(
    showgrid=True,
    gridcolor='#F0F2F6',
    zeroline=False,
    ticklabelposition="outside",
    ticklabelstandoff=7,
    tickfont=dict(size=13, color='#7f808f'),
    type='log',
    # Formatting specific tick locations and their exact labels
    tickvals=[0.01, 0.1, 1, 10, 100],
    ticktext=['$10M', '$100M', '$1B', '$10B', '$100B']
)

c_bar.update_yaxes(
    showgrid=False,
    showticklabels=True,
    zeroline=False,
    ticklabelstandoff=8,
    tickfont=dict(size=14, color='#2C3E50', weight='bold'),
    categoryorder='total ascending'
)

# c_bar.write_html("interactive_graphs/top_spending_organisations.html")

# c_bar.show()




# Finding most Expensive Launches
# We saw thet Russians spent 10 Billion Dollars on just two launches
# lets examine deeply to see which launches costed more than others:



df_top10_launches = df.sort_values("Price", ascending=False)
print("\n Most Expensive Launches")
print(df_top10_launches.head(10))





# Analysis for the space programs (rocket types)


# We are going to use clean data without na values
# We are going to group the data by rocket type and aggregate its values
prices_without_na = df.dropna(subset=['Price']).copy()

df_program = prices_without_na.groupby(['Rocket_Type', 'Country', 'Organisation'], as_index=False).agg(
    Total_Spending=("Price", "sum"),
    Launch_Count_Total=("Mission_Status", "count"),
    Avr_Spending_by_Launch=("Price", "mean"),
)

# sorting the Programs:
df_program = df_program.sort_values("Total_Spending", ascending=False)

# We are going to plot most 20 Space Launch Program by Expenditure
df_program_top20 = df_program[:20]

# We are going to use same value formatting as before:
df_program_top20['Display_Label'] = df_program_top20['Total_Spending'].apply(format_spending_label)

# Since values are in millions, we are going to need formatting:
df_program_top20['Total_Spending_B'] = df_program_top20['Total_Spending'] / 1000

c_bar = px.bar(
    df_program_top20,
    x='Total_Spending_B',
    y='Rocket_Type',
    orientation='h',
    custom_data=[
        'Total_Spending_B',
        'Launch_Count_Total',
        'Avr_Spending_by_Launch',
    ],
    text='Display_Label',
    color=np.log10(df_program_top20['Total_Spending_B']),
    color_continuous_scale='Emrld',
)


c_bar.update_traces(
    texttemplate='<b>%{text}</b>',
    textposition='outside',
    textfont=dict(size=12, color='#2C3E50'),
    marker_line_width=0,
    hovertemplate=(
        "<b style='font-size:15px;'>%{y}</b><br><br>" +
        "<span>Total Spending:</span> <b>$%{customdata[0]:,.2f} Billion</b><br>" +
        "<span>Number of Launches</span> <b>%{customdata[1]:,.0f}</b><br>" +
        "<span>Average Cost per Launch:</span> <b>$%{customdata[2]:,.0f}M</b><br>" +
        "<extra></extra>" # Removes the messy secondary trace box
    )
)


c_bar.update_layout(
    template='plotly_white',
    title=dict(
        text='<b>Top 20 Missile Program by Total Launch Expenditure</b>',
        font=dict(size=25, family='Helvetica Neue, Arial, sans-serif', color='#54a484'),
        x=0.03, xanchor='left'
    ),
    xaxis_title=dict(
        text='<b>Total Expenditure on Launches</b>',
        font=dict(size=14, family='Arial Helvetica, sans-serif', color='#54a484')),
    yaxis_title='',
    font=dict(family='Helvetica Neue, Arial, sans-serif', size=13, color='#5F6B78'),
    showlegend=False,
    coloraxis_showscale=False,
    margin=dict(l=10, r=70, t=80, b=30),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

c_bar.update_xaxes(
    showgrid=True,
    gridcolor='#F0F2F6',
    zeroline=False,
    ticklabelposition="outside",
    ticklabelstandoff=7,
    tickfont=dict(size=13, color='#0d505d'),
    type='log',
    # Formatting specific tick locations and their exact labels
    tickvals=[2, 4, 10, 16],
    ticktext=['$2B', '$4B', '$10B', '$16B']
)

c_bar.update_yaxes(
    showgrid=False,
    showticklabels=True,
    zeroline=False,
    ticklabelstandoff=8,
    tickfont=dict(size=14, color='#2C3E50', weight='bold'),
    categoryorder='total ascending'
)

# c_bar.write_html("interactive_graphs/top_spending_space_programs.html")
# c_bar.show()


# print(df_program_top20)





# Analysis for average expenditure by space programs (Rocket type) per Launch over time


# we have program dataframe, here we are going to add "date" data to the programs
date_program = df.groupby(["Rocket_Type", "Country"]).agg(Avr_Date=("Date", "mean"))
df_program = df_program.merge(date_program, on="Rocket_Type")


df_program['Avr_Spending_Formatted'] = df_program['Avr_Spending_by_Launch'].apply(format_spending_label)
df_program['Total_Spending_Formatted'] = df_program['Total_Spending'].apply(format_spending_label)

df_program['Avr_Spending_by_Launch_B'] = df_program['Avr_Spending_by_Launch'] / 1000

fig_px = px.scatter(
    df_program,
    x='Avr_Date',
    y='Avr_Spending_by_Launch_B',
    trendline='lowess',
    opacity=0.6,
    title='<b>Average Cost per Launch by Program Over Time</b>',
    custom_data=[
        'Rocket_Type',
        'Avr_Date',
        'Organisation',
        'Country',
        'Total_Spending_Formatted',
        'Launch_Count_Total',
        'Avr_Spending_Formatted'
    ],
    template='plotly_white',
)

hover_html = (
        "<b style='font-size:16px; color:#1A252F'>%{customdata[0]}</b><br>" +
        "<span style='font-size:13px; color:#5F6B78'>%{x|%B %Y}</span><br>" +
        "<span style='font-size:13px; color:#5F6B78'>%{customdata[2]}</span><br>" +
        "<span style='font-size:13px; color:#5F6B78'>%{customdata[3]}</span><br><br>" +
        "<span style='color:#7F8C8D'>Total Spending:</span> <b style='color:#00B8A9'>%{customdata[4]}</b><br>" +
        "<span style='color:#7F8C8D'>Total Count:</span> <b style='color:#00B8A9'>%{customdata[5]:,.0f}</b><br>" +
        "<span style='color:#7F8C8D'>Avg Spending per Launch:</span> <b style='color:#00B8A9'>%{customdata[6]}</b>" +
        "<extra></extra>"
)


fig_px.update_traces(hovertemplate=hover_html, selector=dict(mode='markers'))

fig_px.update_yaxes(
    type='log',
    tickvals=[0.001,0.005, 0.01, 0.1, 1, 5],
    ticktext=['$1M','$5M', '$10M', '$100M', '$1B', '$5B'],
    title_text='Average Cost per Launch by Program Over Time',
    title_font=dict(size=14, color='#F6416C', weight='bold'),
    tickfont=dict(size=13, color='#8898AA'),
    showgrid=True,
    gridcolor='#F0F2F6',
    zeroline=False
)

# We are going extract the traces (scatter and trendline) and design them.
scatter_trace = fig_px.data[0]
trendline_trace = fig_px.data[1]

# scatter points
scatter_trace.marker.size = 16
scatter_trace.marker.color = '#00B8A9'
scatter_trace.marker.line.width = 0.8
scatter_trace.marker.line.color = 'DarkSlateGrey'

# Trendlines
trendline_trace.line.color = '#F6416C'
trendline_trace.line.dash = 'dash'
trendline_trace.line.width = 4

# we are going to create shadows effect for the trendlines
shadow_trace = go.Scatter(
    x=trendline_trace.x,
    y=trendline_trace.y,
    mode='lines',
    line=dict(color='rgba(220, 53, 69, 0.25)', width=15),
    hoverinfo='skip',
    showlegend=False
)

fig = go.Figure( data=[shadow_trace, trendline_trace, scatter_trace], layout=fig_px.layout)

fig.update_layout(
    font_family="Inter, Helvetica, Arial, sans-serif",
    title_font_size=24,
    title_font_color="#BF092F",
    title_x=0.5,
    xaxis_title='Date',
    yaxis_title='Average Spending by Launch',
    font=dict(family='Helvetica Neue, Arial, sans-serif', size=13, color='#5F6B78'),
    xaxis=dict(showgrid=False, zeroline=False, title_font_size=16, title_font_color="#BF092F"),
    yaxis=dict(showgrid=True, gridcolor='#E5E7EB', zeroline=False, title_font_size=16, title_font_color="#BF092F", type='log'),
    plot_bgcolor='rgba(0,0,0,0)',
    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Inter, Helvetica, Arial, sans-serif", bordercolor="#E2E8F0")
)

# fig.write_html("interactive_graphs/avg_cost_program_over_Time.html")

# fig.show()


print("df_program")
print("--------------------------")
print(df_program)




# Analysis of the Years:

launch_year = df.copy()

# Extract the year, ensuring any NaT values are handled appropriately
launch_year['Year'] = df['Date'].dt.year.astype(int)

# Total Launch Count By year
total_launch_count_by_year = (launch_year.groupby('Year', as_index=False)
                              .agg(Total_Launch_Count=("Mission_Status", "count")))

# Total Successful launch Count by year
successful_launches_by_year = launch_year.query("Mission_Status == 'Success'")
successful_launches_by_year = successful_launches_by_year.groupby(["Year"], as_index=False).agg(Total_Successful_Launch_Count=("Mission_Status", "count"))

# Merging the two dataframes:
launch_by_year = total_launch_count_by_year.merge(successful_launches_by_year, on="Year", how="left")

# In case there were no succsess
launch_by_year.Total_Successful_Launch_Count.fillna(0, inplace=True)

# Success Rate:
launch_by_year["Success_Rate"] = launch_by_year.Total_Successful_Launch_Count / launch_by_year.Total_Launch_Count * 100

# Sorting by year:
launch_by_year.sort_values('Year', ascending=True, inplace=True)

# Prepare the Data: Calculate the failed launches
launch_by_year['Failed_Launch_Count'] = launch_by_year['Total_Launch_Count'] - launch_by_year['Total_Successful_Launch_Count']


fig = go.Figure()

fig.add_trace(go.Bar(
    x=launch_by_year['Year'],
    y=launch_by_year['Total_Successful_Launch_Count'],
    name='Successful',
    marker_color='#3F9AAE',
    marker_line_width=0,    # Removes borders for a cleaner, flat-design look
    customdata=launch_by_year[['Total_Launch_Count', 'Success_Rate', 'Failed_Launch_Count']],
    hovertemplate=(
        "<b style='font-size:16px; color:#1A252F'>%{x}</b><br><br>" +
        "<span style='color:#7F8C8D'>Successful Launches:</span> <b style='color:#3F9AAE'>%{y}</b><br>" +
        "<span style='color:#7F8C8D'>Failed Launches:</span> <b style='color:#F96E5B'>%{customdata[2]}</b><br><br>" +
        "<span style='color:#7F8C8D'>Total Launches:</span> <b style='color:#3F9AAE'>%{customdata[0]}</b><br>" +
        "<span style='color:#7F8C8D'>Success Rate:</span> <b style='color:#3F9AAE'>%{customdata[1]:.1f}%</b>" +
        "<extra></extra>"
    )
))

fig.add_trace(go.Bar(
    x=launch_by_year['Year'],
    y=launch_by_year['Failed_Launch_Count'],
    name='Failed',
    marker_color='#F96E5B',
    marker_line_width=0,
    customdata=launch_by_year[['Total_Launch_Count', 'Success_Rate', 'Total_Successful_Launch_Count']],
    hovertemplate=(
        "<b style='font-size:16px; color:#1A252F'>%{x}</b><br><br>" +
        "<span style='color:#7F8C8D'>Failed Launches:</span> <b style='color:#F96E5B'>%{y}</b><br>" +
        "<span style='color:#7F8C8D'>Successful Launches:</span> <b style='color:#3F9AAE'>%{customdata[2]}</b><br><br>" +
        "<span style='color:#7F8C8D'>Total Launches:</span> <b style='color:#3F9AAE'>%{customdata[0]}</b><br>" +
        "<span style='color:#7F8C8D'>Success Rate:</span> <b style='color:#3F9AAE'>%{customdata[1]:.1f}%</b>" +
        "<extra></extra>"
    )
))


fig.update_layout(
    barmode='stack', # we use stack chart here
    template='plotly_white',
    title=dict(
        text='<b style="color:#134686">Space Mission Launches Over Time</b><br>'
             '<span style="font-size:14px; color:#134686">Annual volume of successful vs. failed orbital attempts</span>',
        font=dict(size=22, family='Helvetica Neue, Arial, sans-serif', color='#1A252F'),
        x=0.02,
        xanchor='left'
    ),

    legend=dict(orientation="h", x=0.8, y=1.1, title_text='', font=dict(size=13, color='#5F6B78')),
    xaxis=dict(
        title='',
        showgrid=False,
        tickfont=dict(size=15, color='#132440'),
        tickmode='linear',
        dtick=5, # ticks for every five year
    ),
    yaxis=dict(
        title='Number of Launches',
        title_font=dict(size=14, color='#2C3E50', weight='bold'),
        tickfont=dict(size=13, color='#134686'),
        showgrid=True,
        gridcolor='#F0F2F6',
        zeroline=True,
        zerolinecolor='#E2E8F0',
        zerolinewidth=2
    ),
    margin=dict(l=20, r=20, t=100, b=20),
    hoverlabel=dict(bgcolor="white", font_size=13, bordercolor="#E2E8F0"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

# fig.write_html("interactive_graphs/launch_number_by_year.html")

# fig.show()





# Analysis for the months:
launch_month = df.copy()

# we are going to create month and year column for every entry at our "base" dataframe
df['Year'] = df['Date'].dt.year.astype(int)
df['Month'] = df['Date'].dt.month_name()

# We will now analyze the distribution of the months in which a certain number of satellites were launched
# Grouping by Months and adding the number of launches to the next
launches_per_month = df.groupby('Month', as_index=False).agg(Total_Launch_Count=("Mission_Status", "count"))

# Sort the months by total launches
launches_per_month = launches_per_month.sort_values('Total_Launch_Count', ascending=False)

m_bar = px.bar(
    launches_per_month,
    x='Month',
    y='Total_Launch_Count',
    text='Total_Launch_Count',  # Adds the exact number directly above the bar
    color_continuous_scale='Bluyl',
    color="Total_Launch_Count"
)

# Refining the bars and texts
m_bar.update_traces(
    marker_line_width=0,  # Removes borders for a flat, modern design
    texttemplate='<b>%{text}</b>',
    textposition='outside',  # Places the numbers cleanly above the bars
    textfont=dict(size=12, color='#2C3E50'),
    # Custom Hover Template
    hovertemplate=(
            "<b style='font-size:15px; color:#2C3E50'>%{x}</b><br><br>" +
            "<span style='color:#467289'>Total Launches:</span> <b style='color:#0F4C75'>%{y}</b>" +
            "<extra></extra>"
    )
)

#  Layout and Typography Arrangements:
m_bar.update_layout(
    template='plotly_white',
    title=dict(
        text='<b>Distribution of Space Launch Counts by Month</b>',
        font=dict(size=22, family='Helvetica Neue, Arial, sans-serif', color='#1B6F7A'),
        x=0.02,
        xanchor='left'
    ),
    xaxis=dict(
        title='',
        tickfont=dict(size=13, color='#0F4C75'),
        showgrid=False,
        categoryorder='total descending'
    ),
    yaxis=dict(
        title='Total Launches',
        title_font=dict(size=14, color='#2C3E50', weight='bold'),
        tickfont=dict(size=13, color='#8898AA'),
        showgrid=True,
        gridcolor='#F0F2F6',  # soft grid lines
        zeroline=False,
        # Expands the top of the graph so the text labels don't get cut off
        range=[0, launches_per_month['Total_Launch_Count'].max() * 1.15]
    ),
    margin=dict(l=20, r=20, t=80, b=20),
    hoverlabel=dict(bgcolor="white", font_size=13, bordercolor="#E2E8F0"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    coloraxis_showscale=False,

)

# m_bar.write_html("interactive_graphs/distribution_of_months.html")

# m_bar.show()





# How has the Launch Price varied Over Time?

launch_prices = df.dropna(subset=['Price'])

# Group by Year and calculate statistics
price_trends = launch_prices.groupby("Year", as_index=False).agg(
    Min_Price=("Price", "min"),    # Average price per year
    Max_Price=("Price", "max"),    # Average price per year
    Avg_Price=("Price", "mean"),    # Average price per year
    pctl_25=("Price", ("q25", lambda x: x.quantile(0.25))),  # Median price per year
    Median=("Price", "median"),  # Average price per year
    pctl_75=("Price", ("q75", lambda x: x.quantile(0.75))),  # Median price per year
    Standard_Deviation=("Price", "std"),  # Median price per year
    Total_Cost=("Price", "sum"),    # Total cost of launches per year
    Launch_Count_Price_Avaliable=("Price", "count"), # Number of launches per year
)


# Adding General Launch Count:
# Since we dropped the column with missing values in our previous dataframe,
# here we are going to create a new grouped dataframe and merge with main dataframe
price_available = df.groupby("Year", as_index=False).agg(Total_Launch_Count=("Mission_Status", "count"))
price_trends = price_trends.merge(price_available, on='Year', how='left')

# displaying-format for the price values:
price_trends['Total_Cost_Fmt'] = price_trends['Total_Cost'].apply(format_spending_label)
price_trends['Avg_Price_Fmt'] = price_trends['Avg_Price'].apply(format_spending_label)
price_trends['Min_Price_Fmt'] = price_trends['Min_Price'].apply(format_spending_label)
price_trends['Max_Price_Fmt'] = price_trends['Max_Price'].apply(format_spending_label)
price_trends['Median_Fmt'] = price_trends['Median'].apply(format_spending_label)

# Price layout for the y-axis
price_trends['Total_Cost_B'] = price_trends['Total_Cost'] / 1000

# year moving average so that lines has a tune
moving_average = price_trends['Total_Cost_B'].rolling(window=3).mean()


fig = go.Figure()

# Scatter graph
fig.add_trace(go.Scatter(
    x=price_trends['Year'],
    y=price_trends['Total_Cost_B'],
    mode='markers',
    name='Total Expenditure',
    marker=dict(color='#467289', size=15, opacity=0.8, line=dict(width=1.5, color='white')),
    # for hovertemplate:
    customdata=price_trends[[
        'Total_Cost_Fmt', 'Avg_Price_Fmt', 'Min_Price_Fmt',
        'Max_Price_Fmt', 'Median_Fmt', 'Launch_Count_Price_Avaliable', 'Total_Launch_Count'
    ]],
    hovertemplate=(
            "<b style='font-size:16px; color:#1A252F'>Year: %{x}</b><br><br>" +
            "<span style='font-size:13px; color:#7F8C8D'>Total Spending:</span> <b style='font-size:13px; color:#467289'>%{customdata[0]}</b><br><br>" +
            "<span style='color:#7F8C8D'>Average Price:</span> <b style='color:#467289'>%{customdata[1]}</b><br>" +
            "<span style='color:#7F8C8D'>Min Price:</span> <b style='color:#467289'>%{customdata[2]}</b><br>" +
            "<span style='color:#7F8C8D'>Max Price:</span> <b style='color:#467289'>%{customdata[3]}</b><br>" +
            "<span style='color:#7F8C8D'>Median Price:</span> <b style='color:#467289'>%{customdata[4]}</b><br><br>" +
            "<span style='color:#7F8C8D'>Launches (Cost Known):</span> <b style='color:#467289'>%{customdata[5]}</b><br>" +
            "<span style='color:#7F8C8D'>Total Launches:</span> <b style='color:#467289'>%{customdata[6]}</b>" +
            "<extra></extra>"
    )
))

# Rolling Average line
fig.add_trace(go.Scatter(
    x=price_trends['Year'],
    y=moving_average,
    mode='lines',
    name='3-Year Rolling Average',
    line=dict(color='#D9534F', width=3, shape='spline'),
    hoverinfo='skip'
))

# Layout Styling
fig.update_layout(
    template='plotly_white',
    title=dict(
        text='<b>Total Expenditure on Satellite Launches by Year</b>',
        font=dict(size=22, family="Helvetica Neue, Arial, sans-serif", color="#1A252F"),
        y=0.95, x=0.02,
        xanchor='left', yanchor='top'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom", xanchor="right",
        y=1.02, x=0.98,
        bgcolor="rgba(255, 255, 255, 0)",
        font=dict(size=13, color='#5F6B78')
    ),
    hovermode='closest',  # this renders custom HTML cards
    hoverlabel=dict(bgcolor="white", font_size=13, bordercolor="#E2E8F0"),
    margin=dict(l=60, r=40, t=100, b=60),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

# Axes Arrangements
fig.update_xaxes(
    tickangle=0,
    tickmode='linear',
    tick0=1965, dtick=5,
    showgrid=False,
    tickfont=dict(size=13, color='#8898AA'),
    range=[1962, 2021]
)

fig.update_yaxes(
    title=dict(text="Total Cost", font=dict(size=14, color='#2C3E50', weight='bold')),
    showgrid=True,
    gridcolor='#F0F2F6',  # soft grid lines
    tickformat='$,.0f',  # Formats numbers as $2, $4, $6
    ticksuffix='B',  # Appends a 'B' to make it $2B, $4B
    tickfont=dict(size=13, color='#8898AA'),
    zeroline=False
)

# fig.write_html("interactive_graphs/total_cost_by_year.html")

# fig.show()

print(price_trends)


#
# Chart the Number of Launches over Time by the Top 10 Organisations.
# How has the dominance of launches changed over time between the different players?


top10_org_counts = (df.groupby(['Year', 'Organisation'])
                    .agg(Total_Launch_Count=("Mission_Status", "count"))
                    .reset_index())

# Get the top 10 organizations with the most total launches
top_10_orgs = top10_org_counts.groupby('Organisation')['Total_Launch_Count'].sum().nlargest(12).index

top10_org_counts = top10_org_counts[top10_org_counts['Organisation'].isin(top_10_orgs)]

df_country_organisation = df.groupby(["Organisation"]).agg(Country=("Country", "max"))

top10_org_counts = top10_org_counts.merge(df_country_organisation, on='Organisation', how='inner')


# high-contrast  color palette
color_palette = [
'#1f77b4', '#d62728', '#2ca02c', '#ff7f0e', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#FF21C5',
]

fig = px.line(
    top10_org_counts,
    x='Year',
    y='Total_Launch_Count',
    color='Organisation',
    custom_data=['Organisation', 'Country'],
    color_discrete_sequence=color_palette
)

# html cover cards
hover_html = (
    "<b style='font-size:16px; color:#1A252F'>%{customdata[0]}</b><br>" +
    "<span style='font-size:13px; color:#5F6B78'>%{customdata[1]}</span><br><br>" +
    "<span style='color:#7F8C8D'>Year:</span> <b style='color:#2C687B'>%{x}</b><br>" +
    "<span style='color:#7F8C8D'>Launches:</span> <b style='color:#2C687B'>%{y}</b>" +
    "<extra></extra>"
)

fig.update_traces(
    mode='lines',         # This removes the noisy dots
    line=dict(width=2.5),
    hovertemplate=hover_html
)

fig.update_layout(
    template='plotly_white',
    title=dict(
        text='<b>Space Launches Over Time</b><br><span style="font-size:14px; color:#2C687B">Annual orbital attempts by the top 11 organizations</span>',
        font=dict(size=22, family='Helvetica Neue, Arial, sans-serif', color='#E03F4F'),
        x=0.02,
        xanchor='left'
    ),
    xaxis=dict(
        title='',
        showgrid=False,
        tickfont=dict(size=13, color='#2C687B'),
        tickmode='linear',
        dtick=10 # Shows every 10 years to keep the x-axis  clean
    ),
    yaxis=dict(
        title='Number of Launches',
        title_font=dict(size=14, color='#2C687B', weight='bold'),
        tickfont=dict(size=13, color='#8898AA'),
        showgrid=True,
        gridcolor='#F0F2F6',
        zeroline=True,
        zerolinecolor='#E2E8F0',
        zerolinewidth=2,
    ),
    legend=dict(title_text='',font=dict(size=13, color='#5F6B78')),
    margin=dict(l=20, r=20, t=100, b=20),
    hoverlabel=dict(bgcolor="white", font_size=15, bordercolor="#E2E8F0"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

fig.write_html("interactive_graphs/top_10_organizations_by_year.html")

# fig.show()







# Cold War Space Race: USA vs USSR
# The cold war lasted from the start of the dataset up until 1991.
# Create a Plotly Pie Chart comparing the total number of launches of the USSR and the USA
# we are going to to include former Soviet Republics like Kazakhstan when analysing the total number of launches.


cold_war_data = df.groupby(['Country', 'Year'], as_index=False).agg(Total_Launches=('Mission_Status','count'))

# Group Russia and Kazakhstan by Year and sum their launches
soviet_union_data = cold_war_data[cold_war_data["Country"].isin(["Russian Federation", "Kazakhstan"])]
soviet_union_data = soviet_union_data.groupby("Year", as_index=False)["Total_Launches"].sum()

# Add the "Soviet Union" label
soviet_union_data["Country"] = "Soviet Union"

# Append this new data to cold_war_data
cold_war_data = pd.concat([cold_war_data, soviet_union_data], ignore_index=True)

usa_and_soviet = cold_war_data.loc[cold_war_data["Country"].isin(["Soviet Union", "USA"])]

thematic_colors = ['#1A5F7A', '#D9534F']

l_chart = px.line(
    usa_and_soviet,
    x='Year',
    y='Total_Launches',
    color='Country',
    color_discrete_sequence=thematic_colors
)

hover_html = (
    "<b style='font-size:16px; color:#1A252F'>%{data.name}</b><br><br>" +
    "<span style='color:#7F8C8D'>Year:</span> <b style='color:#7D5A50'>%{x}</b><br>" +
    "<span style='color:#7F8C8D'>Total Launches:</span> <b style='color:#7D5A50'>%{y}</b>" +
    "<extra></extra>"
)

l_chart.update_traces(line=dict(width=3),hovertemplate=hover_html)

l_chart.update_layout(
    template='plotly_white',
    title=dict(
        text='<b>The Space Race: USA vs. Soviet Union</b><br>'
             '<span style="font-size:14px; color:#7F8C8D">Annual orbital launch attempts by superpower</span>',
        font=dict(size=22, family='Helvetica Neue, Arial, sans-serif', color='#1A252F'),
        x=0.01,xanchor='left'
    ),

    xaxis=dict(
        title='',
        showgrid=False,
        tickfont=dict(size=14, color='#7D5A50'),
        tickmode='linear',
        dtick=10
    ),

    yaxis=dict(
        title='Number of Launches',
        title_font=dict(size=14, color='#2C3E50', weight='bold'),
        tickfont=dict(size=14, color='#7D5A50'),
        showgrid=True, gridcolor='#F0F2F6',
        zeroline=True, zerolinecolor='#E2E8F0', zerolinewidth=2
    ),
    legend=dict(
        title_text='',
        orientation="h",
        yanchor="bottom", xanchor="right",
        y=1.02,  x=0.98,
        font=dict(size=13, color='#5F6B78'),
        bgcolor="rgba(255, 255, 255, 0)"
    ),
    margin=dict(l=20, r=20, t=100, b=20),
    hoverlabel=dict(bgcolor="white", font_size=13, bordercolor="#E2E8F0"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

# l_chart.write_html("interactive_graphs/usa_vs_soviet.html")

# l_chart.show()





# For Every Year Show which Country was in the Lead in terms of Total Number of Launches up to and including  2020)
# Do the results change if we only look at the number of successful launches?
# Create a Year-on-Year Chart Showing the Organisation Doing the Most Number of Launches
# Which organisation was dominant in the 1970s and 1980s? Which organisation was dominant in 2018, 2019 and 2020?


cntry_and_org_data = df.copy()

# Count total launches per country per year
total_launches_per_year = (cntry_and_org_data
                           .groupby(['Year', 'Country'])
                           .size().reset_index()
                           .rename(columns={0: 'Total_Launches'}))

leading_country_per_year = total_launches_per_year.loc[total_launches_per_year.groupby('Year')['Total_Launches'].idxmax()]

country_colors = {
    'USA': '#1A5F7A',
    'Russian Federation': '#D9534F',
    'Kazakhstan': '#E89694',
    'China': '#F3A712'
}

c_bar = px.bar(
    leading_country_per_year,
    x='Year',
    y='Total_Launches',
    color='Country',
    color_discrete_map=country_colors,
    custom_data=['Country']
)

hover_html = (
    "<b style='font-size:16px; color:#1A252F'>%{customdata[0]}</b><br><br>" +
    "<span style='color:#7F8C8D'>Year:</span> <b style='color:#7D5A50'>%{x}</b><br>" +
    "<span style='color:#7F8C8D'>Total Launches:</span> <b style='color:#7D5A50'>%{y}</b>" +
    "<extra></extra>"
)

c_bar.update_traces( hovertemplate=hover_html, marker_line_width=0)

c_bar.update_layout(
    template='plotly_white',
    title=dict(
        text='<b>Global Leaders in Space Exploration</b><br>'
             '<span style="font-size:14px; color:#7F8C8D">Country with the highest volume of orbital launches per year</span>',
        font=dict(size=22, family='Helvetica Neue, Arial, sans-serif', color='#1A252F'),
        x=0.01,
        xanchor='left'
    ),
    xaxis=dict(
        title='',
        showgrid=False,
        tickfont=dict(size=14, color='#7D5A50'),
        tickmode='linear',
        dtick=10
    ),
    yaxis=dict(
        title='Number of Launches',
        title_font=dict(size=14, color='#2C3E50', weight='bold'),
        tickfont=dict(size=14, color='#7D5A50'),
        showgrid=True, gridcolor='#F0F2F6',
        zeroline=True, zerolinecolor='#E2E8F0', zerolinewidth=2
    ),
    legend=dict(
        title_text='',
        orientation="h",
        yanchor="bottom", xanchor="right",
        y=1.02, x=0.98,
        font=dict(size=13, color='#5F6B78'),
        bgcolor="rgba(255, 255, 255, 0)" # Transparent background
    ),
    margin=dict(l=20, r=20, t=100, b=20),
    hoverlabel=dict(bgcolor="white", font_size=15, bordercolor="#E2E8F0"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)


# c_bar.write_html("interactive_graphs/leading_country_by_year.html")

# c_bar.show()