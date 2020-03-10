import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0',9600)

dataList = []


while True:
    while ser.in_waiting > 0:
        read_serial=ser.readline()
        print read_serial
        if "#" in read_serial:
            data = ser.readline()
            print("data is " + data)
            dataList = data.split(',')
            print("Datalist = ")
            print(dataList)
            
    sleep(1)
    ser.write('gottem')
    print('sent')
    sleep(10)
