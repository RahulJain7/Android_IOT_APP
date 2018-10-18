from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.base        import runTouchApp
from kivy.config      import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang        import Builder
from kivy.utils       import platform
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from functools import partial
from kivy.uix.screenmanager import SlideTransition
from kivy.properties import StringProperty
from kivy.lib import osc


RecvPort = 3000
SendPort = 3002
# osc.init()
# oscid = osc.listen(ipAddr='127.0.0.1', port=RecvPort)




app_config = {}
client_id = ''
widget_dict = {}

class SettingsScreenManager(ScreenManager):
	def __init__(self,**kwargs):
		super(SettingsScreenManager, self).__init__(**kwargs)
		self.config_dict = {}

class MainScreen(BoxLayout):
	def __init__(self,**kwargs):
		super(MainScreen, self).__init__(**kwargs)
		self.mainmenu = MainMenu()
		self.mainmenu.bind(on_select=self.screen_selection)

	def screen_selection(self,instance,x):
		self.ids.ssm.transition = SlideTransition(direction='left')
		self.ids.ssm.current = x

class Config(Screen):
	def __init__(self,**kwargs):
		super(Config, self).__init__(**kwargs)	

	def save(self):
		global client_id
		global server_ip
		client_id = str(self.ids.client_id_text.text)
		server_ip = str(self.ids.server_ip_text.text)
		print server_ip
		print client_id
		osc.sendMsg('/clientID',[client_id],port=3000)
		osc.sendMsg('/serverIP',[server_ip],port=3000)

class LoadingScreen(Screen):
	def __init__(self,**kwargs):
		super(LoadingScreen, self).__init__(**kwargs)	
		Clock.schedule_once(self.goto_home,1)

	def goto_home(self,dt):
		print 'yes reached'
		self.parent.transition = SlideTransition(direction='left')
		print 'yes'
		self.parent.current = 'Home'

class Home(Screen):

	def __init__(self,**kwargs):
		super(Home, self).__init__(**kwargs)
		
	def load_screen(self):
		self.ids.location_list.clear_widgets()
		global app_config
		if app_config == {}:
			goto_config = Location(height=50,text='Location/Device Configuration')
			goto_config.bind(on_press=self.config)
			self.ids.location_list.add_widget(goto_config)
		else:
			for key in app_config:
				new_location = Location(height=50,text='[b]'+key+'[/b]')
				location_callback = partial(self.location,key)
				new_location.bind(on_press=location_callback)
				self.ids.location_list.add_widget(new_location)
					
	def location(self,key,instance):
		self.parent.present_location = key
		self.parent.transition = SlideTransition(direction='left')	
		self.parent.current = 'DeviceScreen'

	def config(self,instance):
		self.parent.transition = SlideTransition(direction='left')	
		self.parent.current = 'Settings'

	def slider_change(self,value):
		if value >= 0:
			self.ids.slider.value=value

	def scroll_change(self, value):
		self.ids.scrv.scroll_y = value


class DeviceScreen(Screen):
	def __init__(self,**kwargs):
		super(DeviceScreen, self).__init__(**kwargs)

	def load_screen(self):
		global app_config
		global widget_dict
		print app_config
		print widget_dict
		print self.parent.present_location
		self.location_name = self.parent.present_location
		print self.location_name
		self.ids.device_list.clear_widgets()
		for name, wgt in widget_dict[self.location_name].iteritems():
				self.ids.device_list.add_widget(wgt)
			 

	def slider_change(self,value):
		if value >= 0:
			self.ids.slider.value=value

	def scroll_change(self, value):
		self.ids.scrv.scroll_y = value

class Sld(Slider):
	pass

class TypeMenu(DropDown):
	def __init__(self,**kwargs):
		super(TypeMenu, self).__init__(**kwargs)

class MainMenu(DropDown):
	def __init__(self,**kwargs):
		super(MainMenu, self).__init__(**kwargs)

class AddLocationPopup(Popup):
	def __init__(self,**kwargs):
		super(AddLocationPopup, self).__init__(**kwargs)

	def save(self):
		self.dismiss()
		global locations
		locations[self.ids.location_text.text] = []
		print locations



