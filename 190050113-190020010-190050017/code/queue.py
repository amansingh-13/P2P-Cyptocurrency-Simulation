import heapq

#stores the evnt queue
eventq = []

#function to add event in the queue
def pushq(event):
    heapq.heappush(eventq, (event.time, event))