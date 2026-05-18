import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pandas.plotting import register_matplotlib_converters
from matplotlib.ticker import FuncFormatter
register_matplotlib_converters()
import matplotlib.ticker as ticker
import textwrap

# Notebook Presentation
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


data = pd.read_csv('csv_files/movies_box_office_figures.csv')

# How many rows and columns does the dataset contain?
print("\nShape of the data:")
print(data.shape)

print("\nFirst entries of the data:")
print(data.head())

print("\nLast entries of the data:")
print(data.tail())

# Are there any NaN values present?
print("\nIs There any NaN values in the data:")
print(data.isna().values.any())

# Are there any duplicate rows?
print("\nIs There any duplicated values in the data:")
print(data.duplicated().values.any())

# Inspection of the dataframe
print(data.info())


# Conversion of string values into numeric datatype
# Note that domestic in this context refers to the United States.

chars_to_remove = [',', '$']
columns_to_clean = ['USD_Production_Budget', 'USD_Worldwide_Gross', 'USD_Domestic_Gross']

for col in columns_to_clean:
    for char in chars_to_remove:
        # Replace each character with an empty string
        data[col] = data[col].astype(str).str.replace(char, "")

    # Convert column to a numeric data type
    data[col] = pd.to_numeric(data[col])


# Convert the Release_Date column to a Pandas Datetime type.
data.Release_Date = pd.to_datetime(data.Release_Date)


print("Infos of the data:")
print(data.info())


print("\nDescriptive analysis of the dataframe")
columns_to_analyze = ["USD_Production_Budget", "USD_Worldwide_Gross", "USD_Domestic_Gross"]
print(data[columns_to_analyze].describe())


# Now we can investigate the data set more thoroughly.

# What is the average production budget of the films in the data set?
print(f"\nMean budget: $ {data.USD_Production_Budget.mean()}")

# What is the average worldwide gross revenue of films?
print(f"Mean worldwide gross revenue: $ {data.USD_Worldwide_Gross.mean()}")

# What were the minimums for worldwide and domestic revenue?
print(f"Minimum revenue: $ {data.USD_Domestic_Gross.min()}")


# Finding particular entries
# Movie with the lowest budget:
movie_lowest_budget = data.USD_Production_Budget == 1100.00
print("\nThe movie with the lowest Budget:")
print(data[movie_lowest_budget])

#Movie with the highest budget:
movie_highest_budget = data.USD_Production_Budget == 425000000.00
print("\nThe movie with the highest Budget:")
print(data[movie_highest_budget])



# How many films grossed $0 domestically (i.e., in the United States)?
# What were the highest budget films that grossed nothing?

non_profit_movies_usa = data[data.USD_Domestic_Gross == 0]
non_profit_movies_usa = non_profit_movies_usa.sort_values('USD_Production_Budget', ascending=False)

print("\nShape of the dataframe:")
print(non_profit_movies_usa.shape)
print("\nFirst five entries:")
print(non_profit_movies_usa.head())


# How many films grossed $0 im worldwide (i.e., in the United States)?

non_profit_movies_worldwide = data[data.USD_Worldwide_Gross == 0]
non_profit_movies_worldwide = non_profit_movies_worldwide.sort_values('USD_Production_Budget', ascending=False)

print("\nShape of the dataframe:")
print(non_profit_movies_worldwide.shape)
print("\nRandom five entries:")
print(non_profit_movies_worldwide.sample(5))




# Filtering based on multiple conditions
# For example, films which made money internationally, but had zero box office revenue in the United States:

# international_movies = data.loc[(data.USD_Domestic_Gross == 0) & (data.USD_Worldwide_Gross != 0)] # alt. way
international_movies = data.query('USD_Domestic_Gross == 0 and USD_Worldwide_Gross != 0')
international_movies = international_movies.sort_values('USD_Worldwide_Gross', ascending=False)

print("\nShape of the dataframe:")
print(international_movies.shape)

print("\nFirst entries of the dataframe:")
print(international_movies.head(11))



# Cleaning the dataframe:

# Identifying which films were not released yet as of the time of data collection (May 1st, 2018).
# We are going to remove these movies.

# First, create the time stamp:
data_retrieving_date = pd.Timestamp('2018-5-1')

no_revenue_data_movies = data[data.Release_Date >= data_retrieving_date]
no_revenue_data_movies = no_revenue_data_movies.sort_values("USD_Production_Budget", ascending=False)

print("\nMovies that haven't been released yet::")
print("\nShape of the dataframe:")
print(no_revenue_data_movies.shape)
print("\nSome of these movies")
print(no_revenue_data_movies.head())


# There are also some films that were produced before our data collection date;
# although they were ready for release,
# they were not released due to production issues and therefore generated no revenue.


non_released_movies = data.query('USD_Worldwide_Gross == 0 and Release_Date < @data_retrieving_date')
non_released_movies = non_released_movies.sort_values("USD_Production_Budget", ascending=False)

print("\nMovies that were not released due to the issues:")
print("\nShape of the dataframe:")
print(non_released_movies.shape)
print("\nSome of these movies")
print(non_released_movies.head())


# We are going to remove them from the dataframe:
clean_data = data.drop(no_revenue_data_movies.index)
clean_data = clean_data.drop(non_released_movies.index)


remaining_movies = clean_data.shape[0]
print(f"The clean DataFrame now contains {remaining_movies} movies that are ready for the analysis.")


# Profit Analysis

# Creating a new column for profits:
# Profit = worldwide_gross = Domestic Gross + International gross
clean_data['Profit'] = clean_data.USD_Worldwide_Gross - clean_data.USD_Production_Budget

#Inspection of Profit:
print("\nDescriptive Analysis for Profit:")
print(clean_data[['USD_Production_Budget', 'Profit']].describe())



# Now, we can calculate the percentage of films that did not break even at the box office?
# We already saw that more than the bottom quartile of movies appears to lose money when we ran .describe().
# However, what is the true percentage of films where the costs exceed the worldwide gross Profit?

unprofitable_films = clean_data[clean_data.Profit < 0]
pct_loss_movies = len(unprofitable_films) / len(clean_data) * 100
print(f"% {pct_loss_movies:.4}")


# Creating another column for profit margins (as percentages)
clean_data['Profit_Margin'] = (clean_data.Profit / clean_data.USD_Production_Budget) * 100
clean_data = clean_data.sort_values('Profit_Margin', ascending=False)
print("\nProfit Margins:")
print(clean_data.head(9))


# Dropping sceptical data
deep_throat_1972 = clean_data[clean_data.Rank == 5356]
clean_data.drop(deep_throat_1972.index, inplace=True)
print("\nWithout Deep Throat(1972):")
print(clean_data.head())

print("\nProfit Margin Descriptive Analysis:")
print(clean_data['Profit_Margin'].describe())


# Now we can Visualize the data:🔴⚫⚪

# Top 20 Movies with the highest budgets:
top_15_budget = clean_data.sort_values('USD_Production_Budget', ascending=False)[:15]

sns.set_theme(style="whitegrid", context="talk")
fig, ax = plt.subplots(figsize=(16, 8), dpi=300)

sns.barplot(
    x=top_15_budget.Movie_Title,
    y=top_15_budget.USD_Production_Budget,
    hue=top_15_budget.Movie_Title,
    palette="Set2",
    edgecolor=".2",
    width=0.75,
    legend=False
)

plt.title('Top 15 Movies with the Highest Production Budgets', fontsize=22, fontweight='bold', pad=25, color='#222222')
plt.xlabel('')
plt.ylabel('Production Budget', fontsize=12, fontweight='bold', labelpad=10)
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12)

# wrap labels
labels = ax.get_xticklabels()
new_labels = [textwrap.fill(label.get_text(), 10) for label in labels]
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(new_labels)

