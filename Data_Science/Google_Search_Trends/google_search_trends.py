import datetime

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.dates as mdates


df_tesla = pd.read_csv('csv_files/TESLA_Search_Trend_vs_Price.csv')
print("\nTesla Dataframe:")

print("\nShape of the DataFrame:")
print(df_tesla.shape)

print("\nInitial Insight into the DataFrame:")
print(df_tesla.head())

print("\nGeneral Structure of the DataFrame:")
print(df_tesla.info())

print("\nKey Statistics in the DataFrame:")
print(df_tesla.describe())



df_btc_search = pd.read_csv('csv_files/Bitcoin_Search_Trend.csv')
print("\nBitcoin Search Dataframe:")

print("\nShape of the DataFrame:")
print(df_btc_search.shape)

print("\nInitial Insight into the DataFrame:")
print(df_btc_search.head())

print("\nGeneral Structure of the DataFrame:")
print(df_btc_search.info())

print("\nKey Statistics in the DataFrame:")
print(df_btc_search.describe())




df_btc_price = pd.read_csv('csv_files/Daily_Bitcoin_Price.csv')
print("\nBitcoin Price Dataframe:")

print("\nShape of the DataFrame:")
print(df_btc_price.shape)

print("\nInitial Insight into the DataFrame:")
print(df_btc_price.head())

print("\nKey Statistics in the DataFrame:")
print(df_btc_price.describe())




df_unemployment = pd.read_csv('csv_files/UE_Benefits_Search_vs_UE_Rate_2004-19.csv')
print("\nUnemployment Dataframe:")

print("\nShape of the DataFrame:")
print(df_unemployment.shape)

print("\nInitial Insight into the DataFrame:")
print(df_unemployment.head())

print("\nKey Statistics in the DataFrame:")
print(df_unemployment.describe())


print(f'Missing values for Tesla?: {df_tesla.isna().values.any()}')
print(f'Missing values for U/E?: {df_unemployment.isna().values.any()}')
print(f'Missing values for BTC Search?: {df_btc_search.isna().values.any()}')
print(f'Missing values for BTC price?: {df_btc_price.isna().values.any()}')


print(f'Sum of missing values for BTC price?: {df_btc_price.isna().values.sum()}')
df_btc_price = df_btc_price.dropna()



# Converting strings to a datetime

df_tesla.MONTH = pd.to_datetime(df_tesla.MONTH)
df_btc_search.MONTH = pd.to_datetime(df_btc_search.MONTH)
df_unemployment.MONTH = pd.to_datetime(df_unemployment.MONTH)
df_btc_price.DATE = pd.to_datetime(df_btc_price.DATE)


# Relation between Tesla stock Price and Search Trend

# Converting a daily based datetime to a monthly based datetime with resample()
# df_btc_monthly = df_btc_price.resample('ME', on='DATE').last()
df_btc_monthly = df_btc_price.resample('ME', on='DATE').mean()

print(df_btc_monthly.shape)
print(df_btc_monthly.head())


# Define locators and formatters
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')



sns.set_theme(style="whitegrid", context="talk", font_scale=0.8)

# Create figure with high resolution
plt.figure(figsize=(10, 5), dpi=150)
plt.title('Tesla Web Search Trend vs. Stock Price', fontsize=14, fontweight='bold', pad=15)

ax1 = plt.gca()
ax2 = ax1.twinx()

# Plot using Seaborn's lineplot
sns.lineplot(
    data=df_tesla,
    x='MONTH',
    y='TSLA_USD_CLOSE',
    color='#E6232E',
    linewidth=2.5,
    ax=ax1,
    label='TESLA Stock Price'
)

sns.lineplot(
    data=df_tesla,
    x='MONTH',
    y='TSLA_WEB_SEARCH',
    color='#2B90B6',
    linewidth=2.5,
    ax=ax2,
    label='Search Trend'
)

