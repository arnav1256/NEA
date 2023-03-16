import requests
import random
import string
import pickle
import xml.etree.ElementTree as ET


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


class LinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, value):
        new_node = LinkedListNode(value)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

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
        current_node = self.head
        while current_node.next is not None:
            i += 1
            if i == index:
                val = current_node.next.value
                current_node.next = current_node.next.next
                if current_node.next is None:
                    self.tail = current_node
                self.length -= 1
                return val
            current_node = current_node.next

    def __str__(self):
        result = []
        current_node = self.head
        while current_node is not None:
            result.append(current_node.value)
            current_node = current_node.next
        return ' -> '.join(map(str, result))

    # def prepend(self, value):
    #     newNode = Node(value)
    #     if self.head is None:
    #         self.head = newNode
    #         self.tail = newNode
    #     else:
    #         newNode.next = self.head
    #         self.head = newNode
    #     self.length += 1

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

    # def remove(self, value):
    #     if self.head is None:
    #         return
    #     if self.head.value == value:
    #         self.head = self.head.next
    #         if self.head is None:
    #             self.tail = None
    #         self.length -= 1
    #         return
    #     currentNode = self.head
    #     while currentNode.next is not None:
    #         if currentNode.next.value == value:
    #             currentNode.next = currentNode.next.next
    #             if currentNode.next is None:
    #                 self.tail = currentNode
    #             self.length -= 1
    #             return
    #         currentNode = currentNode.next


class User:
    def __init__(self, name, pwdhash, salt):
        self.username = name
        self.password = pwdhash
        self.salt = salt
        self.journeys = []


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, source, destination, weight):
        self.graph[source].append((destination, weight))

    def add_vertex(self, id_):
        self.graph[id_] = []

    def get_neighbours(self, node):
        if node not in self.graph:
            return []
        else:
            return self.graph[node]

    def get_vertices(self):
        return list(self.graph.keys())


class DijkstraNode:
    def __init__(self, name, dist):
        self.name = name
        self.dist = dist
        self.prev = None


def dijkstra(g, start, end):
    visited = {}
    queue = []
    for node in g.graph:
        visited[node] = DijkstraNode(node, float('inf'))
    visited[start].dist = 0
    queue.append(visited[start])
    while len(queue) != 0:
        current_node = queue[0]
        queue = queue[1:]
        if current_node.name == end:
            break
        for neighbor, weight in g.get_neighbours(current_node.name):
            new_distance = visited[current_node.name].dist + float(weight) + 0.38
            if new_distance < visited[neighbor].dist:
                visited[neighbor].dist = new_distance
                visited[neighbor].prev = current_node
                queue.append(visited[neighbor])
    path = []
    node = visited[end]
    while node.name != start:
        path.append(node.name)
        node = visited[path[-1]].prev
    path.append(start)
    path.reverse()
    for i in range(len(path)):
        path[i] = places[path[i]]
    return path, visited[end].dist


def traverse(g, start, end, algo="bfs"):
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
            for i in range(len(path)):
                path[i] = places[path[i]]
            distance = round_num(distance)
            return path, distance
        visited.add(node)
        for neighbour, weight in g.get_neighbours(node):
            if neighbour not in visited:
                queue.append((neighbour, path + [neighbour], distance + float(weight) + 0.38))
    return [], float('inf')


def hash(key, salt, pepper):
    key = [chr(ord(key[i]) ^ ord(salt[i])) for i in range(min(len(key), len(salt)))]
    a = 0x192873
    for c in key:
        a = ((pepper * a) ^ ord(c)) & 0xffffffff
    a ^= len(key)
    if a == -1:
        a = -2
    return a


def generate_salt(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for _ in range(str_size))


def signup():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    confirm = input("Enter your password again: ")
    exists = False
    try:
        with open("login.txt", "rb") as f:
            try:
                d = pickle.load(f)
            except:
                d = []
            for i in d:
                if i.username == username:
                    exists = True
                    print("Username already exists")
    except:
        open("login.txt", "w").close()
    while (not confirm == password) or exists:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        confirm = input("Enter your password again: ")
        for i in d:
            if i.username == username:
                exists = True
                break
        else:
            exists = False
    with open("login.txt", "wb") as g:
        salt = generate_salt(len(password) + random.randint(0, 5), string.ascii_letters + string.punctuation)
        user = User(username, str(hash(password, salt, pepper)), salt)
        d.append(user)
        pickle.dump(d, g)
    print("Signed up successfully.")