# formatting the axes for money-wise designing (Converts numbers to $M and $B)
def currency_formatter(x, pos):
    if x >= 1e9:
        return f'${x*1e-9:.1f}B'
    elif x >= 1e6:
        return f'${x*1e-6:.0f}M'
    elif x == 0:
        return '$0'
    return f'${x}'

ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
ax.yaxis.grid(True, alpha=0.25)
ax.set_axisbelow(True)

sns.despine(left=True, top=True, right=True)
plt.tight_layout()

# plt.show()
plt.close()




# Movies with the highest profits:

# Top 15 Movies with the highest profits:
top_15_profit = clean_data.sort_values('Profit', ascending=False)[:15]

sns.set_theme(style="whitegrid", context="talk")
fig, ax = plt.subplots(figsize=(16, 8), dpi=300)

sns.barplot(
    x=top_15_profit.Movie_Title,
    y=top_15_profit.Profit,
    hue=top_15_profit.Movie_Title,
    palette="muted",
    edgecolor=".2",
    width=0.75,
    legend=False
)

plt.title('Top 15 Movies with the Highest Box-Office Profit', fontsize=22, fontweight='bold', pad=25, color='#222222')
plt.xlabel('')
plt.ylabel('Profit', fontsize=12, fontweight='bold', labelpad=10)
plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12)

# wrap labels
labels = ax.get_xticklabels()
new_labels = [textwrap.fill(label.get_text(), 10) for label in labels]
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(new_labels)

# formatting the axes for money-wise designing (Converts numbers to $M and $B)
def currency_formatter(x, pos):
    if x >= 1e9:
        return f'${x*1e-9:.1f}B'
    elif x >= 1e6:
        return f'${x*1e-6:.0f}M'
    elif x == 0:
        return '$0'
    return f'${x}'

ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
ax.yaxis.grid(True, alpha=0.25)
ax.set_axisbelow(True)

sns.despine(left=True, top=True, right=True)
plt.tight_layout()

# plt.show()
plt.close()

print("Graph 1:")
print("\n Top 15 Profit movie:")
print(top_15_profit[['Release_Date','Movie_Title', 'USD_Production_Budget']])





#  The movies that had a budget over the mean amount at budgest had the biggest profit margings

mean_budget_at_all_movies = 30000000

# movies_over_avg = clean_data[clean_data.USD_Production_Budget > mean_budget_at_all_movies]
movies_over_avg = clean_data.query('USD_Production_Budget >= @mean_budget_at_all_movies')

print("\nNumber of movies over the average production budget:")
print(movies_over_avg.shape)

movies_over_avg_profit = movies_over_avg.sort_values('Profit_Margin', ascending=False)[:20]
movies_over_avg_profit = movies_over_avg_profit.sort_values('Profit_Margin', ascending=True) # it should be descending for horizontal graph

# print("\nMovies over average budget:")
# print(movies_over_avg_profit.head(20))



# This will be an interactive data, therefore we will make some arrangements

# We are going to display the release years of related movies along with the graph.
# This converts release dates to release years
release_years = pd.to_datetime(movies_over_avg_profit['Release_Date']).dt.year

# We are going to display these parameters at hovering option for particular values.
display_components = list(zip(release_years,
                              movies_over_avg_profit['USD_Production_Budget'],
                              movies_over_avg_profit['Profit']))

bar = px.bar(
    movies_over_avg_profit,
    x='Profit_Margin',
    y='Movie_Title',
    orientation='h',
    color='Profit_Margin',
    color_continuous_scale='phase',
    text=movies_over_avg_profit['Profit_Margin'], # Display the profit margins
)

# Options for styling, text formatting, and hover template
bar.update_traces(
    texttemplate='<b>%{text:,.0f}%</b>', # Formatting profit margins to percentages.
    textposition='outside', textfont_size=12, marker_line_width=0,  # Arrangements for bars.
    customdata=display_components, # These are the arrangements for hover display
    hovertemplate=(
        "<b>%{y}</b><br>" +
        "Release Year: %{customdata[0]}<br>" +
        "Budget: $%{customdata[1]:,.0f}<br>" +
        "Profit: $%{customdata[2]:,.0f}" +
        "<extra></extra>"
    )
)


