from kivy.lib import osc
from kivy.app import App
import paho.mqtt.client as paho
import time
import json 


class testapp(App):
	def __init__(self,**kwargs):
		super(testapp, self).__init__(**kwargs)
		self.client_id = '001'
		self.mqtt_topics = []
		self.server_ip = ''
		self.broker_1 = ''
		self.broker_2 = ''
		self.send_topic = ''
		self.ack_topic = ''
		self.connected = False
		osc.init()
		self.oscid = osc.listen(ipAddr='127.0.0.1', port=3000)	
		osc.bind(self.oscid, self.get_serverIP, '/serverIP')
		osc.bind(self.oscid, self.get_clientID, '/clientID')
		osc.bind(self.oscid, self.send_command, '/command')

 	
 	def mqtt_connect(self):
		self.client = paho.Client(self.client_id)
 		self.client.on_connect= self.on_connect
 		self.client.on_message = self.on_message
 		self.client.connect(self.server_ip)
 		self.client.loop_start()
 		self.connected = True  		
 	
 	def get_serverIP(self, message, *args):
 		self.server_ip = message[2]

	def get_clientID(self, message, *args):
		self.client_id = message[2]
		self.send_topic = self.client_id + '_' + 'command'
		self.ack_topic = self.client_id + '_' + 'ack'

	def send_command(self, message, *args):
		print self.send_topic
		self.client.publish(self.send_topic,message[2])

	def on_connect(self,client, userdata, flags, rc):
		if rc == 0:
				client.subscribe(self.ack_topic)
		else:
			print("Connection failed")

	def on_message(self, client, userdata, message):
		msg = message.payload
		osc.sendMsg('/ack',[msg],port=3002)


	def start_service(self):
		while True:
			while self.client_id == '' or self.server_ip == '':
				osc.readQueue(self.oscid)
			if not self.connected:
				self.mqtt_connect() 
			osc.readQueue(self.oscid)
			


class myapp(App):
	def build(self):
		n = testapp()
		n.start_service()

if __name__ == '__main__':
	myapp().run()