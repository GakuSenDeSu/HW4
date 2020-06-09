import paho.mqtt.client as paho
mqttc = paho.Client()
import matplotlib.pyplot as plt
import numpy as np
import serial
import time
 
# Settings for connection
host = "localhost"
topic= "mbed"
port = 1883
 
# Callbacks
def on_connect(mosq, obj, rc):
    print("connect rc: "+str(rc))
    mqttc.publish("mbed-sample","Python Script Test Message.")
 
def on_message(mosq, obj, msg):
    print( "Received on topic: " + msg.topic + " Message: "+str(msg.payload) + "\n")
 
def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")
 
# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
 
# Connect and subscribe
print("Connecting to " +host +"/" +topic)
mqttc.connect(host, port, 60)
mqttc.subscribe(topic, 0)

# Plot parameter
t = np.arange(0,10,0.1) # time vector; create Fs samples between -0.5 and 10 sec.
y1k = np.arange(0,10,0.1)
y2k = np.arange(0,10,0.1)
y3k = np.arange(0,10,0.1)
y4k = np.arange(0,10,0.1)

serdev = '/dev/ttyACM0'
s = serial.Serial(serdev,115200)

# Wait forever, receiving messages
rc = 0
while rc == 0:
    rc = mqttc.loop()
 
print(str(rc))
# Maybe not right
for x in range(0,int(100)):
    line=s.readline() # Read an echo string from PC terminated with '\n'
    y1=line.decode().strip().split(" ")[0]
    y1k[x] = float(y1)
for x in range(0,int(100)):
    line=s.readline() # Read an echo string from PC terminated with '\n'
    y2=line.decode()
    y2k[x] = float(y2)
for x in range(0,int(100)):
    line=s.readline() # Read an echo string from PC terminated with '\n'
    y3=line.decode()
    y3k[x] = float(y3)
for x in range(0,int(100)):
    line=s.readline() # Read an echo string from PC terminated with '\n'
    y4=line.decode()
    y4k[x] = float(y4)


fig, ax = plt.subplots(2, 1)
ax[0].plot(t,y1k,'r')
ax[0].plot(t,y2k,'b')
ax[0].plot(t,y3k,'g')
ax[0].legend(labels = ['x', 'y', 'z'], loc = 'best')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Acc Vector')
ax[1].stem(t,y4k,use_line_collection=True) # plotting the spectrum
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Tilt')
plt.show()
s.close()