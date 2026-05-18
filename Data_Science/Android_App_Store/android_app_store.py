import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math

from matplotlib.pyplot import legend

# Show numeric output in decimal format e.g., 2.15
pd.options.display.float_format = '{:,.2f}'.format

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Uploading and displaying the data
df_apps = pd.read_csv('csv_files/apps.csv')
print("\nRaw data:Apps:")
print(df_apps.shape)
print(df_apps.head())


# The .sample(n) method will give us n random rows. This is another handy way to inspect our DataFrame.

print("\nSample")
print(df_apps.sample(6))

# Columns (values) of the Dataframe
print("\nColumns (values) of the Dataframe:")
print(df_apps.columns)


# Droping columns:
df_apps.drop(['Last_Updated', 'Android_Ver'], axis=1, inplace=True)


# NaN and Duplicates:
nan_values = df_apps[df_apps.Rating.isna()]
print(nan_values.isna().values.sum())

print("\nNaN values:")
print(nan_values)
df_apps_clean = df_apps.dropna()


# Displaying the duplicated rows
duplicated_rows = df_apps_clean[df_apps_clean.duplicated()]
print("\nDuplicated rows:")
print(duplicated_rows[['App', 'Size_MBs', 'Type', 'Price']].head())


# Selective removing:
# Removing the duplicated data using subset

# Filtering the DataFrame to obtain the desired Section:
df_instagram = df_apps_clean[df_apps_clean.App == 'Instagram']
print("\nInstagram data:")
print(df_instagram)


# Determining the components for duplicate values and removing the values based on these criteria:
identity_of_apps = ['App', 'Type', 'Price']
df_apps_clean = df_apps_clean.drop_duplicates(subset=identity_of_apps)

# Displaying the clean data:
df_instagram_clean = df_apps_clean[df_apps_clean.App == 'Instagram'].head()
print("\nClean Instagram Data:")
print(df_instagram_clean)

print(df_apps_clean.shape)


# Sorting
sorted_by_rating = df_apps_clean.sort_values('Rating', ascending=False)
sorted_by_size = df_apps_clean.sort_values('Size_MBs', ascending=False)
sorted_by_review = df_apps_clean.sort_values('Reviews', ascending=False)

print(sorted_by_review.head(10)[['App', 'Category', 'Rating', 'Reviews', 'Type']])




ratings = df_apps_clean.Content_Rating.value_counts()

fig = px.pie(labels=ratings.index,
             values=ratings.values,
             title="Content Rating",
             names=ratings.index,
             hole=0.4,
             )

fig.update_traces(textposition='outside', textinfo='percent+label', textfont_size=13)

fig.update_layout(
    title=dict(
        text="Content Rating Distribution",
        font=dict(size=22, family="Arial, sans-serif", color='#2C3E50'),
        x=0.5, y=0.95
    ),

    # Adding the text inside the doughnut hole
    annotations=[dict(
        text='Ratings',
        x=0.5, y=0.5,
        font=dict(size=18, color='#7F8C8D', family="Arial"), showarrow=False
    )],

    legend=dict(
        font=dict(size=13, color='#34495E'),
        orientation="v",
        x=1.05, y=0.5
    ),

    margin=dict(t=100, b=40, l=40, r=40),
    showlegend=True,
    paper_bgcolor='white',
    plot_bgcolor='white'
)

# Configure the download button for high resolution
download_config = {
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'Content_Rating_Pie',
        'width': 900, 'height': 600,
        'scale': 3
    }
}

# fig.show(config=download_config)
# fig.write_html("interactive_graphs/content_rating_pie.html")
# This hole creates donut pies.




# Removing commas from the data:

print(df_apps_clean.Installs.describe())

# df_apps_clean.Installs = df_apps_clean.Installs.astype(str).str.replace(',', "")
df_apps_clean.loc[:, 'Installs'] = df_apps_clean['Installs'].astype(str).str.replace(',', "")

df_apps_clean.Installs = pd.to_numeric(df_apps_clean.Installs)


