import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import statsmodels



# Notebook Presentation:
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 125)
pd.set_option('display.width', None)

# Retrieving Data
df_data = pd.read_csv('csv_files/nobel_prize_data.csv')


# Exploring the Initial data
print("\nNobel Prize Data:")
print("Shape of the dataframe:")
print(df_data.shape)
print("\nColumns of the Dataset:")
print(df_data.columns)
print("\nFirst 5 Rows")
print(df_data.head(5))

print("\nOverview of the Dataframe")
print(df_data.info())

# Convert the birth_date column to Pandas Datetime objects
df_data.birth_date = pd.to_datetime(df_data.birth_date)




# Handling with NaN and duplicate values:
print("\nIs there any NaN values?")
print(df_data.isna().values.any())

print("\nIs there any duplicated values?")
print(df_data.duplicated().values.any())


# We can get a count of the NaN values per column using this:
print("\nNumbers of the NaN values per column:")
print(df_data.isna().sum())


# Filtering on the NaN values in the birth date column we see that we get back a bunch of organisations, like the UN or the Red Cross.
columns_to_display = ['year', 'category', 'full_name', 'birth_date', 'birth_country', 'laureate_type','organization_name']


# look what are the other colums when birth date is na:
print("\nThe entries when birth date is empty")
df_no_birthday = df_data.loc[df_data.birth_date.isna()]
print(df_no_birthday[columns_to_display].head())


# we are going to add two Column

# Share percentage which has the laureates' share as a percentage in the form of a floating-point number:
share_of_prize = df_data.prize_share.str.split('/', expand=True)
numerator = pd.to_numeric(share_of_prize[0])
denominator = pd.to_numeric(share_of_prize[1])
df_data['share_pct'] = numerator / denominator

# The ages of Scientists when they won the Nobel Prize.
birth_years = df_data.birth_date.dt.year
df_data['winning_age'] = df_data.year - birth_years

print("\nDescriptive Analysis for the winning Age::")
print(df_data.winning_age.describe())

# Oldest and Youngest Winners

print("\nThe Youngest winner of the Nobel Prize:")
print(df_data.nsmallest(n=1, columns='winning_age').iloc[0])

print("\nThe Oldest Winner of the Nobel Prize:")
print(df_data.nlargest(n=1, columns='winning_age').iloc[0])




# Analysis for the sex of the laureates.

df_gender = df_data.groupby(["sex"], as_index=False).agg({'prize': pd.Series.count})

pie_graph_colors = ['#18BC9C', '#2C3E50', '#E74C3C']

fig = go.Figure(data=[go.Pie(
    labels=df_gender['sex'],
    values=df_gender['prize'],
    hole=0.4,
    textinfo='label+percent',
    textposition='outside',
    textfont=dict(size=16, color='#2C3E50', family='Arial Black'),
    insidetextorientation='radial',
    marker=dict(colors=pie_graph_colors, line=dict(color='#FFFFFF', width=3)),
    pull=[0, 0.05]     # Slightly 'pull' a slice out to highlight it
)])

fig.update_layout(
    title=dict(text="Contribution of Nobel Prizes by Gender", x=0.5, xanchor='center',
        font=dict(size=22, family="Arial Black", color="#E74C3C")),
    annotations=[
        dict(
            text='Nobel<br>Prizes',
            x=0.5, y=0.5,
            font_size=18, font=dict(family="Arial Black", color="#E74C3C"),
            showarrow=False
        )
    ],
    showlegend=False,   # Hiding the egend
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=80, b=40, l=40, r=40)
)

# fig.write_html("interactive_graphs/gender_distribution.html")

# fig.show()


# Female Winners:
# What are the names of the first 3 female Nobel laureates?
print("\nFirst five Women who won Nobel Prizes")
df_women = df_data[df_data.sex == 'Female']
df_women.sort_values('year')
print(df_women[columns_to_display].head(5))

# # to reset ids:
# df_women[["full_name", "birth_country"]][:3].reset_index(drop=True)



# Multiple Winners
# Did some people get a Nobel Prize more than once? If so, who were they?
print("\nMultiple Winners:")

is_winner = df_data.duplicated(subset=['full_name'], keep=False)    # keep=False parameter prevents recurrence

multiple_winners = df_data[is_winner]
print(f'There are {multiple_winners.full_name.nunique()} winners who were awarded the prize more than once.\n')
print(multiple_winners[columns_to_display].sort_values('full_name'))




# Analysis for the Categories:

df_category = df_data.groupby(["category"], as_index=False).agg({'prize': pd.Series.count})