bar.update_layout(
    template='plotly_white',
    title=dict(text='<b>Top 20 Movies with the Highest Profit Margins</b>',
               font=dict(size=26, family='Verdana', color='#9e48d7'), x=0.02),
    xaxis_title='', yaxis_title='', # No title they are obvious
    font=dict(family='Arial, sans-serif', size=13, color='#555555'),
    showlegend=False, # No legend
    coloraxis_showscale=False, # No coloraxis
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, ticklabelposition="outside", ticklabelstandoff=13, tickfont=dict(size=14, family="Arial Black", color='black')),
    yaxis=dict(showgrid=False, ticklabelposition="outside", ticklabelstandoff=7, tickfont=dict(size=13, family="Arial Black", color='black')),
    margin=dict(l=10, r=70, t=70, b=20),

)


# bar.write_html("interactive_graphs/top_20_profit_margin_movies.html")
#
# bar.show()

print("Graph 2:")
print("\n Top 20 highest Profit margin movie:")
print(movies_over_avg_profit)





# Movies with the biggest deficits:

movies_biggest_loss = clean_data.sort_values('Profit', ascending=True)[:20]

# Creating absolut loses column to design the graph more easyl:
movies_biggest_loss['Absolute_Loss'] = movies_biggest_loss['Profit'].abs()
movies_biggest_loss = movies_biggest_loss.sort_values(by='Absolute_Loss', ascending=False)


red_colors = ['#E50505', '#CC0404', '#C00404', '#B00404', '#A00404', '#930303', '#830303', '#6E0202']
# Again, this will be an interactive graph:

# We are going to display these parameters at hovering option for particular values.
display_components = list(zip(release_years,
                              movies_biggest_loss['USD_Production_Budget'],
                              movies_biggest_loss['USD_Worldwide_Gross'],
                              movies_biggest_loss['Profit'],
                              movies_biggest_loss['Profit_Margin']))

bar = px.bar(
    movies_biggest_loss,
    x='Absolute_Loss', # This forces bars to start on the left and go right
    y='Movie_Title',
    orientation='h',
    color='Absolute_Loss',
    color_continuous_scale=red_colors
)

bar.update_traces(
    text=movies_biggest_loss['Profit'],
    texttemplate='<b>%{text:$,.3s}</b>',
    textposition='outside',
    textfont=dict(size=12, family='Inter, Arial, sans-serif', color='#333333'),
    marker_line_width=0,
    customdata=display_components,
    hovertemplate=(
        "<b style='font-size:15px; color:#1A1A1A;'>%{y}</b><br><br>" +
        "<span style='color:#555555;'>Release Year:</span> <b style='color:#1A1A1A;'>%{customdata[0]}</b><br>" +
        "<span style='color:#555555;'>Budget:</span> <b style='color:#1A1A1A;'>%{customdata[1]:$,.0f}</b><br>" +
        "<span style='color:#555555;'>Worldwide Gross:</span> <b style='color:#1A1A1A;'>%{customdata[2]:$,.0f}</b><br>" +
        "<span style='color:#D32F2F;'>Loss:</span> <b style='color:#D32F2F;'>%{customdata[3]:$,.0f}</b><br>" +
        "<span style='color:#555555;'>Loss Rate:</span> <b style='color:#1A1A1A;'>%{customdata[4]:.1f}%</b><br>" +
        "<extra></extra>"
    )
)

bar.update_layout(
    template='plotly_white',
    title=dict(
        text='<b>Top 20 Movies with the Biggest Losses</b>', x=0.02, y=0.95,
        font=dict(size=22, family='Inter, Arial, sans-serif', color='#c60404')),
    xaxis_title='', yaxis_title='',
    font=dict(family='Inter, Arial, sans-serif', size=13, color='#555555'),
    showlegend=False,
    coloraxis_showscale=False,
    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, ticklabelstandoff=10,
               tickfont=dict(size=14, family="Arial Black", color='black')),
    yaxis=dict(showgrid=False, ticklabelposition="outside", ticklabelstandoff=5,
               autorange="reversed", linecolor='#E0E0E0', linewidth=1,
               tickfont=dict(size=14, family="Arial Black", color='black')),
    margin=dict(l=10, r=90, t=80, b=20),
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#E0E0E0",
        font_size=13,
        font_family="Inter, Arial, sans-serif"
    )
)

