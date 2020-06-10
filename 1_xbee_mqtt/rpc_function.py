import paho.mqtt.client as paho
import time
import serial
import matplotlib.pyplot as plt
import numpy as np
mqttc = paho.Client()

# time parameter
t = np.arange(0,10,1) # time vector; create Fs samples between 0 and 10 sec.
xk = np.arange(0,10,1)
y2k = np.arange(0,10,1) # Num
y2kk = np.arange(0,10,1) # Num

# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

s.write("\n\r".encode())
print('Start')
time.sleep(3)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATRE\r\n".encode())
char = s.read(3)
print("Reset")
print(char.decode())

s.write("ATMY 0x140\r\n".encode())
char = s.read(3)
print("Set MY 0x140.")
print(char.decode())

s.write("ATDL 0x240\r\n".encode())
char = s.read(3)
print("Set DL 0x240.")
print(char.decode())

s.write("ATID 0x5\r\n".encode())
char = s.read(3)
print("Set PAN ID 0x5.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

print("start sending RPC")

time.sleep(3)
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)
s.write("/getAcc/run\r".encode())

print('')
time.sleep(3)

serdev1 = '/dev/ttyACM0'
s1 = serial.Serial(serdev1, 9600)
    
print('')
time.sleep(3)

# Record acc from PC
y1k=[] #list

line=s1.readline() # Read an echo string from K66F terminated with '\n' (to Remote)
print('')
line=s1.readline() # Read an echo string from K66F terminated with '\n' (RPC)
print(line)
time.sleep(1)

y1=line.decode().strip().split(",")[0]
y1k.append(y1)
    
y2=line.decode().strip().split(",")[1]
y2k[0] = float(y2)
print(y2k[0])
y2kk[0] = 1

mqttc.publish(topic, y1)

for x in range(1,int(10)):

    line=s1.readline() # Read an echo string from K66F terminated with '\n' (to Remote)
    print('')
    line=s1.readline() # Read an echo string from K66F terminated with '\n' (RPC)
    print(line)
    time.sleep(1)

    y1=line.decode().strip().split(",")[0]
    y1k.append(y1)
    
    y2=line.decode().strip().split(",")[1]
    y2k[x] = float(y2)
    print(y2k[x])
    y2kk[x] = y2k[x] - y2k[x-1]
    print(y2kk[x])

    mqttc.publish(topic, y1)

print('ALL y1 = ')
print(y1k)
print('ALL y2kk = ')
print(y2kk)
print('ALL x = ')
print(xk)

# Num plot
plt.figure()
plt.plot(xk, y2kk)
plt.xlabel("timestamp")
plt.ylabel("number")
plt.title("# collected data plot")
plt.show()
s.close()