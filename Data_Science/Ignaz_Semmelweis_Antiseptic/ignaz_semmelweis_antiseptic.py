import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import gaussian_kde
from pandas.plotting import register_matplotlib_converters
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create locators for ticks on the time axis
register_matplotlib_converters()

# Notebook Presentation:
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 125)
pd.set_option('display.width', None)

# Retrieving the data
df_yearly = pd.read_csv('csv_files/annual_deaths_by_clinic.csv')
df_monthly = pd.read_csv('csv_files/monthly_deaths.csv')

df_yearly["year"] = pd.to_datetime(df_yearly["year"], format="%Y")
df_monthly.date = pd.to_datetime(df_monthly.date)


print("Yearly Data:")
print(df_yearly)
print("\nMonthly Data:")
print(df_monthly)

print("\nIs there any empty or duplicated values on Yearly data:")
print(f"Missing Values: {df_yearly.isna().values.any()}")
print(f"Duplicated Values: {df_yearly.duplicated().any()}")

print("\nIs there any empty or duplicated values on Monthly data:")
print(f"Missing Values: {df_monthly.isna().values.any()}")
print(f"Duplicated Values: {df_monthly.duplicated().any()}")

# Creating Death Percentages Data:
df_yearly['pct_deaths'] = df_yearly.deaths / df_yearly.births * 100
df_monthly['pct_deaths'] = df_monthly.deaths / df_monthly.births * 100

print("\nOverview of the Dataframes:")
print(df_yearly.info())
print(df_monthly.info())

print("\nDescriptive Analysis of the Dataframes:")
print(df_yearly.describe())
print(df_monthly.describe())

# Using the annual data, calculate the percentage of women giving birth who died throughout the 1840s at the hospital.
mortality_rate = df_yearly.deaths.sum() / df_yearly.births.sum() * 100
print(f'The mortality rate among women who died in childbirth in the hospital in the 1840s was: {mortality_rate:.3}%')



# Analysis of the total number of deaths and births

fig = make_subplots(specs=[[{"secondary_y": True}]])

color_births = "#2E86C1"
color_deaths = "#E23E57"

# Plotting Birth Line
fig.add_trace(
    go.Scatter(
        x=df_monthly['date'],
        y=df_monthly['births'],
        name="Births",
        mode="lines",
        line=dict(color=color_births, width=3),
        hovertemplate="Births: %{y}<extra></extra>"
    ),
    secondary_y=False,
)

# Plotting Death Line
fig.add_trace(
    go.Scatter(
        x=df_monthly['date'],
        y=df_monthly['deaths'],
        name="Deaths",
        mode="lines",
        line=dict(color=color_deaths, width=3, dash="dot"),
        hovertemplate="Deaths: %{y}<extra></extra>"
    ),
    secondary_y=True,
)


# Designing the Layout
fig.update_layout(
    title=dict(
        text="<b>Total Number of Births and Deaths</b> (1841 - 1847)",
        font=dict(size=22, family="Arial, sans-serif", color="#52057B"), x=0.5, xanchor='center'
    ),
    plot_bgcolor="white", paper_bgcolor="white",
    hovermode="x unified",
    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial, sans-serif"),
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
    margin=dict(l=60, r=60, t=100, b=60)
)

# Refining X-axis
fig.update_xaxes(
    title_text="",
    showgrid=True, gridwidth=1, gridcolor="rgba(230, 230, 230, 0.8)",
    dtick="M12", tickformat="%Y",
    tickfont=dict(color="#555555"),
    ticks="outside",
    ticklen=8,
    minor=dict(
        dtick="M1",
        ticklen=4,
        tickcolor="#cccccc",
        ticks="outside"
    ),
    hoverformat="%B %Y",

    # Explicitly pass datetime objects for both the min and max limits
    range=[df_monthly['date'].min(), pd.to_datetime("1847-04-01")]
)

# Refining y-axis (for births)
fig.update_yaxes(
    title_text="<b>Births</b>",
    title_font=dict(color=color_births),
    tickfont=dict(color=color_births),
    showgrid=True, gridwidth=1,
    gridcolor="rgba(230, 230, 230, 0.8)",
    secondary_y=False
)

# Refining y-axis (for deaths)
fig.update_yaxes(
    title_text="<b>Deaths</b>",
    title_font=dict(color=color_deaths),
    tickfont=dict(color=color_deaths),
    showgrid=False,
    secondary_y=True
)

# fig.write_html("interactive_graphs/total_births_and_deaths_until_1847.html")

# fig.show()



#  Analysis for Annual Data:
# We saw there that there are two different clinics at Vienna Hospital.
# We are going to Use plotly to create line charts of the births and deaths of the two different clinics at the Vienna General Hospital.