# bar.write_html("interactive_graphs/top_20_losses_movies.html")

# bar.show()



print("Graph 3:")
print("\n Top 20 highest losses movie:")
print(movies_biggest_loss)



# disappointment_movies = clean_data.query('USD_Production_Budget > 100000000 and Profit < 0')
# disappointment_movies.sort_values('USD_Production_Budget', ascending=False, inplace=True)
# print("\nMovies with budgets exceeding $100 million that lost money:")
# print(disappointment_movies.shape)
# print(disappointment_movies)











# Budget - Revenue Scatter Graph
sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#FBFFFC", "figure.facecolor": "#ffffff"})
fig, ax = plt.subplots(figsize=(16, 8), dpi=300)

scatter = sns.scatterplot(
    data=clean_data,
    x='USD_Production_Budget',
    y='USD_Worldwide_Gross',
    hue='Profit',
    size='Profit',
    sizes=(1, 1000),       # arranging bubble sizes
    alpha=0.6,             # Transparency to handle the overlapping points
    palette="crest",       # Elegant blue-green modern palette
    edgecolor="white",     # Slight white border around bubbles for crispness
    linewidth=0.5,
    ax=ax
)

# formatting the axes for money-wise designing (Converts numbers to $M and $B)
def currency_formatter(x, pos):
    if x >= 1e9:
        return f'${x*1e-9:.1f}B'
    elif x >= 1e6:
        return f'${x*1e-6:.0f}M'
    elif x == 0:
        return '$0'
    return f'${x}'

ax.xaxis.set_major_formatter(FuncFormatter(currency_formatter))
ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))

# setting limits just for the arrangement at the bottom of the graph
ax.set_ylim(-50000000, 3000000000)
ax.set_xlim(-10000000, 450000000)

# Axis labels
ax.set_xlabel('Production Budget', fontsize=18, fontweight='bold', color='#405680', labelpad=20)
ax.set_ylabel('Worldwide Gross Revenue', fontsize=18, fontweight='bold', color='#405680', labelpad=20)

# main and subtitles
fig.text(0.08, 0.96, 'Financial Performance of Movies', fontsize=25, fontweight='bold', color='#405680')
fig.text(0.08, 0.92, 'Comparing Production Budgets to Worldwide Gross and Profitability', fontsize=15, color='#405680')

# arrangement for the legend
legend = ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, title="Profit", title_fontsize=12, labelspacing=1.7)
legend.get_frame().set_linewidth(0.0) # Remove border around legend

# Cleaning up some borders and refining grid lines
sns.despine(left=True, bottom=False)
ax.grid(axis='y', linestyle='--', alpha=0.7) # Keep horizontal grid lines
ax.grid(axis='x', visible=False)             # Removing vertical lines
plt.tight_layout(rect=[0, 0, 0.95, 0.9])

# plt.show()
plt.close()




# Relation between year budget and profit of movies

sns.set_theme(style="whitegrid", font="sans-serif")
plt.figure(figsize=(16, 8), dpi=300)

ax = sns.scatterplot(
    data=clean_data,
    x='Release_Date',
    y='USD_Production_Budget',
    hue='Profit', size='Profit',
    sizes=(20, 700),     # a big size range for better contrast
    alpha=0.75,          # a little bit of transparency to see the overlapped bubbles
    palette="crest",
    edgecolor="white",
    linewidth=0.5
)

# Arrangements for y axis:
def currency_formatter(x, pos):
    if x >= 1e9:
        return f'${x*1e-9:.1f}B'
    elif x >= 1e6:
        return f'${x*1e-6:.0f}M'
    return f'${x:,.0f}'
ax.yaxis.set_major_locator(ticker.MultipleLocator(50_000_000))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(currency_formatter))

