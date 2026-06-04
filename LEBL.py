import matplotlib.pyplot as plt
class Gate:

    def __init__(self, name):

        self.name = name
        self.aircraft = ""

class BoardingArea:

    def __init__(self, name, schengen):

        self.name = name
        self.schengen = schengen
        self.gates = []


class Terminal:

    def __init__(self, name):

        self.name = name
        self.boarding_areas = []
        self.airlines = []


class BarcelonaAP:

    def __init__(self, code):

        self.code = code
        self.terminals = []

def SetGates(area, init_gate, end_gate, prefix):

    if end_gate <= init_gate:
        return -1

    area.gates = []

    for i in range(init_gate, end_gate + 1):

        gate_name = prefix + str(i)

        gate = Gate(gate_name)

        area.gates.append(gate)

    return 0

def LoadAirlines(terminal, t_name):

    filename = t_name + "_Airlines.txt"

    try:

        terminal.airlines = []

        with open(filename, "r", encoding="utf-8") as f:

            for line in f:

                parts = line.strip().split()

                if len(parts) > 0:

                    icao = parts[-1]

                    terminal.airlines.append(icao)

        return 0

    except:

        return -1

def IsAirlineInTerminal(terminal, name):

    if name == "":
        return False

    if name in terminal.airlines:
        # Comprueba si una aerolínea pertenece a una terminal.
        return True

    return False

def SearchTerminal(bcn, name):

    for terminal in bcn.terminals:

        if IsAirlineInTerminal(terminal, name):

            return terminal.name

    return ""

def LoadAirportStructure(filename):

    try:

        with open(filename, "r", encoding="utf-8") as f:

            lines = f.readlines()

        airport_code = lines[0].split()[0]

        bcn = BarcelonaAP(airport_code)

        current_terminal = None

        for line in lines[1:]:

            parts = line.strip().split()

            if len(parts) == 0:
                continue

            # TERMINAL
            if parts[0] == "Terminal":

                terminal_name = parts[1]

                current_terminal = Terminal(terminal_name)

                LoadAirlines(current_terminal, terminal_name)

                bcn.terminals.append(current_terminal)

            # BOARDING AREA
            elif parts[0] == "Area":

                area_name = parts[1]

                schengen_text = parts[2]

                schengen = schengen_text == "Schengen"

                try:

                    init_gate = int(parts[-3])

                    end_gate = int(parts[-1])

                except:

                    continue

                area = BoardingArea(area_name, schengen)

                prefix = current_terminal.name + area_name + "G"

                SetGates(area, init_gate, end_gate, prefix)

                current_terminal.boarding_areas.append(area)

        return bcn


    except Exception as e:

        print("ERROR:", e)

        return None

def AssignGate(bcn, aircraft):

    terminal_name = SearchTerminal(
        bcn,
        aircraft.airline
    )

    # terminal automática
    if terminal_name == "":

        if aircraft.schengen:
            terminal_name = "T1"
        else:
            terminal_name = "T2"

    compatible_gates = []

    # buscar todas las puertas compatibles
    for terminal in bcn.terminals:

        if terminal.name == terminal_name:

            for area in terminal.boarding_areas:

                if area.schengen == aircraft.schengen:

                    for gate in area.gates:

                        compatible_gates.append(gate)
                        # Añade una puerta compatible a la lista.

    # si no hay gates
    if len(compatible_gates) == 0:

        return "SIN GATE"

    # buscar primero una libre
    for gate in compatible_gates:

        if gate.aircraft == "":

            gate.aircraft = aircraft.id

            return gate.name

    # si todas ocupadas -> reutilizar la primera
    gate = compatible_gates[0]

    gate.aircraft = aircraft.id

    return gate.name

def FreeGate(bcn, aircraft_id):

    for terminal in bcn.terminals:

        for area in terminal.boarding_areas:

            for gate in area.gates:

                if gate.aircraft == aircraft_id:

                    gate.aircraft = ""

                    return 0

    return -1

def AssignNightGates(bcn, aircrafts):

    if not aircrafts:
        return -1

    for aircraft in aircrafts:

        if aircraft.origin == "" and aircraft.departure != "":

            AssignGate(bcn, aircraft)

    return 0

def time_to_hour(time_str):

    try:
        return int(time_str.split(":")[0])
    # Extrae únicamente la parte de la hora.

    except:
        return -1

def AssignGatesAtTime(bcn, aircrafts, time):

    hour = time_to_hour(time)

    not_assigned = 0

    # LIBERAR PUERTAS (salidas)
    for aircraft in aircrafts:

        if hasattr(aircraft, "departure") and aircraft.departure != "":
            # Comprueba si el objeto tiene el atributo indicado.

            dep_hour = time_to_hour(aircraft.departure)

            if dep_hour == hour:
                # Libera la puerta cuando llega la hora de salida.

                FreeGate(bcn, aircraft.id)

    # ASIGNAR LLEGADAS
    for aircraft in aircrafts:

        arrival_time = ""

        if hasattr(aircraft, "arrival"):
            arrival_time = aircraft.arrival

        elif hasattr(aircraft, "arrival_time"):
            arrival_time = aircraft.arrival_time

        if arrival_time != "":

            arr_hour = time_to_hour(arrival_time)

            if arr_hour == hour:

                result = AssignGate(bcn, aircraft)

                if result == -1:
                    not_assigned += 1

    return not_assigned

def PlotDayOccupancy(bcn, aircrafts):

    hours = []
    occupied = []
    rejected = []

    for h in range(24):

        time = f"{h}:00"
        # Genera una hora tipo 15:00.

        rejected_count = AssignGatesAtTime(
            bcn,
            aircrafts,
            time
        )

        total = 0

        for terminal in bcn.terminals:

            for area in terminal.boarding_areas:

                for gate in area.gates:

                    if gate.aircraft != "":
                        total += 1

        hours.append(h)
        occupied.append(total)
        rejected.append(rejected_count)

    fig, ax = plt.subplots()

    ax.plot(hours, occupied, label="Occupied gates")
    ax.plot(hours, rejected, label="Rejected aircraft")

    ax.set_xlabel("Hour")
    ax.set_ylabel("Number")

    ax.legend()

    return fig

def GateOccupancy(bcn):
    info = []
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                # ESTADO PUERTA
                if gate.aircraft == "":
                    status = "LIBRE"
                else:
                    status = (f"OCUPADO POR: {gate.aircraft}")
                linea = (f"{terminal.name} | "f"Area {area.name} | "f"{gate.name} | "f"{status}")
                # Une varios textos en una única cadena.

                info.append(linea)
    return info

import copy

def AirportStateAtHour(bcn, aircrafts, hour):

    temp = copy.deepcopy(bcn)

    for h in range(hour + 1):

        AssignGatesAtTime(
            temp,
            aircrafts,
            f"{h}:00"
        )

    return temp

if __name__ == "__main__":
    bcn = LoadAirportStructure("VERSION 2/Terminals.txt")
    print("Aeropuerto:", bcn.code)
    info = GateOccupancy(bcn)
    for x in info:
        print(x)