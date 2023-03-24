from requests import get
from random import randint, choice
from string import ascii_letters, punctuation
from pickle import load, dump
import xml.etree.ElementTree as ET
from timsort import *


class HashTable:
    def __init__(self, size):  # constructor for class
        self.size = size  # number of items in hash table
        self.arr = [[] for _ in range(self.size)]  # stores the hash table as a 2d array

    def __hash(self, key):  # the hash function algorithm to find the index to store a value in
        x = 0x192873
        for char in key:
            x = ((1000003 * x) ^ ord(char)) & 0xffffffff
        x ^= len(key)
        if x == -1:
            x = -2
        return x % self.size  # % operation here makes sure that the index is in the correct range

    def __setitem__(self, key, val):  # deals with when an item needs to be placed in the hash table
        exists = False
        index = self.__hash(key)
        for i, v in enumerate(self.arr[index]):  # loops through the bucket checking if an item with the same key exists
            if len(v) == 2 and v[0] == key:
                self.arr[index][i] = (key, val)  # changes the value for the key if the item exists
                exists = True
                break  # exits the loop if the item is found as the bucket does not need to be iterated over more
        if not exists:
            self.arr[index].append((key, val))  # adds a new element to the bucket if no such item exists

    def __getitem__(self, key):  # deals with when an element is retrieved from the hash table
        index = self.__hash(key)
        for i in self.arr[index]:  # iterates over the bucket looking for the element with the given key
            if i[0] == key:
                return i[1]  # returns the element

    def __delitem__(self, key):  # deals with when an element is deleted from the hash table
        index = self.__hash(key)
        for i, v in enumerate(self.arr[index]): # iterates over the bucket looking for the element with the given key
            if v[0] == key:
                del self.arr[index][i]  # deletes the element


class Train:  # stores the details of each train that will arrive at a station
    def __init__(self, line, direction, time, destination):  # constructor for class
        self.line = line  # line that train is on
        self.direction = direction  # direction train is going in
        self.time = time  # time until the train arrives at the station
        self.destination = destination  # destination for the train

    def __str__(self):  # was mostly for debugging; it runs when a Train object is printed
        return f"{self.line}, {self.direction}, {self.time}, {self.destination}"


class LinkedList:
    def __init__(self):  # constructor for class
        self.head = None  # first element in list
        self.tail = None  # last element in list
        self.length = 0  # number of items in list

    def append(self, value):  # adds an item to the end of the list
        new_node = LinkedListNode(value)
        if self.tail is None:  # checks if the list is empty; if it is, the new item is both head and tail
            self.head = new_node
            self.tail = new_node
        else:  # updates pointer of current tail and tail of list
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1  # updates length

    def pop(self, index):  # removes an element at the specified index
        if self.head is None:  # returns if list is empty
            return
        if index == 0:  # case where first element is to be removed
            val = self.head.value
            self.head = self.head.next
            if self.head is None:  # checks if list is empty after removal
                self.tail = None
            self.length -= 1  # update length
            return val  # returns value of removed element
        # case where any other element is to be removed
        current_node = self.head
        for i in range(index - 1):  # iterated through list looking for node to be removed
            current_node = current_node.next
            if current_node is None:  # return if end of list reached
                return
        val = current_node.next.value
        current_node.next = current_node.next.next
        if current_node.next is None:
            self.tail = current_node
        self.length -= 1  # update length
        return val  # returns value of removed element

    def __str__(self):  # used for debugging, runs when list printed
        result = []
        current_node = self.head
        while current_node is not None:  # iterates through list adding all values to result
            result.append(current_node.value)
            current_node = current_node.next
        return ' -> '.join(map(str, result))  # returns string in nice format

    def prepend(self, value):  # adds item to start of list
        new_node = LinkedListNode(value)
        if self.head is None:  # checks if list is empty
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.length += 1  # update length


class LinkedListNode:  # what each element of the linked list is
    def __init__(self, value):  # constructor for class
        self.value = value  # holds the value of the element
        self.next = None  # pointer to the next element


class User:
    def __init__(self, name, pwdhash, salt):  # constructor for class
        self.username = name  # must be unique
        self.password = pwdhash  # only hashed password stored, not original password
        self.salt = salt  # salt stored as well
        self.journeys = []  # stores a list of journeys


