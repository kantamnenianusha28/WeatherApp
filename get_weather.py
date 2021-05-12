import requests
import datetime
import time
import os
import json
from google.cloud import storage

#apikey = "b38bd132f82247f7a2a174126211005"
#baseUrl = "http://api.weatherapi.com/v1/history.json?key={apikey}&q={city}&dt={date}"
#baseUrl = "http://api.openweathermap.org/data/2.5/forecast/daily?q={city}&cnt={cnt}&appid={apikey}"

newUrl ="https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,alerts,hourly&appid=e428df7e36446360d19a774bc1831b77&units=imperial"
fileName = "output.json"

cityList = {"Detroit": 
                {
                    "lat": "42.3319",
                    "lon": "-83.0458"
                }, 
            "Seattle": {
                    "lat": "47.6062",
                    "lon": "-122.3320"
                }
            }

def getResponseForUrl(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        return {}

    return resp.json()

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    if blob.exists():
        print("File {} already exists. Deleting it.".format(destination_blob_name))
        blob.delete()
    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def createBucket(bucketName):
    # Instantiates a client
    storage_client = storage.Client()
    # Creates the new bucket
    bucket = storage_client.bucket(bucketName)
    if bucket.exists():
        print("Bucket {} already exists".format(bucketName))
        return
    bucket = storage_client.create_bucket(bucketName)
    print("Bucket {} created.".format(bucket.name))

def writeLineToFile(line):
    fileMode = "w"
    if os.path.exists(fileName):
        fileMode = "a"
    
    with open(fileName, fileMode) as outputFile:
        outputFile.write(json.dumps(line))
        outputFile.write("\n")

def deleteExistingFile():
    if os.path.exists(fileName):
        os.remove(fileName)

def epochToTimeConverter(epoch):
    return datetime.datetime.fromtimestamp(epoch)


def convertHourlyData(data, baseJson):        
    for dailyRepo in data["hourly"]:
        tempData  = baseJson
        tempDate = epochToTimeConverter(dailyRepo["dt"])
        tempData["weather_date"] = tempDate.strftime("%Y-%m-%d")
        tempData["time"] = tempDate.strftime("%H:%m:%S")
        tempData["temp"] = dailyRepo["temp"]
        tempData["feels_like"] = dailyRepo["feels_like"]
        tempData["humidity"] = dailyRepo["humidity"]
        tempData["wind_speed"] = dailyRepo["wind_speed"]
        writeLineToFile(tempData)

def convertDailyData(data, baseJson):        
    for dailyRepo in data["daily"]:
        tempData  = baseJson
        tempDate = epochToTimeConverter(dailyRepo["dt"])
        tempData["weather_date"] = tempDate.strftime("%Y-%m-%d")
        tempData["time"] = tempDate.strftime("%H:%m:%S")
        tempData["temp"] = dailyRepo["temp"]["day"]
        tempData["temp_min"] = dailyRepo["temp"]["min"]
        tempData["temp_max"] = dailyRepo["temp"]["max"]
        tempData["humidity"] = dailyRepo["humidity"]
        tempData["wind_speed"] = dailyRepo["wind_speed"]
        writeLineToFile(tempData)

def main():
    mode = "daily"
    print("This script will get weather data for Seattle and Detroit")
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
        print("Missing GOOGLE_APPLICATION_CREDENTIALS variable. Please export and run this script")
        exit
    
    deleteExistingFile()
    # Loop over each city to get its daily forecast
    for city in cityList.keys():
        tempUrl = newUrl.format(lat=cityList[city]["lat"], lon=cityList[city]["lon"])

        print("Quering data for", city)
        data = getResponseForUrl(tempUrl)
        if len(data) <= 0:
            print("Failed to get data for", city)
            continue
        baseJson = {
            "location": city,
            "lat" : data["lat"],
            "long" : data["lon"],

        }

        if mode == "daily":
            convertDailyData(data, baseJson)
        

        #create GCS bucket
    bucket_name = "testweatherdata"
    createBucket(bucket_name)
    upload_blob(bucket_name, fileName, "testweatherdata.json")




if __name__ == "__main__":
    main()