# =============================================================================
# Covid-19 : graphs of Covid-19 development per country 
# =============================================================================
# version 1: March 25th, 2020 Henry Bol

# data input: John Hopkins (via jason from pomber.github)
# output: graph of confirmed, death, death rate, recovered


# =============================================================================
# Import the libraries
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# Import json from pomber and preprocess and plot
# =============================================================================
import urllib.request, json 
with urllib.request.urlopen("https://pomber.github.io/covid19/timeseries.json") as url:
    data = json.loads(url.read().decode())
    # print(data)


# =============================================================================
# Process data
# =============================================================================
## Initialization
# Choose country
# data.keys() # list of countries
# country = 'Korea, South'
country = 'Netherlands'
# country = 'Ireland'
# country = 'Greece'
slice_country = True # on or off
# Choose log scale or not (to check linear growth in exponential curve)
log = False # on or off


## Create data file
# Create country dictionary
dict_country = {k: v for k, v in data.items() if k.startswith(country)}
data_country = dict_country.values()
data_country = list(dict_country.values())

# Create conutry dataframe
a = np.zeros(shape=(np.size(data_country),4))
df_data_country = pd.DataFrame(a, columns = ['date', 'confirmed', 'deaths', 'recovered'])

# Features
for i in range(np.size(data_country)):
    df_data_country.loc[[i], ['date']] = dict_country[country][i]['date']
    df_data_country.loc[[i], ['confirmed']] = dict_country[country][i]['confirmed']
    df_data_country.loc[[i], ['deaths']] = dict_country[country][i]['deaths']
    df_data_country.loc[[i], ['recovered']] = dict_country[country][i]['recovered'] 


# Death rate
df_data_country['% death rate'] = (df_data_country['deaths'] / df_data_country['confirmed'])*100

# Slice from point in time (starting point of breakout)
if slice_country:
    slice = np.nonzero(df_data_country['confirmed'].to_numpy())[0][0] # first index with non-zero value
    df_data_country = df_data_country[slice:]

# Log scale
if log:
    df_data_country.confirmed = np.log(df_data_country.confirmed)
    df_data_country.deaths = np.log(df_data_country.deaths)
    df_data_country.recovered = np.log(df_data_country.recovered)


# =============================================================================
# Plot data
# =============================================================================
# Confirmed cases
fig, ax1 = plt.subplots()
color = 'tab:orange'
ax1.set_title('Covid-19 {}'.format(country), fontsize=10)
ax1.set_xlabel('date')
if log:
    ax1.set_ylabel('# confirmed (log)', color=color)
else: 
    ax1.set_ylabel('# confirmed', color=color)
ax1.plot(df_data_country['date'], df_data_country['confirmed'], color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax1.tick_params(axis="x", labelsize=7)
ax1.set_xticks(df_data_country['date'][::10])
ax1.set_xticklabels(df_data_country['date'][::10], rotation=45)

# No. of deaths
ax2 = ax1.twinx()
color = 'tab:red'
if log:
    ax2.set_ylabel('# deaths (log)', color=color)
else:
    ax2.set_ylabel('# deaths', color=color)
ax2.plot(df_data_country['date'], df_data_country['deaths'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Death rate
ax3 = ax1.twinx()
color = 'tab:blue'
ax3.set_ylabel('% death rate', color=color)
ax3.plot(df_data_country['date'], df_data_country['% death rate'], color=color)
ax3.tick_params(axis='y', labelcolor=color)
ax3.spines["right"].set_position(("axes", 1.2))                                                
     
# Recovered cases
# ax4 = ax1.twinx()
# color = 'tab:green'
# if log:
#     ax4.set_ylabel('# recovered (log)', color=color)
# else:
#     ax4.set_ylabel('# recovered', color=color)
# ax4.plot(df_data_country['date'], df_data_country['recovered'], color=color)
# ax4.tick_params(axis='y', labelcolor=color)
# ax4.spines["right"].set_position(("axes", 1.6))  

# Plot total
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