# (Navy, Soft Teal, Coral, Mustard, Slate Purple, Steel Blue)
category_colors = ['#2C3E50', '#18BC9C', '#E74C3C', '#F39C12', '#8E44AD', '#3498DB']

fig = go.Figure(data=[go.Bar(
    x=df_category['category'],
    y=df_category['prize'],
    text=df_category['prize'],
    textposition='outside',
    textfont=dict(size=15, color='#AD8B73', family="Arial, sans-serif"),
    marker=dict(color=category_colors, opacity=0.9, line=dict(color='white', width=1.5)),
    width=0.55
)])

fig.update_layout(
    title=dict(text="Number of Nobel Prizes by Category",
        font=dict(size=25, family="Arial Black", color="#AD8B73"),
        x=0.5,
        xanchor='center'
    ),

    xaxis=dict(
        title=dict(text="Categories", font=dict(family="Arial Black", size=18, color='#AD8B73')),
        tickfont=dict(size=14, color='#2C3E50'),
        categoryorder='total descending',
        showgrid=False,
        linecolor='#BDC3C7',
        linewidth=1
    ),

    yaxis=dict(
        title=dict(text="Number of Prizes", font=dict(family="Arial Black", size=18, color='#AD8B73')),
        tickfont=dict(size=13, color='#AD8B73'),
        showgrid=True,
        gridcolor='#ECF0F1',
        gridwidth=1,
        zeroline=True,
        zerolinecolor='#BDC3C7',
        zerolinewidth=1,
    ),

    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=80, b=40, l=60, r=40),
    showlegend=False
)

# fig.write_html("interactive_graphs/prize_number_category.html")

# fig.show()



pie_graph_colors = ['#18BC9C', '#2C3E50', '#E74C3C']







# Analysis for the categories by men and women
# We are going to Create a plotly bar chart that shows the split between men and women by category.

category_by_gender = df_data.groupby(['category', 'sex'], as_index=False).agg({'prize': pd.Series.count})
category_by_gender.sort_values('prize', ascending=False, inplace=True)

colors = ['#2C3E50', '#18BC9C']  # Navy and Teal

fig = go.Figure()

# Looping through the unique genders to create the stacked sections
for i, gender in enumerate(category_by_gender['sex'].unique()):
    df_subset = category_by_gender[category_by_gender['sex'] == gender]
    fig.add_trace(go.Bar(
        x=df_subset['category'],
        y=df_subset['prize'],
        name=str(gender),  # naming the items
        marker=dict( color=colors[i % len(colors)], line=dict(color='white', width=1)),  # Color and border styling
        text=df_subset['prize'],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(size=12, color='white', family="Arial, sans-serif"),
        width=0.55  # Elegant bar width
    ))

fig.update_layout(
    barmode='stack', # so that we will have two parameters at bars
    title=dict(text="Nobel Prizes by Category and Gender",
               font=dict(size=24, family="Arial Black", color="#E74C3C"),
               pad=dict(b=40), x=0.5, xanchor='center'),

    legend=dict(orientation="h", yanchor="bottom", y=1.02,
                xanchor="center", x=0.5, font=dict(size=15, color='#2C3E50')),

    xaxis=dict(
        title=dict(text="Categories", font=dict(size=15, color='#E74C3C')),
        tickfont=dict(size=13, color='#2C3E50'),
        categoryorder='total descending',
        showgrid=False,
        linecolor='#BDC3C7',
        linewidth=1
    ),

    yaxis=dict(
        title=dict(text="Number of Prizes", font=dict(size=15, color='#E74C3C')),
        tickfont=dict(size=13, color='#2C3E50'),
        showgrid=True,
        gridcolor='#ECF0F1',
        gridwidth=1,
        zeroline=True,
        zerolinecolor='#BDC3C7',
        zerolinewidth=1,
    ),

    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=100, b=40, l=60, r=40)
)

# fig.write_html("interactive_graphs/prize_by_gender_and_category.html")

# fig.show()




# Number of prizes per year

# We are going to count the number of prizes awarded every year.
# We are going to Create a 5 years rolling average of the number of prizes
# Looking at the chart, did the first and second world wars have an impact on the number of prizes being given out?
# What could be the reason for the trend in the chart?


prize_per_year = df_data.groupby(by='year').count().prize
moving_average = prize_per_year.rolling(window=5).mean()

# To create 5-year tick marks on the x-axis, we generate an array using NumPy:
np.arange(1900, 2021, step=5)

fig = go.Figure()

