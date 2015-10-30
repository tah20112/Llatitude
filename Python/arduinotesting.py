import serial, time

ser = serial.Serial('/dev/ttyACM0', 9600)
# Wait for the Arduino to be ready
time.sleep(2)
ser.write('100')
while True:
	print ser.readline()