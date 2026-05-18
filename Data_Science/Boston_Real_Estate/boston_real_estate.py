import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
from sklearn.linear_model import LinearRegression
import matplotlib.dates as mdates

# Create locators for ticks:
register_matplotlib_converters()

# Notebook Presentation:
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 125)
pd.set_option('display.width', None)

#The first column in the .csv_files file just has the row numbers, so it will be used as the index.
data = pd.read_csv('csv_files/boston.csv', index_col=0)

print("\nShape of DataFrame:")
print(data.shape)
print("\nColumns of DataFrame:")
print(data.columns)
print("\nFirst Entries of DataFrame:")
print(data.head())

print("\nIs there any missing values?:")
print(data.isna().values.any())
print("\nIs there any duplicated values?:")
print(data.duplicated().values.any())

print("\nOverview Of the DataFrame:")
print(data.info())

print("\nDescriptive Analysis of the DataFrame:")
print(data.describe())

#  Attribute Information (in order):
# 1. CRIM     per capita crime rate by town
# 2. ZN       proportion of residential land zoned for lots over 25,000 sq.ft.
# 3. INDUS    proportion of non-retail business acres per town
# 4. CHAS     Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
# 5. NOX      nitric oxides concentration (parts per 10 million)
# 6. RM       average number of rooms per dwelling
# 7. AGE      proportion of owner-occupied units built prior to 1940
# 8. DIS      weighted distances to five Boston employment centres
# 9. RAD      index of accessibility to radial highways
# 10. TAX      full-value property-tax rate per $10,000
# 11. PTRATIO  pupil-teacher ratio by town
# 12. B        1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
# 13. LSTAT    % lower status of the population
# 14. PRICE     Median value of owner-occupied homes in $1000's




# Having looked at some descriptive statistics, lets visualise the data for the model.
# we are going to create a bar chart and superimpose the Kernel Density Estimate (KDE) for the following variables:
#
# PRICE: The home price in thousands.
# RM: the average number of rooms per owner unit.
# DIS: the weighted distance to the 5 Boston employment centres i.e., the estimated length of the commute.
# RAD: the index of accessibility to highways.


# Firstly, we create a general theme for thr Graphs
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams['font.family'] = 'sans-serif'

# We are going to define the arrangements for each plot in one dictionary to optimize the code.
plots_log = [
    {
        'column': 'PRICE',
        'color': '#00B8A9',  # Modern soft blue
        'bins': 50,
        'title': 'House Prices in Boston',
        'avg_text': 'Average: ${:,.2f}',
        'multiplier': 1000,  # Used to scale the average calculation
        'xlabel': 'Price (in $1000)',
        'ylabel': 'Number of Homes'
    },
    {
        'column': 'DIS',
        'color': '#4E9F3D',  # Modern soft green
        'bins': 50,
        'title': 'Distance to Employment Centres',
        'avg_text': 'Average Distance: {:.2f}',
        'multiplier': 1,
        'xlabel': 'Weighted Distance to 5 Boston Employment Centres',
        'ylabel': 'Number of Homes'
    },
    {
        'column': 'RM',
        'color': '#FF9A00',  # Modern soft purple
        'bins': 50,
        'title': 'Distribution of Rooms in Boston',
        'avg_text': 'Average Rooms: {:.2f}',
        'multiplier': 1,
        'xlabel': 'Average Number of Rooms per Owner Unit',
        'ylabel': 'Number of Homes'
    },
    {
        'column': 'RAD',
        'color': '#F6416C',  # Modern soft red
        'bins': 20,
        'title': 'Accessibility to Highways in Boston',
        'avg_text': 'Average Index: {:.2f}',
        'multiplier': 1,
        'xlabel': 'Index of Accessibility to Highways',
        'ylabel': 'Number of Houses'
    }
]