def login():
    loggedIn = False
    while not loggedIn:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        try:
            with open("login.txt", "rb") as f:
                d = pickle.load(f)
        except FileNotFoundError:
            open("login.txt", "w").close()
            print("No Users.")
            return
        except Exception as x:
            print(x)
            return
        for i in d:
            if i.username == username and int(i.password) == hash(password, i.salt, pepper):
                print("Logged in successfully.")
                loggedIn = True
                break
        else:
            print("Incorrect username or password.")
    with open("login.txt", "wb") as f:
        pickle.dump(d, f)
    return username


def save(username):
    hasJourney = False
    while not hasJourney:
        source = input("Enter source station: ")
        destination = input("Enter destination station: ")
        if locations[source] is not None and locations[destination] is not None:
            hasJourney = True
        else:
            print("Incorrect station names.")
    with open("login.txt", "rb") as f:
        d = pickle.load(f)
    for i in d:
        if i.username == username:
            i.journeys.append((source, destination, traverse(graph, locations[source], locations[destination], "bfs"),
                               traverse(graph, locations[source], locations[destination], "dfs"),
                               dijkstra(graph, locations[source], locations[destination])))
    with open("login.txt", "wb") as f:
        pickle.dump(d, f)
    print("Journey saved successfully.")


def read(username):
    with open("login.txt", "rb") as f:
        d = pickle.load(f)
    for i in d:
        if i.username == username:
            if i.journeys == []:
                print("No journeys saved.")
            for j in range(len(i.journeys)):
                print(f"Journey {j + 1}: {i.journeys[j][0]} -> {i.journeys[j][1]}")
                print(f"BFS Route: {' -> '.join(i.journeys[j][2][0])}")
                print(f"Time Taken: {i.journeys[j][2][1]} mins")
                print(f"DFS Route: {' -> '.join(i.journeys[j][3][0])}")
                print(f"Time Taken: {i.journeys[j][3][1]} mins")
                print(f"Dijkstra Route: {' -> '.join(i.journeys[j][4][0])}")
                print(f"Time Taken: {i.journeys[j][4][1]} mins\n")
    with open("login.txt", "wb") as f:
        pickle.dump(d, f)


def print_journey(journey):
    print(f"Journey: {journey[0][0]} -> {journey[0][-1]}")
    print(f"Route: {' -> '.join(journey[0])}")
    print(f"Time Taken: {journey[1]} mins\n")


def calc_min_run(n):
    r = 0
    while n >= 32:
        r |= n & 1
        n >>= 1
    return n + r

# def insertion(arr, left, right):
#     for i in range(left + 1, right + 1):
#         j = i
#         while j > left and arr[j] < arr[j - 1]:
#             arr[j], arr[j - 1] = arr[j - 1], arr[j]
#             j -= 1


def insertion(array, start, end):
    for i in range(start + 1, end + 1):
        key_item = array[i]
        # Binary search to find the correct position to insert key_item
        pos = binary_search(array, key_item, start, i - 1)
        # Shift elements to the right to make space for key_item
        for j in range(i - 1, pos - 1, -1):
            array[j + 1] = array[j]
        # Insert key_item into its correct position
        array[pos] = key_item


def binary_search(array, item, start, end):
    if start == end:
        if array[start] > item:
            return start
        else:
            return start + 1
    elif start > end:
        return start
    mid = (start + end) // 2
    if array[mid] < item:
        return binary_search(array, item, mid + 1, end)
    elif array[mid] > item:
        return binary_search(array, item, start, mid - 1)
    else:
        return mid


def timsort(arr):
    n = len(arr)
    min_run = calc_min_run(n)
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion(arr, start, end)
    size = min_run
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


