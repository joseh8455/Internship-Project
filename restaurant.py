import pprint
import time
import tkinter as tk
from tkinter.constants import BOTH
import xlsxwriter

import googlemaps
import pandas as pd
import requests
from requests import api

import APIkeys
import intro


class RestaurantWindow():


    def __init__(self):
        self.Gkey = APIkeys.googleKey()
        self.tk = tk.Tk()

        self.doc = APIkeys.docuKey()
        self.search = "https://api.documenu.com/v2/restaurants/search/geo?"
        self.menusearch = "https://api.documenu.com/v2/restaurant/"

    def restPage(self):

        self.tk.title('Baldoor Information Gathering')
        self.tk.geometry('440x500')

        google_opts = ['name', 'type', 'url', 'formatted_address', 'formatted_phone_number', 'price_level', 'rating', 'opening_hours/weekday_text']
        google_formtd = '\n'.join(google_opts)

        self.basic_info = tk.Label(self.tk, text = "Basic piece of information you wish to retrieve: ", font=("Roboto"))
        self.basic_info.pack()

        self.basic_frame = tk.LabelFrame(self.tk, text="Basic information options", font=("Roboto"))
        self.basic_frame.pack(ipadx=10)
        self.basic_options = tk.Label(self.basic_frame, text= google_formtd, font=("Roboto") )
        self.basic_options.pack()

        #able to be access entry information in any function i want with the global tag
        global basic_entry
        basic_entry = tk.Entry(self.tk, textvariable='goolemapsAPI')
        basic_entry.pack(ipadx=70, pady=20)

        #specific api information gathering
        self.api_info = tk.Label(self.tk, text="Specific piece of information wish to be retrieved", font=("Roboto"))
        self.api_info.pack()

        self.api_options_list = ['restaurant_name', 'cuisines', 'price_range', 'subsection','menu_item_name', 'menu_item_price']
        self.api_options_formatted = '\n'.join(self.api_options_list)

        self.api_frame = tk.LabelFrame(self.tk, text="Specific information options", font=("Roboto"))
        self.api_frame.pack()
        self.api_options = tk.Label(self.api_frame, text=self.api_options_formatted, font=("Roboto"))
        self.api_options.pack()

        global api_entry
        api_entry = tk.Entry(self.tk)
        api_entry.pack(ipadx=70, pady=20)

        self.google_button = tk.Button(self.tk, text="Display Information", command = lambda: self.PrintOut())
        self.google_button.pack(padx=10)

    #google information
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

        #gplaces.place dump
        
        info_dump = []
        
        #pagination in order to get all of the pages and display the options available
        if 'next_page_token' in search.keys():
            while 'next_page_token' in search.keys():
                time.sleep(2)
                params.update({'page_token': search['next_page_token']})
                search = gplaces.places_nearby(**params)
                for ids in search['results']:
                    places_result = gplaces.place(place_id = ids['place_id'], fields = entries)
                    # return places_result
                    info_dump.append(places_result['result'])
        
        for i in range(0, len(info_dump)):
            if i == (len(info_dump) - 1):
                df = pd.DataFrame(info_dump)
                return df

    #Documenu information
    def DocuData(self):

        addy = intro.IntroPage()

        api_entries = api_entry.get().split()

        # for when unlimitted calls, you can call the amount of pages that are available        
        # req = requests.get(self.search + "address=" + simple_location + "&key=" + self.doc)

        pageNum = 0

        links = []

        info_dump = []

        #pagination, up to page five (only do this because of free api use limitations)
        #remember to make a new acc real quick before presenting
        while pageNum != 5:

            pageNum+=1

            #https://api.documenu.com/v2/restaurants/search/geo?lat=41.304580&lon=-73.908930&distance=3&page=2 <- example of how get link should be
            req = requests.get(self.search + "lat=" + str(addy.latLocation()) + "&lon="+ str(addy.longLocation()) + "&distance=" + addy.simpleRadius() + "&key=" + self.doc)
            data = req.json()

            for i in data['data']:
                
                #get all of the ids in the search request and from there retrieve all of the ids and put all of the ids inside the menu search request
                places_id = i['restaurant_id']
                reqst = (self.menusearch + str(places_id) + "/menuitems" + "?key=" + self.doc)
                links.append(reqst)
                
        for i in range(0, len(links)):
            if i == (len(links) - 1):
                for link in links:
                    last_request = requests.get(link)
                        
                    last_data = last_request.json()
                    
                    for rest_info in last_data['data']:
                        while api_entries:
                            continue
                        info_dump.append(rest_info[api_entries])

        for data_presented in range ( 0, len(info_dump)):
            if data_presented == ( len(info_dump) - 1):
                df = pd.DataFrame(info_dump)
                return df

            

    def PrintOut(self):

        writer = pd.ExcelWriter('multiple_test.xlsx', engine = 'xlsxwriter')

        self.GoogleData().to_excel(writer, sheet_name="Google Data")
        self.DocuData().to_excel(writer, sheet_name= "Documenu Data")

        writer.save()
