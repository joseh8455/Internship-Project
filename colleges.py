import os
import pprint
import time
import tkinter as tk
from tkinter import messagebox

import googlemaps
import pandas as pd
import requests

import APIkeys
import intro


class CollegeWindow():


    def __init__(self):
        self.Gkey = APIkeys.googleKey()
        self.tk = tk.Tk()

    def ColWindow(self):

        self.tk.title('Baldoor Information Gathering')
        self.tk.geometry('440x500')
     
        #this is for the api that has data from 2019

        # google api information is here
        global google_opts, api_options
        google_opts = ['name', 'url', 'formatted_address', 'formatted_phone_number', 'price_level', 'rating', 'opening_hours/weekday_text', 'permanently_closed']
        google_formtd = '\n'.join(google_opts)

        api_options = ['url_school','inst_size', 'chief_admin_name', 'chief_admin_title']
        api_formatted = '\n'.join(api_options)

        basic_info = tk.Label(self.tk, text = "Basic piece of information you wish to retrieve: ", font=("Roboto"))
        basic_info.pack()

        basic_frame = tk.LabelFrame(self.tk, text="Basic information options", font=("Roboto"))
        basic_frame.pack(ipadx=10)
        basic_options = tk.Label(basic_frame, text= google_formtd, font=("Roboto"))
        basic_options.pack()
        api_options_display = tk.Label(basic_frame, text= api_formatted, font=("Roboto"))
        api_options_display.pack()


        #able to be access entry information in any function i want with the global tag
        global basic_entry
        basic_entry = tk.Entry(self.tk, textvariable='goolemapsAPI')
        basic_entry.focus()
        basic_entry.pack(ipadx=70, pady=20)

        self.google_button = tk.Button(self.tk, text="Display Information", command = lambda: self.PrintOut())
        self.google_button.pack(padx=10)

    def GoogleData(self):
        
        #retrieve the entries from the first page (intro.py Entry fields)
        info = intro.IntroPage()

        location = info.locationRetrieval()
        radius = info.radiusRetrieval()
        type = info.typeRetrieval()

        #paramaters for places_nearby
        params = {
            'location': location,
            'radius': radius,
            'type': type
        }

        gplaces = googlemaps.Client(key = self.Gkey)

        search = gplaces.places_nearby(**params)

        entries = basic_entry.get().split()
        intersection_set = list(set.intersection(set(google_opts ), set(entries)))

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
        
        for i in range(0, len(info_dump)):
            if i == (len(info_dump) - 1):
                df = pd.DataFrame(info_dump)
                return df

    def CollegeAPI(self):
        #list of information that is going to be used
        api_information = basic_entry.get().split()
        user_list = list(set.intersection(set(api_options), set(api_information)))
        user_list.append('inst_name')
        #information that is going to be used in the url
        getter = intro.IntroPage()
        state_fips = getter.statefipsRetrieval()
        county_fips = getter.countyFIPSRetrieval()
        
        #https://educationdata.urban.org/api/v1/college-university/ipeds/directory/2019/?fips=36&county_fips=36119 <- this is what the url should look like
        start_url = f"https://educationdata.urban.org/api/v1/college-university/ipeds/directory/2019/?fips={state_fips}&county_fips={county_fips}"

        req = requests.get(start_url)

        data = req.json()

        #change some information value in the dataset
        for info in data['results']:
            if info['inst_size'] == 1:
                info['inst_size'] = "Under 1000"
            elif info['inst_size'] == 2:
                info['inst_size'] = "1,000 - 4,999"
            elif info['inst_size'] == 3:
                info['inst_size'] = "5,000 - 9,9999"
            elif info['inst_size'] == 4:
                info['inst_size'] ="10,000 - 19,999"
            elif info['inst_size'] == 5:
                info['inst_size'] = "20k and above" 
            else:
                info['inst_size'] = "N/A"
        
        df = pd.DataFrame(data['results'], index=None)

        df1 = df[user_list]
        return df1


    def PrintOut(self):
        writer1 = pd.ExcelWriter(path=r'C:\Users\Jhernandez\Downloads\UniData.xlsx', engine='xlsxwriter')

        df1 = self.GoogleData()
        df2 = self.CollegeAPI()

        df1.to_excel(writer1, sheet_name="Google Data", na_rep="N/A", index=False)
        df2.to_excel(writer1, sheet_name="API Data", na_rep="N/A", index=False)
        writer1.save()

        size = os.path.getsize(filename=writer1)
        if size > 0:
            try:
                test = messagebox.askyesno(title="Sucess!", message="Successfully created file. Do you wish to open it now? " + os.path.basename(writer1))
                if test == True:
                    os.system(r"start EXCEL.EXE C:\Users\Jhernandez\Downloads\UniData.xlsx")
            except:
                    print("Impossible to get here")
        else:
            return messagebox.showerror("Error", "Error message.")

        #auto adjust rows width in excel
        # for column in df2:
        #     column_width = max(df2[column].astype(str).map(len).max(), len(column))
        #     col_idx = df2.columns.get_loc(column)
        #     writer.sheets['Information Grabbed'].set_column(col_idx, col_idx, column_width)
