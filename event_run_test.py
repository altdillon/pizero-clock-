#https://docs.python.org/2.7/library/sched.html

# event run test in pythong 2.7
import sched
import time

s = sched.scheduler(time.time, time.sleep)

def sayHi():
    print("hello!")
    s.enter(3,1,sayHi,()) # re qeue the event to we get something that says hello every 3 seconds

s.enter(3,1,sayHi,())
s.run()