# Scatter graph (dots)
fig.add_trace(go.Scatter(
    x=prize_per_year.index,
    y=prize_per_year.values,
    mode='markers',
    name='Prizes per Year',
    marker=dict(color='#3282B8', size=11, opacity=0.6, line=dict(width=1, color='white')),
    hovertemplate='<b>Year:</b> %{x}<br><b>Prizes:</b> %{y}<extra></extra>'
))

# Rolling Average line
fig.add_trace(go.Scatter(
    x=moving_average.index,
    y=moving_average.values,
    mode='lines',
    name='5-Year Rolling Average',
    line=dict(color='#E23E57', width=3, shape='spline'), # spline smoothes the line
    hoverinfo='skip'    # we would like from hover to focus the data points.
))

# Layout styling
fig.update_layout(
    title=dict(
        text='Number of Nobel Prizes Awarded per Year',
        font=dict(size=20, family="Arial Black", color="#424874"),
        y=0.95, x=0.5,
        xanchor='center', yanchor='top'
    ),
    xaxis_title='', # it is obvious
    yaxis=dict(title=dict(text="Number of Prizes", font=dict(size=15, color='#424874'))),
    template='plotly_white', # a modern white background
    hovermode='x unified',
    legend=dict(    # Legend allignments
        xanchor="left", yanchor="top",
        x=0.02, y=0.95,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="lightgrey",
        borderwidth=1
    ),
    margin=dict(l=60, r=40, t=80, b=60)
)

# Axes arrangements
fig.update_xaxes(
    tickangle=45,
    tickmode='linear',
    tick0=1900, dtick=5,
    showgrid=True, gridcolor='#f0f0f0',
    range=[1900, 2020]
)
fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0')

# fig.write_html("interactive_graphs/prize_per_year.html")

# fig.show()



# Analysis for the sharing of the Nobel Prizes

# We are going to investigate if more prizes are shared than before.
# We can work out the rolling average of the percentage share of the prize.
# If more prizes are given out, perhaps it is because the prize is split between more people.
# To see the relationship between the number of prizes and the laureate share even more clearly we can invert the second y-axis.


yearly_avg_share = df_data.groupby(by='year').agg({'share_pct': pd.Series.mean})
share_moving_average = yearly_avg_share.rolling(window=5).mean()

fig = go.Figure()

# Plotting the line with rolling average
fig.add_trace(go.Scatter(
    x=share_moving_average.index,
    y=share_moving_average['share_pct'],
    mode='lines',
    name='5-Year Moving Average',
    line=dict(color='#2c3e50', width=4, shape='spline'),
    fill='tozeroy',
    fillcolor='rgba(44, 62, 80, 0.05)'
))

fig.update_layout(
    title=dict(
        text='Trend in Sharing Nobel Prizes (5-Year Rolling Average)',
        font=dict(size=20, family="Arial Black", color="#3D566F"),
        x=0.5, y=0.95, xanchor='center', yanchor='top'),

    yaxis=dict(title=dict(
        text='Average Share Percentage',
        font=dict(size=13, family="Arial Black", color="#3D566F")),
        autorange="reversed", showgrid=True,gridcolor='#f0f0f0'),

    xaxis=dict(
        tickmode='linear', tick0=1900,
        dtick=5, tickangle=45,
        showgrid=True, gridcolor='#f0f0f0',
        range=[1900, 2020]),


    xaxis_title='',  # No need to name the x-axis.
    template='plotly_white',
    margin=dict(l=60, r=40, t=80, b=60),
    hovermode='x unified'
)

# fig.write_html("interactive_graphs/share_pct_by_year.html")

# fig.show()




# Analysis for the Countries

# We are going to create a bar plot which shows the top 20 countries with the most Nobel Prizes
# The prize column should contain the total number of prizes won.

top20_countries = df_data.groupby(by='birth_country_current', as_index=False).agg({'prize': pd.Series.count})
top20_countries = top20_countries.sort_values('prize', ascending=False)[:20]

# Just for the coloring of the bars we are going to create a logarithmic scale
top20_countries['log_prize'] = np.log10(top20_countries['prize'])

h_bar = px.bar(
    top20_countries,
    x='prize',
    y='birth_country_current',
    orientation='h',
    text='prize', color='log_prize',
    color_continuous_scale='blugrn',
    title='<b>Top 20 Countries by Number of Nobel Prizes</b>',
)

