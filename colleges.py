import time
import tkinter as tk

import os

import googlemaps
import pandas as pd
import requests

import APIkeys
import intro


class CollegeWindow():
    
    def __init__(self):
        self.tk = tk.Tk()
        self.image = tk.PhotoImage(name= 'logo.png')

    def CollegeWindow(self):
        self.tk.title('Baldoor Information Gathering')
        self.tk.geometry('440x500')
        

        #basic information gathering for it to be used in the api link
        #layout of UI (this is basic and doesnt look modern)

        global state_entry
        state_code = tk.Label(self.tk, text="What is the state code you wish to get information on?", font= ("Roboto"))
        state_code.pack()

        state_entry = tk.Entry(self.tk)
        state_entry.focus()
        state_entry.pack(ipadx=70, pady=20)


        global api_options_list
        api_options_list = ['schoolName', 'phone', 'schoolLevel', 'numberOfStudents', 'teachersFulltime', 'percentFreeDiscLunch']
        api_formatted_options = '\n'.join(api_options_list)

        basic_info = tk.Label(self.tk, text = "Information you wish to retrieve: ", font=("Roboto"))
        basic_info.pack()

        basic_frame = tk.LabelFrame(self.tk, text="Information retrieval options", font=("Roboto"))
        basic_frame.pack(ipadx=10)
        api_options = tk.Label(basic_frame, text= api_formatted_options, font=("Roboto"))
        api_options.pack()

        #able to be access entry information in any function i want with the global tag
        global basic_entry
        basic_entry = tk.Entry(self.tk, textvariable='goolemapsAPI')
        basic_entry.pack(ipadx=70, pady=20)

        self.google_button = tk.Button(self.tk, text="Display Information", command = lambda: self.GoogleData())
        self.google_button.pack(padx=10)
    
    def GoogleData(self):
        #this is just basic information on google
        #retrieve the entries from the first page (intro.py Entry fields)
        info = intro.IntroPage()

        location = info.locationRetrieval()
        radius = info.radiusRetrieval()
        type = info.typeRetrieval()
        GKey = APIkeys.googleKey()

        #paramaters for places_nearby search 
        params = {
            'location': location,
            'radius': radius,
            'type': type
        }
        gplaces = googlemaps.Client(key = GKey)
        search = gplaces.places_nearby(**params)

        #filters the inputs to only the ones that are needed for the google api with this
        google_opts = ['name', 'type', 'formatted_address', 'formatted_phone_number', 'rating', 'opening_hours/weekday_text']

        #gplaces.place dump
        info_dump = []
        
        #pagination in order to get all of the pages and display the options available
        if 'next_page_token' in search.keys():
            while 'next_page_token' in search.keys():
                time.sleep(2)
                params.update({'page_token': search['next_page_token']})
                search = gplaces.places_nearby(**params)
                for ids in search['results']:
                    places_result = gplaces.place(place_id = ids['place_id'], fields = google_opts)
                    # return places_result
                    info_dump.append(places_result['result'])
        
        #returns the last dataframe here
        for i in range(0, len(info_dump)):
            if i == (len(info_dump) - 1):
                df = pd.DataFrame(info_dump)
                print (df)

    def PrintOut(self):
   
        writer = pd.ExcelWriter('CollegeData.xlsx', engine='xlsxwriter')

        #information retained from school digger, if you want to buy api license you can get this information and more information (right now just displays dummy data)
        df2 = self.GoogleData()

        df2.to_excel(writer, sheet_name='Google Data', index=False, na_rep='N/A')

        #auto adjust rows width in excel
        # for column in df2:
        #     column_width = max(df2[column].astype(str).map(len).max(), len(column))
        #     col_idx = df2.columns.get_loc(column)
        #     writer.sheets['Information Grabbed'].set_column(col_idx, col_idx, column_width)
