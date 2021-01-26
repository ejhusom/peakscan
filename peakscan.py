#!/usr/bin/env python
# -*- coding: utf-8 -*-
#==========================================================================
# Program by Erik Johannes B. L. G. Husom on 2018-12-22 for Python 3.8
# Description: Scanning workfout
#
# Accepted file formats:
# - .json
#
# USAGE:
# $ python3 peakscan.py
#==========================================================================

# IMPORT STATEMENTS
import numpy as np
import sys, os, time, io, json
import matplotlib.pyplot as plt
from xml.dom import minidom

from TrainingAnalyzer import TrainingAnalyzer

class Peakscan():

    def __init__(self, lat, lon, filepath):

        self.lat = lat
        self.lon = lon
        self.filepath = filepath
        self.tolerance = 1e-3
        self.counter = 0

        for entry in os.listdir(self.filepath):
            
            f = self.filepath + "/" + entry
            self.file = entry

            filename, ext = os.path.splitext(f)
            # print(entry.name)

            # Read json-file
            if (ext=='.json'):
                try:
                    data = json.load(io.open(f, 'r', encoding='utf-8-sig'))
                except UnicodeDecodeError:
                    continue
                # Read data samples
                try:
                    numberOfSamples = len(data["RIDE"]["SAMPLES"])
                except KeyError:
                    continue

                seconds = []
                heartrate = []
                kph = []
                elevation = []
                latitude = []
                longitude = []

                try:
                    first_lat = data["RIDE"]["SAMPLES"][0]["LAT"]
                    first_lon = data["RIDE"]["SAMPLES"][0]["LON"]

                    if abs(self.lat - first_lat) > 1 and abs(self.lon -
                            first_lon) > 1:
                        continue

                except KeyError:
                    continue


                for i in range(numberOfSamples):
                    latitude.append(data["RIDE"]["SAMPLES"][i]["LAT"])
                    longitude.append(data["RIDE"]["SAMPLES"][i]["LON"])

            elif (ext == ".gpx"):

                with open(f, "r") as f:
                    data = f
                    xmldoc = minidom.parse(data)

                track = xmldoc.getElementsByTagName('trkpt')
                elevation_xml = xmldoc.getElementsByTagName('ele')
                datetime_xml = xmldoc.getElementsByTagName('time')
                sample_count = len(track)

                longitude = []
                latitude = []
                elevation = []
                seconds = []
                for s in range(sample_count):
                    lon, lat = track[s].attributes['lon'].value,track[s].attributes['lat'].value
                    longitude.append(float(lon))
                    latitude.append(float(lat))

            else:
                print("Wrong file format. Only .json supported")
                continue

            self.latitude = np.array(latitude)
            self.longitude = np.array(longitude)

            found = self.peakscan()

            # if found:
            #     workout = TrainingAnalyzer(f)
            #     workout.plot_map_mpl()

        print("Count:", self.counter)

    def peakscan(self):

        for lat, lon in zip(self.latitude, self.longitude):

            if abs(self.lat - lat) < self.tolerance:
                if abs(self.lon - lon) < self.tolerance:
                    print("Peak visit registered:", self.file)
                    self.counter += 1
                    return True

        return False




if __name__ == '__main__':
    try:
        lat = float(sys.argv[1])
        lon = float(sys.argv[2])
        files = sys.argv[3]
    except IndexError:
        print('Give name of workout file as command line argument.')
        sys.exit(1)

    workout = Peakscan(lat, lon, files)

