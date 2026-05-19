from Airport import LoadAirports, IsSchengenAirport
class Aircraft:
    def __init__(self, id, airline, origin, arrival_time):
        self.id = id
        self.airline = airline
        self.origin = origin
        self.arrival_time = arrival_time
def LoadArrivals(filename):
    aircrafts = []

    try:
        file = open(filename, "r")
        lines = file.readlines()
        file.close()

        for line in lines[1:]:
            parts = line.strip().split()

            if len(parts) != 4:
                continue

            id = parts[0]
            origin = parts[1]
            time = parts[2]
            airline = parts[3]

            aircraft = Aircraft(id, airline, origin, time)
            aircrafts.append(aircraft)

    except:
        return []

    return aircrafts

import matplotlib.pyplot as plt

class Aircraft:
    def __init__(self, id, origin, arrival_time, airline, schengen):
        self.id = id
        self.origin = origin
        self.arrival_time = arrival_time
        self.airline = airline
        self.schengen = schengen
        try:
            self.hour = int(arrival_time.split(":")[0])
        except:
            self.hour = 0


def LoadArrivals(filename, airports):
    aircrafts = []
    mapa_schengen = {a.code: a.schengen for a in airports}

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.replace(";", " ").replace(",", " ").split()

            if len(parts) < 4:
                continue

            id = parts[0]
            origin = parts[1]
            arrival_time = parts[2]
            airline = parts[3]
            schengen = mapa_schengen.get(origin, False)

            a = Aircraft(id, origin, arrival_time, airline, schengen)
            aircrafts.append(a)

    return aircrafts

def LongDistanceArrivals(aircrafts):
    return aircrafts[:50]

def MapFlights(aircrafts):
    filename = "flights.kml"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("<kml><Document>\n")

        for a in aircrafts:
            f.write(f"<Placemark><name>{a.id}</name></Placemark>\n")

        f.write("</Document></kml>")

def PlotArrivals(aircrafts):

    if len(aircrafts) == 0:
        return None

    hours = [0] * 24

    for a in aircrafts:
        try:
            h = int(a.arrival_time.split(":")[0])
            hours[h] += 1
        except:
            continue

    fig, ax = plt.subplots(figsize=(5,4))

    ax.bar(range(24), hours)

    ax.set_title("Llegadas por hora")

    return fig
def PlotAirlines(aircrafts):

    if len(aircrafts) == 0:
        return None

    airlines = {}

    for a in aircrafts:
        if a.airline in airlines:
            airlines[a.airline] += 1
        else:
            airlines[a.airline] = 1

    names = list(airlines.keys())
    values = list(airlines.values())

    fig, ax = plt.subplots(figsize=(5,4))

    ax.barh(names, values)

    ax.set_xlabel("Vuelos")
    ax.set_ylabel("Aerolínea")
    ax.set_title("Vuelos por aerolínea")

    return fig
def PlotAirportsType(airports):

    if len(airports) == 0:
        return None

    schengen = 0
    no_schengen = 0

    for a in airports:

        if a.schengen:
            schengen += 1
        else:
            no_schengen += 1

    fig, ax = plt.subplots(figsize=(5,4))

    ax.bar(
        ["Schengen", "No Schengen"],
        [schengen, no_schengen]
    )

    ax.set_title("Aeropuertos Schengen vs No Schengen")
    ax.set_ylabel("Número de aeropuertos")

    return fig
from Airport import LoadAirports

def distance(lat1, lon1, lat2, lon2):
    return ((lat1 - lat2)**2 + (lon1 - lon2)**2)**0.5 * 111


def MapFlights(aircrafts):

    print("GENERANDO MAPA...")

    airports = LoadAirports("VERSION 2/Airports.txt")

    bcn_lat = 41.297
    bcn_lon = 2.083

    file = open("flights.kml", "w")

    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    file.write('<Document>\n')

    for a in aircrafts:
        for ap in airports:

            if a.origin.strip()[-4:] == ap.code.strip():

                d = distance(ap.lat, ap.lon, bcn_lat, bcn_lon)

                file.write('<Placemark>\n')

                if d > 2000:
                    file.write('<Style><LineStyle><color>ff0000ff</color></LineStyle></Style>\n')  # rojo
                else:
                    file.write('<Style><LineStyle><color>ffff0000</color></LineStyle></Style>\n')  # azul

                file.write(f'<name>{ap.code} - LEBL</name>\n')
                file.write('<LineString>\n')
                file.write('<coordinates>\n')

                file.write(f"{ap.lon},{ap.lat}\n")
                file.write(f"{bcn_lon},{bcn_lat}\n")

                file.write('</coordinates>\n')
                file.write('</LineString>\n')
                file.write('</Placemark>\n')

    file.write('</Document>\n')
    file.write('</kml>\n')

    file.close()

import math


def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) * 111


from Airport import LoadAirports


def LongDistanceArrivals(aircrafts):
    result = []

    airports= LoadAirports("VERSION 2/Airports.txt")

    for a in aircrafts:
        for ap in airports:
            if a.origin.strip()[-4:] == ap.code.strip():
                d = distance(ap.lat, ap.lon, 41.297, 2.083)  # Barcelona

                if d > 2000:
                    result.append(a)

    return result

if __name__ == "__main__":

    airports = LoadAirports("VERSION 2/airports.txt")

    aircrafts = LoadArrivals("VERSION 2/Arrivals.txt", airports)
    print("Número de vuelos:", len(aircrafts))

    PlotArrivals(aircrafts)
    PlotAirlines(aircrafts)
    PlotFlightsType(aircrafts)

    SaveFlights(aircrafts, "output.txt")

    long_flights = LongDistanceArrivals(aircrafts)
    print("Vuelos largos:", len(long_flights))

    MapFlights(aircrafts)

