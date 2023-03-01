# # data = [('Central', 'Northbound', 213, 'Epping'),
# #         ('Central', 'Northbound', 483, 'Epping'),
# #         ('Central', 'Southbound', 543, 'West Ruislip'),
# #         ('Central', 'Southbound', 903, 'Ealing Broadway'),
# #         ('Piccadilly', 'Eastbound', 183, 'Cockfosters'),
# #         ('Piccadilly', 'Eastbound', 603, 'Cockfosters'),
# #         ('Piccadilly', 'Westbound', 1023, 'Uxbridge'),
# #         ('Piccadilly', 'Westbound', 1443, 'Heathrow T123 + 5')]
#
# data = [('Central', 'Eastbound', 5, 'Newbury Park'), ('Central', 'Eastbound', 185, 'Epping'), ('Central', 'Eastbound', 815, 'Hainault via Newbury Park'), ('Central', 'Eastbound', 935, 'Loughton'), ('Central', 'Eastbound', 1055, 'Hainault via Newbury Park'), ('Central', 'Eastbound', 1115, 'Epping'), ('Central', 'Eastbound', 1235, 'Newbury Park'), ('Central', 'Eastbound', 1475, 'Epping'), ('Central', 'Eastbound', 1475, 'Epping'), ('Central', 'Westbound', 126, 'Ealing Broadway'), ('Central', 'Westbound', 276, 'West Ruislip'), ('Central', 'Westbound', 396, 'White City'), ('Central', 'Westbound', 576, 'Northolt'), ('Central', 'Westbound', 696, 'Ealing Broadway'), ('Central', 'Westbound', 935, 'West Ruislip'), ('Central', 'Westbound', 1115, 'Ealing Broadway'), ('Central', 'Westbound', 1295, 'West Ruislip'), ('Central', 'Westbound', 1475, 'Ealing Broadway'), ('Central', 'Westbound', 1595, 'West Ruislip'), ('Piccadilly', 'Eastbound', 36, 'Cockfosters'), ('Piccadilly', 'Eastbound', 216, 'Arnos Grove'), ('Piccadilly', 'Eastbound', 276, 'Cockfosters'), ('Piccadilly', 'Eastbound', 336, 'Cockfosters'), ('Piccadilly', 'Eastbound', 456, 'Cockfosters'), ('Piccadilly', 'Eastbound', 696, 'Cockfosters'), ('Piccadilly', 'Eastbound', 996, 'Cockfosters'), ('Piccadilly', 'Eastbound', 1296, 'Arnos Grove'), ('Piccadilly', 'Eastbound', 1536, 'Cockfosters'), ('Piccadilly', 'Westbound', 66, 'Rayners Lane'), ('Piccadilly', 'Westbound', 216, 'Heathrow via T4 Loop'), ('Piccadilly', 'Westbound', 456, 'Uxbridge'), ('Piccadilly', 'Westbound', 636, 'Heathrow T123 + 5'), ('Piccadilly', 'Westbound', 876, 'Heathrow via T4 Loop'), ('Piccadilly', 'Westbound', 1056, 'Northfields'), ('Piccadilly', 'Westbound', 1116, 'Rayners Lane'), ('Piccadilly', 'Westbound', 1296, 'Heathrow T123 + 5'), ('Piccadilly', 'Westbound', 1536, 'Heathrow via T4 Loop')]
#
# class Train:
#     def __init__(self, line, direction, time, destination):
#         self.line = line
#         self.direction = direction
#         self.time = time
#         self.destination = destination
#
#     def __str__(self):
#         return f"{self.line}, {self.direction}, {self.time}, {self.destination}"
#
#
#
# # create a dictionary with keys as line names and values as dictionaries
# # where the keys are directions and values are dictionaries with station as keys and list of time values as values
# timetable = {}
# trains = []
# for line, direction, time, destination in data:
#     trains.append(Train(line, direction, time, destination))
# for train in trains:
#     if train.line not in timetable:
#         timetable[train.line] = {'Northbound': {}, 'Southbound': {}, 'Eastbound': {}, 'Westbound': {}}
#     if train.destination not in timetable[train.line][train.direction]:
#         timetable[train.line][train.direction][train.destination] = []
#     timetable[train.line][train.direction][train.destination].append(train.time)
#
# # loop over the dictionary and print the timetable
# for line, directions in timetable.items():
#     print(line)
#     for direction, entries in directions.items():
#         if entries:
#             print(f"\t{direction}")
#             for station, times in entries.items():
#                 print(f"\t\t{station} : {', '.join(str(roundNum(time/60)) for time in times)}")
#     print()

## FROM ARRIVALS FUNCTION LEGACY THING
# d = [{k: v[k] for k in ("lineName", "platformName", "expectedArrival", "timeToStation", "currentLocation", "towards")} for v in data.json()]

# print(sorted([d[i]["timeToStation"] for i in range(len(d))]))
# print(sorted(d, key=lambda x: x['timeToStation']))
# print(sorted(d, key=lambda x: (x['platformName'].split()[0], x['timeToStation'])))
# for i in range(len(d)):
#     print(d[i])