# Here we are going to create a graph for each value in dictionary.
for plot in plots_log:
    plt.figure(figsize=(14, 7), dpi=300)

    # we display some values on the graph:
    avg_val = data[plot['column']].mean() * plot['multiplier']
    formatted_avg = plot['avg_text'].format(avg_val)
    full_title = f"{plot['title']}\n{formatted_avg}"

    # we are going to use histplot with kde
    ax = sns.histplot(
        data=data,
        x=plot['column'],
        bins=plot['bins'],
        kde=True,
        color=plot['color'],
        alpha=0.6,
        edgecolor='white',  # a subtle edge fot he bars
        linewidth=1.5,
        line_kws={'linewidth': 2.5}
    )

    # Titles:
    plt.title(full_title, fontsize=17, fontweight='bold', pad=20, loc='left', color='#333333')
    plt.xlabel(plot['xlabel'], fontsize=14, fontweight='bold', color='#555555', labelpad=20)
    plt.ylabel(plot['ylabel'], fontsize=14, fontweight='bold', color='#555555', labelpad=20)

    # Cleaning the gridlines:
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.grid(axis='x', visible=False)

    sns.despine(left=True, bottom=True)  # Removes top, right, left, and bottom borders
    plt.tight_layout()
    # plt.show()
    plt.close()
plt.close()





# Create a bar chart with plotly for CHAS to show many more homes are away from the river versus next to it.
# You can make your life easier by providing a list of values for the x-axis (e.g., x=['No', 'Yes'])


river_data = data.groupby('CHAS', as_index=False).agg({'CHAS': pd.Series.count})

print(river_data)



# Understanding the Relationships in the Data
# Runing a Pair Plot
# There might be some relationships in the data that we should know about.
#
# What would you expect the relationship to be between pollution (NOX) and the distance to employment (DIS)?
# What kind of relationship do you expect between the number of rooms (RM) and the home value (PRICE)?
# What about the amount of poverty in an area (LSTAT) and home prices?
# Run a Seaborn .pairplot() to visualise all the relationships at the same time.
# Note, this is a big task and can take 1-2 minutes! After it's finished check your intuition regarding the questions above on the pairplot.



sns.set_theme(style="whitegrid", palette="mako")

plt.figure(figsize=(18, 6), dpi=300)

g = sns.pairplot(
    data,
    x_vars=["NOX", "RM", "LSTAT"],
    y_vars=["DIS", "PRICE"],
    kind='scatter',
    height=4,
    aspect=1.2, # width-to-height ratio
    plot_kws={
        'alpha': 0.6,  # Transparency for the dots
        's': 50,  # point sizes
        'edgecolor': 'white',  # A subtle white border around dots
        'linewidth': 0.75,
        'color': '#364F6B'
    }
)

# Enhancing the layout
g.fig.suptitle("Housing Market Dynamics: Environment, Space, and Demographics",
               fontsize=16, fontweight='bold', color='#E23E57')

# labels:
for ax in g.axes.flatten():
    ax.set_xlabel(ax.get_xlabel(), fontweight='bold', color='#E23E57')
    ax.set_ylabel(ax.get_ylabel(), fontweight='bold', color='#E23E57')
    ax.grid(color='#e0e0e0', linestyle='--', linewidth=0.5)

g.fig.subplots_adjust(top=0.90)
# plt.show()
plt.close()


# Seaborn's .pairplot() is a powerful visualization tool for exploring pairwise relationships in a dataset.
# It creates a grid of scatter plots for each pair of numerical variables in the dataset, along with histograms or kernel density plots on the diagonal to show the distribution of individual variables.
# This makes it ideal for quickly analyzing the relationships, correlations, and distributions of features in a dataset.
# Users can customize the plot by specifying hue to color points by a categorical variable, enabling easy observation of group-based differences.
# Additional arguments allow customization of the plot's aesthetics, such as marker styles, palette, and axes limits, making .pairplot() a versatile and intuitive tool for exploratory data analysis.





# We want to show the individual relationships in detail.
#
# DIS and NOX
# INDUS vs NOX
# LSTAT vs RM
# LSTAT vs PRICE
# RM vs PRICE
# Try adding some opacity or alpha to the scatter plots using keyword arguments under joint_kws.


