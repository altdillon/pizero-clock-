from listevents import getWakeupEvent
import dateutil.parser
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