def round_num(n, d=0):
    a = ((n * (10 ** d) + 0.5) // 1) / (10 ** d)
    if d <= 0:
        return int(a)
    else:
        return a


def arrivals(loc):
    try:
        if locations[loc] is None:
            print("Invalid Station name.")
            return
        data = requests.get(f"https://api.tfl.gov.uk/StopPoint/{locations[loc]}/Arrivals?mode=tube")
        d = [v for v in data.json()]
        a = [(i["lineName"], i['platformName'].split()[0], i["timeToStation"], i["towards"]) for i in d]
        temp = []
        [temp.append(i) for i in a if i not in temp]
        return timsort(temp)
    except Exception as x:
        print(x)
        return


def print_arrivals(data):
    timetable = {}
    trains = []
    for line, direction, time, destination in data:
        trains.append(Train(line, direction, time, destination))
    for train in trains:
        if train.line not in timetable:
            timetable[train.line] = {'Northbound': {}, 'Southbound': {}, 'Eastbound': {}, 'Westbound': {}, 'Inner': {},
                                     'Outer': {}}
        if train.destination not in timetable[train.line][train.direction]:
            timetable[train.line][train.direction][train.destination] = []
        timetable[train.line][train.direction][train.destination].append(train.time)
    for line, directions in timetable.items():
        print(line)
        for direction, entries in directions.items():
            if entries:
                print(f"\t{direction}")
                for station, times in entries.items():
                    print(f"\t\t{station} : {', '.join(str(round_num(time / 60)) for time in times)}")
        print()


def print_status():
    data = requests.get("http://cloud.tfl.gov.uk/TrackerNet/LineStatus")
    tree = ET.ElementTree(ET.fromstring(data.content))
    li = [[w.attrib for w in v] for v in tree.getroot()]
    arr = [v.attrib["StatusDetails"] for v in tree.getroot()]
    for i in range(len(li)):
        print(li[i][1]["Name"])
        print(li[i][2]["Description"])
        if arr[i] != "":
            print(arr[i])
        print()


def api_journey(start, end):
    #print(start, end)
    data = requests.get(f"https://api.tfl.gov.uk/Journey/JourneyResults/{start}/to/{end}").json()
    count = 1
    for i in data["journeys"]:
        print(f"Journey {count}:")
        print(f"Duration: {i['duration']} mins")
        print(f"Cost: £{i['fare']['totalCost'] / 100}")
        for j in i["legs"]:
            print(j["instruction"]["summary"])
        print()
        count += 1


def main():
    global pepper
    pepper = 1000003
    global locations
    locations = HashTable(503)
    with open("thing.txt") as f:
        for line in f:
            val, key = line.strip().split(",")
            locations[key] = val
    global places
    places = HashTable(503)
    with open("thing.txt") as f:
        for line in f:
            key, val = line.strip().split(",")
            places[key] = val
    global graph
    graph = Graph()
    for i in locations.arr:
        if i:
            for j in i:
                graph.add_vertex(j[1])
    data = requests.get("https://raw.githubusercontent.com/egkoppel/tube-timings/main/data.txt")
    li = [i.split() for i in data.text.split("\n")][:-1]
    for i in li:
        graph.add_edge(i[0], i[1], i[2])
    option = input("1: Signup\n2: Login\n3: Journey\n4: Arrivals\n5. Status updates\n6. Exit\n")
    while option != 6:
        try:
            option = int(option)
        except:
            print("Invalid choice")
            pass
        if option == 1:
            signup()
        elif option == 2:
            username = login()
            if username is not None:
                choice = int(input("Enter 1 to save a journey and 2 to read all journeys saved: "))
                if choice == 1:
                    save(username)
                elif choice == 2:
                    read(username)
        elif option == 3:
            print("Choose a graph traversal algorithm (ranked by efficiency):\n\t1. TfL API\n\t2. Dijkstra\n\t3. BFS"
                  "\n\t4. DFS")
            choice = input()
            try:
                choice = int(choice)
                start = input("Choose a starting station: ")
                end = input("Choose a destination: ")
                while locations[start] is None or locations[end] is None:
                    print("Invalid station name.")
                    start = input("Choose a starting station: ")
                    end = input("Choose a destination: ")
            except:
                print("Invalid choice")
            if choice == 1:
                api_journey(locations[start], locations[end])
            elif choice == 2:
                print_journey(dijkstra(graph, locations[start], locations[end]))
            elif choice == 3:
                print_journey(traverse(graph, locations[start], locations[end], "bfs"))
            elif choice == 4:
                print_journey(traverse(graph, locations[start], locations[end], "dfs"))
        elif option == 4:
            station = input("Select which station to get arrivals for: ")
            arr = arrivals(station)
            if arr is not None:
                print_arrivals(arr)
        elif option == 5:
            print_status()
        elif option == 6:
            exit()
        option = input("1: Signup\n2: Login\n3: Journey\n4: Arrivals\n5. Status updates\n6. Exit\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)

# with open("thing.txt", "r") as f:
#     a = [v[:-20] + "\n" for v in f.read().splitlines()]
# with open("thing.txt", "w") as f:
#     f.writelines(a)


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
