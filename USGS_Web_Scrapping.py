import urllib.request
import json
from pathlib2 import Path
import os
import pandas
import pickle
# import numpy
# import urllib.request


def get_data_from_url(event_magnitude):
    def read_from_url(url):
        url = url
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        return data

    def save_data(extracted_data, yyear):
        with open('{}.json'.format(yyear), 'w') as outfile:
            json.dump(extracted_data, outfile)

    for year in range(1970, 2018):
        # Data are starting from 1970
        print('Obtaining Data of Year : {}'.format(year))
        link = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={0}-01-01&endtime={0}-01-02&minmagnitude={1}'.format(
            year, event_magnitude)
        data = read_from_url(link)
        save_data(data, year)


def convert_data_to_array():

    def load_data_old(yyear):

        filename = '{}.json'.format(yyear)
        if filename:
            with open(filename) as f:
                return json.loads(f.read())
    data = {}
    for yyear in range(2018, 2019):
        temp_data = load_data_old(yyear)
        temp_data = temp_data['features'][0]
        data = data.append(temp_data)

    return data


def convert_data_to_dataframe():

    def load_data(filename):
        with open(filename) as f:
            return json.loads(f.read())

    keys = ['Event', 'Date', 'Magnitude', 'Gap', 'Dmin', 'Coordinates']
    Data = {key: [] for key in keys}
    # The detail of the keys should referring to URL of USGS below:
    # https://earthquake.usgs.gov/data/comcat/data-eventterms.php
    # and https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php

    for yyear in range(1970, 2019, 1):
        print('Processing year of {}'.format(yyear))
        filedir = Path('D:\Google Drive\Myself\Mechince Learning\Pytorch\EarthQuake\{}.json'.format(yyear))

        # The json file are saved in an order of the year in the current directory as 'year'.json

        filedir = os.path.normpath(filedir)
        print(filedir)

        datalist = load_data(filedir)['features']
        # Data List from Json file.
        number_of_events = len(datalist)
        # print(datalist[0])
        print('Number of Events in {} : {}'.format(yyear, number_of_events))

        for temp_data in datalist:

            # Pandas can directly reading data from json.

            if temp_data['properties']['type'] == 'earthquake':
                # temp_prop = temp_data['properties']
                # temp_geo = temp_data['geometry']
                # print(temp_prop, '\n', temp_geo, '\n')
                temp_event_name, temp_event_date = temp_data['properties']['place'], temp_data['properties']['time']

                # Times are reported in milliseconds since the epoch ( 1970-01-01T00:00:00.000Z)
                # Leap Seconds are ignored
                temp_mag, temp_gap, temp_dmin = temp_data['properties']['mag'], temp_data['properties']['gap'], \
                                                temp_data['properties']['dmin']
                # mag : magnitude of the earthquake event,
                # gap : the largest azimuthal gap between azimuthally adjacent stations,(the smaller the gap, the lesser the uncertainty
                # dmin : Horizontal distance from the epicenter to the nearest station (in degrees).
                temp_coor = temp_data['geometry']['coordinates']
                # The coordinates are encoded the array as [longitude, latitude, depth]

                # print(temp_coor)
                # temp_mag = temp_data['properties']['mag']
                # temp_tsunami = temp_data['properties']['tsunami']

                # temp_coor = numpy.array(temp_data['geometry']['coordinate'])

                Data['Event'].append(temp_event_name)
                Data['Date'].append(temp_event_date)
                Data['Magnitude'].append(temp_mag)
                Data['Coordinates'].append(temp_coor)
                Data['Gap'].append(temp_gap)
                Data['Dmin'].append(temp_dmin)

    # print(datadict)
    # print(type(datadict))
    DataFrame = pandas.DataFrame.from_dict(Data)
    print(DataFrame)
    print('Saving the Data Frame.')
    DataFrame.to_pickle("./DataFrame.pkl")
    print('Finished the saving of the Data Frame.')


def convert_df2csv():

    df = pandas.read_pickle('./DataFrame.pkl')
    df.to_csv('./Data_CSV.csv')


if __name__ == '__main__':
    get_data_from_url(0)
    convert_data_to_dataframe()
    #convert_df2csv()

    #temp = load_data(2018)
    #print(temp)
    #Format of the USGA earthquak data is reading from the URL"
    #The format of the URL is https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson"
    #'https://earthquake.usgs.gov/fdsnws/event/1/count?format=geojson'
    #for year in range()

    #T1 = data['features'][0]
    #T2 = data['features'][1]
    #keys = T1.keys()
    #print(keys)
    #print(T1.values())
    #values =
