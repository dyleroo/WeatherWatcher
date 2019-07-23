from bottle import route, request, debug, run, template, static_file
import sqlite3, urllib2, json, datetime
from datetime import date
import time

places = {}


def url_builder(endpoint, lat, lon):
    user_api = 'b5020d6b80c9e17c5b7ae6147a04ace1'
    unit = 'metric'
    mode = 'json'
    return 'http://api.openweathermap.org/' + \
           'data/2.5/' + endpoint + \
           '?mode=' + mode + \
           '&units=' + unit + \
           '&APPID=' + user_api + \
           '&lat=' + str(lat) + \
           '&lon=' + str(lon)


def fetch_data(full_api_url):
    url = urllib2.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    return json.loads(output)


def time_converter(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d %b %I:%M %p')


def convertCoordinates(lat, lon):
    lat = float(lat)
    lon = float(lon)
    mapWidth, mapHeight = 540, 700
    leftLon, rightLon = -10.663, -5.428
    topLat, bottomLat = 55.384, 51.427
    lonRange = abs(leftLon - rightLon)
    latRange = abs(topLat - bottomLat)
    result = []
    result.append(int(round(abs(mapWidth * \
                                ((abs(leftLon) - abs(lon)) / lonRange)))))
    result.append(int(round(abs(mapHeight * \
                                ((abs(topLat) - abs(lat)) / latRange)))))
    return result


def getPlaces():
    places = {}
    connect = sqlite3.connect('forecast.db')
    cursor = connect.cursor()
    cursor.execute("select * from locations")
    rows = cursor.fetchall()
    for row in rows:
        places[row[1]] = [row[2], row[3], row[4]]
    return places


def getForecastData():
    connect = sqlite3.connect('forecast.db')
    cursor = connect.cursor()
    global places

    cursor.execute("DELETE FROM forecasts")
    for place in places:
        json_data = fetch_data(url_builder('forecast', places[place][0], places[place][1]))
        for forecast in json_data['list']:
            temperature = int(round(forecast['main']['temp'], 0))
            symbol = forecast['weather'][0]['icon']
            timestamp = forecast['dt']
            cursor.execute("INSERT INTO forecasts(location, temperature, symbol, timestamp) "
                           "VALUES(?,?,?,?)",
                           (place, temperature, symbol, timestamp))
    connect.commit()

    cursor.execute("SELECT DISTINCT timestamp FROM forecasts \
                    ORDER BY timestamp ASC")
    timestamps = cursor.fetchall()
    mapData = []
    timestampData = []
    for timestamp in timestamps:
        cursor.execute("SELECT * FROM forecasts \
                        WHERE timestamp = ?", (timestamp[0],))
        allLocationData = cursor.fetchall()
        singleMapData = []
        for locationData in allLocationData:
            place = locationData[1]
            symbol = locationData[3]
            imageCoords = convertCoordinates(places[place][0], \
                                             places[place][1])
            symbolURL = "http://openweathermap.org/img/w/" + \
                        symbol + ".png"
            singleMapData.append([imageCoords[0], \
                                  imageCoords[1], symbolURL, locationData[2], \
                                  place])
        mapData.append(singleMapData)
        timestampData.append(time_converter(timestamp[0]))
    cursor.close()
    connect.close()
    return mapData, timestampData


@route('/manage')
@route('/manage', method='post')
def manage():
    global places
    if request.forms.get('updateTowns'):
        for place, values in places.iteritems():
            if request.forms.get(place):
                values[2] = 1
            else:
                values[2] = 0
    return template('manage.tpl', places=places)


@route('/choosePlace', method='post')
def choosePlace():
    global timestampData
    if request.forms.get('updateTimes'):
        for stamp, values in timestampData.iteritems():
            if request.forms.get(stamp):
                values[2] = 1
            else:
                values[2] = 0
    return template('manage.tpl', timestampData=timestampData)


@route('/addPlace', method='post')
def addPlace():
    connect = sqlite3.connect('forecast.db')
    cursor = connect.cursor()
    global places

    newLocation = request.forms.get('location')
    latitude = request.forms.get('latitude')
    longitude = request.forms.get('longitude')
    places[newLocation] = [latitude, longitude, 1]

    cursor.execute("INSERT INTO locations(location, latitude, longitude,checkval)"
                   "VALUES(?,?,?,?)",
                   ((newLocation), (latitude), (longitude), 1))
    connect.commit()
    cursor.close()
    connect.close()
    mapData, timestampData = getForecastData()
    getForecastData()
    return template('manage.tpl', places=places, timestampData=timestampData)
"""
@route('/chooseToday', method='post')
def chooseToday():
    connect = sqlite3.connect('forecast.db')
    cursor = connect.cursor()
    global places

    cursor.execute("DELETE FROM forecasts")
    for place in places:
        json_data = fetch_data(url_builder('forecast', places[place][0], places[place][1]))
        for forecast in json_data['list']:
            temperature = int(round(forecast['main']['temp'], 0))
            symbol = forecast['weather'][0]['icon']
            timestamp = forecast['dt']
            cursor.execute("INSERT INTO forecasts(location, temperature, symbol, timestamp) "
                           "VALUES(?,?,?,?)",
                           (place, temperature, symbol, timestamp))
    connect.commit()

    cursor.execute("SELECT DISTINCT timestamp FROM forecasts \
                        ORDER BY timestamp ASC")
    timestamps = cursor.fetchall()
    mapData = []
    timestampData = []
    for timestamp in timestamps:
        ts = date.today()
        ts = time.mktime(datetime.timetuple())
        print ts
        cursor.execute("SELECT * FROM forecasts \
                                            WHERE timestamp >= ? and timestamp <= ?", (ts))
        allLocationData = cursor.fetchall()
        print allLocationData
        singleMapData = []
        for locationData in allLocationData:
            place = locationData[1]
            symbol = locationData[3]
            imageCoords = convertCoordinates(places[place][0], \
                                             places[place][1])
            symbolURL = "http://openweathermap.org/img/w/" + \
                        symbol + ".png"
            singleMapData.append([imageCoords[0], \
                                  imageCoords[1], symbolURL, locationData[2], \
                                  place])
        mapData.append(singleMapData)
        timestampData.append(time_converter(timestamp[0]))
    cursor.close()
    connect.close()
    return mapData, timestampData
"""



"""
@route('/chooseToday', method='post')
def chooseToday():
    connect = sqlite3.connect('forecast.db')
    cursor = connect.cursor()
    global places

    cursor.execute("DELETE FROM forecasts")
    for place in places:
        json_data = fetch_data(url_builder('forecast', places[place][0], places[place][1]))
        for forecast in json_data['list']:
            temperature = int(round(forecast['main']['temp'], 0))
            symbol = forecast['weather'][0]['icon']
            timestamp = forecast['dt']
            cursor.execute("INSERT INTO forecasts(location, temperature, symbol, timestamp) "
                           "VALUES(?,?,?,?)",
                           (place, temperature, symbol, timestamp))
    connect.commit()

    cursor.execute("SELECT DISTINCT timestamp FROM forecasts \
                        ORDER BY timestamp ASC")
    timestamps = cursor.fetchall()
    mapData = []
    timestampData = []
    
    if request.forms.get('Options'):
        for timestamp in timestamps:
            if request.forms.get('Today'):
                cursor.execute("SELECT * FROM forecasts \
                                WHERE timestamp = ?", (timestamp[0],))
                allLocationData = cursor.fetchall()
                singleMapData = []
                for locationData in allLocationData:
                    place = locationData[1]
                    symbol = locationData[3]
                    imageCoords = convertCoordinates(places[place][0], \
                                             places[place][1])
                    symbolURL = "http://openweathermap.org/img/w/" + \
                                symbol + ".png"
                    singleMapData.append([imageCoords[0], \
                                          imageCoords[1], symbolURL, locationData[2], \
                                          place])
            mapData.append(singleMapData)
            timestampData.append(time_converter(timestamp[0]))
    cursor.close()
    connect.close()
    return mapData, timestampData
    
    elseif request.forms.get('Options'):
        for timestamp in timestamps:
            if request.forms.get('Tomorrow'):
                <code similar to above but to select timestamps from 1 day forward from today>
    
    elseif request.forms.get('Options'):
        for timestamp in timestamps:
            if request.forms.get('MaxTemp'):
                <code similar to above but to select maximum temperature>
    
    else:
    <revert to default map>
"""

debug(True)

#code for selecting timestamps, using similar method to chooseLocation
@route('/manage')
@route('/manage', method='post')
def selectTimestamp():
    global places, timestampData
    if request.forms.get('updateTowns'):
        for place, values in places.iteritems():
            if request.forms.get(place):
                values[2] = 1
            else:
                values[2] = 0
    return template('manage.tpl', places=places, timestampData=timestampData)


def send_image(filename):
    return static_file(filename, root='./images/')

@route('/')
@route('/<id>')
def showMap(id=0):
    global mapData, timestampData, places
    chosenLocations = []
    for place, values in places.iteritems():
        if values[2] == 1:
            chosenLocations.append(place)
    id = int(id)
    prev = id - 1 if id > 0 else id
    next = id + 1 if id < len(mapData) - 1 else \
        len(mapData) - 1
    return template('showWeatherMap.tpl', \
                    chosenLocations=chosenLocations, \
                    mapData=mapData[id], \
                    timestampData=timestampData[id], \
                    prev=prev, next=next)


places = getPlaces()

mapData, timestampData = getForecastData()
debug(True)
run(reloader=True)