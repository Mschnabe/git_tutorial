import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0',9600)

dataList = []
past_light = 0;
start = True
light_up = False
flag_p = 0
flag_f = 0
flag_h = 0
flag_s = 0
sleep(5)

print("starting")
ser.reset_input_buffer()
print("done")

while True:

   # ser.reset_input_buffer()

    while ser.in_waiting > 0:
        read_serial=ser.readline()
        print read_serial
        if "#" in read_serial:
            data = ser.readline()
            #print("data is " + data)
            dataList = data.split(',')
            #print("Datalist = ")
            #print(dataList)

        if "pump_end" in read_serial:
            flag_p = 0
            print("Pump Stopped")

        if "fans off" in read_serial:
            flag_f = 0
            print("Fans Stopped")

        if "heat_off" in read_serial:
            flag_h = 0
            print("Heater Stopped")

    sleep(1)

    if dataList != []:
    #read specifications
        temperature_upper = 80
        temperature_lower = 65
        humidity_upper = 95
        humidity_lower = 80
        light_cycle = 8
        #radish 60-65, 80-95, 6

        if light_cycle != past_light:
            light_up = False
            while light_up == False:
                print("SL")
                ser.write("light")
                sleep(1)
                ser.write(str(light_cycle))
                if "time" in ser.readline():
                    light_up = True
                    print("lighting set")
            past_light = light_cycle 

        sleep(1)
        soil_1 = 700 #dataList[0]
        soil_2 = 300 #dataList[1]
        temp_1 = 90#dataList[2]
        hum_1 = 80#dataList[3]
        temp_2 = 90#dataList[4]
        hum_2 = 85#dataList[5]
        temp_3 = 90#dataList[6]
        hum_3 = 85#dataList[7]
        outside_temp = 80#dataList[8]
        outside_hum = 60#dataList[9]

        inside_temp = (temp_1 + temp_2 + temp_3) / 3
        inside_hum = (hum_1 + hum_2 + hum_3) / 3

        print('Soil = ' + str(soil_1) + ' : ' + str(soil_2))
        print('Inside Temperature:Humidity = ' + str(inside_temp) + ':' + str(inside_hum))
        print('Outside Temperature:Humidity = ' + str(outside_temp) + ':' + str(outside_hum))
    
        #check if active
        if (soil_1 > 550 or soil_2 > 550):
            if flag_p == 0:
                ser.write('pump')
                print('Pump Activated')
                flag_p = 1
    

        if (inside_temp > temperature_upper) or (inside_hum > humidity_upper):
            if flag_f == 0:
                ser.write('fans')
                print("Fans On")
                flag_f = 1

        if (inside_temp < temperature_lower):
            if flag_h == 0:
                ser.write("heat")
                print("heater activated")
                flag_h = 1

        if inside_hum < humidity_lower:
            if flag_s == 0:
                ser.write("spray")
                print("spray initiating")
                flag_s = 1

    sleep(1)


