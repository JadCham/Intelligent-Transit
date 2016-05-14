from __future__ import generators
from math import radians, cos, sin, asin, sqrt
import json
import urllib2
import time


class PriorityDictionary(dict):

    #Constructor
    def __init__(self):
        self.__heap = []
        dict.__init__(self)

    def __iter__(self):
        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]

        return iterfn()

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v, k) for k, v in self.iteritems()]
            self.__heap.sort()
        else:
            newPair = (val, key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and newPair < heap[(insertionPoint - 1) // 2]:
                heap[insertionPoint] = heap[(insertionPoint - 1) // 2]
                insertionPoint = (insertionPoint - 1) // 2
            heap[insertionPoint] = newPair

    def smallest(self):
        if len(self) == 0:
            raise IndexError, "smallest of empty priorityDictionary"
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while 1:
                smallChild = 2*insertionPoint+1
                if smallChild+1 < len(heap) and heap[smallChild] > heap[smallChild+1] :
                    smallChild += 1
                if smallChild >= len(heap) or lastItem <= heap[smallChild]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild
        return heap[0][1]

    def setdefault(self,key,val):
        if key not in self:
            self[key] = val
        return self[key]


def dijkstra(g, start, end=None):

    # dictionary of final distances
    d = {}
    # dictionary of predecessors
    p = {}
    #Dictionary
    q = PriorityDictionary()
    q[str(start)] = 0

    for v in q:
        d[str(v)] = q[str(v)]
        if v == end: break

        for w in g[str(v)]:
            vwlength = d[str(v)] + int(g[str(v)][str(w)])
            if w in d:
                if vwlength < d[str(w)]:
                    raise ValueError, "Dijkstra: found better path to already-final vertex"
            elif w not in q or vwlength < q[str(w)]:
                q[str(w)] = vwlength
                p[str(w)] = v

    return d, p


def shortestpath(g, start, end):
    d, p = dijkstra(g, start, end)
    path = []
    while 1:
        path.append(end)
        if end == start:
            break
        end = p[end]
    path.reverse()
    return path


class Transit:

    def __init__(self):
        self.Graph = []
        self.Markers = []
        self.Routes = []
        self.Crosses = []
        self.getdata()
        self.source = {}
        self.destination = {}
        self.key = "YOUR_KEY_HERE"


    def getdata(self):
        # Fetch Graph
        f = open("json/graph.json")
        data = f.read()
        self.Graph = json.loads(data)

        # Fetch Markers nodes
        f = open("json/markers.json")
        data = f.read()
        self.Markers = json.loads(data)

        # Fetch Routes
        f = open("json/routes.json")
        data = f.read()
        self.Routes = json.loads(data)

        # Fetch Crosses
        f = open("json/crosses.json")
        data = f.read()
        self.Crosses = json.loads(data)

    def findpath(self, source, destination):

        src = self.findnearestmarker(source[0], source[1])
        self.source['title'] = "Source"
        self.source['lat'] = source[1]
        self.source['long'] = source[0]

        dest = self.findnearestmarker(destination[0], destination[1])
        self.destination['title'] = "Destination"
        self.destination['lat'] = destination[1]
        self.destination['long'] = destination[0]

        src_buses_list = []
        dest_buses_list = []

        for i in range(len(self.Markers)):
            if src == str(self.Markers[i]["title"].split("-")[0]):
                src_buses_list.append(self.Markers[i]["id"])
            if dest == str(self.Markers[i]["title"].split("-")[0]):
                dest_buses_list.append(self.Markers[i]["id"])

        the_path = []
        min_cost = int(10e10)

        for s in src_buses_list:
            for d in dest_buses_list:
                path = shortestpath(self.Graph, s, d)
                cost = self.calculate_cost(path)
                if cost < min_cost:
                    the_path = path[:]
                    min_cost = cost
        return the_path

    def calculate_cost(self, path):
        if len(path) == 0:
            return 0
        cost = 0
        for i in range(0, len(path) - 1):
            cost += int(self.Graph[path[i]][path[i + 1]])
        return cost

    #Plot Path
    def plot_path(self, path):
        superlist = {}
        list = [self.source]
        for step in path:
            for marker in self.Markers:
                if int(step) == int(marker["id"]):
                    # print marker["title"]
                    list.append(marker)

        superlist['markers'] = list
        list.append(self.destination)
        return superlist

    def haversine(self, lon1, lat1, lon2, lat2):
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km

    def findnearestmarker(self, lng, lat):
        dist = int(10e10)
        response = ""
        temp = {}
        temp["title"] = "temp"
        temp["lat"] = lat
        temp["long"] = lng
        for marker in self.Markers:
            lon = float(marker["long"])
            la = float(marker["lat"])
            d = self.haversine(lng, lat, lon, la)
            if d < 2:
                newd = self.getdistance(self.geturl(temp, marker))
                if newd < dist:
                    dist = newd
                    response = str(marker["title"].split("-")[0]).strip()
        return response

        # Format URL to Send to API
    def geturl(self, src, dest):
        marker1 = src
        marker2 = dest
        url = "https://maps.googleapis.com/maps/api/directions/json?origin=%.6f,%.6f&destination=%.6f,%.6f&key=%s" % (
            float(marker1["long"]), float(marker1["lat"]), float(marker2["long"]), float(marker2["lat"]), self.key)
        return url

    # Get API Response From Google
    def getdistance(self, url):
        try:
            result = json.load(urllib2.urlopen(url))
        except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code)
            return
        except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason)
            return
        except Exception:
            print "Exception Occured"
            return
        else:
            # time.sleep(.4)
            if len(result["routes"]) > 0:
                if len(result["routes"][0]["legs"]) > 0:
                    driving_time = result["routes"][0]["legs"][0]["duration"]["value"]
                else:
                    print "Couldn't find distance"
                    driving_time = int(1e5)
            else:
                print "Couldn't find distance"
                driving_time = int(1e5)
        return driving_time

# transit = Transit()
# print transit.Markers[0]
#
# # Get Info from float
# src1 = float(33.902810)
# src2 = float(35.481494)
# dest1 = float(33.880652)
# dest2 = float(35.539945)
#
# # Format info into tuples
# source = (src1, src2)
# destination = (dest1, dest2)
#
# path = transot.findpath(source, destination)
#
# plotted_paths = transot.plot_path(path)
# json_path = json.dumps(plotted_paths)
# pass