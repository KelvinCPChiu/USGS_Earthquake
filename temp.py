import json
from pathlib2 import Path
import os
import pandas
import pickle

#import numpy
#import urllib.request

def load_data(filename):
    with open(filename) as f:
        return json.loads(f.read())
    
yyear = 2018
filedir = Path('D:\Google Drive\Myself\Mechince Learning\Pytorch\EarthQuake\{}.json'.format(yyear))

# The json file are saved in an order of the year in the current directory as 'year'.json

filedir = os.path.normpath(filedir)
print(filedir)

datalist = load_data(filedir)['features']
# Data List from Json file.
keys = ['Event', 'Date', 'Magnitude', 'Gap', 'Dmin', 'Coordinates']
Data = {key: [] for key in keys}
number_of_events = len(datalist)

#print(datalist[0])
print('Number of Events in {} : {}'.format(yyear, number_of_events))
# The detail of the keys should referring to URL of USGS below:
# https://earthquake.usgs.gov/data/comcat/data-eventterms.php
# and https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php

for temp_data in datalist:
    
    # Pandas can directly reading data from json.
    
    if temp_data['properties']['type']=='earthquake':
        
        #temp_prop = temp_data['properties']
        #temp_geo = temp_data['geometry']
        #print(temp_prop, '\n', temp_geo, '\n')
        temp_event_name, temp_event_date= temp_data['properties']['place'], temp_data['properties']['time']
        
        # Times are reported in milliseconds since the epoch ( 1970-01-01T00:00:00.000Z)
        # Leap Seconds are ignored
        temp_mag, temp_gap, temp_dmin = temp_data['properties']['mag'], temp_data['properties']['gap'], temp_data['properties']['dmin']
        # mag : magnitude of the earthquake event, 
        # gap : the largest azimuthal gap between azimuthally adjacent stations,(the smaller the gap, the lesser the uncertainty
        # dmin : Horizontal distance from the epicenter to the nearest station (in degrees).
        temp_coor = temp_data['geometry']['coordinates']
        # The coordinates are encoded the array as [longitude, latitude, depth]
                
        #print(temp_coor)
        #temp_mag = temp_data['properties']['mag']
        #temp_tsunami = temp_data['properties']['tsunami']
        
        #temp_coor = numpy.array(temp_data['geometry']['coordinate'])
        
        Data['Event'].append(temp_event_name)
        Data['Date'].append(temp_event_date)
        Data['Magnitude'].append(temp_mag)
        Data['Coordinates'].append(temp_coor)
        Data['Gap'].append(temp_gap)
        Data['Dmin'].append(temp_dmin)
        
        
#print(datadict)
#print(type(datadict))
DataFrame = pandas.DataFrame.from_dict(Data)
print(DataFrame)
print('Saving the Data Frame.')
DataFrame.to_pickle("./DataFrame.pkl")
print('Finished saving of the Data Frame.')