# Designing the layout
h_bar.update_layout(
    plot_bgcolor='white',paper_bgcolor='white',
    font_family='Arial, Helvetica, sans-serif',
    font_color='#2c3e50',
    title_font_size=22,
    title_x=0.01,
    margin=dict(t=80, l=120, r=50, b=40),
    xaxis_title='', yaxis_title='',
    yaxis=dict(
        categoryorder='total ascending',
        showgrid=False,showline=False,
        ticks='outside', ticklen=7, tickcolor='white',
        tickfont=dict(family='Arial Black', size=13, color='#2c3e50')
    ),
    xaxis=dict(showgrid=True,gridcolor='#f0f0f0', showline=False, zeroline=False, showticklabels=False),
    coloraxis_showscale=False,
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
        '<span style="font-size: 13px;">Total Nobel Prizes: </span>' +
        '<b style="font-size: 14px;">%{x}</b>' +
        '<extra></extra>'
    ),
)

# h_bar.write_html("interactive_graphs/top_20_countries.html")

# h_bar.show()






# Choropleth Map (Real Map)
# We are going to create a choropleth map for the whole world in terms of Nobel winners.

# Creating the dataframe
df_countries = df_data.groupby(['birth_country_current', 'ISO'], as_index=False).agg({'prize': pd.Series.count})
df_countries = df_countries.sort_values('prize', ascending=False)

print("df_countries")
print(df_countries.to_string())

# Add logarithmic column to evenly distribute the color gradient
df_countries['log_prize'] = np.log10(df_countries['prize'])

# 2. Plotting the Choropleth
world_map = px.choropleth(
    df_countries,
    locations='ISO',
    color='log_prize',
    hover_name='birth_country_current',
    custom_data=['prize'],
    color_continuous_scale='tempo',
    title='<b style="color:#152346;">Global Distribution of Nobel Laureates</b>'
)

# Layout adjustments
world_map.update_layout(
    font_family='Arial, Helvetica, sans-serif',
    font_color='#2c3e50',
    title_font_size=22,
    title_x=0.01,
    margin=dict(t=80, l=0, r=0, b=0),
    geo=dict(
        showframe=False,  # remove the border around the world
        showcoastlines=False,  # remove the thick lines
        projection_type='natural earth',  # an earth projection
        bgcolor='rgba(0,0,0,0)',  # transparent background
        lakecolor='#ffffff',  # fill lakes with white to blend in cleanly
    ),

    coloraxis_colorbar=dict(
        title=dict(text="Total Prizes", font=dict(size=14, color='#2c3e50')),
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
    marker_line_width=0.4,  # but hey must be thin

    # Hover arrangements:
    hovertemplate=(
            '<b style="font-size: 14px; color: #152346;">%{hovertext}</b><br>' +
            '<span style="font-size: 13px; color: #555;">Total Nobel Prizes: </span>' +
            '<b style="font-size: 14px; color: #2c3e50;">%{customdata[0]}</b>' +
            '<extra></extra>'
    ),

    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial", bordercolor="#e2e8f0")
)

# world_map.write_html("interactive_graphs/nobel_winners_world_map.html")

# world_map.show()






# Country Bar Chart with Prize Category
# Analysis for country - category (stacked chart)

# we are going to divide up the plotly bar chart to show the which categories made up the total number of prizes.


# Creating the dataset

prize_by_category_and_country = df_data.groupby(['birth_country_current', 'category'], as_index=False).agg({'prize': pd.Series.count})

# Next, we can merge the DataFrame above with the top20_countries DataFrame that we created previously.
# That way we get the total number of prizes in a single column too.

top20_countries = df_data.groupby(by='birth_country_current', as_index=False).agg({'prize': pd.Series.count}).sort_values('prize', ascending=False)[:20]

# This is important since we want to control the order for our bar chart.

df_category_and_country = pd.merge(prize_by_category_and_country, top20_countries, on='birth_country_current')


# change column names
df_category_and_country.columns = ['birth_country_current', 'category', 'cat_prize', 'total_prize']
df_category_and_country.sort_values(by='total_prize', inplace=True)

# color palette for the 6 categories
elegant_palette = ['#2A668F', '#E76F51', '#F4A261', '#2A9D8F', '#E9C46A', '#8AB17D']

# Plotting the bar chart
cat_cntry_bar = px.bar(
    df_category_and_country,
    x='cat_prize',
    y='birth_country_current',
    color='category',
    orientation='h',
    color_discrete_sequence=elegant_palette,
    title='<b style="color:#0F4C75;" >Nobel Prizes by Country and Category</b>'
)

# Layout Design
cat_cntry_bar.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_family='Arial, Helvetica, sans-serif',
    font_color='#2c3e50',
    title_font_size=22,
    title_x=0.01,
    margin=dict(t=110, l=140, r=50, b=40),  # Added top margin (t) to fit the new legend
    xaxis_title='', yaxis_title='',

    yaxis=dict(
        categoryorder='total ascending',
        showgrid=False, showline=False,
        ticks='outside', ticklen=10, tickcolor='white',
        tickfont=dict(size=14, color='#2c3e50')),

    xaxis=dict(showgrid=True, gridcolor='#f0f0f0',showline=False, zeroline=False),

    legend=dict(title='', orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0.01,
        font=dict(size=13, color='#2c3e50'))
)

