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

def GateOccupancy(bcn):

    info = []

    for terminal in bcn.terminals:

        for area in terminal.boarding_areas:

            for gate in area.gates:

                # estado puerta
                if gate.aircraft == "":

                    status = "LIBRE"

                else:

                    status = (
                        f"OCUPADO POR: {gate.aircraft}"
                    )

                linea = (
                    f"{terminal.name} | "
                    f"Area {area.name} | "
                    f"{gate.name} | "
                    f"{status}"
                )

                info.append(linea)

    return info

if __name__ == "__main__":

    bcn = LoadAirportStructure(
        "VERSION 2/Terminals.txt"
    )

    print("Aeropuerto:", bcn.code)

    info = GateOccupancy(bcn)

    for x in info:

        print(x)