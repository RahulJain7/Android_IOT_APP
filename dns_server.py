import paho.mqtt.client as paho
import time
import json 


dns_send_topic = 'general_send/#'
dns_ack_topic = 'general_ack/#'

connected = False


def on_message(client, userdata, message):
	msg = message.payload
	print message.topic
	# client.publish(ack_topic,msg)

def on_connect(client, userdata, flags, rc):
	print 'yes'
	if rc == 0:
		client.subscribe(dns_send_topic)
	else:
		print("Connection failed")

server_ip = '127.0.0.1'

def mqtt_connect():
	global server_ip
	global connected
	client = paho.Client('dns_server')
	client.on_connect= on_connect
	client.on_message = on_message
	client.connect(server_ip)
	client.loop_start()
	connected = True

while True:
	if not connected:
		mqtt_connect() 
	time.sleep(3) 