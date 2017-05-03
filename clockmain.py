from digitobj import Digit # import the digit class
from displayobj import Display # input the display class
from listevents import getWakeupEvent # import get wakeup event
import dateutil.parser
import datetime
import time
import json
import sched
import os.path
import daemon # import from python deamon

# alarm clock class is the class that actually runs the allarm clock

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

    def read_time(self): # returns true if it's time to sound the alarm.  This is going to be called several times a second
        out=false
        if self.ringTime :  # make sure that the ring time member function is defined.  Idealy the first call to update_time_file occures before the first call to this function
            #see if the current is with +- 1 second of the time that the object has saved
            now=datetime.datetime.now()
            if now == self.ringTime :  # this makes my common sence tingle, this might make some trouble in the future
                out=true

        return out


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
    # init all the objects that we'll need for running an alarm clock
    alarmclock=AlarmClock()
    alarmclock.update_time_file() # inital call to get a new update file 
    s = sched.scheduler(time.time, time.sleep)
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

    #alarmclock.update_time_file() # update time time file, test call

    # setup events for geting time from google api and seeing if it's time to getup
    def update_wakeup_from_googleapi():
        alarmclock.update_time_file()
        s.enter(30,1,update_wakeup_from_googleapi,()) # re add event to the event que

    def check_wakeup():
        if alarmclock.read_time() :
            clockdisplay.play_buzzer(5) # play buzzer for 5 seconds

    # todo next time this code is editied: init the event que for the two nested methods
    # init event que
    s.enter(3,1,update_wakeup_from_googleapi,())
    s.enter(3,1,check_wakeup,())

    # main loop, this is really starting to smell like a micro controller program!
    while True:
        clockdisplay.set_displayvalue(alarmclock.update_clock_display()) # update the values with the current time
        clockdisplay.draw_bus() # update the current time to the display bus

# weird if statment that python needs to run it's main function
if __name__ == "__main__":
    # init stuff before we can start the main loop:
    # http://stackoverflow.com/questions/1369526/what-is-the-python-keyword-with-used-for
    # https://docs.python.org/3/whatsnew/2.6.html#pep-343-the-with-statement
    #http://www.tldp.org/HOWTO/HighQuality-Apps-HOWTO/boot.html

    with daemon.DaemonContext():
        main_loop()
