# =============================================================================
# Covid-19 : visualisation of Covid-19 spreading in The Netherlands
# =============================================================================
# version 1: March 24th, 2020 Henry Bol

# data input: www.rivm.nl
# data has partly been extracted from the wayback machine and has already been preprocessed in correct formats)
# output: for visualisation in Tableau


# =============================================================================
# Import the libraries
# =============================================================================
import pandas as pd
import glob
import regex as re
import datetime as dt


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

# And put it all in a dataframe
frame = pd.concat(li, axis=1, join='outer').sort_index()


# =============================================================================
## Clean up frame
# =============================================================================
# NaN handling
frame = frame.fillna(0)

# Combine 'double' named cities
# frame.loc[Beekdaelen,:] += frame[BeekDaelen]
# Bergen()

# Delete the 'Aantal per 100.000 inwoners'
frame.drop(columns = ['Aantal per 100.000 inwoners'], inplace=True)

# Set column names to dates
frame.columns = ['2020-03-04', '2020-03-05', '2020-03-06', '2020-03-07', '2020-03-08', '2020-03-09', '2020-03-10', 
                     '2020-03-11','2020-03-12', '2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16', '2020-03-17', 
                     '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21', '2020-03-22', '2020-03-23']


# =============================================================================
# Location to Latitude and Longitude
# =============================================================================
# Add latitude and longitude for each location
import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises", timeout=3)
frame['Latitude'] = 0.
frame['Longitude'] = 0.
for i in range(len(frame)):
    loc = frame.index[i]
    location = geolocator.geocode(loc)
    frame.Latitude[i] = location.latitude
    frame.Longitude[i] = location.longitude
    print(loc)

# Keep copy of Latitude/Longitude
frame_lat_long = frame[['Latitude', 'Longitude']]

# Adjust manually some misplaced locations 
# Latitude and Longitude corrections from www.latlong.net
frame.Latitude['Altena'] = 51.814560
frame.Longitude['Altena'] = 4.994680
frame.Latitude['Borne'] = 52.300500
frame.Longitude['Borne'] = 6.755500
frame.Latitude['Elburg'] = 52.448750
frame.Longitude['Elburg'] = 5.833340
frame.Latitude['Epe'] = 52.347810
frame.Longitude['Epe'] = 5.983990
frame.Latitude['Grave'] = 51.757870
frame.Longitude['Grave'] = 3.890290
frame.Latitude['Goes'] = 51.503979
frame.Longitude['Goes'] = 3.890290
frame.Latitude['Kapelle'] = 51.486350
frame.Longitude['Kapelle'] = 3.959130
frame.Latitude['Harlingen'] = 53.173640
frame.Longitude['Harlingen'] = 5.420870
frame.Latitude['Soest'] = 52.173380
frame.Longitude['Soest'] = 5.312920
frame.Latitude['Vlissingen'] = 51.455681
frame.Longitude['Vlissingen'] = 3.576490
frame.Latitude['Westland'] = 51.992490
frame.Longitude['Westland'] = 4.207630

frame.reset_index(inplace=True)
frame = frame.rename(columns = {'index': 'city'})
frame.to_csv('output/rivm_data_nl.csv')

# Check confirmed cases
frame['2020-03-23'].sum()



# =============================================================================
# Export file for input to Tableau visualization
# =============================================================================
# Create a 'long' dataframe with all dates under each other 
frame_long = pd.melt(frame, id_vars=['city', 'Latitude', 'Longitude'], 
                     value_vars=['2020-03-04', '2020-03-05', '2020-03-06', '2020-03-07', '2020-03-08', '2020-03-09', '2020-03-10', 
                     '2020-03-11','2020-03-12', '2020-03-13', '2020-03-14', '2020-03-15', '2020-03-16', '2020-03-17', 
                     '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21', '2020-03-22', '2020-03-23'],
                     var_name='date', value_name='confirmed')

# Set correct data types 
frame_long['date'] =  pd.to_datetime(frame_long['date']).dt.date
frame_long['confirmed'] = frame_long['confirmed'].astype('int32')
# frame_long.info()

# Write output file
frame_long.to_csv('output/rivm_data_nl_{}.csv'.format(dt.date.today()))

