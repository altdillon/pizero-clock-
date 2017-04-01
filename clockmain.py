from digitobj import Digit # import the digit class
from displayobj import Display # input the display class
from listevents import getWakeupEvent # import get wakeup event
import dateutil.parser
import datetime
import time
import json
import sched
import os.path

class AlarmClock:

    def __init__ (self):
        self.filename="lasttime.json"
        self.currentTime=[8,8,8,8] # set the defult value
        self.ringTime=None # defult value for ring time; ring time will hold a value of type datetime
        #self.update_time_file() # update or create the time file when the program starts

    def update_clock_display(self): # update the current time digit list with the current time; usehalftime is true if the clock is running in 12 hour time
        now=datetime.datetime.now() #get the current time and date
        # break it down into seconds minutes and hours and put it into the current time list
        self.currentTime=[now.hour/10,now.hour%10,now.minute/10,now.minute%10]
        #print(self.currentTime)
        return self.currentTime

    # init the event callback that's responcable for checking the alarm
    def init_alarm_ring(self):
        s = sched.scheduler(time.time, time.sleep) # thread scheduler object
        # setup the event that will see if the alarm is going to be able to run or not
        def _check_alarm(): # * not at all tested as of 2am 4/1/2017
            if self.ringTime: # if ringTime is defined
                if datetime.datetime.now() - self.ringTime < 3: # if the current time is +- 4 seconds from now
                    print("ring!!!!") # place holder for the api call to ring the alarm
                s.enter(1,1,_check_alarm,()) # re add this function to the queue

        # enter the inital callback for _check_alarm
        s.enter(1,1,_check_alarm,())



    def update_time_file(self):
        # see if a file containging the last alarm time exists, if not then get the current time and update it to the new file
        if os.path.isfile(self.filename):

            filenameIO=open(self.filename,"r+")
            jsonbuffer=filenameIO.read(150)
            dt=json.loads(jsonbuffer)
            # figure out when this json file was last updated
            last_timestamp=dateutil.parser.parse(dt["timestamp"])
            deltadatetime=datetime.datetime.now()-last_timestamp
            # if more than 1 hour has ellisped then update the json file, time is in seconds
            if deltadatetime.seconds > 3600:
                # close the file and then re open it with diffent permissions
                filenameIO.close()
                filenameIO=open(self.filename,"w+")
                # update the time and write it to the json file
                wakeupevent=getWakeupEvent() # update the wakeup event from the server
                self.ringTime=wakeupevent # assign the data pulled from google calander
                newjsondata={"timestamp":str(datetime.datetime.now()),"savetime":wakeupevent.__str__()}
                filenameIO.write(json.dumps(newjsondata))

            # else, we don't really need to do any thing

            filenameIO.close()
        else:
            # if the file does not exist, then create one
            filenameIO=open(self.filename,"w+")
            now=datetime.datetime.now()
            wakeuptime=getWakeupEvent()
            jsonbuffer=json.dumps({"timestamp":str(now),"savetime":wakeuptime.__str__()})
            filenameIO.write(jsonbuffer)
            filenameIO.close()


#from digitobj import Digit # import the digit class
#from displayobj import Display # input the display class

# pulls the time down from google calander
# def update_time():
#     nextAlarm=getWakeupEvent()
#     jsondata=json.dumps(['wakeuptime',nextAlarm])


def main_loop():
    alarmclock=AlarmClock()
    #alarmclock.update_time_file() # test call for update_time_file
    #alarmclock.update_clock_display() # test call for updateing the clock display
    #alarmclock.init_alarm_ring() # test to init alarm ring
    # new up 4 digit objects for the 4 clock displays
    d_one=Digit(8,1)
	d_two=Digit(9,2)
	d_three=Digit(7,3)
	d_four=Digit(0,4)
    # new up a display object, with the digit objects
    clockdisplay=Display([d_one,d_two,d_three,d_four])

    # main loop, this is really starting to smell like a micro controller program!
    while True:
        clock.set_displayvalue(alarmclock.update_clock_display()) # update the values with the current time
        clock.draw_bus()

# weird if statment that python needs to run it's main function
if __name__ == "__main__":
    main_loop()