df_yearly['proportion_deaths'] = df_yearly['deaths'] / df_yearly['births']

fig = px.line(
    df_yearly,
    x='year',
    y='proportion_deaths',
    color='clinic',
    markers=True,
    hover_data={
        'proportion_deaths': ':.1%',
        'births': True,
        'deaths': True
    },
    labels={
        'year': 'Year',
        'proportion_deaths': 'Mortality Rate',
        'clinic': 'Clinic',
        'births': 'Total Births',
        'deaths': 'Total Deaths'
    },
    template='plotly_white',
    color_discrete_sequence=['#00B8A9', '#F6416C']
)

# Designing the layout
fig.update_layout(
    title=dict(
        text='<b>Yearly Mortality Rate by Clinic</b><br><sup>Proportion of deaths per birth at Vienna General Hospital (1841-1846)</sup>',
        font=dict(size=23, family="Arial, sans-serif", color="#406AAF")
    ),
    font_family="Arial",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig.update_yaxes(tickformat=".1%", showgrid=True, gridcolor='LightGray')
fig.update_xaxes(showgrid=False)
fig.update_traces(line=dict(width=4))

# fig.write_html("interactive_graphs/clinic_comparison.html")
# fig.show()

# We  see that, not only were more people born in clinic 1, more people also died in clinic 1 too.






# Challenge: The Effect of Handwashing

# Semmelweis noticed something shocking:
# Women delivered by doctors died much more often than those delivered by midwives
# Doctors often came straight from autopsies to childbirth without washing their hands
# So he introduced handwashing with a chlorine solution before examining patients.
# Antisepsis = preventing infection by killing germs on hands, tools, or wounds

# Create two subsets from the df_monthly data:
# before and after Dr Semmelweis ordered washing hand.
# Calculate the average death rate prior to June 1846.
# Calculate the average death rate after June 1846.

new_policy_date = pd.Timestamp('1847-06-01')

before_washing_hand = df_monthly.query("date < @new_policy_date")
after_washing_hand = df_monthly.query("date >= @new_policy_date")

before_avg_rate = before_washing_hand.deaths.sum() / before_washing_hand.births.sum() * 100
after_avg_rate = after_washing_hand.deaths.sum() / after_washing_hand.births.sum() * 100

print(f'Average death rate before 1847 was {before_avg_rate:.4}%')  # 10.53%
print(f'Average death rate after 1847 is {after_avg_rate:.3}%') # 2.15%





# Rolling Average of the Death Rate

# we are going to create a DF that has 6-month rolling average death rate before handwashing.
# here, we need to set the dates as the index, in order to avoid the date column being dropped.

roll_df = before_washing_hand.set_index('date')
roll_df = roll_df.rolling(window=6).mean()
print("\n6 months Rolled Data Before Antisepsis: ")
print(roll_df[5:10])

# Setting the date column as the index is essential for performing a rolling average correctly.


# Highlighting Subsections of a Line Chart

text_color = '#4a4a4a'

fig, ax = plt.subplots(figsize=(16, 8), dpi=300)

# Plotting the data before 1847
ax.plot(roll_df.index,
        roll_df.pct_deaths,
        color='#D14D72',
        linewidth=2.5,
        label='Before Handwashing (6m Moving Average)')

# Plotting the data after 1847
ax.plot(after_washing_hand.date,
        after_washing_hand.pct_deaths,
        color='#FF9A00',
        linewidth=2.5,
        marker='o',
        markersize=6,
        markerfacecolor='white',
        markeredgewidth=1.5,
        label='After Handwashing')

# The turning point:
ax.axvline(x=after_washing_hand.date.min(), color='#b0b0b0', linestyle='--', linewidth=1.5, zorder=0)

# Designing the layout
ax.set_title('Percentage of Monthly Maternal Deaths over Time',
             fontsize=16, fontweight='bold', color='#102C57', pad=20, loc='left')
ax.set_ylabel('Percentage of Deaths (%)', fontsize=13, color=text_color, labelpad=20)
ax.set_xlabel('')
ax.set_xlim([df_monthly.date.min(), df_monthly.date.max()])

# Ticks at x-axis
ax.tick_params(axis='both', which='major', labelsize=12, colors=text_color, length=0)
plt.xticks(rotation=0)

# Gridlines
ax.grid(axis='y', color='#e0e0e0', linestyle='-', linewidth=0.8)
ax.grid(axis='x', visible=False)

# A clear open graph
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#cccccc')

# Legend and chart size:
ax.legend(frameon=False, fontsize=12, loc='upper right', labelcolor=text_color)
plt.tight_layout()

# plt.show()
# plt.close()




# Calculating the Difference in the Average Monthly Death Rate

# By how much did handwashing reduce the average chance of dying in childbirth in percentage terms?
# How do these numbers compare to the average for all the 1840s that we calculated earlier?
# How many times lower are the chances of dying after handwashing compared to before?

mean_diff = before_avg_rate - after_avg_rate
improvement_rate = before_avg_rate / after_avg_rate

print(f"Hemmelweis' introduction of antisepsis reduced the monthly mortality rate by {mean_diff:.3}%!")
print(f'This is a {improvement_rate:.2}x improvement!')




# Using Box Plots to Show How the Death Rate Changed Before and After Handwashing
# The statistic above is impressive, but how do we show it graphically?
# With a box plot we can show how the quartiles, minimum, and maximum values changed in addition to the mean.
# Use NumPy's .where() function to add a column to df_monthly that shows if a particular date was before or after the start of handwashing.

# Then use plotly to create box plot of the data before and after handwashing.
# How did key statistics like the mean, max, min, 1st and 3rd quartile changed as a result of the new policy

df_monthly["handwashing"] = np.where(df_monthly.date >= new_policy_date, 'After', 'Before')
df_monthly['date_str'] = df_monthly['date'].dt.strftime('%Y-%m-%d')
display_data=["date_str", "pct_deaths", "births", "deaths"]

fig = px.box(
    df_monthly,
    x="handwashing",
    y="pct_deaths",
    color="handwashing",
    title="Impact of Handwashing on Monthly Death Rate",
    points="all",
    template="plotly_white",
    color_discrete_map={"Before": "#DA0037", "After": "#6FAF4F"},
    custom_data=display_data
)

# Refining the layout
fig.update_layout(
    title_font_size=25,
    title_font_family="Arial Black",
    title_x=0.5,
    font=dict(size=16, color="#967E76"),
    showlegend=False,
    margin=dict(t=80, b=40, l=60, r=40),
    yaxis_title="Monthly Deaths (%)",
    xaxis_title="Antisepsis Policy",
    hoverlabel=dict(bgcolor="white", font_size=15, font_family="Arial, sans-serif")
)

# Customizing the hover template
fig.update_traces(
    marker=dict(size=5, opacity=0.7, line=dict(width=0)),
    line=dict(width=2),
    boxmean=True,
    hovertemplate=(
        "<b>Death Rate:</b> %{customdata[1]:.1f}%<br>"
        "<b>Date:</b> %{customdata[0]}<br>"
        "<b>Total Births:</b> %{customdata[2]}<br>"
        "<b>Total Deaths:</b> %{customdata[3]}<br>"
        "<extra></extra>"
    )
)

# fig.write_html("interactive_graphs/boxplot_before_and_after_handwashing.html")

# fig.show()





# Monthly Distribution of Outcomes

# Create a plotly histogram to show the monthly percentage of deaths.
# Use the color parameter to display two overlapping histograms.
# The time period of handwashing is shorter than not handwashing.
# Change histnorm to percent to make the time periods comparable.
# Which number works well in communicating the range of outcomes?

fig = px.histogram(
    df_monthly,
    x="pct_deaths",
    color="handwashing",
    opacity=0.75,
    nbins=30,  # How many box do we want here
    barmode="overlay",
    histnorm="percent",
    marginal="box",        # show statistical plots at the top
    title="Distribution of Monthly Death Rates: Before vs. After Antisepsis Policy",
    template="plotly_white",
    color_discrete_map={"Before": "#DF2E38", "After": "#48A111"},
)

# Refining the layout
fig.update_layout(
    title=dict(font=dict(size=22,family="Arial Black",color="#A47251"), x=0.05),
    font=dict(size=14, color="#333333"),
    xaxis_title="Monthly Death Rate (%)",
    yaxis_title="Frequency (% of Months)",
    legend=dict(
        title="<b>Antisepsis Policy</b>",
        orientation="h", xanchor="right", yanchor="bottom", # Horizontal legend
        x=1, y=1.02,        # The legend will be above the chart.
    ),
    margin=dict(t=120, b=50, l=60, r=40),
    hoverlabel=dict(font_size=14, font_family="Arial, sans-serif")
)

# Subtle gridlines:
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F0F0F0', zeroline=False)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F0F0F0', zeroline=False)

