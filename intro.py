import tkinter as tk
from tkinter.constants import END
from tkinter import messagebox

from geopy.geocoders import Nominatim
from requests.api import options
import restaurant
import schools


class IntroPage(tk.Tk):
    
    def __init__ (self):
         self.tk = tk.Tk()

    def FirstPage(self):
        
        #window settings for app
        self.tk.title('Baldoor Information Gathering')
        self.tk.geometry('440x500')

        #labels & entries
        location = tk.Label(self.tk, text="Enter Address to search surrounding area for: ", font= ("Roboto"))
        location.pack(padx=1, pady=4)

        global locatent        
        self.locent = tk.Entry(self.tk)
        self.locent.pack(ipadx=80, ipady=5)
        self.locent.focus()
        locatent = self.locent

        radius = tk.Label(self.tk, text="Mile Radius to search: (Max radius distance is 31 miles) ", font= ("Roboto"))
        radius.pack(padx=1, pady=4)

        global radent
        radent = tk.Entry(self.tk)
        radent.pack(ipadx=80, ipady=5)

        type = tk.Label(self.tk, text="Type of location you want to search for: ", font=("Roboto"))
        type.pack(padx=1, pady=4)

        global location_options
        location_options = ['school','restaurant']
        api_formatted_options = '\n'.join(location_options)
        basic_frame = tk.LabelFrame(self, text="Information retrieval options", font=("Roboto"))
        basic_frame.pack(ipadx=10)
        api_options = tk.Label(basic_frame, text= api_formatted_options, font=("Roboto"))
        api_options.pack()

        global type_entry
        type_entry = tk.Entry(self.tk)
        type_entry.pack(ipadx=80, ipady=5)

        #button & function calls
        resetButton = tk.Button(self.tk, text="Reset", command = self.resetFunction)
        resetButton.pack(pady = (15,10), padx=(10, 0))

        googleButton = tk.Button(self.tk, text= "Gather more information", command= self.gatherInfo())
        googleButton.pack(pady = (15,10), padx=(10, 0),)

    #command function calls for the buttons
    def resetFunction(self):
        locatent.delete(0, END)
        radent.delete(0, END)
        type_entry.delete(0, END)

     #if the fields are empty, send a error message that says to complete all the fields

    #retrieve the input gathered and add a pop up with specified questions based off of the input entry
    def gatherInfo(self):
         type_info = type_entry.get().lower()
         radius = radent.get()
         location = locatent.get

         school_api_type = ['primary_school', 'school', 'secondary_school']

         #window for restaurant specific information gathering 
         if type_info == "restaurant":
              rest_window = restaurant.RestaurantWindow()
              return rest_window.restPage()

         for school_type in school_api_type:
               if type_info == school_type:
                    school_window = schools.SchoolWindow()
                    return school_window.schoolWindow()

         # error handling right here
         all_together = [type_info, radius, location]

         for information in all_together:
               if information == '':
                    return messagebox.showerror(title="Error", message="Please fill out empty field")
        
         for location in location_options:
              if type_info != location:
                   return messagebox.showerror(title="Error", message="Please pick a valid location available to use")
          
    #seperate information grabber to run googlemaps library
    def locationRetrieval(self):
         locator = Nominatim(user_agent="interface")

         type_field = locator.geocode(locatent.get().lower())
         return [type_field.latitude, type_field.longitude]

    def latLocation(self):
         locator = Nominatim(user_agent="interface")

         type_field = locator.geocode(locatent.get().lower())
         return type_field.latitude

    def longLocation(self):
         locator = Nominatim(user_agent="interface")

         type_field = locator.geocode(locatent.get().lower())
         return type_field.longitude
   
    def typeRetrieval(self):
         type_types = type_entry.get().lower()
         return type_types

    def radiusRetrieval(self):
         meter_info = radent.get()
         
         meters = float(meter_info)
         miles = meters * 1609.34

         return miles

    def simpleRadius(self):
         radius = radent.get()
         return radius

    def zipCode(self):
         locator = Nominatim(user_agent="interface")

         type_field = locator.geocode(locatent.get().lower(), addressdetails=True)

         zip_code = type_field.raw['address']['postcode']
         return zip_code
    