import json
import pprint
import time
import tkinter as tk

import googlemaps
from numpy import kaiser
import pandas as pd
import requests

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
     

        global google_opts, api_options_list
        google_opts = ['name', 'type', 'url', 'formatted_address', 'formatted_phone_number', 'price_level', 'rating', 'opening_hours/weekday_text']
        api_options_list = ['restaurant_name', 'price_range','cuisines', 'subsection','menu_item_name', 'menu_item_price']
        google_formtd = '\n'.join(google_opts)
        api_formatted_options = '\n'.join(api_options_list)

        basic_info = tk.Label(self.tk, text = "Basic piece of information you wish to retrieve: ", font=("Roboto"))
        basic_info.pack()

        basic_frame = tk.LabelFrame(self.tk, text="Basic information options", font=("Roboto"))
        basic_frame.pack(ipadx=10)
        basic_options = tk.Label(basic_frame, text= google_formtd, font=("Roboto"))
        basic_options.pack()
        api_options = tk.Label(basic_frame, text= api_formatted_options, font=("Roboto"))
        api_options.pack()

        #able to be access entry information in any function i want with the global tag
        global basic_entry
        basic_entry = tk.Entry(self.tk, textvariable='goolemapsAPI')
        basic_entry.pack(ipadx=70, pady=20)
        basic_entry.focus()

        self.google_button = tk.Button(self.tk, text="Display Information", command = lambda: self.DocuDataParsed())
        self.google_button.pack(padx=10)

    def GoogleData(self):
        
        #retrieve the entries from the first page (intro.py Entry fields)
        info = intro.IntroPage()

        location = info.locationRetrieval()
        radius = info.radiusRetrieval()
        type = info.typeRetrieval()

        #paramaters for places_nearby search 
        params = {
            'location': location,
            'radius': radius,
            'type': type
        }
        gplaces = googlemaps.Client(key = self.Gkey)
        search = gplaces.places_nearby(**params)

        #filters the inputs to only the ones that are needed for the google api with this
        entries = basic_entry.get().split()
        intersection_set = set.intersection(set(entries), set(google_opts))
        intersection_list = list(intersection_set)

        #gplaces.place dump
        info_dump = []
        
        #pagination in order to get all of the pages and display the options available
        if 'next_page_token' in search.keys():
            while 'next_page_token' in search.keys():
                time.sleep(2)
                params.update({'page_token': search['next_page_token']})
                search = gplaces.places_nearby(**params)
                for ids in search['results']:
                    places_result = gplaces.place(place_id = ids['place_id'], fields = intersection_list)
                    # return places_result
                    info_dump.append(places_result['result'])
        
        #returns the last dataframe here
        for i in range(0, len(info_dump)):
            if i == (len(info_dump) - 1):
                df = pd.DataFrame(info_dump)
                return df

    def DocuDataLinks(self):
        
        #retrieve information for documenu api and put it in its proper place, respectively
        addy = intro.IntroPage()

        latitude = addy.latLocation()
        long = addy.longLocation()
        radius = addy.simpleRadius()

        #pageNum is used for pagination
        pageNum = 0

        #link dump
        links = []

        menu_links = []

        #this is pagination, going from page 1 to page 5
        while pageNum != 2:

            pageNum+=1

            #https://api.documenu.com/v2/restaurants/search/geo?lat=41.304580&lon=-73.908930&distance=3&page=2 <- example of how get link should be
            links.append(self.search + "lat=" + str(latitude) + "&lon="+ str(long) + "&distance=" + radius + f"&page={pageNum}"+ "&key=" + self.doc)

        for i in range(0, len(links)):
            if i == (len(links) - 1):
                links
        
        for link in links:
            req = requests.get(link)
            data = req.json()

            #returns links that needs to be able to retrieve information from it and display the proper info
            for j in data['data']:
                place_ids = j['restaurant_id']
                menu_links.append(self.menusearch + str(place_ids) + "/menuitems/?key=" + self.doc)
                menu_links
        
        #returns the last element in list with all of the links with apis
        for i in range(0, len(menu_links)):
            if i == (len(menu_links) - 1):
                return menu_links
    
    def DocuDataParsed(self):

        user_entry = basic_entry.get().split()

        intersection_set = list(set.intersection(set(api_options_list ), set(user_entry)))

        interesting = self.DocuDataLinks()

        print (interesting)

    def PrintOut(self):

        # writer = pd.ExcelWriter('multiple_test4.xlsx', engine = 'xlsxwriter')

        # self.GoogleData().to_excel(writer, sheet_name="Google Data")
        # self.DocuDataParsed().to_excel(writer, sheet_name= "Documenu Data")

        pprint.pprint(self.DocuDataParsed())
        # writer.save()