# Axis labels
ax1.set_xlabel('Date', fontsize=11, fontweight='bold', color='gray')
ax1.set_ylabel('TESLA Stock Price (USD)', color='#E6232E', fontsize=11, fontweight='bold')
ax2.set_ylabel('Search Trend Volume', color='#2B90B6', fontsize=11, fontweight='bold')

# Setting limits
# We are applying this just to get rid of small empty spaces at the start and end of the graph.
ax1.set_ylim([0, 600])
ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

# Making gridlines very transparent.
# When working with two axes, the gridlines for the second should be turned off.
ax1.grid(True, alpha=0.2)
ax2.grid(False)

# Formating the x-axis dates
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')


# Combining the legends into one clean box
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', frameon=True, shadow=False, borderpad=1)
ax2.get_legend().remove() # Remove the redundant secondary legend

# Adjusting layout so that nothing gets cut off.
plt.tight_layout()

plt.show()



print("------")
print(df_btc_monthly.head(20))
print("------")
print(df_btc_monthly.tail(20))

print("----------------------------")
print("------")
print(df_btc_search.head(20))
print("------")
print(df_btc_search.tail(20))

print(df_btc_search.shape)

# Plot configuration for bitcoin

sns.set_theme(style="ticks", context="talk")

# Creating the figure and the primary axis
fig, ax1 = plt.subplots(figsize=(10, 5), dpi=120)

# Defining distinct colors for two Variables
color_price = '#2ca02c'  # Sleek financial green
color_search = '#1f77b4' # Tech/data blue

# Plotting stock price on the primary (left) y-axis
ax1.set_xlabel('Date', fontweight='bold', fontsize=12)
ax1.set_ylabel('BTC Price (USD)', color=color_price, fontweight='bold', fontsize=12)

# Set the minimum and maximum values on the axes
ax1.set_ylim(bottom=0, top=15000)
ax1.set_xlim([df_btc_monthly.index.min(), df_btc_monthly.index.max()])

# Plotting the line for the price data
sns.lineplot(data=df_btc_monthly, x=df_btc_monthly.index, y='CLOSE',
             color=color_price, linewidth=2.5, ax=ax1)

# Color match the ticks to the line and add a soft grid
ax1.tick_params(axis='y', labelcolor=color_price)
ax1.grid(True, axis='y', linestyle='--', alpha=0.4)


# Creating the secondary (right) y-axis sharing the same x-axis
ax2 = ax1.twinx()

# Plotting Google Search Trend of Bitcoin on the secondary y-axis
ax2.set_ylabel('Search Trend', color=color_search, fontweight='bold', fontsize=12)

# Plotting the line for the data
sns.lineplot(data=df_btc_search, x=df_btc_monthly.index, y='BTC_NEWS_SEARCH',
             color=color_search, linewidth=2.5, ax=ax2)

# Color match the ticks for the second axis
ax2.tick_params(axis='y', labelcolor=color_search)
ax2.set_ylim(bottom=0)

# Cleaning up the x-axis formatting (our original locators)
years = mdates.YearLocator()
years_fmt = mdates.DateFormatter('%Y')
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)

# Rotating the labels on the primary axis to read them better
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=10)

# Adding title and clean up borders
plt.title('Bitcoin: Web Search vs. Price', fontsize=16, fontweight='bold', pad=15)
sns.despine(top=True, right=False)

fig.tight_layout()
plt.show()







# Plot configuration for unemployment

# First we are going to get rolling averages:

# # Calculate rolling averages
df_unemployment['UNRATE_ROLLING'] = df_unemployment['UNRATE'].rolling(window=3).mean()
df_unemployment['SEARCH_ROLLING'] = df_unemployment['UE_BENEFITS_WEB_SEARCH'].rolling(window=3).mean()



sns.set_theme(style="white", context="talk")

# Create a figure with 2 subplots sharing the x-axis
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 6), dpi=150, sharex=True)

# Defining Different colors for the data
color_ue = '#2b5b84'      # Deep corporate blue
color_search = '#d95f02'  # Muted burnt orange


