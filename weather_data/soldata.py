import requests
import json
import datetime
import random

#the link to the data we're using
MSL_DATA_LINK = "https://mars.nasa.gov/rss/api/?feed=weather&category=msl&feedtype=json"
#the folder name we're in
BASE_FP = "weather_data/"
#the path of the default.json file (which stores the data as of 4/8/2023)
DEFAULT_JSON_FP = BASE_FP + "default.json"
#the length of the default.json file
DEFAULT_LENGTH = 3598
#How many sols in a year (technically 668.6)
SOLS_IN_YEAR = 668

#Returns the default json dictionary
def getDefaultJson():
    return json.load(open(DEFAULT_JSON_FP, "r"))

#Aggregates sol data and returns it as a dictionary. Sols numbers are modded by 668
#with 0 being the day curiosity touched down. Sunrise and sunset times are minute offsets
#from 00:00
def getAggregatedSolData():
    #this is the json data we'll read
    jsondata = {}

    try:
        response = requests.get(MSL_DATA_LINK)

        #If we were able to get the json data from the website then let's go with the most recently updated one
        if response.status_code == 200:
            jsondata = response.json()
            #if they removed data let's go with the default
            if (len(jsondata["soles"]) < DEFAULT_LENGTH):
                raise Exception
        else:
            raise Exception
    except Exception:
        #if we're offline or could'd get the data o with the data we have saved from 4/8/2023
        jsondata = getDefaultJson()

    #This is the list of days and data
    solList = jsondata["soles"]

    aggregateSolData = {}
    for sol in solList:
        #get the information from that sol
        moddedSol = int(sol["sol"]) % SOLS_IN_YEAR
        min_temp = int(sol["min_temp"]) if sol["min_temp"] != "--" else None
        max_temp = int(sol["max_temp"]) if sol["max_temp"] != "--" else None
        pressure = int(sol["pressure"]) if sol["pressure"] != "--" else None

        splitSunrise = sol["sunrise"].split(":")
        sunrise = 60 * int(splitSunrise[0]) + int(splitSunrise[1])

        splitSunset = sol["sunset"].split(":")
        sunset = 60 * int(splitSunset[0]) + int(splitSunset[1])

        uvIndex = sol["local_uv_irradiance_index"] if sol["local_uv_irradiance_index"] != "--" else None

        #if we haven't initialized this sol yet
        if (not moddedSol in aggregateSolData):
            #let's intialize it
            aggregateSolData[moddedSol] = {
                "min_min_temp" : min_temp,
                "max_min_temp" : min_temp,
                "min_max_temp" : max_temp,
                "max_max_temp" : max_temp,
                "min_pressure" : pressure,
                "max_pressure" : pressure,
                "min_sunrise" : sunrise,
                "max_sunrise" : sunrise,
                "min_sunset" : sunset,
                "max_sunset" : sunset,
                "uv_indices" : [],
            }
            #We'll add the uvIndex to the uvIndex list if it exists
            if uvIndex != None:
                aggregateSolData[moddedSol]["uv_indices"].append(uvIndex)
        else:
            #We already had some data here, we're gonna update it
            data = aggregateSolData[moddedSol]

            #if we have min_temp data to add
            if min_temp != None:
                if data["min_min_temp"] == None:
                    #this means we haven't initialized min min or max max, let's do that
                    data["min_min_temp"] = min_temp
                    data["max_min_temp"] = min_temp
                else:
                    #Let's see if anything could use an update
                    if min_temp < data["min_min_temp"]:
                        data["min_min_temp"] = min_temp
                    if min_temp > data["max_min_temp"]:
                        data["max_min_temp"] = min_temp     

            #if we have max_temp data to add
            if max_temp != None:
                if data["min_max_temp"] == None:
                    #this means we haven't initialized min min or max max, let's do that
                    data["min_max_temp"] = max_temp
                    data["max_max_temp"] = max_temp
                else:
                    #Let's see if anything could use an update
                    if max_temp < data["min_max_temp"]:
                        data["min_max_temp"] = max_temp
                    if max_temp > data["max_max_temp"]:
                        data["max_max_temp"] = max_temp  

            #if we have pressure data to add
            if pressure != None:
                if data["min_pressure"] == None:
                    #this means we haven't initialized min or max, let's do that
                    data["min_pressure"] = pressure
                    data["max_pressure"] = pressure
                else:
                    #Let's see if anything could use an update
                    if pressure < data["min_pressure"]:
                        data["min_pressure"] = pressure
                    if pressure > data["max_pressure"]:
                        data["max_pressure"] = pressure     

            #We should always have sunrise to add
            #Let's see if anything could use an update
            if sunrise < data["min_sunrise"]:
                data["min_sunrise"] = sunrise
            if sunrise > data["max_sunrise"]:
                data["max_sunrise"] = sunrise    

            #We should always have sunset to add
            #Let's see if anything could use an update
            if sunset < data["min_sunset"]:
                data["min_sunset"] = sunset
            if sunset > data["max_sunset"]:
                data["max_sunset"] = sunset   

            #We'll add the uvIndex to the uvIndex list if it exists
            if uvIndex != None:
                aggregateSolData[moddedSol]["uv_indices"].append(uvIndex)                                                                   

    return aggregateSolData

#Given a sol number and a dictionary of aggregateSolData, 
#returns a randomized sol for that sol number based on the data
def getRandomizedSolData(solnumber, aggregatedSolData):
    #get the aggregated data for the specified sole
    sol = aggregatedSolData[solnumber]

    return {
        "min_temp" : random.randint(sol["min_min_temp"], sol["max_min_temp"]),
        "max_temp" : random.randint(sol["min_max_temp"], sol["max_max_temp"]),
        "pressure" : random.randint(sol["min_pressure"], sol["max_pressure"]),
        "sunrise" : random.randint(sol["min_sunrise"], sol["max_sunrise"]),
        "sunset" : random.randint(sol["min_sunset"], sol["max_sunset"]),
        "uv_index" : random.choice(sol["uv_indices"])
    }