df_installs_count = df_apps_clean[['App', 'Installs']].groupby('Installs').count()
print(df_installs_count.head(10))




# .to_numeric function converts datatype to integer from object.

print(df_apps_clean.Price.describe())

# df_apps_clean.Price = df_apps_clean.Price.astype(str).str.replace('$', "")
df_apps_clean.loc[:, 'Price'] = df_apps_clean['Price'].astype(str).str.replace('$', "")
df_apps_clean.Price = pd.to_numeric(df_apps_clean.Price)


df_apps_clean = df_apps_clean.sort_values('Price', ascending=False)
print(df_apps_clean.head(6))




# Removing the apps which cost more than 250 $

df_apps_clean = df_apps_clean[df_apps_clean['Price'] < 250]
df_apps_clean = df_apps_clean.sort_values('Price', ascending=False)




#Calculating the revenue:

df_apps_clean['Revenue_Estimate'] = df_apps_clean.Installs.mul(df_apps_clean.Price)
df_apps_clean = df_apps_clean.sort_values('Revenue_Estimate', ascending=False)

print(df_apps_clean[['App', 'Price', 'Category', 'Revenue_Estimate']].head(10))



# Let’s analyse this with bar charts and scatter plots and figure out which categories are dominating the market.

# This gives number of unique values:
print(df_apps_clean.Category.nunique())



top10_category = df_apps_clean.Category.value_counts()[:10]
top10_category = top10_category.sort_values(ascending=False)


fig = px.bar(
    x=top10_category.index,
    y=top10_category.values,
    orientation='v', # Vertical allignment
    title="Top 10 App Categories",
    text=top10_category.values, # Add data labels directly to bars
    color=top10_category.index, # To make very distinguished colors
    color_continuous_scale='Agsunset',
)

# Updating the layout for a elegant look
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Helvetica, Arial, sans-serif", size=12, color="#333333"),
    title_font=dict(size=24, color="#111111", family="Helvetica, Arial, sans-serif"),
    margin=dict(l=0, r=20, t=60, b=20),
    xaxis_title="Categories",
    yaxis_title="Number of Apps",
    xaxis_title_font=dict(size=14, family='Arial Black'),
    yaxis_title_font=dict(size=14, family='Arial Black'),
    coloraxis_showscale=True, # Hide color scale
    showlegend=False # Dont show the legend
)

# Adding a little bit of opacity.
fig.update_traces(opacity=0.9)

# fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False) # Hide x-axis entirely
# fig.update_yaxes(showgrid=False, tickfont=dict(size=14, color="#555555")) # Clean up y-axis font

download_config = {
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'top_10_categories',
        'width': 960, 'height': 540,
        'scale': 3
    }
}
# fig.show(config=download_config)
# fig.write_html("interactive_graphs/top_10_categories.html")






# Obtaining the most popular apps by downloads

cat_number = df_apps_clean.groupby('Category').agg({'App': pd.Series.count})
category_installs = df_apps_clean.groupby('Category').agg({'Installs': pd.Series.sum})

# For a clear view, get the most 20 apps.
category_installs_sorted = category_installs.sort_values(by='Installs', ascending=True)[-20:]

print("\nTop 20 App Categories:")
print(category_installs_sorted)


h_bar = px.bar(
    x=category_installs_sorted.Installs,
    y=category_installs_sorted.index,
    orientation='h',
    title='<b>App Category Popularity by Downloads</b>',
    text_auto='.2s', # Automatically formats large numbers (e.g., 1.5B, 500M)
    color_continuous_scale="Teal",
    color=category_installs_sorted.Installs
)


h_bar.update_layout(
    template='plotly_white', # Removes the default gray background
    xaxis_title='',
    yaxis_title='',
    font=dict(family='Inter, Helvetica, Arial, sans-serif', size=13, color='#34495E'),
    title_font=dict(size=20, color='#2C3E50'),
    margin=dict(l=0, r=40, t=60, b=0), # Tightens up the white space
    height=800, # Gives the bars enough room to
    showlegend=False,
    coloraxis_showscale=False
)