# Setting a clean theme
sns.set_theme(style="ticks", context="notebook", font_scale=1.1)
plt.figure(figsize=(18, 6), dpi=300)
# Creating a list of dictionaries that we are going the plot at the graph:
plots_relations = [
    {'x': 'DIS', 'y': 'NOX', 'color': '#7f3c8d', 'title': 'Distance to Employment vs. Nitric Oxides'},
    {'x': 'INDUS', 'y': 'NOX', 'color': '#11a579', 'title': 'Non-Retail Business Acres vs. Nitric Oxides'},
    {'x': 'LSTAT', 'y': 'RM', 'color': '#3969ac', 'title': 'Lower Status Population vs. Number of Rooms'},
    {'x': 'LSTAT', 'y': 'PRICE', 'color': '#f2b701', 'title': 'Lower Status Population vs. Home Price'},
    {'x': 'RM', 'y': 'PRICE', 'color': '#e73f74', 'title': 'Number of Rooms vs. Home Price'}
]

# Looping through the plots and genereting jointplots for every relation
for plot in plots_relations:
    g = sns.jointplot(
        data=data,
        x=plot['x'],
        y=plot['y'],
        kind='scatter',
        height=7,
        color=plot['color'],
        joint_kws={
            'alpha': 0.6,  # Transparency to reveal density
            's': 45,  # Optimal dot size
            'edgecolor': 'white',  # Crisp white borders around dots
            'linewidth': 0.5
        },
        # Refine the marginal histograms
        marginal_kws={
            'kde': True,  # Adds a smooth density curve over the bars
            'alpha': 0.7  # Slightly transparent bars
        }
    )

    # Add a title to the figure (adjusting 'y' to prevent overlap)
    g.fig.suptitle(plot['title'], y=1.0, fontsize=15, fontweight='bold', color='#333333')

    g.fig.subplots_adjust(top=0.90)

    # Cleanly display and then close the plot to free up memory
    # plt.show()
    plt.close()
plt.close()


# Seaborn's .jointplot() is a versatile visualization tool for analyzing the relationship between two variables by combining scatter plots (or other bivariate plots) with marginal histograms or density plots.
# It provides insights into both the joint distribution and individual distributions of the variables in a single figure.
# Users can specify different kinds of plots for the main panel, such as scatter, reg (regression), hex (hexbin), or kde (kernel density estimate), depending on the analysis needs.
# Marginal plots on the axes provide an intuitive view of the individual variable distributions, and options like hue allow grouping by a categorical variable.
# This makes .jointplot() ideal for exploring bivariate relationships while contextualizing them with univariate distributions.






# Split Training & Test Dataset / train test split
#
# We can't use all 506 entries in our dataset to train our model.
# The reason is that we want to evaluate our model on data that it hasn't seen yet (i.e., out-of-sample data).
# That way we can get a better idea of its performance in the real world.
#
# Import the train_test_split() function from sklearn
# Create 4 subsets: X_train, X_test, y_train, y_test
# Split the training and testing data roughly 80/20.
# To get the same random split every time you run your notebook use random_state=10.
# This helps us get the same results every time and avoid confusion while we're learning.
#
# Hint: Remember, your target is your home PRICE, and your features are all the other columns you'll use to predict the price.


from sklearn.model_selection import train_test_split


target_variable = data['PRICE']
features = data.drop('PRICE', axis=1)

X_train, X_test, y_train, y_test = train_test_split(features,
                                                    target_variable,
                                                    test_size=0.2,
                                                    random_state=10)

# % of training set
train_pct = len(X_train)/len(features) * 100
print(f'Training data is {train_pct:.3}% of the total data.')

# % of test data set
test_pct = 100 * X_test.shape[0] / features.shape[0]
print(f'Test data makes up the remaining {test_pct:0.3}%.')




# Multivariable Regression
#
# We have a total of 13 features.
# Therefore, our Linear Regression model will have the following form:
#
# PRICE = θ_0 + θ_1*M + θ_2 *NOX + θ_3 *DIS + θ_4 *CHAS ... + θ_13 *LSTAT
#
# Using sklearn to run the regression on the training dataset.
# How high is the r-squared for the regression on the training data?

from sklearn.linear_model import LinearRegression
Regression = LinearRegression()

# # Explanatory Variable(s) or Feature(s)
# X = pd.DataFrame(X_test)
# # Response Variable or Target
# y = pd.DataFrame(y_test)
# Since they are both datasets we dont have to do this.

