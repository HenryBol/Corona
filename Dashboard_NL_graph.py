# =============================================================================
# Covid-19 : graph of Covid-19 spreading in The Netherlands
# =============================================================================
# version 1: March 25th, 2020 Henry Bol

# data input: www.rivm.nl
# data has partly been extracted from the wayback machine and has already been preprocessed in correct formats
# output: for visualisation in Tableau


# =============================================================================
# Import the libraries
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle


# =============================================================================
# Load the data
# =============================================================================
df = pd.DataFrame()
filename = read('output/NL_dataframe.pkl', 'rb')
df = pickle.load(file)
file

# =============================================================================
# Process the data
# =============================================================================
# Create new df with sum of values
df_sum = pd.Datadf(df.sum())
# Rename column name to Confirmed
df_sum.columns = ['Confirmed']

# Add delta ('first derivative') and inflection ('second derivative')
df_sum['Delta'] = 0.
df_sum['Inflection'] = 0.
for i in range(1,len(df_sum)):
    df_sum.Delta[i] = (df_sum.Confirmed[i] - df_sum.Confirmed[i-1]).astype(float)    
for i in range(2,len(df_sum)):
    df_sum.Inflection[i] = (df_sum.Delta[i] / df_sum.Delta[i-1]).astype(float)

# Set Date as a seperate feature
df_sum.reset_index(inplace=True)
df_sum.rename(columns={'index': 'Date'}, inplace=True)


# =============================================================================
# Plot the data
# =============================================================================
fig, ax1 = plt.subplots()

# Confirmed cases
color = 'tab:orange'
ax1.set_xlabel('Date')
ax1.set_ylabel('Confirmed', color=color)
ax1.set_title('The Netherlands - Covid-19 cases / inflection')
ax1.plot(df_sum['Date'], df_sum['Confirmed'], color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.tick_params(axis="x", labelsize=7)
ax1.set_xticks(df_sum['Date'][::2])
ax1.set_xticklabels(df_sum['Date'][::2], rotation=45)

# Second derivative (inflection point is the point where convex turns into concave)
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Inflection', color=color)
ax2.plot(df_sum['Date'], df_sum['Inflection'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# ax3 = ax1.twinx()
# color = 'tab:blue'
# ax3.set_ylabel('% death rate', color=color)
# ax3.plot(df_data_country['date'], df_data_country['% death rate'], color=color)
# ax3.tick_params(axis='y', labelcolor=color)
# ax3.spines["right"].set_position(("axes", 1.2))         

fig.tight_layout() # otherwise the right y-label is slightly clipped
plt.show()