cat_cntry_bar.update_traces(
    marker_line_color='white',
    marker_line_width=1.5,
    hovertemplate=(
            '<b style="font-size: 14px; color:#0F4C75;">%{y}</b><br>' +
            '<span style="font-size: 13px; color: #555;">%{data.name}: </span>' +
            '<b style="font-size: 14px; color: #2c3e50;">%{x}</b>' +
            '<extra></extra>'),
    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial", bordercolor="#e2e8f0")
)

# cat_cntry_bar.write_html("interactive_graphs/prize_by_country_and_category.html")

# cat_cntry_bar.show()




# Analysis for the prizes by Country over Time

# Every country's fortunes wax and wane over time.
# Investigate how the total number of prizes awarded changed over the years.
# When did the United States eclipse every other country in terms of the number of prizes won?
# Which country or countries were leading previously?


# we are going to calculate the cumulative number of prizes won by each country in every year.
# Again, use the birth_country_current of the winner to calculate this.
# To see how the prize was awarded over time we are going to count the number of prizes by country by year.

prize_by_year = df_data.groupby(by=['birth_country_current', 'year'], as_index=False).count()
prize_by_year = prize_by_year.sort_values('year')[['year', 'birth_country_current', 'prize']]

# Then we can create a series that has the cumulative sum for the number of prizes won.
cumulative_prizes = prize_by_year.groupby(by=['birth_country_current', 'year']).sum().groupby(level=[0]).cumsum()
cumulative_prizes.reset_index(inplace=True)

# .sum() is applied to ensure that numeric columns (like prize) are summed within each group.
# In this case, since there is only one row per group, it won't change the data.
# Second Grouping (groupby(level=[0])):
# This groups the resulting data by the first level of the index (birth_country_current) only.
# The level=[0] argument specifies that only the outermost grouping (country) should be considered, ignoring the year.
# Cumulative Sum (cumsum())
# Calculates the cumulative sum of prizes within each country across the years.


# We group by country, find their max prizes, sort descending, and get the list of names.
country_totals = cumulative_prizes.groupby('birth_country_current')['prize'].max().sort_values(ascending=False)
ordered_countries = country_totals.index.tolist()


country_line = px.line(
    cumulative_prizes,
    x='year',
    y='prize',
    color='birth_country_current',
    hover_name='birth_country_current',
    hover_data={'birth_country_current': False},
    category_orders={"birth_country_current": ordered_countries},
    color_discrete_sequence=px.colors.qualitative.Alphabet
)

country_line.update_layout(
    title="<b>Cumulative Nobel Prizes by Country Over Time</b>",
    template='plotly_white',  # Removing the default  background and gridlines
    font=dict(family="Helvetica, Arial, sans-serif", size=14, color="#333333"),
    title_font=dict(size=18, color="#E84545"),
    xaxis_title='<b style="color:#E84545;">Year</b>',
    yaxis_title='<b style="font-size: 14px; color:#E84545;">Number of Prizes</b>',
    legend_title='<b style="font-size: 14px; color:#E84545;">Country (Ranked by Total)</b>',

    legend=dict(
        yanchor="top", xanchor="left",
        y=1, x=1.02, # positioning the legend outside the plotting area
        font=dict(size=11),
        itemsizing='constant'),

    margin=dict(l=40, r=40, t=60, b=40)
)

country_line.update_xaxes(showgrid=False, showline=True, linewidth=1.5, linecolor='lightgray')
country_line.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', showline=False)

# country_line.write_html("interactive_graphs/prize_by_country_over_years.html")

# country_line.show()







# Nobel by Organizations
# Create a bar chart showing the organizations affiliated with the Nobel laureates

top20_orgs = df_data.organization_name.value_counts()[:20]
top20_orgs.sort_values(ascending=True, inplace=True)

org_bar = go.Figure()