Regression.fit(X_train,y_train)

# Coefficient of Determination
r_squared = Regression.score(X_train, y_train)
print(f'Training data r-squared: {r_squared:.2}')

# 0.75 is a very high r-squared!



# Evaluating of  the Coefficients of the Model
#
# Here we do a sense check on our regression coefficients.
# The first thing to look for is if the coefficients have the expected sign (positive or negative).


print(f"\nThe constant Theta value: ")
print(Regression.intercept_)

# coefficients:
print(Regression.coef_)

regression_coefficients = pd.DataFrame(data=Regression.coef_, index=X_train.columns, columns=['Coefficient'])
print("Regression Coefficients:")
print(regression_coefficients)


# Based on the coefficients, how much more expensive is a room with 6 rooms compared to a room with 5 rooms?
# According to the model, what is the premium you would have to pay for an extra room?

# # Premium for having an extra room
extra = regression_coefficients.loc['RM'].values[0] * 1000  # i.e., ~3.11 * 1000
print(f'The additional price for having an extra room is ${extra:.5}')



# Analyse the Estimated Values & Regression Residuals
# The next step is to evaluate our regression.
# How good our regression is depends not only on the r-squared.
# It also depends on the residuals - the difference between the model's predictions ( y^i ) and the true values ( yi ) inside y_train.

print("xtrain:")
print(X_train)

print("xtest")
print(X_test)

print("y_train")
print(y_train)

print("y_test")
print(y_test)
print("\n")
print("\n")

predicted_values = Regression.predict(X_train)
residuals = (y_train - predicted_values)
print(residuals)


# Creating two scatter plots.
#
# The first plot should be actual values (y_train) against the predicted value values:
# The cyan line in the middle shows y_train against y_train.
# If the predictions had been 100% accurate then all the dots would be on this line.
# The further away the dots are from the line, the worse the prediction was.
# That makes the distance to the cyan line, you guessed it, our residuals 😊
# The second plot should be the residuals against the predicted prices. Here's what we're looking for:



sns.set_theme(style="whitegrid", palette="deep")

# we are going to create a graph with 1 row and 2 columns.
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6), dpi=300)

# First Plot : Actual vs Predicted values
sns.scatterplot(x=y_train, y=predicted_values, ax=axes[0], color='#2c3e50', alpha=0.6, s=60, edgecolor=None)

# The ideal prediction line (x=y) (y_train = y_train).
axes[0].plot(y_train, y_train, color='#F45B26', linewidth=2, linestyle='--')

axes[0].set_title('Actual vs. Predicted Prices', fontsize=15, fontweight='bold', pad=15)
axes[0].set_xlabel('Actual Prices in $1000', fontsize=12)
axes[0].set_ylabel('Predicted Prices in $1000', fontsize=12)

# Second plot: Distribution of residuals
sns.scatterplot(x=predicted_values, y=residuals, ax=axes[1], color='#406AAF', alpha=0.6, s=60, edgecolor=None)

# reference for residual points
axes[1].axhline(y=0, color='#F45B26', linestyle='--', linewidth=2, alpha=0.8)

# axes titles
axes[1].set_title('Residuals vs. Predicted Values', fontsize=15, fontweight='bold', pad=15)
axes[1].set_xlabel('Predicted Prices', fontsize=12)
axes[1].set_ylabel('Residuals', fontsize=12)

fig.suptitle('Regression Model Performance', fontsize=20, color='#F45B26', fontweight='bold', y=1.0)

# Layout arrangements and print
sns.despine(left=True, bottom=True)
plt.tight_layout()
# plt.show()
plt.close()



# Why do we want to look at the residuals?
# We want to check that they look random. Why?
# The residuals represent the errors of our model. If there's a pattern in our errors, then our model has a systematic bias.
# We can analyse the distribution of the residuals.
# In particular, we're interested in the skew and the mean.
# In an ideal case, what we want is something close to a normal distribution.
# A normal distribution has a skewness of 0 and a mean of 0.
# A skew of 0 means that the distribution is symmetrical - the bell curve is not lopsided or biased to one side.
# we are going to calculate the mean and the skewness of the residuals.

