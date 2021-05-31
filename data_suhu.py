import csv
import time
import sys
import RPi.GPIO as GPIO
import smbus

def sensortgs(): 
	bus = smbus.SMBus(1) 
	bus.write_i2c_block_data(0x44, 0x2C, [0x06]) # b669fbc0
	time.sleep(0.5)
	data = bus.read_i2c_block_data(0x44, 0x00, 6)
	temp = data[0] * 256 + data[1]
	x = -45 + (175 * temp / 65535.0)
	fTemp = -49 + (315 * temp / 65535.0)
	y = 100 * (data[3] * 256 + data[4]) / 65535.0

	cTemp  = float("{:.1f}".format(x))
	humidity = float("{:.1f}".format(y))
	sendData = ""
	temp_sht = 0
	humi_sht = 0
	sendData += str(cTemp) #10
	sendData += ";"
	sendData += str(humidity) #11
	sendData += ";"

	print(sendData)
	sys.stdout.flush()
	return(sendData)
    
def temperature():
	return(cTemp)

def humi():
	return(humidity)
	
	
def write_to_csv():
	with open("data_sensor_suhu.csv", mode="a") as sensor_readings:
		sensor_write = csv.writer(sensor_readings, delimiter=",", quotechar="”", quoting=csv.QUOTE_MINIMAL)
		write_to_log = sensor_write.writerow([sensortgs()])
		return(write_to_log)
    

while True:
	sensortgs() #write_to_csv()
	time.sleep(1)
