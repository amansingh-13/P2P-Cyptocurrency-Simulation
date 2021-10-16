import heapq
from params import *

#stores the evnt queue
eventq = []

#function to add event in the queue
def pushq(event):
    if(event.time <= SIM_TIME):
        heapq.heappush(eventq, (event.time, event))