class Journey:  # journey that is stored for each user
    def __init__(self, src, dst):  # constructor for class
        self.source = src
        self.destination = dst
        self.bfs = traverse(graph, locations[src], locations[dst], "bfs")  # gets bfs journey
        self.dfs = traverse(graph, locations[src], locations[dst], "dfs")  # gets dfs journey
        self.djk = dijkstra(graph, locations[src], locations[dst])  # gets dijkstra journey


class Graph:
    def __init__(self):  # constructor for class
        self.graph = {}  # stores the graph of the london underground network

    def add_edge(self, source, destination, weight):  # adds a weighted edge between 2 vertices
        self.graph[source].append((destination, weight))

    def add_vertex(self, id_):  # adds a new vertex
        self.graph[id_] = []

    def get_neighbours(self, node):  # returns the list of neighbours for a vertex
        if node not in self.graph:
            return []
        else:
            return self.graph[node]


class DijkstraNode:  # used to get the path using dijkstra's algorithm
    def __init__(self, name, dist):  # constructor for class
        self.name = name
        self.dist = dist
        self.prev = None  # previous node in the path


def dijkstra(g, start, end):  # dijkstras algorithm
    visited = {}
    queue = []
    for node in g.graph:  # creates a DijkstraNode for each node with infinite distance
        visited[node] = DijkstraNode(node, float('inf'))
    visited[start].dist = 0
    queue.append(visited[start])  # adds start node to queue
    while len(queue) != 0:
        current_node = queue[0]
        queue = queue[1:]  # removes first element of queue
        if current_node.name == end:  # breaks out of loop is target node is found
            break
        for neighbour, weight in g.get_neighbours(current_node.name):  # updates distance if lower than old distance
            new_distance = visited[current_node.name].dist + float(weight) + 0.38
            if new_distance < visited[neighbour].dist:
                visited[neighbour].dist = new_distance
                visited[neighbour].prev = current_node
                queue.append(visited[neighbour])
    path = []
    node = visited[end]
    while node.name != start:  # gets the path using the DijkstraNode class
        path.append(node.name)
        node = visited[path[-1]].prev
    path.append(start)
    path.reverse()
    for i in range(len(path)):  # converts ids to common names
        path[i] = places[path[i]]
    return path, round_num(visited[end].dist)  # returns path and time taken


def traverse(g, start, end, algo="bfs"):  # bfs and dfs graph traversal
    queue = LinkedList()  # uses linked list
    queue.append((start, [start], 0))  # adds first element
    visited = set()  # set is a data structure where every element is unique
    while queue:
        if algo == "dfs":  # pops last element (acting as a stack) if doing dfs
            a = queue.pop(queue.length - 1)
            (node, path, distance) = a
        else:  # pops first element (acting as a queue) if doing bfs
            a = queue.pop(0)
            (node, path, distance) = a
        if node == end:  # finds path, distance and return it
            for i in range(len(path)):
                path[i] = places[path[i]]
            distance = round_num(distance)
            return path, distance
        visited.add(node)
        for neighbour, weight in g.get_neighbours(node):  # adds neighbours to queue if not visited
            if neighbour not in visited:
                queue.append((neighbour, path + [neighbour], distance + float(weight) + 0.38))
    return [], float('inf')  # path not found


def hash(key, salt, pepr):  # hash algorithm for passwords using a salt and pepper
    key = [chr(ord(key[i]) ^ ord(salt[i])) for i in range(min(len(key), len(salt)))]
    a = 0x192873
    for char in key:
        a = ((pepr * a) ^ ord(char)) & 0xffffffff
    a ^= len(key)
    if a == -1:
        a = -2
    return a


def generate_salt(str_size, allowed_chars):  # generates random salt for password hashing
    return ''.join(choice(allowed_chars) for _ in range(str_size))


def signup():
    username = input("Enter your username: ")  # user input
    password = input("Enter your password: ")
    confirm = input("Enter your password again: ")  # input verification
    exists = False
    try:  # check if user with given username already exists
        with open("login.txt", "rb") as f:
            try:
                d = load(f)
            except:  # empty file
                d = []
            for i in d:
                if i.username == username:
                    exists = True
                    print("Username already exists")
    except:  # file does not exist
        open("login.txt", "w").close()  # create file
        d = []
    while (not confirm == password) or exists:  # invalid input by user
        print("Username already exists or password input incorrectly. ")
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        confirm = input("Enter your password again: ")
        for i in d:
            if i.username == username:
                exists = True
                break
        else:
            exists = False
    with open("login.txt", "wb") as g:  # hash password and store in file
        salt = generate_salt(len(password) + randint(0, 10), ascii_letters + punctuation)
        user = User(username, str(hash(password, salt, pepper)), salt)
        d.append(user)
        dump(d, g)
    print("Signed up successfully.")