h_bar.update_traces(
    textfont_size=14, textangle=0, textposition="outside",
    cliponaxis=False # Ensures labels at the very edge don't get cut off
)

download_config = {
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'app_category_by_downloads',
        'width': 1920, 'height': 1920, 'scale': 3
    }
}

# h_bar.show(config=download_config)
# h_bar.write_html("interactive_graphs/app_category_by_downloads.html")






cat_merged_df = pd.merge(cat_number, category_installs, on='Category', how="inner")
cat_merged_df = cat_merged_df.sort_values('Installs', ascending=False)


print("\n Categories on app and installation numbers:")
print(cat_merged_df)



# Now we can create the chart.
# Note that we can pass in an entire DataFrame and specify which columns should be used for the x and y by column name.

scatter = px.scatter(
    cat_merged_df,
    x='App',
    y='Installs',
    title='Category Concentration: Apps vs. Installs',
    size='App',
    size_max=45,
    hover_name=cat_merged_df.index,
    color=cat_merged_df.Installs,
    color_continuous_scale=px.colors.sequential.Teal,  # Modern, clean color gradient
    template='plotly_white'  # Removes the default gray background
)

# Updating traces to add professional borders and opacity to the bubbles
scatter.update_traces(
    marker=dict(
        line=dict(width=1, color='DarkSlateGrey'),  # Crisp borders around bubbles
        opacity=0.75
    )
)

scatter.update_layout(
    # Center the title and use a clean, modern font
    title=dict(
        font=dict(size=25, family="Helvetica Neue, Helvetica, Arial, sans-serif", color='#2b5876'),
        x=0.5, xanchor='center'
    ),
    # Global font settings
    font=dict(family="Helvetica Neue, Helvetica, Arial, sans-serif", size=12, color='#555555'),

    # X-Axis styling
    xaxis_title="Number of Apps (Lower = More Concentrated)",
    xaxis=dict(
        showgrid=True,
        gridcolor='#EBEBEB',
        gridwidth=1,
        zeroline=False  # Removes the harsh zero line
    ),

    # Y-Axis styling
    yaxis_title="Total Installs",
    yaxis=dict(
        type='log',
        showgrid=True,
        gridcolor='#EBEBEB',
        gridwidth=1,
        griddash='dot',
        zeroline=False
    ),

    xaxis_title_font=dict(size=14, family='Arial Black', color='#2b5876'),
    yaxis_title_font=dict(size=14, family='Arial Black', color='#2b5876'),

    # Cleaning up the colorbar-legend
    coloraxis_colorbar=dict(
        title="Installs",
        thicknessmode="pixels", thickness=15,
        lenmode="pixels", len=300,
        yanchor="middle", y=0.5,
        ticks="outside",
        tickformat=".2s"  # Formats large numbers (e.g., 100M instead of 100,000,000)
    ),

    # Add breathing room around the edges
    margin=dict(l=60, r=40, t=80, b=60)
)

# download_config = {
#     'toImageButtonOptions': {
#         'format': 'png',
#         'filename': 'scatter_category_downloads',
#         'width': 1920, 'height': 1080, 'scale': 3
#     }
# }
# scatter.show()
#
# scatter.write_html("interactive_graphs/scatter_category_downloads.html")









# Analyzing Genres
# We somehow need to separate the genre names to get a clear picture.
print(df_apps_clean.Genres.nunique())

df_genres_count = (df_apps_clean.Genres.value_counts())
print(df_genres_count.sort_values(ascending=False).tail())

# print(df_apps_clean.head())

genres_list = df_apps_clean.Genres.str.split(';', expand=True).stack()
num_genres = genres_list.value_counts().sort_values(ascending=False)

print(num_genres.shape)
print(len(num_genres))
print(num_genres.head())

# lets create a graph for most 20 popular genres on App store
top_20 = num_genres[:20].sort_values(ascending=True)

print("\n most poulor genres in google play store:")
print(top_20.sort_values(ascending=False))

