import paho.mqtt.client as paho
import time
import json 

send_topic = 'general_send/Rahul001'
ack_topic = 'general_ack/Rahul001'
connected = False

def on_message(client, userdata, message):
	msg = message
	print msg
	client.publish(send_topic,message[2])

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		client.subscribe(ack_topic)
	else:
		print("Connection failed")


server_ip = '127.0.0.1'

def mqtt_connect():
	global connected
	global client
	client = paho.Client('test_server')
	client.on_connect= on_connect
	client.on_message = on_message
	client.connect(server_ip)
	client.loop_start()
	connected = True


while True:
	print 'homeserver_mqtt_loop'
	if not connected:
		mqtt_connect() 
	if connected:
		client.publish(send_topic,'hiiii')
	time.sleep(3) 