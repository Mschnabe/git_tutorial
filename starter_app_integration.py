import requests
import json
import time
import libraries.RGB_LED
import time
from libraries.RGB_LED.RGB_LED.COLOR import Color
from libraries.DHT22 import DHT22
from libraries.MCP300X import MCP300X


#DHT
dht22_pin = 16

dht22 = DHT22(dht22_pin)

mcp3004 = MCP300X.MCP3004

mcp = MCP300X(mcp3004)
#RGB Setup


red_pin = 22
green_pin = 27
blue_pin = 17
is_common_anode=True
rgb = libraries.RGB_LED.RGB_LED(red_pin, green_pin, blue_pin,is_common_anode)
color = Color()

# the address we will make the request to
# TODO:  REPLACE WITH YOUR URL
url='https://intro-to-iot-ece.herokuapp.com/'
dataUrl='https://intro-to-iot-ece.herokuapp.com/api/data'
settingsUrl='https://intro-to-iot-ece.herokuapp.com/api/settings'
statsUrl='https://intro-to-iot-ece.herokuapp.com/api/statistics'

# make a get request to retrieve the current settings and stats, and extract the JSON from it
Settings = requests.get(settingsUrl)
Stats = requests.get(statsUrl)

settings = Settings.json()
oldStats = Stats.json()

print(settings)
print(oldStats)

# get the color to the lightColor field of the settings object
colorStr = settings['lightColor']
# colorStr contains the color of the light selected on the webapp
# TODO: set the color of the led based on the color from the webapp
print(colorStr)
#divide = colorStr.split('#')
#colorS = divide[1]
RGB = [colorStr[i:i+2] for i in range(0, len(colorStr), 2)] 
print(RGB)
r = int('0x'+RGB[0], 0)
g = int('0x'+RGB[1], 0)
b = int('0x'+RGB[2], 0)
print(r)
print(g)
print(b)
color.set_color(r,g,b)
rgb.set_color(color)


# initialize an empty dictionary
# TODO: fill up packet dictionary with the appropriate data
#			i.e. temperature, humidity, brightness data
humidity, temperature = dht22.get_temperature_and_humidity()
lighting = mcp.read(mcp.CH2)
print(lighting)
brightness = str(lighting)
print(humidity,temperature)
packet = {}
packet['temperature'] = round(temperature, 3)
packet['humidity'] = round(humidity, 3)
packet['brightness'] = brightness

# just a debug, comment it out when you know the script works
print(packet)

# submit the post request.
r = requests.post(dataUrl,json=packet)



past = {
        'avgTemperature' : oldStats['avgTemperature'],
        'avgHumidity' : oldStats['avgHumidity'],
        'avgBrightness' : oldStats['avgBrightness'],
        'timeInHot' : oldStats['timeInHot'],
        'timeInCold' : oldStats['timeInCold'],
        'timeInHumid' : oldStats['timeInHumid'],
        'timeInDry' : oldStats['timeInDry'],
        'timeOn' : oldStats['timeOn'],
        'timeTotal' : oldStats['timeTotal']
}

sets = {
        'LightIsOn': settings['lightIsOn'],
        'coldThreshold' : settings['coldThreshold'],
        'hotThreshold' : settings['hotThreshold'],
        'humidThreshold' : settings['humidThreshold'],
        'darkThreshold' : settings['darkThreshold'],
        'dryThreshold' : settings['dryThreshold'],
}
print(sets)

print(past)

        
# newStats dictionary, updated with the oldStats and the current reading
# TODO: update stats after reading new values from the sensors
timeTotal = past['timeTotal'] + 1
print(timeTotal)

print(type(packet['temperature']))
print(type(past['avgTemperature']))

avgTemperature = past['avgTemperature'] + ( (packet['temperature'] - past['avgTemperature'] ) / timeTotal)
print(avgTemperature)

avgHumidity = past['avgHumidity'] + ( (packet['humidity'] - past['avgHumidity'] ) / timeTotal)
print(avgHumidity)

#print(type(past['avgBrightness']))
#print(type(packet['brightness']))

avgBrightness = past['avgBrightness'] + ( (int(packet['brightness']) - past['avgBrightness'] ) / timeTotal)
print(avgBrightness)

timeInHot = past['timeInHot']
timeInCold = past['timeInCold']

if packet['temperature'] > sets['hotThreshold']:
    timeInHot += 1
elif packet['temperature'] < sets['coldThreshold']:
    timeInCold += 1
print (timeInHot)
print (timeInCold)

timeInHumid = past['timeInHumid']
timeInDry = past['timeInDry']

if packet['humidity'] > sets['humidThreshold']:
    timeInHumid += 1
elif packet['humidity'] < sets['dryThreshold']:
    timeInDry += 1

print(timeInHumid)
print(timeInDry)

timeOn = past['timeOn']
if (sets['LightIsOn']):
    timeOn += 1
print(timeOn)


newStats = {
  'avgTemperature': round(avgTemperature, 3) ,
  'avgHumidity': round(avgHumidity, 3),
  'avgBrightness': avgBrightness,
  'timeInHot': timeInHot,
  'timeInCold': timeInCold,
  'timeInHumid': timeInHumid,
  'timeInDry': timeInDry,
  'timeOn': timeOn,
  'timeTotal': timeTotal
}

print(json.dumps(newStats))
r = requests.put(statsUrl, newStats)
print(r)