bar = px.bar(
    x=top_20.values,
    y=top_20.index,
    orientation='h',  # horizontal alignment
    title='Top 20 App Genres',
    text=top_20.values,  # Direct labeling on the bars
    color_continuous_scale=px.colors.sequential.Bluyl,
    color= top_20.values
)

bar.update_layout(
    template='plotly_white', # a white background
    title_font=dict(size=24, family='Arial, sans-serif', color='#2C3E50'),
    title_x=0.02,  # Align title neatly with the chart
    xaxis_title='Number of Apps',
    yaxis_title='', # We dont need y axis title
    font=dict(family='Arial, sans-serif', size=13, color='#555555'),

    # Cleaning up the axes
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(showgrid=False, ticklabelposition="outside"),

    margin=dict(l=10, r=40, t=70, b=20)
)

# Formating the bars
bar.update_traces(
    textposition='outside',
    marker_line_width=0,  # Removes the border around bars for a flatter, modern look
    textfont_size=12
)

# bar.show()
# bar.write_html("interactive_graphs/top_20_app_genres.html")








# Now lets dealing with types (free or paid) of apps

print("\nDistribution of Apps:")
print(df_apps_clean.Type.value_counts())


df_free_vs_paid = df_apps_clean.groupby(["Category", "Type"], as_index=False).agg({'App': pd.Series.count})

print("\ngrouping by free and paid")
print(df_free_vs_paid.shape)
print(df_free_vs_paid.head(60))



# Creating bar chart for this type data:
custom_colors = {'Free': '#2A4B7C', 'Paid': '#E07A5F'}

g_bar = px.bar(
    df_free_vs_paid,
    x='Category',
    y='App',
    color='Type',
    barmode='group',
    color_discrete_map=custom_colors,  # Apply the custom palette
)

g_bar.update_layout(
    template='plotly_white',

    font=dict(family="Inter, Roboto, Arial, sans-serif", size=13, color="#444444"),

    title={
        'text': '<b>Free vs Paid Apps by Category</b>',
        'y': 0.95,
        'x': 0.05,
        'xanchor': 'left',
        'yanchor': 'top',
        'font': dict(size=22, color='#222222')
    },


    legend=dict(
        title=None,
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),

    # Streamlined X-Axis
    xaxis=dict(
        title=None,  # "Category" is obvious
        categoryorder='total descending',
        tickangle=-45,
        showgrid=False,
        showline=True,
        linecolor='#DDDDDD',
        linewidth=1
    ),

    # Refined Y-Axis
    yaxis=dict(
        title='Number of Apps (Log Scale)',
        type='log',
        showgrid=True,
        gridcolor='#F0F0F0',  # Very faint gridlines
        zeroline=False
    ),

    # For a cleaner interactivity:
    hovermode='x unified',

    margin=dict(t=100, b=50, l=60, r=40)
)

g_bar.update_traces(marker_line_width=0, opacity=0.9)

# g_bar.show()
# g_bar.write_html("interactive_graphs/free_vs_paid_apps.html")





# Create a box plot that shows the number of Installs for free versus paid apps.
# How does the median number of installations compare? Is the difference large or small?


box = px.box(
    df_apps_clean,
    y='Installs',
    x='Type',
    color='Type',
    notched=True,
    points='all',  # It should display all the install numbers
    title='<b>How Many Downloads are Paid Apps Giving Up?</b>', # Here, we are using html tag.
    template='plotly_white', # white background
    color_discrete_sequence=['#2C3E50', '#18BC9C'] # Dark blue and green palette
)

box.update_layout(
    yaxis=dict(
        type='log',
        title='Number of Installs (Log Scale)',
        showgrid=True,
        gridcolor='#EBF0F8', # Subtle gridlines
        zeroline=False,
    tickformat=',' # Adds commas to y-axis numbers for readability
    ),
    xaxis=dict( title='', showgrid=False),
    title_x=0.5, title_font_size=20,
    showlegend=False,
    margin=dict(t=80, b=40, l=60, r=40),
    hoverlabel=dict(
        bgcolor="white", font_size=14, font_family="Arial"
    )
)

