import requests
import datetime
import os
import json

apikey = "b38bd132f82247f7a2a174126211005"
baseUrl = "http://api.weatherapi.com/v1/history.json?key={apikey}&q={city}&dt={date}"

def getResponseForUrl(url):
    resp = requests.get(url)
    
    if resp.status_code != 200:
        return {}

    return resp.json()

def main():
    print("Hello World!")
    cityList = ["Detroit", "Seattle"]
    weatherStartDate = datetime.datetime(2021, 5, 3)   
    weatherUrlDict = {}

    for city in cityList:
        date = weatherStartDate
        weatherUrlDict[city] = {}
        for i in range(8): 
            dateStr = date.strftime("%Y-%m-%d")
            print("Requesting weather data of {} on {}".format(city, dateStr))
            tempUrl = baseUrl.format(apikey=apikey, city=city, date=dateStr)
            weatherUrlDict[city][dateStr] = getResponseForUrl(tempUrl)
            if len(weatherUrlDict[city][dateStr]) > 0:
                print("Seccessfully retrieved Data")
            date += datetime.timedelta(days=1)
        
        # create a folder to save all the json output from requests
        if not os.path.exists(city):
            os.makedirs(city)



    with open('data.json', 'w') as json_file:
        json.dump(weatherUrlDict, json_file)

if __name__ == "__main__":
    main()