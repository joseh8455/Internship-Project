import json
import pprint
import time
import tkinter as tk

import googlemaps
import pandas as pd
import requests

import APIkeys
import intro


class CollegeWindow():


    def __init__(self):
        global base_url
        self.Gkey = APIkeys.googleKey()
        self.tk = tk.Tk()
        base_url = "https://educationdata.urban.org/api/v1/college-university/"

    def ColWindow(self):

        self.tk.title('Baldoor Information Gathering')
        self.tk.geometry('440x500')
     
        #this is for the api that has data from 2019 years before (still updating for data in 2020?)

        # google api information is here
        global google_opts
        google_opts = ['name', 'type', 'url', 'formatted_address', 'formatted_phone_number', 'price_level', 'rating', 'opening_hours/weekday_text', 'permanently_closed']
        google_formtd = '\n'.join(google_opts)

        basic_info = tk.Label(self.tk, text = "Basic piece of information you wish to retrieve: ", font=("Roboto"))
        basic_info.pack()

        basic_frame = tk.LabelFrame(self.tk, text="Basic information options", font=("Roboto"))
        basic_frame.pack(ipadx=10)
        basic_options = tk.Label(basic_frame, text= google_formtd, font=("Roboto"))
        basic_options.pack()


        #able to be access entry information in any function i want with the global tag
        global basic_entry
        basic_entry = tk.Entry(self.tk, textvariable='goolemapsAPI')
        basic_entry.focus()
        basic_entry.pack(ipadx=70, pady=20)

        self.google_button = tk.Button(self.tk, text="Display Information", command = lambda: self.PrintOut())
        self.google_button.pack(padx=10)

    def GoogleData(self):
        #this is just basic information on google
        #retrieve the entries from the first page (intro.py Entry fields)
        info = intro.IntroPage()

        location = info.locationRetrieval()
        radius = info.radiusRetrieval()
        type = info.typeRetrieval()
        GKey = APIkeys.googleKey()

        user_entry = basic_entry.get().split()

        #paramaters for places_nearby search 
        params = {
            'location': location,
            'radius': radius,
            'type': type
        }
        gplaces = googlemaps.Client(key = GKey)
        search = gplaces.places_nearby(**params)

        #filters the inputs to only the ones that are needed for the google api with this
        intersection_set = list(set.intersection(set(google_opts ), set(user_entry)))

        #gplaces.place dump
        info_dump = []
        
        #pagination in order to get all of the pages and display the options available
        if 'next_page_token' in search.keys():
            while 'next_page_token' in search.keys():
                time.sleep(2)
                params.update({'page_token': search['next_page_token']})
                search = gplaces.places_nearby(**params)
                for ids in search['results']:
                    places_result = gplaces.place(place_id = ids['place_id'], fields = intersection_set)
                    # return places_result
                    info_dump.append(places_result['result'])
        else:
            for ids in search['results']:
                    places_result = gplaces.place(place_id = ids['place_id'], fields = intersection_set)
                    info_dump.append(places_result['result'])
        
        #returns the last dataframe here
        for i in range(0, len(info_dump)):
            if i == (len(info_dump) - 1):
                df = pd.DataFrame(info_dump)
                return (df)

    def CollegeAPI(self):
        print('placeholder')



    def PrintOut(self):


        self.GoogleData().to_excel('UniversityData.xlsx', sheet_name='Google Data', index=False, na_rep='N/A')
        #auto adjust rows width in excel
        # for column in df2:
        #     column_width = max(df2[column].astype(str).map(len).max(), len(column))
        #     col_idx = df2.columns.get_loc(column)
        #     writer.sheets['Information Grabbed'].set_column(col_idx, col_idx, column_width)
