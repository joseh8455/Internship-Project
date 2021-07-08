import tkinter as tk
from tkinter.constants import END

from geopy.geocoders import Nominatim
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
        locatent = self.locent

        radius = tk.Label(self.tk, text="Mile Radius to search: (Max radius distance is 31 miles) ", font= ("Roboto"))
        radius.pack(padx=1, pady=4)

        global radent
        radent = tk.Entry(self.tk)
        radent.pack(ipadx=80, ipady=5)

        type = tk.Label(self.tk, text="Type of location you want to search for: ", font=("Roboto"))
        type.pack(padx=1, pady=4)

        global type_entry
        type_entry = tk.Entry(self.tk)
        type_entry.pack(ipadx=80, ipady=5)

        #button & function calls
        resetButton = tk.Button(self.tk, text="Reset", command = self.resetFunction)
        resetButton.pack(pady = (15,10), padx=(10, 0))

        googleButton = tk.Button(self.tk, text= "Gather more information", command= lambda: [self.gatherInfo(), self.emptyFields(), self.firstEmptyField(), self.secondEmptyField(), self.thirdEmptyField()])
        googleButton.pack(pady = (15,10), padx=(10, 0),)

    #command function calls for the buttons
    def resetFunction(self):
        locatent.delete(0, END)
        radent.delete(0, END)
        type_entry.delete(0, END)

     #if the fields are empty, send a error message that says to complete all the fields
    def emptyFields(self):
         location = locatent.get()
         radius = radent.get()
         types = type_entry.get()

         if location  == "":
          if radius == "":
           if types == "":
                empty_window = tk.Toplevel(self.tk)
                empty_window.title("Error")
                
                error_message = tk.Label(empty_window, text="Please fill out all of the fields before you can continue", font = ("Robot"))
                error_message.pack(pady=7, padx=7)
     
    def firstEmptyField(self):
          location = locatent.get()

          if location == "":
                empty_window = tk.Toplevel(self.tk)
                empty_window.title("Error")
                
                error_message = tk.Label(empty_window, text="Please fill out the first field before you can continue", font = ("Robot"))
                error_message.pack(pady=7, padx=7)

    def secondEmptyField(self):
          radius = radent.get()

          if radius == "":
                empty_window = tk.Toplevel(self.tk)
                empty_window.title("Error")
                
                error_message = tk.Label(empty_window, text="Please fill out the second before you can continue", font = ("Robot"))
                error_message.pack(pady=7, padx=7)
     
    def thirdEmptyField(self):
          types = type_entry.get()

          if types == "":
                empty_window = tk.Toplevel(self.tk)
                empty_window.title("Error")
                
                error_message = tk.Label(empty_window, text="Please fill out the third field before you can continue", font = ("Robot"))
                error_message.pack(pady=7, padx=7)

    #retrieve the input gathered and add a pop up with specified questions based off of the input entry
    def gatherInfo(self):
         type_info = type_entry.get().lower()

         school_api_type = ['primary_school', 'school', 'secondary_school']

         #window for restaurant specific information gathering 
         if type_info == "restaurant":
              rest_window = restaurant.RestaurantWindow()
              return rest_window.restPage()

         for school_type in school_api_type:
               if type_info == school_type:
                    school_window = schools.SchoolWindow()
                    return school_window.schoolWindow()


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
    