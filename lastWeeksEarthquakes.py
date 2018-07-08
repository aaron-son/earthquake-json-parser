"""
USGS (US Geological Survey) publishes various earthquake data as JSON feed. Here's a feed spanning all domestic earthquages from the past week:
https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson
Using this JSON feed:
1) identify every earthquake in California from past week,
2) list them chronologically (ascending),
3. and finally output in a format resembling the following e.g.:
2017-07-13T20:43:37+00:00 | 3km NW of Greenville, California | Magnitude: 1
2017-07-13T22:09:53+00:00 | 41km SW of Ferndale, California | Magnitude: 2.76
2017-07-13T22:31:04+00:00 | 11km E of Mammoth Lakes, California | Magnitude: 1.31
2017-07-13T22:32:48+00:00 | 15km SE of Mammoth Lakes, California | Magnitude: 0.92
2017-07-13T22:37:52+00:00 | 12km E of Mammoth Lakes, California | Magnitude: 0.95
2017-07-13T22:45:28+00:00 | 37km SE of Bridgeport, California | Magnitude: 1.7
2017-07-13T22:49:58+00:00 | 8km ENE of Mammoth Lakes, California | Magnitude: 0.92
2017-07-13T22:54:30+00:00 | 3km SE of Atascadero, California | Magnitude: 2.04
"""
import requests
import re
import time

# retrieve json from url
earthquakes = requests.get(url='https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson')
earthquakesJson = earthquakes.json()

# count the number features in parent class
numberOfQuakesInCalifornia = len(earthquakesJson['features'])
# print(numberOfQuakes)
listOfQuakesInCalifornia = []

for i in range(0, numberOfQuakesInCalifornia):
    # access features[i] of property title
    # format: M 0.6 - 5km WNW of Lake Henshaw, CA
    details = earthquakesJson['features'][i]['properties']['title']
    # split state from details
    earthquakeData = details.split(",")
    state = earthquakeData[-1]
    if ('CA' in state) or ('California' in state):
        epochTime = earthquakesJson['features'][i]['properties']['updated']
        listOfQuakesInCalifornia.append(str(epochTime) + " - " + details)

listOfQuakesInCalifornia.sort()

for quakes in listOfQuakesInCalifornia:
    splitData = quakes.split("-")
    epochTime = splitData[0]
    # divide epoch time from milliseconds to seconds
    quakeDate = time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.localtime(float(epochTime)/1000))
    title = splitData[2]
    magnitude = splitData[1]
    magnitude = re.sub('[M]', 'Magnitude:', magnitude)
    print(quakeDate + " | " + title + " | " + magnitude)