box.update_traces(
    marker=dict(opacity=0.5, size=4),
    line=dict(width=2),
    # Simplifying hover text:
    hovertemplate="<b>%{y:,.0f}</b> Installs<extra></extra>"
)

# box.show()
# box.write_html("interactive_graphs/box_plot_free_vs_paid_apps.html")





# Looking at the hover text, how much does the median app earn in the Tools category?

# Filtering the data for paid apps:
df_paid_apps = df_apps_clean[df_apps_clean['Type'] == 'Paid']

box = px.box(
    df_paid_apps,
    x='Category',
    y='Revenue_Estimate',
    title='Estimated Revenue of Paid Apps by Category',
    color_discrete_sequence=['#F75270']
)

box.update_layout(
    template='plotly_white', # white background
    title={
        'y': 0.95, 'x': 0.5,
        'xanchor': 'center', 'yanchor': 'top',
        'font': dict(size=20, color='#C80000', family="Helvetica, Arial Black, sans-serif")
    },
    xaxis_title='App Category',
    yaxis_title='Revenue Estimate (USD, Log Scale)',
    xaxis_title_font=dict(size=13, family='Arial Black', color='#C80000'),
    yaxis_title_font=dict(size=13, family='Arial Black', color='#C80000'),

    xaxis=dict(
        categoryorder='max descending',
        tickangle=-45,
        showline=True,
        linewidth=1,
        linecolor='lightgrey'
    ),

    yaxis=dict(
        type='log',
        showgrid=True,
        gridcolor='#f0f0f0',
        showline=True,
        linewidth=1,
        linecolor='lightgrey'
    ),

    hoverlabel=dict(
        bgcolor="white", font_color="#C80000",
        font_size=14, font_family="Arial"
    ),

    margin=dict(l=60, r=40, t=80, b=120)
)

box.update_traces(
    marker=dict(size=5, opacity=0.6, color='#C80000'),
    line=dict(width=1.5),
    hovertemplate="<b>%{y:,.0f}</b> Installs<extra></extra>"
)

# box.show()
# box.write_html("interactive_graphs/revenue_by_category.html")






# What is the median price for a paid app?
# Then compare pricing by category by creating another box plot.
# Examine the prices (instead of the revenue estimates) of the paid apps.
# I recommend using {categoryorder':'max descending'} to sort the categories.


df_paid_apps = df_apps_clean[df_apps_clean['Type'] == 'Paid']

print(df_paid_apps.Price.describe())


# Create the base plot with a cleaner template and professional color

box = px.box(df_paid_apps,
             x='Category',
             y="Price",
             title='<b>Distribution of Prices of Paid Apps by Category</b>',
             template='plotly_white',
             color_discrete_sequence=['#748DAE'])


box.update_layout(
    font=dict(family="Arial, Helvetica, sans-serif", size=12, color="#333333"),
    title_x=0.5,
    title_font_size=18,
    xaxis_title='<b>App Category</b>',
    yaxis_title='<b>Price (USD)</b>',

    xaxis=dict(
        categoryorder='max descending',
        tickangle=-45, # Angles the category labels so they don't overlap
        showgrid=False # Removes vertical grid lines to reduce clutter
    ),

    yaxis=dict(
        type='log',
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E7EB',
        zeroline=False
    ),

    margin=dict(t=80, b=80, l=60, r=40),
    showlegend=False,

    hoverlabel=dict(
        bgcolor="white", font_color="#213448",
        font_size=14, font_family="Arial"
    ),

)

# Refine the look of the boxes and outlier points
box.update_traces(
    marker=dict(size=5, opacity=0.6, color='#213448'),  # Contrast color for outliers
    line=dict(width=1.5),
    hovertemplate="<b>%{y:,.0f}</b> Installs<extra></extra>"
)

# box.show()
# box.write_html("interactive_graphs/prices_by_category.html")