org_bar.add_trace(go.Bar(
    x=top20_orgs.values,
    y=top20_orgs.index,
    orientation='h',
    text=top20_orgs.values,
    textposition='outside', # Puts the number neatly outside the bar
    textfont=dict(family="Arial, sans-serif", size=12, color='#2C3E50'),
    marker=dict(
        color=top20_orgs.values,
        colorscale='temps',
        line=dict(color='rgba(255, 255, 255, 1)', width=1)
    )
))

org_bar.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text='<b>Top 20 Research Institutions</b><br><span style="font-size: 18px; color: #009392;">By Number of Nobel Prizes</span>',
        x=0.02, y=0.95, # Align slightly to the left
        font=dict(family="Arial, sans-serif", size=25, color='#cf597e')),

    yaxis=dict(
        showgrid=False,showline=False, title='',
        tickfont=dict(family="Arial, sans-serif", size=15, color='#34495E')),

    xaxis=dict(showgrid=False, showline=False, showticklabels=False, zeroline=False, title=''),
    margin=dict(l=200, r=50, t=100, b=30),
    height=750
)

# org_bar.write_html("interactive_graphs/top20_organizations.html")

# org_bar.show()



# we are going to Create another plotly bar chart graphing the top 20 organisation cities of the research institutions associated with a Nobel laureate.

top20_org_cities = df_data.organization_city.value_counts()[:20]
top20_org_cities.sort_values(ascending=True, inplace=True)

city_bar = go.Figure()

city_bar.add_trace(go.Bar(
    x=top20_org_cities.values,
    y=top20_org_cities.index,
    orientation='h',
    text=top20_org_cities.values,
    textposition='outside', # Puts the number neatly outside the bar
    textfont=dict(family="Arial, sans-serif", size=12, color='#2C3E50'),
    marker=dict(
        color=top20_org_cities.values,
        colorscale='portland',
        line=dict(color='rgba(255, 255, 255, 1)', width=1)
    )
))

city_bar.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text='<b>Top 20 Research Cities</b><br><span style="font-size: 18px; color: #0c3b88;">By Number of Nobel Prizes</span>',
        x=0.02, y=0.95, # Align slightly to the left
        font=dict(family="Arial, sans-serif", size=25, color='#d91e1e')),

    yaxis=dict(
        showgrid=False,showline=False, title='',
        ticks='outside', ticklen=7, tickcolor='white',
        tickfont=dict(family="Arial, sans-serif", size=16, color='#34495E')),

    xaxis=dict(showgrid=False, showline=False, showticklabels=False, zeroline=False, title=''),
    margin=dict(l=200, r=50, t=100, b=30),
    height=750
)

# city_bar.write_html("interactive_graphs/top20_cities.html")

# city_bar.show()





px.colors.sequential.Plasma
# Would you expect to see the most populous cities producing the highest number of Nobel laureates?
# Create a plotly bar chart graphing the top 20 birth cities of Nobel laureates.
# Use a named colour scale called Plasma for the chart.

top20_birth_cities = df_data.birth_city.value_counts()[:20]
top20_birth_cities.sort_values(ascending=True, inplace=True)

birth_city_bar = go.Figure()

birth_city_bar.add_trace(go.Bar(
    x=top20_birth_cities.values,
    y=top20_birth_cities.index,
    orientation='h',
    text=top20_birth_cities.values,
    textposition='outside', # Puts the number neatly outside the bar
    textfont=dict(family="Arial, sans-serif", size=12, color='#2C3E50'),
    marker=dict(
        color=top20_birth_cities.values,
        colorscale='bluyl',
        line=dict(color='rgba(255, 255, 255, 1)', width=1)
    )
))

birth_city_bar.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    title=dict(
        text='<b>The 20 cities where the most Nobel laureates were born.',
        x=0.02, y=0.95, # Align slightly to the left
        font=dict(family="Arial, sans-serif", size=25, color='#045275')),

    yaxis=dict(
        showgrid=False,showline=False, title='',
        ticks='outside', ticklen=7, tickcolor='white',
        tickfont=dict(family="Arial, sans-serif", size=16, color='#34495E')),

    xaxis=dict(showgrid=False, showline=False, showticklabels=False, zeroline=False, title=''),
    margin=dict(l=200, r=50, t=100, b=30),
    height=750
)

# birth_city_bar.write_html("interactive_graphs/top20_birth_cities.html")

# birth_city_bar.show()



# Sunburst - All in one
#
# Each country has a number of cities, which contain a number of cities, which in turn contain the research organisations.
# The sunburst chart is perfect for representing this relationship.
# It will give us an idea of how geographically concentrated scientific discoveries are!

# First, we are going to Create a DataFrame that groups the number of prizes by organisation.