mean_residual = round(residuals.mean(), 2)
skew_residual = round(residuals.skew(), 2)

plt.figure(figsize=(16, 8), dpi=300)
sns.set_theme(style="whitegrid")

ax = sns.histplot(
    residuals,
    bins=50,
    kde=True,
    color='#3C467B',
    edgecolor='white', # Adds crisp white borders between the bars
    linewidth=1,
    alpha=0.7 # Softens the color
)

# Adding a vertical line to display the mean:
plt.axvline(x=mean_residual, color='#BF1A1A', linestyle='--', linewidth=3, label='Mean')

# Displaying mean and skew values:
stats_text = f"Skew: {skew_residual:.2f}\nMean: {mean_residual:.2f}"
plt.text(
    0.95, 0.95, stats_text,
    transform=ax.transAxes,
    fontsize=15, verticalalignment='top', horizontalalignment='right',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='lightgray')
)

# axes-labels:
plt.title('Distribution of Residuals', fontsize=24, fontweight='bold', pad=15, color='#BF1A1A', y=1.1)
plt.xlabel('Residual Error', fontsize=17)
plt.ylabel('Frequency', fontsize=17)

ax.grid(color='#e0e0e0', linestyle='--', linewidth=0.5)

sns.despine(left=True, bottom=True)
plt.legend(frameon=False)
plt.tight_layout()

# plt.show()

plt.close()

# We see that the residuals have a skewness of 1.46.
# There could be some room for improvement here.




# Data Transformations for a Better Fit

# we are going to transform our data to make it fit better with our linear model.
# we are going to investigate if the target data['PRICE'] could be a suitable candidate for a log transformation.
# we are going to Calculate the skew of that distribution.
# we are going to Use NumPy's log() function to create a Series that has the log prices
# we are going to Create a graph to show a histogram and KDE of the price data.
# we are going to Plot the log prices and calculate the skew.

# Calculate your variables
skew_price = data['PRICE'].skew()
log_price = np.log(data['PRICE'])
skew_log_price = log_price.skew()

sns.set_theme(style="whitegrid")

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 5), dpi=300)

# First Graph: Original price graph:
sns.histplot(
    data['PRICE'],
    kde=True,
    ax=axes[0],
    color='#27ae60',
    edgecolor='white',
    linewidth=1,
    alpha=0.7
)

axes[0].text(
    0.95, 0.95, f"Skew: {skew_price:.3f}",
    transform=axes[0].transAxes,
    fontsize=12, verticalalignment='top', horizontalalignment='right',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='lightgray')
)

axes[0].set_title('Original Price Distribution', fontsize=16, fontweight='bold', pad=20)
axes[0].set_xlabel('Prices in $1000', fontsize=14)
axes[0].set_ylabel('Frequency', fontsize=14)


# Second Graph:
sns.histplot(
    log_price,
    kde=True,
    ax=axes[1],
    color='#2980b9',
    edgecolor='white',
    linewidth=1,
    alpha=0.7
)

axes[1].text(
    0.95, 0.95, f"Skew: {skew_log_price:.3f}",
    transform=axes[1].transAxes,
    fontsize=12, verticalalignment='top', horizontalalignment='right',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='lightgray')
)

axes[1].set_title('Log-Transformed Prices', fontsize=16, fontweight='bold', pad=20)
axes[1].set_xlabel('Log(Prices) in $1000', fontsize=14)
axes[1].set_ylabel('Frequency', fontsize=14)

fig.suptitle('Evaluating Log Transformation for Target Variable', fontsize=18, fontweight='bold', color='#7D5A50')
sns.despine(left=True, bottom=True)

plt.tight_layout()
# plt.show()
plt.close()





# How does the log transformation work?
# Using a log transformation does not affect every price equally.
# Large prices are affected more than smaller prices in the dataset.
# Here's how the prices are "compressed" by the log transformation:

# We can see this when we plot the actual prices against the (transformed) log prices.

plt.figure(dpi=150)
plt.scatter(data.PRICE, np.log(data.PRICE))

