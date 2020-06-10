import time
import serial
import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
mqttc = paho.Client()

# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883
 
# Plot parameter
t = np.arange(0,10,1) # time vector; create Fs samples between -0.5 and 10 sec.
y1k = np.arange(0,10,1)
y2k = np.arange(0,10,1)
y3k = np.arange(0,10,1)
y4k = np.arange(0,10,1)
Num = 0

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    global Num
    print(str(msg.payload) + "\n")
    line = msg.payload.decode()
    y1= line.split(" ")[0]
    y1k[Num] = float(y1)
    y2= line.split(" ")[1]
    y2k[Num] = float(y2)
    y3 = line.split(" ")[2]
    y3k[Num] = float(y3)
    y4 = line.split(" ")[3]
    y4k[Num] = float(y4)
    Num = Num + 1
    return y1k, y2k, y3k, y4k, Num
    

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
 
# Wait forever, receiving messages
rc = 0
while rc == 0:
    rc = mqttc.loop()
    print('Num = ' + str(Num))
    if Num == 10:
        break
print('Finish!')



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