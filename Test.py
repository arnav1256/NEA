import requests, math
from datetime import datetime
import time
# locations = {}
# with open("thing.txt") as f:
#     for line in f:
#         val, key = line.strip().split(",")
#         locations[key] = val

class HashTable:
    def __init__(self, size):
        self.size = size
        self.arr = [[] for i in range(self.size)]

    def _hash(self, key):
        x = 0x192873
        for c in key:
            x = ((1000003 * x) ^ ord(c)) & 0xffffffff
        x ^= len(key)
        if x == -1:
            x = -2
        return x % self.size

    def __setitem__(self, key, val):
        exists = False
        index = self._hash(key)
        for i, v in enumerate(self.arr[index]):
            if len(v) == 2 and v[0] == key:
                self.arr[index][i] = (key, val)
                exists = True
                break
        if not exists:
            self.arr[index].append((key, val))

    def __getitem__(self, key):
        index = self._hash(key)
        for i in self.arr[index]:
            if i[0] == key:
                return i[1]

    # def __delitem__(self, key):
    #     index = self._hash(key)
    #     for i, v in enumerate(self.arr[index]):
    #         if v[0] == key:
    #             del self.arr[index][i]

class Train:
    def __init__(self, line, direction, time, destination):
        self.line = line
        self.direction = direction
        self.time = time
        self.destination = destination

    def __str__(self):
        return f"{self.line}, {self.direction}, {self.time}, {self.destination}"

def calcMinRun(n):
    r = 0
    while n >= 32:
        r |= n & 1
        n >>= 1
    return n + r

def insertion(arr, left, right):
    for i in range(left + 1, right + 1):
        j = i
        while j > left and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1

def timSort(arr):
    n = len(arr)
    minRun = calcMinRun(n)
    for start in range(0, n, minRun):
        end = min(start + minRun - 1, n - 1)
        insertion(arr, start, end)
    size = minRun
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))
            if mid < right:
                merge(arr, left, mid, right)
        size = 2 * size
    return arr

def merge(arr, start, mid, end):
    start2 = mid + 1
    if arr[mid] <= arr[start2]:
        return
    while start <= mid and start2 <= end:
        if arr[start] <= arr[start2]:
            start += 1
        else:
            value = arr[start2]
            index = start2
            while index != start:
                arr[index] = arr[index - 1]
                index -= 1
            arr[start] = value
            start += 1
            mid += 1
            start2 += 1

def roundNum(n, d = 0):
    a = ((n * (10 ** d) + 0.5) // 1) / (10 ** d)
    if d<=0 :
        return int(a)
    else:
        return a
#x = requests.get('https://api.tfl.gov.uk/line/central/arrivals')

def arrivals(loc):
    locations = HashTable(503)
    with open("thing.txt") as f:
        for line in f:
            val, key = line.strip().split(",")
            locations[key] = val
    #print(locations.arr)
    try:
        data = requests.get(f"https://api.tfl.gov.uk/StopPoint/{locations[loc]}/Arrivals?mode=tube")
        d = [v for v in data.json()]
        a = [(i["lineName"], i['platformName'].split()[0], i["timeToStation"], i["towards"]) for i in d]
        temp = []
        [temp.append(i) for i in a if i not in temp]
        #print(timSort(a))
        #print(timSort(temp))
        return timSort(temp)
    except:
        print("RequestError")
        exit()

def printArrivals(data):
    timetable = {}
    trains = []
    for line, direction, time, destination in data:
        trains.append(Train(line, direction, time, destination))
    for train in trains:
        if train.line not in timetable:
            timetable[train.line] = {'Northbound': {}, 'Southbound': {}, 'Eastbound': {}, 'Westbound': {}, 'Inner': {}, 'Outer': {}}
        if train.destination not in timetable[train.line][train.direction]:
            timetable[train.line][train.direction][train.destination] = []
        timetable[train.line][train.direction][train.destination].append(train.time)
    for line, directions in timetable.items():
        print(line)
        for direction, entries in directions.items():
            if entries:
                print(f"\t{direction}")
                for station, times in entries.items():
                    print(f"\t\t{station} : {', '.join(str(roundNum(time/60)) for time in times)}")
        print()

def main():
    ## NICE INPUT STUFF SHOULD BE DONE HERE
    printArrivals(arrivals("King's Cross St. Pancras"))

if __name__ == '__main__':
    main()

# with open("thing.txt", "r") as f:
#     a = [v[:-20] + "\n" for v in f.read().splitlines()]
# with open("thing.txt", "w") as f:
#     f.writelines(a)