plt.title('Mapping the Original Price to a Log Price')
plt.ylabel('Log Price')
plt.xlabel('Actual $ Price in 000s')
# plt.show()
plt.close()







# Regression using Log Prices
# Using log prices instead, our model has changed to:
# log(PRICE) = θ_0 + θ_1 *RM + θ_2 *NOX + θ_3 *DIS +θ_4 *CHAS +... + θ_13 *LSTAT
#
# We are going to use train_test_split() with the same random state as before to make the results comparable.
# We are going to run a second regression, but this time use the transformed target data.
#
# What is the r-squared of the regression on the training data?
# Have we improved the fit of our model compared to before based on this measure?

new_target_variable = np.log(data['PRICE']) # Use log prices
features = data.drop('PRICE', axis=1)

X_train, X_test, log_y_train, log_y_test = train_test_split(features,
                                                            new_target_variable,
                                                            test_size=0.2,
                                                            random_state=10)


log_regression = LinearRegression()
log_regression.fit(X_train, log_y_train)

log_r_squared = log_regression.score(X_train, log_y_train)
print(f'Training data r-squared:')
print(f'{log_r_squared:.2}')

# This time we got an r-squared of 0.79 compared to 0.75. This looks like a promising improvement.

log_predictions = log_regression.predict(X_train)
log_residuals = (log_y_train - log_predictions)

print("\nMean of new Residuals:")
print(log_residuals.mean())
print("\nSkew of new Residuals:")
print(log_residuals.skew())






# Evaluating Coefficients with Log Prices
#
# Do the coefficients still have the expected sign?
# Is being next to the river a positive based on the data?
# How does the quality of the schools affect property prices?
# What happens to prices as there are more students per teacher?

coefficients_log_regression = pd.DataFrame(data=log_regression.coef_, index=X_train.columns, columns=['coef'])
print("\nCoefficients for transformed logarithmic Regression:")
print(coefficients_log_regression)


# So how can we interpret the coefficients?
# The key thing we look for is still the sign - being close to the river results in higher property prices because CHAS has a coefficient greater than zero.
# Therefore property prices are higher next to the river.
# More students per teacher - a higher PTRATIO - is a clear negative.
# Smaller classroom sizes are indicative of higher quality education, so have a negative coefficient for PTRATIO.
#
#
# Regression with Log Prices & Residual Plots
# Use indigo as the colour for the original regression and navy for the color using log prices.


sns.set_theme(style="whitegrid")

# Defining a dictionary for all plots
plots_log = [
    {
        'x': y_train, 'y': predicted_values, 'color': '#7f3c8d',
        'title': f'Original: Actual vs Predicted (R² {r_squared:.3f})',
        'xlabel': 'Actual Prices ($1000s)', 'ylabel': 'Predicted Prices ($1000s)',
        'plot_type': 'regression'
    },
    {
        'x': log_y_train, 'y': log_predictions, 'color': '#11a579',
        'title': f'Log Transformed: Actual vs Predicted (R² {log_r_squared:.2f})',
        'xlabel': 'Actual Log Prices', 'ylabel': 'Predicted Log Prices',
        'plot_type': 'regression'
    },
    {
        'x': predicted_values, 'y': residuals, 'color': '#3969ac',
        'title': 'Original: Residuals vs Predicted',
        'xlabel': 'Predicted Prices ($1000s)', 'ylabel': 'Residuals',
        'plot_type': 'residual'
    },
    {
        'x': log_predictions, 'y': log_residuals, 'color': '#f2b701',
        'title': 'Log Transformed: Residuals vs Predicted',
        'xlabel': 'Predicted Log Prices', 'ylabel': 'Residuals',
        'plot_type': 'residual'
    }
]


fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 12), dpi=300)