ax.set_title("Movie Budgets Over the Years", fontsize=25, fontweight='bold', color='#405680', pad=20)
ax.set_xlabel("Release Year", fontsize=18, fontweight='bold', color='#405680', labelpad=14)
ax.set_ylabel("Production Budget", fontweight='bold', fontsize=18, color='#405680', labelpad=14)

# arrangement for the legend:
legend = ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, title="Profit", title_fontsize=12, labelspacing=1.5)
legend.get_frame().set_linewidth(0.0) # Remove border around legend

# adjusting the layout
sns.despine(left=False, bottom=False)
plt.tight_layout(rect=[0, 0, 0.95, 0.9])

# plt.show()
plt.close()




year_2000 = pd.Timestamp('2000-01-01')
revolutionary_movie = clean_data.query('USD_Production_Budget >= 200000000 and Release_Date < @year_2000')
print("\nThe first film with a budget of over $200 million that went on to generate enormous profits:")
print(revolutionary_movie.iloc[0])








# Converting the date data to Decades:

# We are going to create a column in data_clean that has the decade of the movie release.
# To create a DatetimeIndex, we just call the constructor and provide our release date column as an argument.

release_date_indexes = pd.DatetimeIndex(clean_data.Release_Date)
years = release_date_indexes.year

decades = years//10*10
clean_data['Decade'] = decades

old_films = clean_data[clean_data.Decade <= 1960]
new_films = clean_data[clean_data.Decade > 1960]


old_films = old_films.sort_values('USD_Worldwide_Gross', ascending=False)
print("\nMovies before 1960 with biggest revenues:")
print(old_films.head())




# Plotting Linear Regressions with Seaborn
# Visualizing the relationship between the budget and the revenue using linear regression.
# we are going to use .regplot() function.
# This creates a scatter plot and draws a linear regression line together with the confidence interval at the same time.


sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#fbfbfb", "grid.color": "#e9ecef"})
plt.figure(figsize=(16, 8), dpi=300)

ax = sns.regplot(
    data=old_films,
    x='USD_Production_Budget',
    y='USD_Worldwide_Gross',
    color="#2c3e50",
    line_kws={'color': '#DC143C', 'linewidth': 3 },  # adjustments for liner regression line
    scatter_kws={
        'alpha': 0.6,          # we would like to display the dots a little bit transparent.
        's': 90,               # this arranges marker sizes
        'edgecolor': 'white',  # a subtle border for the dots
    }
)

# this function converts raw numbers into clean texts
def currency_formatter(x, pos):
    if x >= 1e9:
        return f'${x*1e-9:.1f}B'
    elif x >= 1e6:
        return f'${x*1e-6:.0f}M'
    return f'${x:,.0f}'

ax.xaxis.set_major_formatter(ticker.FuncFormatter(currency_formatter))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(currency_formatter))

# plt.suptitle('Production Budget vs. Worldwide Gross', fontsize=24, fontweight='bold', pad=20, color='#333333', loc='left')

plt.suptitle('Movies Before 1960',
             fontsize=18, fontweight='bold', color='#333333',
             x=0.07, y=0.98, ha='left')

plt.title('Production Budget vs. Worldwide Gross', fontsize=22, fontweight='bold', pad=20, color='#DC143C', loc='left')
plt.xlabel('Production Budget ($)', fontsize=14, fontweight='bold', labelpad=12, color='#DC143C')
plt.ylabel('Worldwide Gross ($)', fontsize=14, fontweight='bold', labelpad=12, color='#DC143C')

# these lines soften the tick labels
plt.xticks(fontsize=11, color='#666666')
plt.yticks(fontsize=11, color='#666666')

# Arrangements for the graph layout
sns.despine(left=True, bottom=True)
plt.tight_layout()

# Render the plot
# plt.show()
plt.close()




sns.set_theme(style="whitegrid", rc={"axes.facecolor": "#fbfbfb", "grid.color": "#e9ecef"})
plt.figure(figsize=(16, 8), dpi=300)