# Hover arrangements:
fig.update_traces(
    hovertemplate=(
        "<b>Death Rate Range:</b> %{x}%<br>"
        "<b>Frequency:</b> %{y:.1f}% of observed months<br>"
        "<extra></extra>"
    ),
    selector=dict(type="histogram")  # marginal box plot won't break at hovers
)

# Design for box plots:
fig.update_traces(boxmean=True, marker=dict(opacity=0.5), selector=dict(type="box"))

# fig.write_html("interactive_graphs/histogram_before_and_after_handwashing.html")

# fig.show()





# histnorm='percent': Normalizes the y-axis values to show percentages instead of raw counts.
# marginal='box': Adds a boxplot above the histogram, which provides additional insights into the data distribution.
# It summarizes key statistics (e.g., median, quartiles) for pct_deaths.





# Kernel Density Estimate (KDE) to visualise a smooth distribution

# Now, we have only about 98 data points or so, so our histogram looks a bit jagged.
# It's not a smooth bell-shaped curve. However, we can estimate what the distribution would look like with a Kernel Density Estimate (KDE).

# Use Seaborn's .kdeplot() to create two kernel density estimates of the pct_deaths, one for before handwashing and one for after.
# Use the shade parameter to give your two distributions different colours.
# What weakness in the chart do you see when you just use the default parameters?
# Use the clip parameter to address the problem.
# However, the problem is that we end up with a negative monthly death rate on the left tail.
# The doctors would be very surprised indeed if a corpse came back to life after an autopsy!
# The solution is to specify a lower bound of 0 for the death rate.
# We are gone use .clip parameter.



