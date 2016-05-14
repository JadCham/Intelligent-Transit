#!/usr/bin/bash

import urllib2
import json
import time

class network_data:

    def __init__(self):
        self.Graph = {}
        self.Markers = {}
        self.Routes = {}
        self.Crosses = {}
        self.key = "AIzaSyBfrpplBMipxHYSeoW7EPukhoWwho1KkEc"

    def getdata(self):

        # Fetch Markers nodes
        try:
            read = urllib2.urlopen("http://kebbe.blob.core.windows.net/transit/markers-lebanon-reduced.json")
        except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code)
            return
        except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason)
            return
        else:
            string = read.read()
            read.close()
            self.Markers = json.loads(string)["markers"]

        # Fetch routes
        try:
            read = urllib2.urlopen("http://kebbe.blob.core.windows.net/transit/routes.json")
        except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code)
            return
        except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason)
            return
        else:
            string = read.read()
            read.close()
            self.Routes = json.loads(string)["routes"]

        # Fetch crosses
        try:
            read = urllib2.urlopen("http://kebbe.blob.core.windows.net/transit/crosses.json")
        except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code)
            return
        except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason)
            return
        else:
            string = read.read()
            read.close()
            self.Crosses = json.loads(string)["crosses"]

    # Build the Graph using Google API
    def buildgraph(self):
        count = 0
        for i in range(len(self.Routes)):
            route_markers = self.Routes[i]["markers"]
            for j in range(0, len(route_markers) - 1):
                if not self.Graph.has_key(route_markers[j]):
                    self.Graph[route_markers[j]] = {}
                if not self.Graph.has_key(route_markers[j + 1]):
                    self.Graph[route_markers[j + 1]] = {}

                if route_markers[j + 1] not in self.Graph[route_markers[j]]:
                    url = self.geturl(route_markers[j], route_markers[j + 1])
                    distance = self.getdistance(url)
                    count += 1
                    print count
                    self.Graph[route_markers[j]][route_markers[j + 1]] = distance

                    if route_markers[j] not in self.Graph[route_markers[j + 1]]:
                        self.Graph[route_markers[j + 1]][route_markers[j]] = distance

        for i in range(len(self.Crosses)):
            cross_markers = self.Crosses[i]["markers"]
            for j in range(len(cross_markers)):
                cur_marker = cross_markers[j]
                for k in range(len(cross_markers)):
                    if cross_markers[k] != cur_marker:
                        self.Graph[cur_marker][cross_markers[k]] = self.Crosses[i]["cost"]

    # Format URL to Send to API
    def geturl(self, src, dest):
        marker1 = self.getmarkerinfo(src)
        marker2 = self.getmarkerinfo(dest)
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
            time.sleep(.4)
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

    def getmarkerinfo(self, marker):
        ret = {}
        for mar in self.Markers:
            if mar["id"] == marker:
                ret = mar
                break
        return ret

    def write_to_files(self):
        write = open("../../json/graph1.json", "w")
        json_string = json.dumps(self.Graph, separators=(",", ":"))
        write.write(json_string)
        write.close()

        write = open("../../json/markers1.json", "w")
        json_string = json.dumps(self.Markers, separators=(",", ":"))
        write.write(json_string)
        write.close()

        write = open("../../json/routes1.json", "w")
        json_string = json.dumps(self.Routes, separators=(",", ":"))
        write.write(json_string)
        write.close()

        write = open("../../json/crosses1.json", "w")
        json_string = json.dumps(self.Crosses, separators=(",", ":"))
        write.write(json_string)
        write.close()

data = network_data()

data.getdata()
data.buildgraph()
data.write_to_files()
pass