import os
import time
import tkinter as tk
from tkinter import messagebox

import googlemaps
import pandas as pd
import requests

import APIkeys
import intro

#global variables created
digID = None
digKey = None
digURL = None
basic_entry = None
api_options_list = None
state_entry = None
zip_entry = None
specific_digURL = None
google_opts = None


class SchoolWindow():

    def __init__(self):
        global digID, digKey, digURL, specific_digURL

        digID = APIkeys.diggerID()

        digKey = APIkeys.diggerKey()

        digURL = 'https://api.schooldigger.com/v1.2/schools?'

        specific_digURL = 'https://api.schooldigger.com/v1.2/schools/'
        
        self.tk = tk.Tk()

    def schoolWindow(self):
        self.tk.title('Baldoor Information Gathering')
        self.tk.geometry('440x500')


        #basic information gathering for it to be used in the api link
        #layout of UI (this is basic and doesnt look modern)

        global api_options_list, google_opts
        google_opts = ['name', 'formatted_address', 'formatted_phone_number', 'rating', 'opening_hours/weekday_text','permanently_closed']
        google_formatted = '\n'.join(google_opts)

        api_options_list = ['schoolLevel', 'numberOfStudents', 'teachersFulltime', 'percentFreeDiscLunch']
        api_formatted_options = '\n'.join(api_options_list)

        basic_info = tk.Label(self.tk, text = "Information you wish to retrieve: ", font=("Roboto"))
        basic_info.pack()

        basic_frame = tk.LabelFrame(self.tk, text="Information retrieval options", font=("Roboto"))
        basic_frame.pack(ipadx=10)
        google_options = tk.Label(basic_frame, text = google_formatted, font = ("Roboto"))
        google_options.pack()
        api_options = tk.Label(basic_frame, text= api_formatted_options, font=("Roboto"))
        api_options.pack()

        #able to be access entry information in any function i want with the global tag
        global basic_entry
        basic_entry = tk.Entry(self.tk, textvariable='goolemapsAPI')
        basic_entry.focus()
        basic_entry.pack(ipadx=70, pady=20)

        self.google_button = tk.Button(self.tk, text="Display Information", command = lambda: self.PrintOut())
        self.google_button.pack(padx=10)

    
    def SchoolData(self):

        #this piece of code returns the set of keys that need to be accessed with more information and the ones that dont need to be
        more_indepth = ['numberOfStudents', 'teachersFulltime', 'percentFreeDiscLunch']
        basic_info = ['schoolName', 'phone', 'schoolLevel']
        user_entry = basic_entry.get().split()

        #get all the keys thanks to user entries
        intersection_set = set.intersection(set(more_indepth ), set(user_entry))
        user_list = list(set.intersection(set(basic_info), set(user_entry)))
        user_list.insert(0,'schoolName')
        user_list.insert(1,'phone')
        
        #retrieve information that will be used in the url
        getter = intro.IntroPage()
        state_info = getter.stateRetrieval()
        zip_code = getter.zipCode()

        #url example -> https://api.schooldigger.com/v1.2/schools?st=NY&zip=10474&appID=639d1add&appKey=1cb4b90b8078b87d24aa6b6821993a24
        url = requests.get(digURL + f'st={state_info}&zip={zip_code}&appID={digID}&appKey={digKey}')
        data = url.json()


        #this one is works perfectly fine as is
        df = pd.DataFrame(data['schoolList'])      
        basic_result = df[user_list]

        #test2
        num_school = -1
        dump = []

        while num_school != data['numberOfSchools']-1:
            num_school+=1
            df2 = pd.DataFrame(data['schoolList'][num_school]['schoolYearlyDetails'])
            #dump the dataframes created into the list, use of head(1) to get the first element since there are several dictionaries inside the list, we want the first
            #one which is the latest information (2020)
            dump.append(df2[list(intersection_set)].head(1))

            #because all the dataframes that were appened to the list were seperate, this combines all of them into one big dataframe without repeating index numbers
            result = pd.concat(dump, ignore_index=True)
        
        #retrieves the last dataframe in the list since for each one, when a new line is added, it prints out a new dataframe
        for i in range(0, len(result)):
            if i == (len(result) - 1):
                result

        #this combines the first and second dataframe created into one big dataframe that will be printed out into an excel sheet to use       
        return pd.concat([basic_result, result],axis=1, ignore_index=False)

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
                return df




    #print out dataframes into an excel sheet
    #the only issues is that it doesnt open the file created when the ask the user if they want to open it
    def PrintOut(self):
   
        writer = pd.ExcelWriter(path=r'C:\Users\Jhernandez\Downloads\SchoolData.xlsx', engine='xlsxwriter')

        #information retained from school digger, if you want to buy api license you can get this information and more information (right now just displays dummy data)
        df = self.SchoolData() 
        df2 = self.GoogleData()

        df.to_excel(writer, sheet_name='Information Grabbed', index=False, na_rep='No Data Available')
        df2.to_excel(writer, sheet_name='Google Data', index=False, na_rep='No Data Available')
        writer.save()

        #this will let the user open up the file that has just been created
        size = os.path.getsize(filename=writer)
        if size > 0:
            try:
                test = messagebox.askyesno(title="Sucess!", message="Successfully created file. Do you wish to open it now? " + os.path.basename(writer))
                if test == True:
                    os.system(r"start EXCEL.EXE C:\Users\Jhernandez\Downloads\SchoolData.xlsx")
            except:
                    print("Impossible to get here")
        else:
            return messagebox.showerror("Error", "Error message.")

        
        # #auto adjust rows width in excel
        # for column in df:
        #     column_width = max(df[column].astype(str).map(len).max(), len(column))
        #     col_idx = df.columns.get_loc(column)
        #     writer.sheets['Information Grabbed'].set_column(col_idx, col_idx, column_width)

    #error handling
    