# We use 500 points to make the curve perfectly smooth
x_range = np.linspace(0, 40, 500)

# Calculation of Kernel Density Estimates using SciPy
kde_before = gaussian_kde(before_washing_hand['pct_deaths'])
kde_after = gaussian_kde(after_washing_hand['pct_deaths'])

# Evaluating of the KDEs across the defined x_range
y_before = kde_before(x_range)
y_after = kde_after(x_range)


fig = go.Figure()

# Plotting the data before 1847
fig.add_trace(go.Scatter(
    x=x_range,
    y=y_before,
    fill='tozeroy',  # Fill the buttom of the line
    mode='lines',
    line=dict(color='#EF553B', width=3),
    fillcolor='rgba(239, 85, 59, 0.4)',
    name='Before Antisepsis',
    hovertemplate="<b>Death Rate:</b> %{x:.1f}%<br><b>Density:</b> %{y:.4f}<extra></extra>"
))

# Plotting the data after 1847
fig.add_trace(go.Scatter(
    x=x_range,
    y=y_after,
    fill='tozeroy',
    mode='lines',
    line=dict(color='#00CC96', width=3),
    fillcolor='rgba(0, 204, 150, 0.4)',
    name='After Antisepsis',
    hovertemplate="<b>Death Rate:</b> %{x:.1f}%<br><b>Density:</b> %{y:.4f}<extra></extra>"
))

# Refining the layout
fig.update_layout(
    title=dict(text="Estimated Distribution of Monthly Death Rates",
               font=dict(size=22,family="Arial Black",color="#A47251"), x=0.05),
    template="plotly_white",
    font=dict(size=14, color="#333333"),
    xaxis_title="Monthly Death Rate (%)",
    yaxis_title="Estimated Density",

    # Legend formatting and placement
    legend=dict(
        title="<b>Antisepsis Policy</b>",
        orientation="h",
        yanchor="bottom", xanchor="right",
        y=1.03, x=1.1
    ),
    margin=dict(t=120, b=50, l=60, r=40),
    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial, sans-serif")
)

# Subtle gridlines
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F0F0F0', zeroline=True, zerolinecolor='#D3D3D3')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F0F0F0', zeroline=True, zerolinecolor='#D3D3D3')

# fig.write_html("interactive_graphs/kde_before_and_after_handwashing.html")

# fig.show()



# Now that we have an idea of what the two distributions look like,
# we can further strengthen our argument for handwashing by using a statistical test.

# We can test whether our distributions ended up looking so different purely by chance
# (i.e., the lower death rate is just an accident) or if the 8.4% difference in the average death rate is statistically significant.





# Use a T-Test to Show Statistical Significance
# Use a t-test to determine if the differences in the means are statistically significant or purely due to chance.

# If the p-value is less than 1% then we can be 99% certain that handwashing has made a difference to the average monthly death rate.
# Import stats from scipy
# Use the .ttest_ind() function to calculate the t-statistic and the p-value
# Is the difference in the average proportion of monthly deaths statistically significant at the 99% level?

import scipy.stats as stats


t_stat, p_value = stats.ttest_ind(a=before_washing_hand.pct_deaths, b=after_washing_hand.pct_deaths)

print(f'p-palue is {p_value:.10f}')
print(f't-statstic is {t_stat:.4}')

# When we calculate the p_value we see that it is 0.0000002985 or .00002985% which is far below even 1%.
# In other words, the difference in means is highly statistically significant and we can go ahead on publish our research pape