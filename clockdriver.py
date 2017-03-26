from digitobj import Digit # import the digit class
from displayobj import Display # input the display class 

if __name__ == "__main__":
	d_one=Digit(8,1)
	d_two=Digit(9,2)
	d_three=Digit(7,3)
	d_four=Digit(0,4)
	clock=Display([d_one,d_two,d_three,d_four])#,d_two,d_three,d_four])
	displayvalues=[1,2,5,2] # set values to display
	clock.set_displayvalue(displayvalues)
	clock.print_scodes()
	while 1:
		clock.draw_bus()	
