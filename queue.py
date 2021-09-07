import heapq

eventq = []

def pushq(event):
    heapq.heappush(eventq, (event.time, event))