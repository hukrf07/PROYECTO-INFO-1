#Step 1
class Airport:
    def __init__(self, code, lat, lon):
        self.code = str(code)
        self.lat = float(lat)
        self.lon = float(lon)
        self.schengen = False
def IsSchengenAirport(code):
    if not code:
        return False
    prefixes = [
        'LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
        'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES',
        'LS'
    ]
    inicio =  code[0:2]
    if inicio in prefixes:
        return True
    else:
        return False
def SetSchengen(airport):
    resultado=IsSchengenAirport(airport.code)
    airport.schengen=resultado
def PrintAirport(airport):
    print("Airpott code: ", airport.code)
    print("Coordinates", airport.lat, airport.lon)
    print("Is Schengen?: ", airport.schengen)

#Step 2
airport1=Airport("LEBL",41.297445, 2.0832941)
SetSchengen(airport1)
PrintAirport(airport1)
"LEBL"
airport2=Airport("KJFK", 40.641, -73.778)
SetSchengen(airport2)
PrintAirport(airport2)

#Step 3
def ConvertToDecimal(coord_str):
    direction = coord_str[0]
    if len(coord_str) == 8:
        degrees = float(coord_str[1:4])
        minutes = float(coord_str[4:6])
        seconds = float(coord_str[6:8])
    else:
        degrees = float(coord_str[1:3])
        minutes = float(coord_str[3:5])
        seconds = float(coord_str[5:7])

    decimal = degrees + (minutes / 60) + (seconds / 3600)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal
def LoadAirports(filename):
    airports = []
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()[1:]
            for line in lines:
                parts = line.split()
                if len(parts) >= 3:
                    nuevo = Airport(parts[0], ConvertToDecimal(parts[1]), ConvertToDecimal(parts[2]))
                    airports.append(nuevo)
    except FileNotFoundError:
        return []
    return airports
def SaveSchengenAirports(airports, filename):
    if not airports:
        return -1
    schengen_list = [a for a in airports if a.schengen]
    if not schengen_list:
        return -1
    with open(filename, 'w') as f:
        f.write("CODE LAT LON\n")
        for a in airports:
            if a.schengen:
                f.write(f"{a.code} {a.lat} {a.lon}\n")
    return 0
def AddAirport(airports, airport):
    for a in airports:
        if a.code == airport.code:
            return
    airports.append(airport)
def RemoveAirport(airports, code):
    for i in range(len(airports)):
        if airports[i].code == code:
            airports.pop(i)
            return 0
    return -1

#Step 5
import matplotlib.pyplot as plt
def PlotSchengenDistribution(airports):
    si = 0
    no = 0
    for a in airports:
        if a.schengen:
            si += 1
        else:
            no += 1

    categorias = ['Schengen', 'No Schengen']
    valores = [si, no]

    plt.figure(figsize=(6, 4))
    barras = plt.bar(categorias, valores, color=['black', 'yellow'])
    plt.bar_label(barras)
    plt.title("Total de Aeropuertos por Zona")
    plt.ylabel("Cantidad")
    plt.show()
