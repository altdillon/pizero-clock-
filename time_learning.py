# for learning about time formats in python
# http://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
# https://docs.python.org/2/library/time.html#module-time
# https://docs.python.org/2/library/datetime.html#datetime.datetime
# https://www.tutorialspoint.com/python/python_date_time.htm
# http://stackoverflow.com/questions/466345/converting-string-into-datetime

import time
import datetime
import json
import dateutil.parser
from listevents import getWakeupEvent



if __name__ == "__main__":
    #print(getWakeupEvent().time().hour)
    #print(getWakeupEvent().time().minute)
    #print(getWakeupEvent().time().second)
    #print(getWakeupEvent().time().time)
    now=datetime.datetime.now()
    wakeuptime=getWakeupEvent()
    #print(wakeuptime.__str__())
    a=json.dumps({"timestamp":str(now),"savetime":wakeuptime.__str__()})
    #print(wakeuptime)
    #print(a)
    b=json.loads(a) # returns a dictionary
    print("time stamp ",b["timestamp"])
    print("save time ",b["savetime"])
    dt=dateutil.parser.parse(b["savetime"])
    print(dt.time().hour)