ax = sns.regplot(
    data=new_films,
    x='USD_Production_Budget',
    y='USD_Worldwide_Gross',
    color="#2c3e50",
    line_kws={'color': '#DC143C', 'linewidth': 3 },  # adjustments for liner regression line
    scatter_kws={
        'alpha': 0.6,          # we would like to display the dots a little bit transparent.
        's': 90,               # this arranges marker sizes
        'edgecolor': 'white',  # a subtle border for the dots
    }
)

# this function converts raw numbers into clean texts
def currency_formatter(x, pos):
    if x >= 1e9:
        return f'${x*1e-9:.1f}B'
    elif x >= 1e6:
        return f'${x*1e-6:.0f}M'
    return f'${x:,.0f}'

ax.xaxis.set_major_formatter(ticker.FuncFormatter(currency_formatter))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(currency_formatter))

# plt.suptitle('Production Budget vs. Worldwide Gross', fontsize=24, fontweight='bold', pad=20, color='#333333', loc='left')

plt.suptitle('Movies After 1960',
             fontsize=18, fontweight='bold', color='#333333',
             x=0.07, y=0.98, ha='left')

plt.title('Production Budget vs. Worldwide Gross', fontsize=22, fontweight='bold', pad=20, color='#DC143C', loc='left')
plt.xlabel('Production Budget ($)', fontsize=14, fontweight='bold', labelpad=12, color='#DC143C')
plt.ylabel('Worldwide Gross ($)', fontsize=14, fontweight='bold', labelpad=12, color='#DC143C')

# these lines soften the tick labels
plt.xticks(fontsize=11, color='#666666')
plt.yticks(fontsize=11, color='#666666')

# Arrangements for the graph layout
sns.despine(left=True, bottom=True)
plt.tight_layout()


# plt.show()
plt.close()



# Use scikit-learn to Run Your Own Regression

from sklearn.linear_model import LinearRegression

regression = LinearRegression()

# Now we should specify our features and our targets (i.e., our response variable).
# Explanatory Variable(s) or Feature(s)
x = pd.DataFrame(new_films, columns=['USD_Production_Budget'])
# Response Variable or Target
y = pd.DataFrame(new_films, columns=['USD_Worldwide_Gross'])

# Find the best-fit line
regression.fit(x, y)


# To find theta 0:
print("\nIntercept of the Relation:")
print(regression.intercept_)

#To find theta 1:
print("\nRegression Coefficient:")
print(regression.coef_)



# We have just estimated the intercept and slope for the Linear Regression model.

# Now we can use it to make a prediction!
# For example, how much global revenue does our model estimate for a film with a budget of $350 million?

budget = 350000000
revenue_estimate = regression.intercept_[0] + regression.coef_[0,0]*budget
revenue_estimate = round(revenue_estimate, -6)

print(f'\nThe estimated revenue for a 350 Million Dollars film is around ${revenue_estimate:,}')

# Analyzing R squared:
# One measure of figuring out how well our model fits our data is by looking at a metric called r-squared.
# This is a good number to look at in addition to eyeballing our charts.

print(regression.score(x, y))


# We see that the r-squared is around 0.558.
# This means that the model explains about 56% of the variance in movie revenue.
# That's actually pretty amazing, considering we've got the simplest possible model,with only one explanatory variable.
# The real world is super complex, so in many academic circles,
# if a researcher can build a simple model that explains over 50% or so of what is actually happening, then it's a pretty decent model.




# Run a linear regression for the old_films.
# Calculate the intercept, slope and r-squared.
# How much of the variance in movie revenue does the linear model explain in this case?

x = pd.DataFrame(old_films, columns=['USD_Production_Budget'])
y = pd.DataFrame(old_films, columns=['USD_Worldwide_Gross'])
regression.fit(x, y)

print("\nRegression Analysis for Old Movies:")
print(f'The slope coefficient is: {regression.coef_[0][0]:.3}')
print(f'The intercept is: {regression.intercept_[0]:.3}')
print(f'The r-squared is: {regression.score(x, y):.3}')