class Setings(Screen):
	def __init__(self,**kwargs):
		super(Setings, self).__init__(**kwargs)

	def load_screen(self):
		self.ids.location_list.clear_widgets()
		for key in self.parent.config_dict:
			location_widget = LocationWidget(height=100,location_name=key)
			editdevices_callback = partial(self.edit_devices,key)
			removelocation_callback = partial(self.remove_location,key)
			location_widget.ids.EditDevices.bind(on_press=editdevices_callback)
			location_widget.ids.RemoveLocation.bind(on_press=removelocation_callback)
			self.ids.location_list.add_widget(location_widget) 		
		
	def add_location(self):
		#global locations_added
		self.parent.config_dict[self.ids.location_text.text] = []
		print self.parent.config_dict
		self.load_screen()
		# for key in self.parent.config_dict:
		# 	location_widget = LocationWidget(height=100,location_name=key)
		# 	editdevices_callback = partial(self.edit_devices,key)
		# 	location_widget.ids.EditDevices.bind(on_press=editdevices_callback)
		# 	self.ids.location_list.add_widget(location_widget) 
	

	def remove_location(self,key,instance):
		del self.parent.config_dict[key]
		print self.parent.config_dict
		self.load_screen()
	
	def edit_devices(self,key,instance):
		print key
		self.parent.present_config_location = key
		self.parent.transition = SlideTransition(direction='left')
		self.parent.current = 'LocationSettings'

	def slider_change(self,value):
		print value
		if value >= 0:
			self.ids.slider.value=value

	def scroll_change(self, value):
		print value
		self.ids.scrv.scroll_y = value
	
	def save(self):
		global app_config
		global widget_dict     
		app_config = self.parent.config_dict
		widget_dict = {}
		for location in app_config:
			widget_dict[location] = {}
			for device in app_config[location]:
				print 'device = ' 
				print device
				if device['type'] == 'Light':
					light_widget = LightWidget(height=100,device_name=device['name'],device_type=device['type'],device_location=location)
					widget_dict[location][device['name']] = light_widget
				elif device['type'] == 'Fan':
					fan_widget = FanWidget(height=100,device_name=device['name'],device_type=device['type'],device_location=location)
					widget_dict[location][device['name']] = fan_widget
				elif device['type'] == 'Curten':
					curten_widget = CurtenWidget(height=100,device_name=device['name'],device_type=device['type'],device_location=location,device_ttime=device['time'])
					widget_dict[location][device['name']] = curten_widget
		self.parent.transition = SlideTransition(direction='left')
		self.parent.current = 'Home'
		print widget_dict



class LocationSettings(Screen):
	def __init__(self,**kwargs):
		super(LocationSettings, self).__init__(**kwargs)
		self.typemenu = TypeMenu()
		self.typemenu.bind(on_select=self.selection)



	def load_screen(self):
		self.location_name = self.parent.present_config_location
		self.ids.device_list.clear_widgets()
		for device in self.parent.config_dict[self.parent.present_config_location]:
			print device['name']
			print device['type']
			if device['type'] == 'Curten':
				device_widget = DeviceCurtainWidget(height=80,device_name=device['name'],device_type=device['type'],device_ttime=device['time']) 
				device_index = self.parent.config_dict[self.parent.present_config_location].index(device)
				settime_callback = partial(self.set_time,device_index,device_widget)
				device_widget.ids.SetTime.bind(on_press=settime_callback)
			else:
				device_widget = DeviceWidget(height=80,device_name=device['name'],device_type=device['type'])
			device_index = self.parent.config_dict[self.parent.present_config_location].index(device)
			removedevice_callback = partial(self.remove_device,device_index)
			device_widget.ids.RemoveDevice.bind(on_press=removedevice_callback)
			
			print device_widget.device_name
			self.ids.device_list.add_widget(device_widget)

	def set_time(self,index,device_widgt,instance):
		print instance
		print index
		total_time = str(device_widgt.ids.curtain_time.text)
		self.parent.config_dict[self.parent.present_config_location][index]['time'] = total_time

	def selection(self,instance,x):
		self.type_selected = x

	def add_device(self):
		#global locations_added
		device_dict = {'name':self.ids.device_text.text,'type':self.type_selected,'time':''}
		self.parent.config_dict[self.parent.present_config_location].append(device_dict)
		self.load_screen()

	def remove_device(self,index,instance):
		del self.parent.config_dict[self.parent.present_config_location][index]
		self.load_screen()

 	def previous(self):
 		self.parent.transition = SlideTransition(direction='left')
		self.parent.current = 'Settings'		

	def slider_change(self,value):
		if value >= 0:
			self.ids.slider.value=value

	def scroll_change(self, value):
		self.ids.scrv.scroll_y = value


