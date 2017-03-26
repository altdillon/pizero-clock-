from listevents import getWakeupEvent
from dateutil import parser
import datetime
import time
import json
import sched
import os.path

class AlarmClock:

    def __init__ (self):
        self.filename="lasttime.json"

    def update_time_file(self):
        # see if a file containging the last alarm time exists, if not then get the current time and update it to the new file
        if os.path.isfile(self.filename):
            # file does exist
            print("doing stuff for a file")
        else:
            # if the file does not exist, then create one
            now=datetime.datetime.now()
            jsonbuffer=json.dumps({"timestamp":str(now),"savetime":str(getWakeupEvent)})
            print(jsonbuffer)

        #filenameIO.close()


#from digitobj import Digit # import the digit class
#from displayobj import Display # input the display class

# pulls the time down from google calander
# def update_time():
#     nextAlarm=getWakeupEvent()
#     jsondata=json.dumps(['wakeuptime',nextAlarm])


def main():
    alarmclock=AlarmClock()
    alarmclock.update_time_file()


# weird if statment that python needs to run it's main function
if __name__ == "__main__":
    main()