country_city_org = (df_data
                    .groupby(by=['organization_country', 'organization_city', 'organization_name'], as_index=False)
                    .agg({'prize': pd.Series.count}))

country_city_org = country_city_org.sort_values('prize', ascending=False)
country_city_org['log_prize'] = np.log10(country_city_org['prize'])


burst = px.sunburst(
    country_city_org,
    path=['organization_country', 'organization_city', 'organization_name'],
    values='prize',
    color='log_prize',
    color_continuous_scale='portland',
    title='<b>Global Hubs of Scientific Discovery</b><br><sup>Nobel Prizes by Country, City, and Organization</sup>'
)

burst.update_layout(
    font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif", size=13, color="#444444"),
    title_font=dict(size=22, color="#222222"),
    title_x=0.5, title_y=0.95,
    margin=dict(t=90, l=20, r=20, b=20),
    paper_bgcolor="white",
    coloraxis_showscale=False
)

burst.update_traces(
    textinfo='label+percent parent',
    insidetextorientation='radial',
    marker=dict(line=dict(color='#FFFFFF', width=1.5)),
    hovertemplate=(
        '<b>%{label}</b><br>'
        'Total Nobel Prize: <b>%{value}</b><br>'
        '<i>%{percentParent:.1%} of parent category</i>'
        '<extra></extra>'
    )
)

# burst.write_html("interactive_graphs/sunburst_organization.html")

# burst.show()


# Analysis for the Age of the laureates

sns.set_theme(style="white", context="notebook")
plt.figure(figsize=(12, 6), dpi=300)

ax = sns.histplot(
    data=df_data,
    x='winning_age',
    bins=50,
    color="#3465a4",
    edgecolor="white",
    linewidth=1.5,
    alpha=0.9
)

plt.title('Age distribution of the Nobel Laureates',
          fontsize=22, pad=20, fontweight='bold', color='#F05454')
plt.xlabel('Age', fontsize=15, labelpad=15, fontweight='bold', color='#F05454')
plt.ylabel('Number of Winners', fontsize=15,fontweight='bold', labelpad=15, color='#F05454')

ax.grid(axis='y', color='#dddddd', linestyle='--', alpha=0.8)
ax.tick_params(axis='both', which='major', labelsize=13, colors='#555555', length=0)
ax.set_axisbelow(True)

sns.despine(left=True, bottom=False)
plt.tight_layout()

# plt.show()
plt.close()






# Are Nobel laureates being nominated later in life than before?
# Have the ages of laureates at the time of the award increased or decreased over time?
# According to the best fit line, how old were Nobel laureates in the years 1900-1940 when they were awarded the prize?
# According to the best fit line, what age would it predict for a Nobel laureate in 2020?

# lowess=True
# What it does: Enables Locally Weighted Scatterplot Smoothing (LOWESS), a non-parametric regression technique.
# Purpose: Instead of fitting a straight line (as in standard regression), LOWESS fits a smooth curve that adapts to the data's trends.
# This is especially useful for identifying patterns in scatterplots where the relationship between variables might not be linear.
# Use case: Ideal for visualizing trends in noisy data without assuming a specific type of relationship.

fig_px = px.scatter(
    df_data,
    x='year',
    y='winning_age',
    trendline='lowess',
    hover_name='full_name',
    hover_data={'full_name': False,'category': True, 'year': True, 'winning_age': True},
    opacity=0.6,
    title='Age distribution of the Laureates over Time',
    labels={'year': 'Award Year', 'winning_age': 'Age at Award', 'category': 'Prize Category'},
    template='plotly_white'
)

# We are going extract the traces (scatter and trendline) and design them.
scatter_trace = fig_px.data[0]
trendline_trace = fig_px.data[1]

# scatter points
scatter_trace.marker.size = 10
scatter_trace.marker.color = '#3498DB'
scatter_trace.marker.line.width = 0.8
scatter_trace.marker.line.color = 'DarkSlateGrey'

# Trendlines
trendline_trace.line.color = '#DC3545'
trendline_trace.line.dash = 'dash'
trendline_trace.line.width = 4

# we are going to create shadows effect for the trendlines
shadow_trace = go.Scatter(
    x=trendline_trace.x,
    y=trendline_trace.y,
    mode='lines',
    line=dict(color='rgba(220, 53, 69, 0.25)', width=14),
    hoverinfo='skip',
    showlegend=False
)

# applying the customization.
fig = go.Figure(
    data=[shadow_trace, trendline_trace, scatter_trace],
    layout=fig_px.layout
)

