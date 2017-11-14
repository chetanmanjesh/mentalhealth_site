#api demo

from urllib.request import urlopen
#from urllib2 import urlopen
import json
import geocoder
from random import randint

"""
&location=42.3912%2C-72.5267%2C100&user_location=42.3912%2C-72.5267&skip=0&limit=10&user_key=349beaed7c0fbb0a3384f8e45209205a
"""
def betterdoctor_search(latlng, apiKey):
    url = "https://api.betterdoctor.com/2016-03-01/doctors?specialty_uid=psychologist&user_key=" + apiKey
    latlngUrl = str(latlng[0]) + "%2C" + str(latlng[1])
    locationUrl = "&location=" + latlngUrl + "%2C100&user_location=" + latlngUrl
    skip = str(randint(0, 38) * 5)
    finalUrl = url + locationUrl + "&skip=" + skip + "&limit=5"
    json_obj = urlopen(finalUrl)
    data = json.load(json_obj)
    dataJSON = data["data"]
    storage = []
    for docInfo in dataJSON:
        practice = docInfo["practices"]
        practiceName = practice[0]["name"]
        address = practice[0]["visit_address"]
        street = address["street"]
        city = address["city"]
        state = address["state"]
        zip = address["zip"]

        phones = practice[0]["phones"]
        pNumber = phones[0]["number"]

        profile = docInfo["profile"]
        fname = profile["first_name"]
        lname = profile["last_name"]
        bio = profile["bio"]
        storage.append({
            "fname": fname,
            "lname": lname,
            "bio": bio,
            "practice name": practiceName,
            "street": street,
            "city": city,
            "state": state,
            "zip": zip,
            "phone": pNumber
        })
    return storage

def betterdoctor_searchDriver():
    betterdoctor_api = "349beaed7c0fbb0a3384f8e45209205a"
    g = geocoder.ip("me")
    return betterdoctor_search(g.latlng, betterdoctor_api)
