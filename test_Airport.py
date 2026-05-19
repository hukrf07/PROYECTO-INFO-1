#Step 2
from Airport import *
airport = Airport("LEBL", 41.297445, 2.0832941)
SetSchengen(airport)
PrintAirport(airport)

#Step 4
from Airport import *

lista = LoadAirports("airports.txt")

schengen = []
no_schengen = []

for aero in lista:
    SetSchengen(aero)
    PrintAirport(aero)

    if aero.schengen:
        schengen.append(aero)
    else:
        no_schengen.append(aero)

with open("resultado_todos.txt", "w", encoding="utf-8") as f:
    f.write("=== SCHENGEN ===\n")
    for a in schengen:
        f.write(f"{a.code} - {a.lat} - {a.lon}\n")

    f.write("\n=== NO SCHENGEN ===\n")
    for a in no_schengen:
        f.write(f"{a.code} - {a.lat} - {a.lon}\n")


#Step 5
import os
from Airport import LoadAirports, SetSchengen

def GenerateKML(airports, filename="airports_map.kml"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>

    <Style id="schengen">
        <IconStyle>
            <color>ffff0000</color> <!-- rojo -->
            <scale>1.2</scale>
            <Icon>
              <href>http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png</href>
            </Icon>
        </IconStyle>
    </Style>

    <Style id="no_schengen">
        <IconStyle>
            <color>ffff00ff</color> <!-- amarillo -->
            <scale>1.2</scale>
            <Icon>
               <href>http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png</href>
            </Icon>
        </IconStyle>
    </Style>
""")

        for a in airports:
            estilo = "#schengen" if a.schengen else "#no_schengen"

            f.write(f"""
    <Placemark>
        <name>{a.code}</name>
        <styleUrl>{estilo}</styleUrl>
        <Point>
            <coordinates>{a.lon},{a.lat},0</coordinates>
        </Point>
    </Placemark>
""")

        f.write("""
</Document>
</kml>
""")

    os.system(f"start {filename}")

if __name__ == "__main__":
    airports = LoadAirports("airports.txt")
    print("Aeropuertos cargados:", len(airports))
    for a in airports:
        SetSchengen(a)
    GenerateKML(airports)