# Layout Design
fig.update_layout(
    font_family="Inter, Helvetica, Arial, sans-serif",
    title_font_size=24,
    title_font_color="#BF092F",
    title_x=0.5,
    xaxis=dict(showgrid=False, zeroline=False, title_font_size=16, title_font_color="#BF092F"),
    yaxis=dict(showgrid=True, gridcolor='#E5E7EB', zeroline=False, title_font_size=16, title_font_color="#BF092F"),
    plot_bgcolor='rgba(0,0,0,0)',
    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Inter, Helvetica, Arial, sans-serif")
)

# fig.write_html("interactive_graphs/winning_age_over_time.html")

# fig.show()





# Age distribution of laureates by category
#
# Which category has the longest "whiskers"?
# In which prize category are the average winners the oldest?
# In which prize category are the average winners the youngest?

fig = px.box(
    df_data,
    x="category",
    y="winning_age",
    color="category",
    title="Age Distribution of Nobel Laureates by Category",
    labels={"category": "Prize Category", "winning_age": "Age at Award"},
    color_discrete_sequence=px.colors.qualitative.Bold,
    template="plotly_white"
)

fig.update_layout(
    font_family="Inter, Helvetica, Arial, sans-serif",
    title_font_size=24, title_font_color="#008695", title_font_family="Arial Black",
    title_x=0.5, # Center the title
    showlegend=False, # No need to show legend
    xaxis=dict(showgrid=False, zeroline=False, title_font_size=16, tickfont=dict(size=12), title_font_color="#008695"),
    yaxis=dict(showgrid=True, gridcolor='#E5E7EB', zeroline=False, title_font_size=16, title_font_color="#008695"),
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=80, b=40, l=40, r=40)
)

# Polish the boxes themselves (line width and outlier styling)
fig.update_traces(
    marker=dict(size=6, opacity=1, line=dict(width=1, color='DarkSlateGrey')),
    line=dict(width=1.5)
)

# fig.write_html("interactive_graphs/winning_age_by_category.html")

# fig.show()






# Now we are going to use Seaborn's .lmplot() and the row parameter to create 6 separate charts for each prize category.
# What are the winning age trends in each category?
# Which category has the age trending up and which category has the age trending down?
# To get a more complete picture, we should look at how the age of winners has changed over time.

with sns.axes_style('whitegrid'):
    bx = sns.lmplot(data=df_data,
               x='year',
               y='winning_age',
               row = 'category',
               lowess=True,
               aspect=2,
               scatter_kws = {'alpha': 0.6},
               line_kws = {'color': 'black'},)

# plt.show()
plt.close()


#This creates line charts for every category.
# aspect=2 means that the width of each subplot will be twice its height.
# The total width of the plot is determined by aspect * height, where height is the default or user-defined height of each facet.


fig = px.scatter(
    df_data,
    x='year',
    y='winning_age',
    color='category',
    trendline='lowess',
    hover_name='full_name',
    hover_data={ 'category': False, 'year': True, 'winning_age': True},
    title='Winning Age Trends by Nobel Prize Category',
    labels={'year': 'Award Year', 'winning_age': 'Age at Award', 'category': 'Prize Category'},
    color_discrete_sequence=px.colors.qualitative.Vivid,
    template='plotly_white'
)
# Designing for the trend lines
fig.update_traces(line=dict(width=5), selector=dict(mode='lines'))

# Designing for the scatter plots.
fig.update_traces(
    marker=dict(size=8, opacity=0.55, line=dict(width=0.5, color='white')),
    selector=dict(mode='markers')
)

# Layout Arrangements
fig.update_layout(
    font_family="Inter, Helvetica, Arial, sans-serif",
    title_font_family="Arial Black", # Keeping your preferred bold title
    title_font_size=24,
    title_font_color="#764e9e",
    title_x=0.5, # Centers the title
    xaxis=dict(showgrid=False, zeroline=False, title_font_size=16, title_font_color="#764e9e"),
    yaxis=dict(showgrid=True, gridcolor='#E5E7EB', zeroline=False, title_font_size=16,  title_font_color="#764e9e"),
    # legend layout:
    legend=dict(
        title_font_family="Inter, Helvetica, Arial, sans-serif",
        font=dict(size=12),
        yanchor="top", xanchor="left",
        y=1, x=1.02, # Locating the legend outside the graph
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#E5E7EB", borderwidth=1
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=80, b=40, l=40, r=120), # Extra right margin to fit the legend safely
    hoverlabel=dict(bgcolor="white", font_size=13)
)

# fig.write_html("interactive_graphs/linear_model_plot_category.html")

# fig.show()