def login():
    logged_in = False
    while not logged_in:
        username = input("Enter your username: ")  # user input
        password = input("Enter your password: ")
        try:  # get list of users
            with open("login.txt", "rb") as f:
                d = load(f)
        except FileNotFoundError:  # no file; no login
            open("login.txt", "w").close()
            print("No Users.")
            return
        for i in d:  # check if username and hashed password match
            if i.username == username and int(i.password) == hash(password, i.salt, pepper):
                print("Logged in successfully.")
                logged_in = True
                break
        else:
            print("Incorrect username or password.")
    with open("login.txt", "wb") as f:  # write data to file
        dump(d, f)
    return username


def save(username):  # save a journey
    has_journey = False
    while not has_journey:  # user input validation
        source = input("Enter source station: ")
        destination = input("Enter destination station: ")
        if locations[source] is not None and locations[destination] is not None:  # checks if stations exist
            has_journey = True
        else:
            print("Incorrect station names.")
    with open("login.txt", "rb") as f:  # get list of users from file
        d = load(f)
    for i in d:  # add a journey to the list of journeys if the usernames match
        if i.username == username:
            j = Journey(source, destination)
            i.journeys.append(j)
    with open("login.txt", "wb") as f:  # write data back to file
        dump(d, f)
    print("Journey saved successfully.")


def read(username):  # read saved journeys
    with open("login.txt", "rb") as f:  # get list of users from file
        d = load(f)
    for i in d:  # iterates through users
        if i.username == username:
            if not i.journeys:  # case where no journeys saved
                print("No journeys saved.")
            for j in range(len(i.journeys)):  # print journeys in a readable format
                print_journey(i.journeys[j].bfs, 1)
                print_journey(i.journeys[j].dfs, 2)
                print_journey(i.journeys[j].djk, 3)
    with open("login.txt", "wb") as f:  # write data back to file
        dump(d, f)


def print_journey(journey, n=0):  # prints a journey in a nice format
    a = n if n !=0 else ''
    print(f"Journey {a}: {journey[0][0]} -> {journey[0][-1]}")
    print(f"Route: {' -> '.join(journey[0])}")
    print(f"Time Taken: {journey[1]} mins\n")


