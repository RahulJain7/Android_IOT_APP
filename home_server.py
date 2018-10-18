import paho.mqtt.client as paho
import time
import json 

send_topic = 'Rahul001_command'
ack_topic = 'Rahul001_ack'
connected = False

curtain_dict = {}

def on_message(client, userdata, message):
	msg = message.payload
	msg_arr = msg.strip('_')
	print msg_arr
	http_msg = ''
	location = msg_arr[0]
	device_type = msg_arr[1]
	device_name = msg[2]
	value = str(msg[3])
	curtain_direction = ''
	
	if location == 'portico':
		location_conversion = '1'
	
	elif location == 'bedroom':
		location_conversion = '2'
	
	elif device_type == 'light':
		http_msg = value+location_conversion
	
	elif device_type == 'fan':
		http_msg = 'FAN'+location_conversion+'_'+value
	
	elif device_type == 'curtain':
		total_time = float(msg_arr[4])
		present_value = int(value)
		
		if device_name in curtain_dict:
			previous_value = curtain_dict[device_name]
		else:
			previous_value = 0
		diff_value = present_value - previous_value
		curtain_dict[device_name] = present_value
		run_time = str(abs(diff_value) * total_time / 100.0)
		
		if diff_value > 0:
			curtain_direction = 'F'
		else:
			curtain_direction = 'R'
		http_msg = 'CU'+location+'_'+run_time+'_'+curtain_direction
	
	else:
		print('invalid message')
		http_msg = ''

	if http_msg != '':
		params = ('pin',http_msg)
		try:
			data = requests.get('http://192.168.1.106/', params=params)
			response = (data.text)
			response = response[0:1]
			if response == 'A':
				client.publish(ack_topic,msg)
				print ("Acknowledgement message: "+msg+" sent to the server    date:", dt.datetime.now())
			else:
				print("ESP needs reboot")
		except:
			E = "ESP1D".encode('utf-8')
			ack_msg = msg+' failed'
			client.publish(ack_topic,ack_msg)
			print ("Ack sent for failed ON1 to svr:", E, "    date:", dt.datetime.now())

def on_connect(client, userdata, flags, rc):
	print 'yes'
	if rc == 0:
		client.subscribe(send_topic)
	else:
		print("Connection failed")


server_ip = '127.0.0.1'

def mqtt_connect():
	global server_ip
	global connected
	client = paho.Client('home_server')
	client.on_connect= on_connect
	client.on_message = on_message
	client.connect(server_ip)
	client.loop_start()
	connected = True 

while True:
	if not connected:
		mqtt_connect() 
	time.sleep(3) 