class Location(Button):
	def yes(self):
		print 'yes'

class LocationWidget(AnchorLayout):
	location_name = StringProperty('')
	# def __init__(self,**kwargs):
	# 	super(LocationWidget, self).__init__(**kwargs)	

class DeviceWidget(AnchorLayout):
	device_name = StringProperty('')
	device_type = StringProperty('')
	# def __init__(self,**kwargs):
	# 	super(DeviceWidget, self).__init__(**kwargs)
	# 	self.device_name = ''
	# 	self.device_type = ''
class DeviceCurtainWidget(AnchorLayout):
	device_name = StringProperty('')
	device_type = StringProperty('')
	device_time = StringProperty('')

class LightWidget(AnchorLayout):
	device_name = StringProperty('')
	device_type = StringProperty('')
	device_location = StringProperty('')
	device_value = StringProperty('')
	status = StringProperty('OFF')

	def pressed(self):
		
		if self.status == 'ON':
			self.device_value = 'OFF'
		else:
			self.device_value = 'ON'
		final_msg = str(self.device_location + '_' + self.device_type + '_' + self.device_name + '_' + self.device_value)
		print final_msg
		osc.sendMsg('/command',[final_msg],port=3000)

class FanWidget(AnchorLayout):
	device_name = StringProperty('')
	device_location = StringProperty('')
	device_type = StringProperty('')
	device_value = StringProperty('')
	status = StringProperty('0')
	slid_value = 0

	def on_slid(self):
		self.device_value = str(self.ids.fan_slider.value)
		final_msg = str(self.device_location + '_' + self.device_type + '_' + self.device_name + '_' + self.device_value)
		print final_msg
		osc.sendMsg('/command',[final_msg],port=3000)

class CurtenWidget(AnchorLayout):
	device_name = StringProperty('')
	device_location = StringProperty('')
	device_type = StringProperty('')
	device_value = StringProperty('')
	device_ttime = StringProperty('')
	status = StringProperty('OFF')
	slid_value = 0

	def on_slid(self):
		self.device_value = str(self.ids.curtain_slider.value)
		print self.ids.curtain_slider.value
		final_msg = str(self.device_location + '_' + self.device_type + '_' + self.device_name + '_' + self.device_value + '_' + self.device_ttime)
		print final_msg
		osc.sendMsg('/command',[final_msg],port=3000)

	def pressed_onof(self):
		if self.status == 'ON':
			self.status = 'OFF'
		else:
			self.status = 'ON'

	def pressed_pause(self):
		print 'yes'



design = Builder.load_file("design.kv")

class MyApp(App):
	def on_acknowledge(self, message, *args):
		global widget_dict
		print 'received'
		msg = message[2]
		msg_arr = msg.split('_')
		location_name = msg_arr[0]
		device_name = msg_arr[1]
		Status = msg_arr[2]
		widget_dict[location_name][device_name].status = Status


	def build(self):
		osc.init()
		oscid = osc.listen(ipAddr='127.0.0.1', port=3002)
		osc.bind(oscid, self.on_acknowledge, '/ack')
		Clock.schedule_interval(lambda *x: osc.readQueue(oscid), 0.7)		
		return design


if __name__ == '__main__':
	MyApp().run()
