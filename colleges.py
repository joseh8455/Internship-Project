#still waiting to get access to the key


import requests
import pprint
import pandastable
import intro
import time
import tkinter as tk

url  = "http://www.communitybenefitinsight.org/api/get_hospitals.php?state=NY"

req = requests.get(url)

print (req)