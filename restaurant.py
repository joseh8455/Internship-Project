#status code 524 on seperate api call

import asyncio
import os
import time
import tkinter as tk
from tkinter import messagebox

import googlemaps
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
        google_opts = ['name', 'type', 'url', 'formatted_address', 'formatted_phone_number', 'price_level', 'rating', 'opening_hours/weekday_text', 'permanently_closed']
        api_options_list = ['price_range','cuisines', 'subsection','menu_item_name', 'menu_item_price']
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

    # getting back a response 524 meaning that there wont be a response since there is an error going on with the the website and their servers
    def DocuDataLinks(self):
        
        #retrieve information for documenu api and put it in its proper place, respectively
        addy = intro.IntroPage()

        latitude = addy.latLocation()
        long = addy.longLocation()
        radius = addy.simpleRadius()

        pageNum = 0

        links = []

        ids = []

        #pagination
        while pageNum !=3:
            pageNum += 1
            links.append(self.search + "lat=" + str(latitude) + "&lon="+ str(long) + "&distance=" + radius + f"&page{pageNum}" + "&key=" + self.doc)

        for link in links:
            req = requests.get(link)
            data = req.json()
            
            for info in data['data']:
                ids.append(info['restaurant_id'])


        full_links = []
        filtered_links = []
        #adds brand new links to get more detailed information inside on the restaurant like menu items and prices
        for i in range(0, len(ids)):
            if i == (len(ids) - 1):
                for id in ids:
                    full_links.append(self.menusearch + f"{id}/menuitems?key={self.doc}")

        #gets rid of dups
        for links_available in full_links:
            if links_available not in filtered_links:
                filtered_links.append(links_available)
        
        return filtered_links

    #because im retrieving the same information from the links im able to create an asynchronous function to save time and make it a smaller size file
    async def test(self):
        #set up to run an async function inside tkinter since it doesnt allow to do so normally
        loop = asyncio.get_event_loop()
        urls = self.DocuDataLinks()
        user_entry = basic_entry.get().split()
        api_list = set.intersection(set(api_options_list ), set(user_entry))

        #empty string in order to be able to add dataframes into it
        df_holder = []

        #loop that goes through all of the urls and makes a get request to each of them
        for url in urls:
            future = loop.run_in_executor(None, requests.get, url)

            resp = await future

            data = resp.json()
            
            if data['totalResults'] == 0:
                continue
            else:
                df = pd.DataFrame(data['data'])
            
                df_setup = list(api_list)
                df_setup.append('restaurant_name')
        
                df_holder.append(df[df_setup])

                result = pd.concat(df_holder)

        for i in range(0, len(result)):
            if i == (len(result) - 1):
                df2 = pd.DataFrame(result)
                return df2

    #this function makes it possible to run an async function in tkinter, without this, the function above will return back an error
    def test2(self):
        loop = asyncio.get_event_loop()
        df = loop.run_until_complete( self.test() )
        return df

    #it prints out into seperate files but not together
    def PrintOut(self):

        writer = pd.ExcelWriter('test5.xlsx', engine = 'xlsxwriter')
        df1 = self.GoogleData()
        df2 = self.test2()

        df2.to_excel(writer, sheet_name="Docu Data")
        df1.to_excel(writer, sheet_name="Google Data")
        size = os.path.getsize(filename="test5.xlsx")
        if size > 0:
             try:
                test = messagebox.askyesno(title="Sucess!", message="Successfully created file. Do you wish to open it now? " + os.path.basename(writer))
                if test == True:
                    open(file= writer,  errors="ignore")
             except:
                    print("test")
        elif size == 0:
            return messagebox.showerror("Error", "Error message.")
        else:
            return print("how did you get here?")
        
        writer.save()
        
        # self.DocuDataParsed().to_excel(writer, sheet_name= "Documenu Data")

