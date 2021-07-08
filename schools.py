import pprint
import time
import tkinter as tk

import pandastable
import requests

import intro
import APIkeys

class SchoolWindow():

    def __init__(self):
        global digID, digKey, digURL

        digID = APIkeys.diggerID()

        digKey = APIkeys.diggerKey()

        digURL = 'https://api.schooldigger.com'
        
        self.tk = tk.Tk()

    def schoolWindow(self):
        self.tk.title("Baldoor Information Gathering")
        self.tk.geometry('440x500')

        #google information
        google_opts = ['name', 'type', 'url', 'formatted_address', 'formatted_phone_number', 'price_level', 'rating']
        google_formtd = '\n'.join(google_opts)

        self.basic_info = tk.Label(self.tk, text = "Basic piece of information you wish to retrieve: ", font=("Roboto"))
        self.basic_info.pack()

        self.basic_frame = tk.LabelFrame(self.tk, text="Basic information options", font=("Roboto"))
        self.basic_frame.pack()
        self.basic_options = tk.Label(self.basic_frame, text= google_formtd, font=("Roboto") )
        self.basic_options.pack()

        global basic_entry
        basic_entry = tk.Entry(self.tk, textvariable='goolemapsAPI')
        basic_entry.pack(ipadx=70, pady=20)


        #api related section
        self.api_options_list = ['teachersFulltime', 'numberOfStudents', 'teachersFulltime', 'year', 'lowGrade','highGrade', 'schoolLevel','isVirtualSchool',
                                 'numberofAfricanAmericanStudents', 'numberofHispanicStudents', 'numberofWhiteStudents']
        self.api_options_formatted = '\n'.join(self.api_options_list)

        self.api_frame = tk.LabelFrame(self.tk, text="Specific information options", font=("Roboto"))
        self.api_frame.pack()
        self.api_options = tk.Label(self.api_frame, text=self.api_options_formatted, font=("Roboto"))
        self.api_options.pack()
    