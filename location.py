from geopy.geocoders import Nominatim

locator = Nominatim(user_agent="interface")

address = "30 Undercliff Terrace West Orange NJ 07052"
location = locator.geocode(address, addressdetails=True)

print (location.raw['lat'])