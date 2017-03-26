# for learning about time formats in python
# http://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
# https://docs.python.org/2/library/time.html#module-time
# https://docs.python.org/2/library/datetime.html#datetime.datetime
# https://www.tutorialspoint.com/python/python_date_time.htm

import time
import datetime
import json
from listevents import getWakeupEvent



if __name__ == "__main__":
    #print(getWakeupEvent().time().hour)
    #print(getWakeupEvent().time().minute)
    #print(getWakeupEvent().time().second)
    #print(getWakeupEvent().time().time)
    now=datetime.datetime.now()
    a=json.dumps({"timestamp":str(time.time()),"savetime":str(now)})
    print(a)
    b=json.loads(a) # returns a dictionary 
    print(b["savetime"])
