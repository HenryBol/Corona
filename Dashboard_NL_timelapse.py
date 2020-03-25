# =============================================================================
# Covid-19 : visualisation of Covid-19 spreading in The Netherlands
# =============================================================================
# version 1: March 24th, 2020 Henry Bol

# data input: www.rivm.nl
# data has partly been extracted from the wayback machine and has already been preprocessed in correct formats
# output: for visualisation in Tableau


# =============================================================================
# Import the libraries
# =============================================================================
import pandas as pd
import glob
import regex as re
import datetime as dt
import pickle

# =============================================================================
# Import RIVM data
# =============================================================================
all_files = glob.glob("rivm_daily_report/*.csv")
all_files.sort(key=lambda f: int(re.sub('\D', '', f))) # sort in the right order

# Put all csv files in a list
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=0, sep=';')
    li.append(df)

# And put it all in a datadf
df = pd.concat(li, axis=1, join='outer').sort_index()


# =============================================================================
## Clean up dataframe
# =============================================================================
# NaN handling
df = df.fillna(0)

# Delete the 'Aantal per 100.000 inwoners'
df.drop(columns = ['Aantal per 100.000 inwoners'], inplace=True)

# Combine 'double' named municipalities
municipalities = df.index
df.loc['Beekdaelen'] += df.loc['BeekDaelen']
df.drop('BeekDaelen', inplace=True)
df.loc['Bergen (NH)'] += df.loc['Bergen (NH.)']
df.drop('Bergen (NH.)', inplace=True)
df.loc['Hengelo (O)'] += df.loc['Hengelo']
df.drop('Hengelo', inplace=True)
df.loc['Súdwest-Fryslân'] += df.loc['Súdwest Fryslân']
df.drop('Súdwest-Fryslân', inplace=True)


dates = ['2020-03-04', '2020-03-05', '2020-03-06', '2020-03-07', '2020-03-08', '2020-03-09', '2020-03-10', 
         '2020-03-11','2020-03-12', '2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16', '2020-03-17', 
         '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21', '2020-03-22', '2020-03-23', '2020-03-24', 
         '2020-03-25']
df.columns = dates

# TODO Set column names to dates(work in progress - not matching the df_long format)
# start_date = dt.date(2020, 3, 4) # March 4th is start of RIVM reporting
# end_date   = dt.date.today()
# dates = [start_date + dt.timedelta(n) for n in range(int((end_date - start_date).days))]
# df.columns = dates


## Save data
filename = 'output/NL_dataframe.pkl'
with open(filename, 'wb') as file:
    pickle.dump(df, file)


# =============================================================================
# Location to Latitude and Longitude
# =============================================================================
# Add latitude and longitude for each location
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises", timeout=3)
df['Latitude'] = 0.
df['Longitude'] = 0.
for i in range(len(df)):
    loc = df.index[i]
    location = geolocator.geocode(loc)
    df.Latitude[i] = location.latitude
    df.Longitude[i] = location.longitude
    print(loc)

# Adjust manually some misplaced locations (updates from www.latlong.net)
df.Latitude['Altena'] = 51.814560
df.Longitude['Altena'] = 4.994680
df.Latitude['Borne'] = 52.300500
df.Longitude['Borne'] = 6.755500
df.Latitude['Elburg'] = 52.448750
df.Longitude['Elburg'] = 5.833340
df.Latitude['Epe'] = 52.347810
df.Longitude['Epe'] = 5.983990
df.Latitude['Grave'] = 51.757870
df.Longitude['Grave'] = 3.890290
df.Latitude['Goes'] = 51.503979
df.Longitude['Goes'] = 3.890290
df.Latitude['Kapelle'] = 51.486350
df.Longitude['Kapelle'] = 3.959130
df.Latitude['Harlingen'] = 53.173640
df.Longitude['Harlingen'] = 5.420870
df.Latitude['Soest'] = 52.173380
df.Longitude['Soest'] = 5.312920
df.Latitude['Vlissingen'] = 51.455681
df.Longitude['Vlissingen'] = 3.576490
df.Latitude['Westland'] = 51.992490
df.Longitude['Westland'] = 4.207630
df.Latitude['Den Helder'] = 52.957380
df.Longitude['Den Helder'] = 4.758500
df.Latitude['Texel'] = 53.053921
df.Longitude['Texel'] = 4.796050
df.Latitude['Vlieland'] = 53.296860
df.Longitude['Vlieland'] = 5.074790
df.Latitude['Terschelling'] = 53.358290
df.Longitude['Terschelling'] = 5.216040
df.Latitude['Ameland'] = 53.446240
df.Longitude['Ameland'] = 5.686010

# Keep copy of Latitude/Longitude (to avoid running geolocator every time)
df_lat_long = df[['Latitude', 'Longitude']]
# df['Latitude'] = df_lat_long['Latitude']
# df['Longitude'] = df_lat_long['Longitude']

# Set index ('city') as seperate feature
df.reset_index(inplace=True)
df = df.rename(columns = {'index': 'city'})
df.to_csv('output/rivm_data_nl.csv')

# Check confirmed todays cases (located to a municipality)
df[df.columns[-3]].sum() # 3rd last column


# =============================================================================
# Export file for input to Tableau visualization
# =============================================================================
# Create a 'long' datadf with all dates under each other 
df_long = pd.melt(df, id_vars=['city', 'Latitude', 'Longitude'], 
                     value_vars=['2020-03-04', '2020-03-05', '2020-03-06', '2020-03-07', '2020-03-08', '2020-03-09', '2020-03-10', 
                                 '2020-03-11','2020-03-12', '2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16', '2020-03-17', 
                                 '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21', '2020-03-22', '2020-03-23', '2020-03-24', 
                                 '2020-03-25'],
                     var_name='date', value_name='confirmed')

# Set correct data types 
df_long['date'] =  pd.to_datetime(df_long['date']).dt.date
df_long['confirmed'] = df_long['confirmed'].astype('int32')
# df_long.info()

# Write output file
df_long.to_csv('output/rivm_data_nl_{}.csv'.format(dt.date.today()))

