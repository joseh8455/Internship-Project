import tkinter as tk

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

        global state_entry
        state_code = tk.Label(self.tk, text="What is the state code you wish to get information on?", font= ("Roboto"))
        state_code.pack()

        state_entry = tk.Entry(self.tk)
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

        self.google_button = tk.Button(self.tk, text="Display Information", command = lambda: self.PrintOut())
        self.google_button.pack(padx=10)

    
    def SchoolData(self):

        #this piece of code returns the set of keys that need to be accessed with more information and the ones that dont need to be
        more_indepth = ['numberOfStudents', 'teachersFulltime', 'percentFreeDiscLunch']
        basic_info = ['schoolName', 'phone', 'schoolLevel']
        user_entry = basic_entry.get().split()

        #get all the keys thanks to user entries
        intersection_set = set.intersection(set(more_indepth ), set(user_entry))
        user_entry = set.intersection(set(basic_info), set(user_entry))
        
        #retrieve information that will be used in the url
        state_info = state_entry.get()
        getter = intro.IntroPage()
        zip_code = getter.zipCode()

        #url example -> https://api.schooldigger.com/v1.2/schools?st=NY&zip=10474&appID=639d1add&appKey=1cb4b90b8078b87d24aa6b6821993a24
        url = requests.get(digURL + f'st={state_info}&zip={zip_code}&appID={digID}&appKey={digKey}')
        data = url.json()


        #this one is works perfectly fine as is
        df = pd.DataFrame(data['schoolList'])       
        basic_result = df[list(user_entry)]

        #test2
        num_school = -1
        dump = []

        while num_school != data['numberOfSchools']-1:
            num_school+=1

            df2 = pd.DataFrame(data['schoolList'][num_school]['schoolYearlyDetails'])
            #dump the dataframes created into the list
            dump.append(df2[list(intersection_set)])

            #because all the dataframes that were appened to the list were seperate, this combines all of them into one big dataframe without repeating index numbers
            result = pd.concat(dump, ignore_index=True)
        
        #retrieves the last dataframe in the list since for each one, when a new line is added, it prints out a new dataframe
        for i in range(0, len(result)):
            if i == (len(result) - 1):
                result

        #this combines the first and second dataframe created into one big dataframe that will be printed out into an excel sheet to use       
        return pd.concat([basic_result, result],axis=1, ignore_index=False)



    #print out of the dataframe created above
    def PrintOut(self):
   
        writer = pd.ExcelWriter('SchoolData.xlsx', engine='xlsxwriter')

        df = self.SchoolData() 
        df.to_excel(writer, sheet_name='Information Grabbed', index=False, na_rep='No Data Available')


        for column in df:
            column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets['Information Grabbed'].set_column(col_idx, col_idx, column_width)
        
        writer.save()

        #error handling
    