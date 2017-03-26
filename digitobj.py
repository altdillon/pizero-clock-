# just seeing how exceptions work
class BcdInput(Exception):
    def __init__ (self,badvalue):
         Exception.__init__(self) # I think it's calling the constructor of the super class
         print("value not valid bcd ",badvalue)

# digit is a class that handles each of the seven segment displays
# normally there are 4, the there's 4 seven segment displays

class Digit:

    def __init__ (self,on_pin,dis_id):
        self.on_pin=on_pin
        self.dis_id=dis_id

    def setValue(self,bcd=0): # defult value is zero
        # check to make sure that value is valid bcd
        if bcd < 0 or bcd > 9 :
            raise BcdInput(bcd) # throw the book at who ever's using this
        else:
            self.current_value=bcd
            self.scode=self.getSevenSegmentCode(self,bcd) # this is a klug, not sure why... :(
            #print("seven segment code: ",scode)

    # returns true if the scanID value is the same as the, not really needed, but it might be nice to have
    def isOn(self,scanID):
        out=false
        if scanID == self.dis_id:
            out=true
        return out

    # basicly a look up table for getting converting BCD to seven segment codes
    @staticmethod
    def getSevenSegmentCode(self,bcd_value):
        if bcd_value == 0:
            return ['a','b','c','d','e','f']
        elif bcd_value == 1:
            return ['b','c']
        elif bcd_value == 2:
            return ['a','b','g','e','d']
        elif bcd_value == 3:
            return ['a','b','g','c','d']
        elif bcd_value == 4:
            return ['f','g','b','c']
        elif bcd_value == 5:
            return ['a','f','g','c','d']
        elif bcd_value == 6:
            return ['a','f','g','c','d','e']
        elif bcd_value == 7:
            return ['a','b','c']
        elif bcd_value == 8:
            return ['a','b','c','d','e','f','g']
        elif bcd_value == 9:
            return ['a','b','f','g','c','d']
