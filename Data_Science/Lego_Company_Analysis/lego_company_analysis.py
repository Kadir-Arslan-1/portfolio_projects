import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import textwrap


# Colors that are used in Lego sets:
colors = pd.read_csv('csv_files/colors.csv')

# First insight to the Dataframe


print(colors.head())

print("\nShape:")
print(colors.shape)

# This shows the sum of unique names in project.
print(colors['name'].nunique())

## There are 135 different colors used in Lego sets.


# Some colors are trans and some colors are not, to find the values:
# colors.groupby("is_trans").count()
print(colors.is_trans.value_counts())





# Understanding LEGO Themes vs. LEGO Sets

# Walk into a LEGO store and you will see their products organised by theme.
# Their themes include Star Wars, Batman, Harry Potter and many more.


# A lego **set** is a particular box of LEGO or product.
# Therefore, a single theme typically has many different sets.



sets = pd.read_csv('csv_files/sets.csv')
print(sets.head())

sets = sets.sort_values('num_parts', ascending=False)
print(sets.head())

sets = sets.sort_values('year', ascending=True)
print(sets.head())

sets_from_1945 = sets[sets['year'] == 1949]
print("\nNumber of sets from the year 1949:")
print(sets_from_1945.value_counts().sum())


print("\n --------")

# Sorting sets by year

sorted_sets_by_year = sets.sort_values('year')
sorted_sets_by_year = sorted_sets_by_year.year.value_counts()
print(sorted_sets_by_year.head(7))



sets_by_year = sets.groupby('year')

sets_by_year_counts = sets_by_year.count()
print(sets_by_year_counts["set_num"].head())

sets_by_year_counts = sets_by_year_counts[:-2]





# Line plot graph of set nums per year

# Modern seaborn theme
sns.set_theme(style="whitegrid", context="talk")

fig, ax = plt.subplots(figsize=(12,6))

sns.lineplot(
    data=sets_by_year_counts,
    x=sets_by_year_counts.index,
    y="set_num",
    marker="o"
)

ax.set_title("Number of LEGO Sets Released Per Year", fontsize=16, pad=15)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Sets")

# ax.set_ylim(0, 1000)

plt.tight_layout()
plt.show()





print("-----------")
print("\n")

# Creating a new dataframe:

themes_by_year = sets_by_year.agg({'theme_id': pd.Series.nunique})
themes_by_year = themes_by_year[:-2]

themes_by_year.rename(columns = {'theme_id':'nr_themes'}, inplace = True)

print(themes_by_year.head())





sns.set_theme(style="white", context="talk")

# Figure size and primary axis
fig, ax1 = plt.subplots(figsize=(14, 7))

# Chart title
plt.title('Evolution of Sets and Themes Over Time',
          fontsize=18, fontweight='bold', pad=20)


# colors (Teal for Sets, Coral for Themes)
color_sets = "#2a9d8f"
color_themes = "#e76f51"

# first line on ax1
ax1.plot(sets_by_year_counts.index,
         sets_by_year_counts.set_num,
         color=color_sets, linewidth=3, label='Number of Sets')

# ax1 labels and ticks
ax1.set_xlabel('Year', fontsize=14, fontweight='bold', labelpad=15)
ax1.set_ylabel('Number of Sets', color=color_sets, fontsize=14, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=color_sets)

# Add subtle gridlines to ax1
ax1.grid(True, linestyle='--', alpha=0.6)

# Second axis
ax2 = ax1.twinx()

# Plotting the second line
ax2.plot(themes_by_year.index,
         themes_by_year.nr_themes,
         color=color_themes, linewidth=3, label='Number of Themes')

# ax2 labels and ticks
ax2.set_ylabel('Number of Themes', color=color_themes, fontsize=14, fontweight='bold')
ax2.tick_params(axis='y', labelcolor=color_themes)


# Legend
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', frameon=True, shadow=True)

# Clean up the top border (despine) while keeping the right axis
sns.despine(top=True, right=False)

# Adjust layout so nothing gets cut off
fig.tight_layout()

# Display the chart
plt.show()







# Creating scatter graph on average num parts by year:

parts_per_set = sets_by_year.agg({'num_parts': pd.Series.mean})
parts_per_set = parts_per_set[:-2]

parts_per_set.rename(columns = {'num_parts': 'avg_num_parts' }, inplace = True)



sns.set_theme(style="whitegrid", context="talk")

plt.figure(figsize=(12, 6))

# Plot using Seaborn's scatterplot
# - 's' makes the dots larger
# - 'alpha' adds slight transparency so overlapping dots are visible
# - 'edgecolor' adds a crisp border to each dot
sns.scatterplot(
    x=parts_per_set.index,
    y=parts_per_set.avg_num_parts,
    color="#219ebc",     # A sleek, modern cerulean blue
    s=120,               # Marker size
    alpha=0.8,           # Transparency
    edgecolor="black",   # Crisp border around markers
    linewidth=0.5
)

# titles and axis labels
plt.title('Average Number of Parts per Set Over Time', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Year', fontsize=14, fontweight='bold', labelpad=10)
plt.ylabel('Average Number of Parts', fontsize=14, fontweight='bold', labelpad=10)

# Remove the top and right borders for a cleaner look
sns.despine(top=True, right=True)

# Adjust layout to prevent clipping
plt.tight_layout()

# Display the chart
plt.show()









#Number of Sets per LEGO Theme


# Themes dataframe:

themes = pd.read_csv('csv_files/themes.csv')

print("\n Themes :")
print(themes.head())



# Converting value_counts data to a dataframe with indexes
# Themes id's refer the same theme so we create a new set from the first "sets" dataframe to get the number of counts of these sets.

set_theme_count = sets["theme_id"].value_counts()
set_theme_count = pd.DataFrame({'id': set_theme_count.index, 'set_count': set_theme_count.values})
print(set_theme_count.head())



# Now we are merging the two sets on id.

merged_df = pd.merge(set_theme_count, themes, on='id')
merged_df.sort_values('set_count', ascending=False)

print("\n Merged Dataframe")
print(merged_df.head())





sns.set_theme(style="whitegrid", context="talk")

fig, ax = plt.subplots(figsize=(14, 7))

# 3Create the bar plot
# - 'hue' and 'palette' work together to create a beautiful color gradient
#   (we set legend=False since the x-axis already tells us the names)
# - 'crest' is a modern, professional blue-green gradient palette
# - 'edgecolor' adds a crisp outline to the bars
sns.barplot(
    x=merged_df.name[:10],
    y=merged_df.set_count[:10],
    hue=merged_df.name[:10],
    palette="muted",
    edgecolor=".2",
    width=0.8,
    legend=False
)


plt.title('Top 10 Themes by Number of Sets', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Theme Name', fontsize=14, fontweight='bold', labelpad=10)
plt.ylabel('Number of Sets', fontsize=14, fontweight='bold', labelpad=10)

# Format the tick marks
# - rotation=45 and ha='right' perfectly align long text labels so they don't overlap
# wrap labels
# wrap labels

labels = ax.get_xticklabels()
new_labels = [textwrap.fill(label.get_text(), 12) for label in labels]

# Reapply them
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(new_labels)

plt.xticks(fontsize=12, fontweight='bold')
plt.yticks(fontsize=12)

# 6. Clean up the borders (despine)
# Removing the left, top, and right borders makes the chart feel light and modern
sns.despine(left=True, top=True, right=True)

# Adjust layout so the rotated labels don't get cut off at the bottom
plt.tight_layout()

# Display the chart
plt.show()

