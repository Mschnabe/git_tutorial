import requests
import json
import time
import RGB_LED
import time
from RGB_LED.COLOR import Color
#RGB Setup
red_pin = 22
green_pin = 27
blue_pin = 17
is_common_anode=True
rgb = RGB_LED.RGB_LED(red_pin, green_pin, blue_pin,is_common_anode)
color = Color()

# the address we will make the request to
# TODO:  REPLACE WITH YOUR URL
url='https://intro-to-iot-ece.herokuapp.com/'
dataUrl='https://intro-to-iot-ece.herokuapp.com/api/data'
settingsUrl='https://intro-to-iot-ece.herokuapp.com/api/settings'
statsUrl='https://intro-to-iot-ece.herokuapp.com/api/statistics'

# make a get request to retrieve the current settings and stats, and extract the JSON from it
Settings = requests.get(settingUrl)
Stats = requests.get(statsUrl)

settings = Settings.json()
oldStats = Stats.json()

print(settings)
print(oldStats)

# get the color to the lightColor field of the settings object
colorStr = settings['lightColor']
# colorStr contains the color of the light selected on the webapp
# TODO: set the color of the led based on the color from the webapp
colorStr = "#FF55BB"
print(colorStr)
divide = colorStr.split('#')
colorS = divide[1]
RGB = [colorS[i:i+2] for i in range(0, len(colorS), 2)] 
print(RGB)
r = int('0x'+RGB[0], 0)
g = int('0x'+RGB[1], 0)
b = int('0x'+RGB[2], 0)

color.set_color(r,g,b)
rgb.set_color(color)

exit()

# initialize an empty dictionary
# TODO: fill up packet dictionary with the appropriate data
#			i.e. temperature, humidity, brightness data
packet = {}

# just a debug, comment it out when you know the script works
print(packet)

# submit the post request.
r = requests.post(dataUrl,json=packet)


# newStats dictionary, updated with the oldStats and the current reading
# TODO: update stats after reading new values from the sensors
newStats = {
  'avgTemperature': ,
  'avgHumidity': ,
  'avgBrightness': ,
  'timeInHot': ,
  'timeInCold': ,
  'timeInHumid': ,
  'timeInDry': ,
  'timeOn': ,
  'timeTotal': 
}

print(json.dumps(newStats))
r = requests.put(statsUrl, newStats)
print(r)