# print(sorted(d, key=lambda x: (x["lineName"], x['platformName'].split()[0], x['expectedArrival'])))
# for i in range(len(d)):
#     print(d[i]["expectedArrival"])
#     from dateutil import parser
#     print(parser.parse(d[i]["expectedArrival"][:-1]))
#     print(datetime(*time.strptime(d[i]["expectedArrival"][:-1], "%Y-%m-%dT%H:%M:%S")[:6]))

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, value):
        newNode = Node(value)
        if self.tail is None:
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.next = newNode
            self.tail = newNode
        self.length += 1

    def prepend(self, value):
        newNode = Node(value)
        if self.head is None:
            self.head = newNode
            self.tail = newNode
        else:
            newNode.next = self.head
            self.head = newNode
        self.length += 1

    # def insert_after(self, prev_node, value):
    #     if not prev_node:
    #         raise ValueError("Previous node must be valid")
    #     new_node = Node(value)
    #     new_node.next = prev_node.next
    #     prev_node.next = new_node

    # def search(self, value):
    #     current_node = self.head
    #     while current_node is not None:
    #         if current_node.value == value:
    #             return current_node
    #         current_node = current_node.next
    #     return None

    def remove(self, value):
        if self.head is None:
            return
        if self.head.value == value:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.length -= 1
            return
        currentNode = self.head
        while currentNode.next is not None:
            if currentNode.next.value == value:
                currentNode.next = currentNode.next.next
                if currentNode.next is None:
                    self.tail = currentNode
                self.length -= 1
                return
            currentNode = currentNode.next

    def pop(self, index):
        i = 0
        if self.head is None:
            return
        if i == index:
            val = self.head.value
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.length -= 1
            return val
        currentNode = self.head
        while currentNode.next is not None:
            i += 1
            if i == index:
                currentNode.next = currentNode.next.next
                if currentNode.next is None:
                    self.tail = currentNode
                self.length -= 1
                return currentNode.value
            currentNode = currentNode.next

    def __str__(self):
        result = []
        currentNode = self.head
        while currentNode is not None:
            result.append(currentNode.value)
            currentNode = currentNode.next
        return ' -> '.join(map(str, result))

class HashTable:
    def __init__(self, size):
        self.size = size
        self.arr = [[] for _ in range(self.size)]

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

    def __delitem__(self, key):
        index = self._hash(key)
        for i, v in enumerate(self.arr[index]):
            if v[0] == key:
                del self.arr[index][i]

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, source, destination, weight):
            self.graph[source].append((destination, weight))

    def add_vertex(self, id):
        self.graph[id] = []

    def get_neighbours(self, node):
        if node not in self.graph:
            return []
        else:
            return self.graph[node]

    def get_vertices(self):
        return list(self.graph.keys())

def traverse(graph, start, end, algo="bfs"):
    queue = LinkedList()
    queue.append((start, [start], 0))
    visited = set()
    while queue:
        if algo == "dfs":
            a = queue.pop(queue.length - 1)
            (node, path, distance) = a
        else:
            a = queue.pop(0)
            (node, path, distance) = a
        if node == end:
            places = HashTable(503)
            with open("thing.txt") as f:
                for line in f:
                    key, val = line.strip().split(",")
                    places[key] = val
            for i in range(len(path)):
                path[i] = places[path[i]]
            distance = round(distance)
            return path, distance
        visited.add(node)
        for neighbour, weight in graph.get_neighbours(node):
            if neighbour not in visited:
                queue.append((neighbour, path + [neighbour], distance + float(weight) + 0.38))
    return [], float('inf')

def main():
    locations = HashTable(503)
    with open("thing.txt") as f:
        for line in f:
            val, key = line.strip().split(",")
            locations[key] = val
    graph = Graph()
    for i in locations.arr:
        if i:
            for j in i:
                graph.add_vertex(j[1])
    with open("data.txt", "r") as f:
        li = [i.split() for i in f.readlines()]
        for i in li:
            graph.add_edge(i[0], i[1], i[2])
    print(graph.graph)
    path, distance = a_star_pathfinding(graph, locations["Heathrow Terminals 2&3"], locations["Epping"])
    print(traverse(graph, locations["Heathrow Terminals 2&3"], locations["Epping"], "bfs"))
if __name__ == "__main__":
    main()


# print(traverse(graph, locations["Hammersmith (H&C Line)"], locations["Hammersmith (Dist&Picc Line)"], "bfs"))
# print(traverse(graph, locations["Uxbridge"], locations["Cockfosters"], "bfs"))
# print(traverse(graph, locations["Upminster"], locations["Chesham"], "bfs"))
# print(traverse(graph, locations["Golders Green"], locations["Hammersmith (Dist&Picc Line)"], "bfs"))
# print(traverse(graph, locations["Mill Hill East"], locations["Hammersmith (Dist&Picc Line)"], "bfs"))

# t = HashTable(10)
# t["march 6"] = 130
# t["march 8"] = 20
# t["march 17"] = 10
# del t["march 6"]
# print(t.arr)
# print(t["march 6"])

# li = LinkedList()
# li.append(1)
# li.append(5)
# li.prepend("string")
# li.remove(5)
# print(li)