# --- Top Plot: Unemployment Rate ---
sns.lineplot(data=df_unemployment, x='MONTH', y='UNRATE_ROLLING',
             ax=ax1, color=color_ue, linewidth=2.5)

ax1.fill_between(df_unemployment.MONTH, df_unemployment.UNRATE_ROLLING, color=color_ue, alpha=0.1) # Adds a modern light fill
ax1.set_ylabel('UE Rate (%)', fontweight='bold', color=color_ue, fontsize=12)

ax1.set_title('Unemployment - Macroeconomic & Search Indicators \n(Without Rolling)',
              fontsize=14, fontweight='bold', pad=22, loc='left')


# --- Bottom Plot: Search Trend ---
sns.lineplot(data=df_unemployment, x='MONTH', y='SEARCH_ROLLING',
             ax=ax2, color=color_search, linewidth=2.5)
ax2.fill_between(df_unemployment.MONTH, df_unemployment.SEARCH_ROLLING, color=color_search, alpha=0.1)
ax2.set_ylabel('Search Trend', fontweight='bold', color=color_search, fontsize=12)
ax2.set_xlabel('')


# Formatting and Cleaning up the graph
ax2.xaxis.set_major_locator(mdates.YearLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=10)


# Adding subtle and light horizontal gridlines
ax1.grid(axis='y', color='lightgrey', linestyle='-', alpha=0.7)
ax2.grid(axis='y', color='lightgrey', linestyle='-', alpha=0.7)


sns.despine(fig, left=True, bottom=False)
plt.tight_layout()
plt.show()











df_ue_2020 = pd.read_csv('csv_files/UE_Benefits_Search_vs_UE_Rate_2004-20.csv')

print("\nDataframe for the Unemployment from 2020:")
print(df_ue_2020.shape)
print(df_ue_2020.tail())

df_ue_2020.MONTH = pd.to_datetime(df_ue_2020.MONTH)


# Plot configuration for bitcoin for eu unemployment -monthly
sns.set_theme(style="whitegrid", context="notebook")

# Create a figure with two subplots sharing the same x-axis
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 6), sharex=True, dpi=120)
fig.subplots_adjust(hspace=0.2) # Bring the plots closer together

# Defining colors for the Graphs
color_unrate = "#7B1FA2"
color_search = "#0288D1"

# Defining the time before covid
before_covid = pd.to_datetime('2019-01')

ax1.set_xlim([before_covid, df_ue_2020['MONTH'].max()])
ax2.set_xlim([before_covid, df_ue_2020['MONTH'].max()])

# Plotting Unemployment Rate
sns.lineplot(x=df_ue_2020['MONTH'], y=df_ue_2020['UNRATE'],
             ax=ax1, color=color_unrate, linewidth=2.5)

# Filling underneath of the line for a subtle-modern look
ax1.fill_between(df_ue_2020['MONTH'], df_ue_2020['UNRATE'], color=color_unrate, alpha=0.2)

ax1.set_ylabel('UE Rate (%)', fontsize=10, fontweight='bold', color=color_unrate, labelpad=25)
ax1.set_title('US Unemployment Rate vs. Google Search Trends',
              fontsize=14, fontweight='bold', pad=25)

# Plotting Google Search Trends
sns.lineplot(x=df_ue_2020['MONTH'], y=df_ue_2020['UE_BENEFITS_WEB_SEARCH'],
             ax=ax2, color=color_search, linewidth=2.5)

# Again Filling underneath of the line
ax2.fill_between(df_ue_2020['MONTH'], df_ue_2020['UE_BENEFITS_WEB_SEARCH'], color=color_search, alpha=0.2)

ax2.set_ylabel('Search Index', fontsize=10, fontweight='bold', color=color_search, labelpad=18)
ax2.set_xlabel('Date', fontsize=10, fontweight='bold', labelpad=18)

# Removing top and right borders for a cleaner look
sns.despine(fig=fig)

# Formating x-axis ticks
plt.yticks(fontsize=12)
plt.xticks(fontsize=14)


fig.tight_layout()

plt.show()
# plt.close()


