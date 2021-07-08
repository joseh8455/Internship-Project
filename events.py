import requests
import pprint
import pandastable
import intro
import time
import tkinter as tk

url  = "https://secure.meetup.com/oauth2/authorize"

req = requests.get(url)

data = req.json()

pprint.pprint(data)