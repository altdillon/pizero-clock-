# import wiringpi and time and also digits, don't forget about digits 
import wiringpi
import time
from digitobj import *

# constents for pins 
HIGH=1
LOW=0
OUTPUT=1
INPUT=0

cpins=[8, 9, 7, 0] # pins that turn the displays on and off; not really needed since this is already defined in the digit class
apins=[5,10,15,16,1,6] # pins for segments on display
pins={
	'a':5,
	'b':10,
	'c':4,
	'd':15,
	'e':16,
	'f':1,
	'g':6
}

# controll class for the entire display.
# this is ment to manage all 4 seven segment displays as a list

class Display:
	
	def __init__ (self,digits):
		self.digits=digits # list of the displays
		self.delay=0.005 # delay between drawings 
		wiringpi.wiringPiSetup() # setup the wiringpi lib for gpio 
		self.init_controlbits() # clear all the pins and make sure everythings blank 

	# set all the pins as outputs and then make them all low
	def init_controlbits(self):
		#for p in cpins:
		#	wiringpi.pinMode(p,OUTPUT)
		#	wiringpi.digitalWrite(p,LOW)
		for digit in self.digits:
			wiringpi.pinMode(digit.on_pin,OUTPUT)
			wiringpi.digitalWrite(digit.on_pin,LOW)
	
	# clear the segment bus
	def clr_bus(self):		
		for p in apins:
			wiringpi.pinMode(p,LOW)
	
	# set a value to draw to the segment bus 
	def set_displayvalue(self,value):
		for i in range(0,len(value)):
			self.digits[i].setValue(value[i])	
	
	# print out the segment codes, for debug reasons 
	def print_scodes(self):
		for digit in self.digits:
			print(digit.scode)	
	
	# write a digit to the segment bus, takes in a seven segment code and sets the segment bus to that code 
	# the issue where the c segment goes high when two is called happens in this method... just a note for the future 
	def write_bus(self,scode):
		for s in scode:
			#print(pins[s]) # print out the current scode 
			wiringpi.pinMode(pins[s],OUTPUT)

	# scan through all the digits and write them to the segment bus	
	def draw_bus(self):
		for digit in self.digits:
			#self.clr_bus() # make sure there's nothing on the bus 
			wiringpi.digitalWrite(digit.on_pin,HIGH) # set the display value to high
			self.clr_bus()
			#print(digit.scode)
			self.write_bus(digit.scode)

			# this if statement is a massive kluge. It brings shame to my family.  
			# basicly when the digit two is drawn to the bus the C control also goes to high.  I have no idea what's calling this
			# at some point I'll fix this and I'll get to move on with my life, but now, this will have to stay
			if digit.current_value == 2:
				wiringpi.pinMode(pins['c'],INPUT)
 
			time.sleep(self.delay) # delay so the value actually has time to draw
			wiringpi.digitalWrite(digit.on_pin,LOW) # set the display on pin back to low 