# Looping through the plots and the configurations
# axes.flatten() turns the 2x2 grid into a simple 1D list so we can loop over it easily
for ax, plot in zip(axes.flatten(), plots_log):
    sns.scatterplot(
        x=plot['x'], y=plot['y'],
        ax=ax, color=plot['color'],
        alpha=0.6, s=50, edgecolor=None
    )

    # axes-titles
    ax.set_title(plot['title'], fontsize=16, fontweight='bold', pad=18, color='#7D5A50')
    ax.set_xlabel(plot['xlabel'], fontsize=14)
    ax.set_ylabel(plot['ylabel'], fontsize=14)

    # we need two types of lines here:
    if plot['plot_type'] == 'regression':
        ax.plot(plot['x'], plot['x'], color='#F07B3F', linestyle='--', linewidth=2)
    elif plot['plot_type'] == 'residual':
        ax.axhline(y=0, color='#F6416C', linestyle='--', linewidth=2, alpha=0.8)


sns.despine(left=True, bottom=True)
plt.tight_layout(h_pad=4.0, w_pad=3.0)

# plt.show()
plt.close()


# It's hard to see a difference here just by eye.




# Calculate the mean and the skew for the residuals using log prices.
# Are the mean and skew closer to 0 for the regression using log prices?
#
#
# Distribution of Residuals (log prices) - checking for normality

log_residual_mean = round(log_residuals.mean(), 2)
log_residual_skew = round(log_residuals.skew(), 2)


sns.set_theme(style="white", font_scale=1.1)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Original model plot:
sns.histplot(residuals, kde=True, color='#2A3F54', alpha=0.7,
             edgecolor="white", linewidth=1.5, ax=axes[0])

axes[0].set_title(f'Original Model\nSkew: {skew_residual} | Mean: {mean_residual}',
                  fontsize=14, weight='bold', color='#333333', pad=15)
axes[0].set_xlabel('Residuals', fontsize=12, color='#555555')
axes[0].set_ylabel('Count', fontsize=12, color='#555555')

# Log transformation plot:
sns.histplot(log_residuals, kde=True, color='#1ABC9C', alpha=0.7,
             edgecolor="white", linewidth=1.5, ax=axes[1])

axes[1].set_title(f'Log Price Model\nSkew: {log_residual_skew} | Mean: {log_residual_mean}',
                  fontsize=14, weight='bold', color='#333333', pad=15)
axes[1].set_xlabel('Log Residuals', fontsize=12, color='#555555')
axes[1].set_ylabel('') # keep it empty for a cleaner look

fig.suptitle('Comparison Between Original and Logarithmic Regression Models', fontsize=18, fontweight='bold', color='#7D5A50')

sns.despine(offset=10, trim=True)
plt.tight_layout()
# plt.show()
plt.close()

# Our new regression residuals have a skew of 0.09 compared to a skew of 1.46.
# The mean is still around 0.
# From both a residuals perspective and an r-squared perspective we have improved our model with the data transformation.





# Comparing of Sample Performance
# The real test is how our model performs on data that it has not "seen" yet.
# This is where our X_test comes in.
#
# we are going to compare the r-squared of the two models on the test dataset.
# Which model does better?
# Is the r-squared higher or lower than for the training dataset? Why?


print(f'Coefficient of Distribution(r-squared) at Original Model Test Data:')
print(f"{Regression.score(X_test, y_test):.2}")
print(f'Coefficient of Distribution(r-squared) at Logarithmic Model Test Data:')
print(f"{log_regression.score(X_test, log_y_test):.2}")

# By definition, the model was not optimized for the test data.
# Therefore, its performance will be worse than on the training data.
# However, our R-squared value remains high, so we have created a usable model.




# Predict a Property's Value using the Regression Coefficients
# Our preferred model now has an equation that looks like this:
# log(PRICE)= θ0 + θ1RM + θ2NOX + θ3DIS + θ4CHAS + ... + θ13LSTAT
# The average property has the mean value for all its charactistics:
# Starting Point: Average Values in the Dataset

features = data.drop(['PRICE'], axis=1)
average_property_features = features.mean().values

property_values = pd.DataFrame(data=average_property_features
                               .reshape(1, len(features.columns)),
                               columns=features.columns)

print("Average Property Features")
print(property_values)



# Making prediction:
# next, we are going to predict how much the average property is worth using the stats above.
# What is the log price estimate and what is the dollar estimate?
# first we are going to reverse the log transformation with .exp() to find the dollar value.