def round_num(n, d=0):  # rounds a number to d decimal places
    a = ((n * (10 ** d) + 0.5) // 1) / (10 ** d)
    return int(a) if d <= 0 else a


def arrivals(loc):  # gets arrivals data from api
    try:
        if locations[loc] is None:  # location does not exist
            print("Invalid Station name.")
            return
        data = get(f"https://api.tfl.gov.uk/StopPoint/{locations[loc]}/Arrivals?mode=tube")  # gets data
        d = [v for v in data.json()]
        a = [(i["lineName"], i['platformName'].split()[0], i["timeToStation"], i["towards"]) for i in d]  # parses data
        temp = []
        [temp.append(i) for i in a if i not in temp]  # gets distinct elements
        return timsort(temp)  # returns sorted list
    except Exception as x:  # if arrivals data not available (eg at night)
        print(x)
        return


def print_arrivals(data):  # prints the output of the arrivals function
    timetable = {}
    trains = []
    for line, direction, time, destination in data:  # creates train object for each arriving train
        trains.append(Train(line, direction, time, destination))
    for train in trains:  # places each train in a nested dictionary based on its parameters
        if train.line not in timetable:
            timetable[train.line] = {'Northbound': {}, 'Southbound': {}, 'Eastbound': {}, 'Westbound': {}, 'Inner': {},
                                     'Outer': {}}
        if train.destination not in timetable[train.line][train.direction]:
            timetable[train.line][train.direction][train.destination] = []
        timetable[train.line][train.direction][train.destination].append(train.time)
    for line, directions in timetable.items():  # prints the contents of the nexted dictionary in a nice format
        print(line)
        for direction, entries in directions.items():
            if entries:
                print(f"\t{direction}")
                for station, times in entries.items():
                    print(f"\t\t{station} : {', '.join(str(round_num(time / 60)) for time in times)}")
        print()


def print_status():  # gets status of all the lines
    data = get("http://cloud.tfl.gov.uk/TrackerNet/LineStatus")  # gets data from api
    tree = ET.ElementTree(ET.fromstring(data.content))  # parses xml using library
    li = [[w.attrib for w in v] for v in tree.getroot()]
    arr = [v.attrib["StatusDetails"] for v in tree.getroot()]  # get details for status
    for i in range(len(li)):
        print(li[i][1]["Name"])  # gets name of line
        print(li[i][2]["Description"])  # gets description of status
        if arr[i]:  # prints details of status if they exist
            print(arr[i])
        print()


def api_journey(start, end):
    data = get(f"https://api.tfl.gov.uk/Journey/JourneyResults/{start}/to/{end}").json()  # gets data from api
    for idx, elem in enumerate(data["journeys"]):  # iterates over all the journeys
        print(f"Journey {idx + 1}:")
        print(f"Duration: {elem['duration']} mins")  # prints duration of journey
        try:
            print(f"Cost: £{elem['fare']['totalCost'] / 100}")  # prints cost of journey
        except:  # happens when route is entirely walking
            print("Cost: £0.00")
        for j in elem["legs"]:  # prints summary of each leg of the journey
            print(j["instruction"]["summary"])
        print()


def main():
    option = input("1: Signup\n2: Login\n3: Journey\n4: Arrivals\n5. Status updates\n6. Exit\n")  # user choice
    while option != 6:  # allows for multiple functions without rerunning the program
        try:  # input validation
            option = int(option)
        except:
            print("Invalid choice")
        if option == 1:  # signup option
            signup()
        elif option == 2:  # login option
            username = login()
            if username is not None:  # input validation
                choice = int(input("Enter 1 to save a journey and 2 to read all journeys saved: "))  # user choice
                if choice == 1:  # save journey option
                    save(username)
                elif choice == 2:  # read journey option
                    read(username)
        elif option == 3:  # journey option
            print("Choose a method (ranked by efficiency):\n\t1. TfL API\n\t2. Dijkstra\n\t3. BFS"
                  "\n\t4. DFS")  # user choice
            choice = input()
            try:  # user input
                choice = int(choice)
                start = input("Choose a starting station: ")
                end = input("Choose a destination: ")
                while locations[start] is None or locations[end] is None:  # input validation
                    print("Invalid station name.")
                    start = input("Choose a starting station: ")
                    end = input("Choose a destination: ")
            except:
                print("Invalid choice")
            if choice == 1:  # api journey option
                api_journey(locations[start], locations[end])
            elif choice == 2:  # dijkstra option
                print_journey(dijkstra(graph, locations[start], locations[end]))
            elif choice == 3:  # bfs option
                print_journey(traverse(graph, locations[start], locations[end], "bfs"))
            elif choice == 4:  # dfs option
                print_journey(traverse(graph, locations[start], locations[end], "dfs"))
        elif option == 4:  # arrivals option
            station = input("Select which station to get arrivals for: ")
            arr = arrivals(station)
            if arr is not None:  # checks if there are arrivals
                print_arrivals(arr)
        elif option == 5:  # status option
            print_status()
        elif option == 6:  # exit option
            exit()
        option = input("1: Signup\n2: Login\n3: Journey\n4: Arrivals\n5. Status updates\n6. Exit\n")  # user choice


if __name__ == '__main__':
    pepper = 1000003  # constant
    locations = HashTable(503)  # hash table mapping names to ids
    places = HashTable(503)  # hash table mapping ids to names
    with open("thing.txt") as f:  # open file to write data to hash tables
        for line in f:
            val, key = line.strip().split(",")
            locations[key] = val
            key, val = line.strip().split(",")
            places[key] = val
    graph = Graph()  # graph of underground network
    for i in locations.arr:  # adds all vertices from hash table
        if i:
            for j in i:
                graph.add_vertex(j[1])
    data = get("https://raw.githubusercontent.com/egkoppel/tube-timings/main/data.txt")  # gets github open source data
    li = [i.split() for i in data.text.split("\n")][:-1]  # parses data
    for i in li:  # adds all the edges to the graph
        graph.add_edge(i[0], i[1], i[2])
    try:  # calls main function
        main()
    except Exception as e:  # exception handling
        print(e)