# Make prediction
log_estimate = log_regression.predict(property_values)[0]
# it returns a list with one value in it (price estimation)
print(f'The log price estimate is ${log_estimate:.3}')

# Convert Log Prices to Acutal Dollar Values
dollar_estimation = np.exp(log_estimate) * 1000

print(f'The property is estimated to be worth ${dollar_estimation:.6}')



# Modelling
# Making price estimation based on preferences
#
# Keeping the average values for CRIM, RAD, INDUS and others, value a property with the following characteristics:
# Define Property Characteristics

next_to_river = True
nr_rooms = 8
students_per_classroom = 20
distance_to_town = 5
pollution = data.NOX.quantile(q=0.75) # high
amount_of_poverty =  data.LSTAT.quantile(q=0.25) # low


# Set Property Characteristics
property_values['RM'] = nr_rooms
property_values['PTRATIO'] = students_per_classroom
property_values['DIS'] = distance_to_town
property_values['NOX'] = pollution
property_values['LSTAT'] = amount_of_poverty

if next_to_river:
    property_values['CHAS'] = 1
else:
    property_values['CHAS'] = 0


# Making the  prediction
log_estimate = log_regression.predict(property_values)[0]

# Convert Log Prices to Acutal Dollar Values
dollar_estimation = np.exp(log_estimate) * 1000
print(f'The value of the property that meets the desired criteria is estimated at ${dollar_estimation:.6}')


import warnings
warnings.filterwarnings("ignore", category=UserWarning)


# Optimizing the analysis
# Finding exact price for our preferences:
from scipy.optimize import minimize


#  Defining the Objective Function (Minimize Price)
def objective(features):
    # The optimizer continuously passes new feature arrays to this function.
    # We want to minimize the predicted logarithm of the price.
    # Since lowering the logarithm of the price also lowers the actual price, this works perfectly.
    predicted_log_price = log_regression.predict([features])[0]
    return predicted_log_price


# Defining the Constraints (Max Budget: 30.0)
# SciPy constraints work by checking if the result is >= 0.
# So: np.log(30.0) - predicted_log_price >= 0
def budget_constraint(features):
    target_log_price = np.log(30.0)
    current_log_prediction = log_regression.predict([features])[0]
    return target_log_price - current_log_prediction


# Pack the constraint into a dictionary for SciPy
constraints = [{'type': 'ineq', 'fun': budget_constraint}]

# Defining the Bounds (Desired Features)
# We are going to provide a (min, max) for all 13 features so the optimizer
bounds = [
    (0.0, 1.4),  # CRIM (Crime rate) ->  we want to have a lover crime rate
    (0.0, 15.0),  # ZN  -> unimportant
    (5.0, 12.0),  # INDUS   ->  mean interval
    (1, 1),  # CHAS (0 or 1 for River)  ->  river-side
    (0.0, 0.43),  # NOX (Pollution) -> less polution
    (6.0, 8.0),  # RM (Rooms) -> min 6 rooms
    (40.0, 80.0),  # AGE -> mean interval
    (1.0, 3.0),  # DIS (Distance to work) -> at most 3
    (5.0, 18.0),  # RAD -> at lest 5
    (300.0, 600.0),  # TAX -> mean interval
    (12.6, 15.0),  # PTRATIO (Student-teacher ratio) -> at most 15
    (356.0, 356.0),  # Black population -> unimportant, mean value
    (1.0, 9.0)  # LSTAT (Lower status population %) -> at most 9 percent
]


# Setting Initial Guess and Run Optimizer
initial_guess = average_property_features.copy()

result = minimize(
    fun=objective,
    x0=initial_guess,
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)


if result.success:
    print("Optimization Successful!\n")

    # Calculating final actual price (converting log to normal)
    optimal_house_log_price = result.fun
    optimal_house_actual_price = np.exp(optimal_house_log_price) * 1000
    print(f"Optimized Price for the Desired House: ${optimal_house_actual_price:,.2f}\n")

    print("All of the Conditions of Ideal House:")
    optimal_features = result.x
    for name, value in zip(features.columns, optimal_features):
        print(f"{name:>8}: {value:.2f}")
else:
    print("Optimization failed to find a solution. Your constraints might be too strict.")

