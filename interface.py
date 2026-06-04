import tkinter as tk
from tkinter import filedialog, messagebox
from tkintermapview import TkinterMapView
import matplotlib.patches as patches
from Airport import *
from aircraft import *
from LEBL import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
airports = []
aircrafts = []
departures = []
movements = []
ventana_aerolineas = None
# =========================
# VENTANA PRINCIPAL
# =========================

root = tk.Tk()
root.configure(bg="#DDEEFF")
root.title("Dashboard Aeropuerto LEBL")
COLOR_AEROPUERTOS = "#5DADE2"   # azul claro
COLOR_VUELOS      = "#3498DB"   # azul medio
COLOR_TERMINALES  = "#2874A6"   # azul oscuro
COLOR_V4          = "#1F618D"   # azul muy oscuro
COLOR_TEXTO       = "white"
root.geometry("1600x900")

bcn = LoadAirportStructure("VERSION 2/Terminals.txt")
print(bcn)
airlines_selected=[]
botones_visibles = False
grafico_horas_visible = False
grafico_tipo_visible = False
mostrar_todos_visible = False
grafico_ocupacion_visible = False
fig = None
ax = None
canvas = None
def limpiar_panel(panel):
    for widget in panel.winfo_children():
        widget.destroy()

def limpiar_panel(panel):
    for widget in panel.winfo_children():
        widget.destroy()

def mostrar_grafico(fig):
    global canvas
    limpiar_panel(frame_graficos)

    canvas = FigureCanvasTkAgg(
        fig,
        master=frame_graficos
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )

import os

def mostrar_texto(contenido):

    limpiar_panel(frame_texto)

    scroll = tk.Scrollbar(frame_texto)

    scroll.pack(
        side="right",
        fill="y"
    )

    txt = tk.Text(
        frame_texto,
        yscrollcommand=scroll.set
    )

    txt.pack(
        fill="both",
        expand=True
    )

    scroll.config(
        command=txt.yview
    )

    txt.insert(
        tk.END,
        contenido
    )


def cargar_aeropuertos():
    global airports
    ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if ruta:
        airports = LoadAirports(ruta)
        for a in airports:
            SetSchengen(a)
        messagebox.showinfo("Info", f"Cargados: {len(airports)}")

def nuevo_aeropuerto():

    ventana = tk.Toplevel(root)

    ventana.title("Nuevo aeropuerto")
    ventana.geometry("300x200")

    tk.Label(
        ventana,
        text="Código ICAO"
    ).pack(pady=5)

    entry_codigo = tk.Entry(ventana)
    entry_codigo.pack()

    tk.Label(
        ventana,
        text="Latitud"
    ).pack(pady=5)

    entry_lat = tk.Entry(ventana)
    entry_lat.pack()

    tk.Label(
        ventana,
        text="Longitud"
    ).pack(pady=5)

    entry_lon = tk.Entry(ventana)
    entry_lon.pack()

    def guardar():

        try:

            codigo = entry_codigo.get().strip().upper()

            lat = float(entry_lat.get())

            lon = float(entry_lon.get())

            if len(codigo) != 4:

                messagebox.showerror(
                    "Error",
                    "Código ICAO inválido"
                )
                return

            aeropuerto = Airport(
                codigo,
                lat,
                lon
            )

            SetSchengen(aeropuerto)

            AddAirport(
                airports,
                aeropuerto
            )

            actualizar_contador()

            messagebox.showinfo(
                "Info",
                f"Aeropuerto {codigo} añadido"
            )

            ventana.destroy()

        except ValueError:

            messagebox.showerror(
                "Error",
                "Latitud y longitud deben ser numéricas"
            )

    def eliminar():

        codigo = entry_codigo_eliminar.get().strip().upper()

        if codigo == "":
            messagebox.showwarning(
                "Error",
                "Introduce un código ICAO"
            )
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar {codigo}?"
        )

        if not respuesta:
            return

        resultado = RemoveAirport(
            airports,
            codigo
        )

        if resultado == 0:

            actualizar_contador()

            messagebox.showinfo(
                "Info",
                f"{codigo} eliminado correctamente"
            )

            entry_codigo_eliminar.delete(
                0,
                tk.END
            )

        else:

            messagebox.showerror(
                "Error",
                f"No existe el aeropuerto {codigo}"
            )

    tk.Button(
        ventana,
        text="Guardar",
        command=guardar
    ).pack(pady=10)

    tk.Label(
        ventana,
        text="-------------------------"
    ).pack(pady=5)

    tk.Label(
        ventana,
        text="Eliminar aeropuerto"
    ).pack()

    entry_codigo_eliminar = tk.Entry(
        ventana
    )

    entry_codigo_eliminar.pack()

    tk.Button(
        ventana,
        text="Eliminar",
        bg="#C0392B",
        fg="white",
        command=eliminar
    ).pack(pady=5)

def mostrar_todos():
    contenido = "CODE   |      LAT |      LON\n"
    contenido += "-" * 35 + "\n"

    for a in airports:

        contenido += (
            f"{a.code:<6} | "
            f"{a.lat:>8.3f} | "
            f"{a.lon:>8.3f}\n"
        )

    mostrar_texto(contenido)
def mostrar_schengen():
    contenido = "CODE   |      LAT |      LON\n"
    contenido += "-" * 35 + "\n"

    for a in airports:

        if a.schengen:

            contenido += (
                f"{a.code:<6} | "
                f"{a.lat:>8.3f} | "
                f"{a.lon:>8.3f}\n"
            )

    mostrar_texto(contenido)
def mostrar_no_schengen():
    contenido = "CODE   |      LAT |      LON\n"
    contenido += "-" * 35 + "\n"

    for a in airports:

        if not a.schengen:

            contenido += (
                f"{a.code:<6} | "
                f"{a.lat:>8.3f} | "
                f"{a.lon:>8.3f}\n"
            )

    mostrar_texto(contenido)

def mapa_aeropuertos():

    if not airports:
        messagebox.showwarning(
            "Error",
            "Carga aeropuertos primero"
        )
        return

    limpiar_panel(frame_graficos)

    mapa = TkinterMapView(
        frame_graficos,
        corner_radius=0
    )

    mapa.pack(
        fill="both",
        expand=True
    )

    mapa.set_position(
        41.297,
        2.083
    )

    mapa.set_zoom(4)

    for a in airports:

        color = "#1E88E5" if a.schengen else "#FF9800"

        mapa.set_marker(
            a.lat,
            a.lon,
            text=a.code,
            marker_color_circle=color,
            marker_color_outside=color
        )

def cargar_vuelos():
    def cargar_vuelos():
        global aircrafts
        # Permite modificar una variable definida fuera de la función.
        ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if ruta:
            aircrafts = LoadArrivals(ruta)
            messagebox.showinfo("Info",f"Vuelos cargados: {len(aircrafts)}")
    global aircrafts
    if not airports:
        messagebox.showwarning("Error", "Carga aeropuertos primero")
        return
    ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if ruta:
        aircrafts = LoadArrivals(ruta, airports)
        messagebox.showinfo("Info", f"Vuelos cargados: {len(aircrafts)}")

def cargar_departures():

    global departures

    ruta = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt")]
    )

    if ruta:

        departures = LoadDepartures(ruta)

        messagebox.showinfo(
            "Info",
            f"Departures cargados: {len(departures)}"
        )

def merge_movements():

    global movements

    movements = MergeMovements(
        aircrafts,
        departures
    )

    messagebox.showinfo(
        "Info",
        f"Movimientos unidos: {len(movements)}"
    )

def plot_day():

    global grafico_ocupacion_visible

    if grafico_ocupacion_visible:

        limpiar_panel(frame_graficos)

        grafico_ocupacion_visible = False

        return

    fig = PlotDayOccupancy(
        bcn,
        movements
    )

    mostrar_grafico(fig)

    grafico_ocupacion_visible = True

def grafico_horas():

    if not aircrafts:
        messagebox.showwarning(
            "Error",
            "Carga vuelos primero"
        )
        return

    fig = PlotArrivals(aircrafts)

    mostrar_grafico(fig)

def grafico_aerolineas():

    if not aircrafts:
        messagebox.showwarning(
            "Error",
            "Carga vuelos primero"
        )
        return

    fig = PlotAirlines(aircrafts)

    mostrar_grafico(fig)

def grafico_tipo():

    if not airports:
        messagebox.showwarning(
            "Error",
            "Carga aeropuertos primero"
        )
        return

    schengen = sum(1 for a in airports if a.schengen)
    # Cuenta cuántos aeropuertos son Schengen.
    no_schengen = len(airports) - schengen

    fig, ax = plt.subplots()

    barras = ax.bar(
        ["Schengen", "No Schengen"],
        [schengen, no_schengen],
        color=["#2196F3", "#FF9800"]
    )

    ax.bar_label(barras)

    ax.set_title("Schengen vs No Schengen")
    ax.set_ylabel("Número de aeropuertos")
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    mostrar_grafico(fig)

    mostrar_grafico(fig)
def vuelos_largos():
    vuelos = LongDistanceArrivals(aircrafts)
    texto = "Vuelos >2000 km:\n\n"
    for v in vuelos[:30]:
        texto += f"{v.id} - {v.origin}\n"
    mostrar_texto(texto)

def mapa_vuelos():

    if not aircrafts:
        messagebox.showwarning(
            "Error",
            "Carga vuelos primero"
        )
        return

    limpiar_panel(frame_graficos)
    mapa = TkinterMapView(
        frame_graficos,
        corner_radius=0
    )

    mapa.pack(
        fill="both",
        expand=True
    )

    mapa.set_position(
        41.297,
        2.083
    )

    mapa.set_zoom(4)

    airports_dict = {
        a.code: a
        for a in airports
    }

    lebl_lat = 41.297
    lebl_lon = 2.083

    mapa.set_marker(
        lebl_lat,
        lebl_lon,
        text="LEBL",
        marker_color_circle="black",
        marker_color_outside="black"
    )
    vuelos_largos_set = {
        v.id
        for v in LongDistanceArrivals(aircrafts)
    }

    aeropuertos_mostrados = set()

    for vuelo in aircrafts:

        if vuelo.origin not in airports_dict:
            continue

        origen = airports_dict[vuelo.origin]

        # Crear marcador una sola vez por aeropuerto
        if origen.code not in aeropuertos_mostrados:

            if vuelo.id in vuelos_largos_set:

                mapa.set_marker(
                    origen.lat,
                    origen.lon,
                    text=origen.code,
                    marker_color_circle="red",
                    marker_color_outside="red"
                )

            else:

                mapa.set_marker(
                    origen.lat,
                    origen.lon,
                    text=origen.code,
                    marker_color_circle="blue",
                    marker_color_outside="blue"
                )

            aeropuertos_mostrados.add(origen.code)

        # Color y grosor de la ruta
        if vuelo.id in vuelos_largos_set:

            color = "red"
            ancho = 1

        else:

            color = "blue"
            ancho = 1

        mapa.set_path(
            [
                (origen.lat, origen.lon),
                (lebl_lat, lebl_lon)
            ],
            color=color,
            width=ancho
        )
def actualizar_grafico_aerolineas():

    if not airlines_selected:
        limpiar_panel(frame_graficos)
        return

    nombres = []
    valores = []

    for airline in airlines_selected:

        contador = 0

        for a in aircrafts:

            if a.airline == airline:
                contador += 1

        nombres.append(airline)
        valores.append(contador)

    fig, ax = plt.subplots()

    ax.bar(nombres, valores)

    ax.set_title("Aerolíneas seleccionadas")
    ax.set_xlabel("Aerolínea")
    ax.set_ylabel("Número de vuelos")

    mostrar_grafico(fig)

def seleccionar_todas():
    global airlines_selected
    airlines_selected = sorted(set(a.airline for a in aircrafts))
    actualizar_grafico_aerolineas()

def quitar_todas():
    global airlines_selected
    airlines_selected = []
    actualizar_grafico_aerolineas()



def grafico_aerolinea_individual(airline):
    cantidad = 0
    for a in aircrafts:
        if a.airline == airline:
            cantidad += 1
    plt.figure(figsize=(5,5))
    plt.bar([airline], [cantidad])
    plt.xlabel("Aerolínea")
    plt.ylabel("Número de vuelos")
    plt.title(f"Vuelos de {airline}")
    plt.show()

def seleccionar_aerolinea(airline):

    global airlines_selected
    global ventana_aerolineas

    if airline in airlines_selected:
        airlines_selected.remove(airline)
    else:
        airlines_selected.append(airline)

    actualizar_grafico_aerolineas()

    if ventana_aerolineas and ventana_aerolineas.winfo_exists():

        ventana_aerolineas.after(
            50,
            lambda: ventana_aerolineas.lift()
        )

def mostrar_botones_aerolineas():

    global ventana_aerolineas

    if ventana_aerolineas is not None and ventana_aerolineas.winfo_exists():
        ventana_aerolineas.lift()
        ventana_aerolineas.focus_force()
        return

    ventana_aerolineas = tk.Toplevel(root)

    ventana_aerolineas.title("Seleccionar aerolíneas")

    # Mantenerla delante
    ventana_aerolineas.attributes("-topmost", True)

    frame = tk.Frame(ventana_aerolineas)
    frame.pack(padx=10, pady=10)

    frame_botones = tk.Frame(ventana_aerolineas)
    frame_botones.pack(pady=5)

    tk.Button(
        frame_botones,
        text="Seleccionar todas",
        command=seleccionar_todas
    ).pack(side="left", padx=5)

    tk.Button(
        frame_botones,
        text="Quitar todas",
        command=quitar_todas
    ).pack(side="left", padx=5)

    airlines = sorted(set(a.airline for a in aircrafts))

    fila = 0
    columna = 0

    for airline in airlines:

        btn = tk.Button(
            frame,
            text=airline,
            width=5,
            command=lambda a=airline: seleccionar_aerolinea(a)
        )

        btn.grid(
            row=fila,
            column=columna,
            padx=2,
            pady=2
        )

        columna += 1

        if columna > 5:
            columna = 0
            fila += 1

def cargar_terminales():
    global bcn
    ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if ruta:
        bcn = LoadAirportStructure(ruta)
        if bcn is None:
            messagebox.showerror("Error","No se pudo cargar terminales")
        else:
            messagebox.showinfo("Info","Terminales cargadas correctamente")

def asignar_gates():
    global bcn
    texto = ""
    for a in aircrafts:
        gate = AssignGate(bcn, a)
        if gate == -1:
            texto += f"{a.id} -> SIN GATE\n"
        else:
            texto += ( f"{a.id} | "f"{a.airline} | "f"{gate}\n")
    mostrar_texto(texto)

def mostrar_ocupacion():
    global bcn
    if bcn is None:
        messagebox.showwarning("Error","Carga terminales primero")
        return
    info = GateOccupancy(bcn)
    texto = ""
    for linea in info:
        texto += linea + "\n"
    mostrar_texto(texto)


frame_principal = tk.Frame(root)
frame_principal.pack(fill="both", expand=True)

# CONTENEDOR IZQUIERDO
menu_container = tk.Frame(
    frame_principal,
    width=320,
    bg="#EBF5FB"
)

menu_container.pack(
    side="left",
    fill="y"
)

# CANVAS
canvas_menu = tk.Canvas(
    menu_container,
    bg="#EBF5FB",
    highlightthickness=0
)

# SCROLLBAR
scrollbar_menu = tk.Scrollbar(
    menu_container,
    orient="vertical",
    command=canvas_menu.yview
)

# FRAME REAL DEL MENÚ
frame_menu = tk.Frame(
    canvas_menu,
    bg="#EBF5FB"
)

# CONFIGURAR SCROLL
frame_menu.bind(
    "<Configure>",
    lambda e: canvas_menu.configure(
        scrollregion=canvas_menu.bbox("all")
    )
)

canvas_window = canvas_menu.create_window(
    (0, 0),
    window=frame_menu,
    anchor="nw"
)

def buscar_aeronave():

    global bcn

    identificador = entry_aeronave.get().strip()

    if identificador == "":
        messagebox.showwarning(
            "Error",
            "Introduce un identificador"
        )
        return

    gate_encontrado = None

    for terminal in bcn.terminals:

        for area in terminal.boarding_areas:

            for gate in area.gates:

                if gate.aircraft == identificador:

                    gate_encontrado = gate.name
                    break

    if gate_encontrado:

        label_resultado.config(
            text=f"Aeronave {identificador} en gate {gate_encontrado}"
        )

    else:

        label_resultado.config(
            text=f"Aeronave {identificador} no está en ningún gate"
        )

def plot_ocupacion_terminales():
    if bcn is None:
        return

    if len(movements) == 0:
        return

    if bcn is None:
        messagebox.showwarning(
            "Error",
            "Carga terminales primero"
        )
        return

    if len(movements) == 0:
        messagebox.showwarning(
            "Error",
            "Haz Merge Movements primero"
        )
        return

    hora = hora_var.get()

    estado = AirportStateAtHour(
        bcn,
        movements,
        hora
    )

    nombre_terminal = terminal_var.get()

    terminal = None

    for t in estado.terminals:

        if t.name == nombre_terminal:
            terminal = t
            break

    if terminal is None:
        return

    fig, ax = plt.subplots(
        figsize=(16,10)
    )

    ax.axis("off")

    fig.patch.set_facecolor("#f5f5f5")
    ax.set_facecolor("#f5f5f5")

    numero_areas = len(
        terminal.boarding_areas
    )

    separacion = 10

    x_areas = []

    for i in range(numero_areas):

        x_areas.append(
            10 + i * separacion
        )

    barra_inicio = x_areas[0] - 4
    barra_fin = x_areas[-1] + 4
    centro = (barra_inicio + barra_fin) / 2

    Y_SUPERIOR = 42

    # Barra principal
    ax.plot(
        [barra_inicio, barra_fin],
        [42, 42],  # antes era 30
        linewidth=12,
        color="#005080"
    )

    # Hora
    ax.text(
        centro,
        49,  # antes 46
        f"Hora {hora}:00",
        fontsize=20,
        fontweight="bold",
        ha="center"
    )

    # Nombre terminal
    ax.text(
        centro,
        46,  # antes 44
        terminal.name,
        fontsize=34,
        fontweight="bold",
        ha="center",
        color="#005080"
    )
    ax.set_ylim(-5, 50)
    for idx, area in enumerate(
        terminal.boarding_areas
    ):

        x = x_areas[idx]
        num_gates = len(area.gates)

        y_final = Y_SUPERIOR - 2 - (num_gates * 0.8)

        ax.plot(
            [x, x],
            [y_final, Y_SUPERIOR],
            linewidth=8,
            color="#005080"
        )

        y = Y_SUPERIOR - 2
        ax.text(
            x,
            Y_SUPERIOR +1.5,
            terminal.name + area.name,
            fontsize=16,
            fontweight="bold",
            ha="center"
        )

        y = Y_SUPERIOR - 2

        for gate in area.gates:

            ax.plot(
                [x-2,x],
                [y,y],
                linewidth=3,
                color="#005080"
            )

            ocupado = (
                gate.aircraft != ""
            )

            color = (
                "#ff0000"
                if ocupado
                else "#00aa00"
            )

            rect = patches.Rectangle((x-2.8, y-0.25),0.8,0.5,facecolor=color,edgecolor="black")
            ax.add_patch(rect)
            if ocupado:
                ax.text(x-3.2,y,gate.aircraft,fontsize=9,ha="right",va="center")
            y -= 0.8
    mostrar_grafico(fig)

def resize_frame(event):canvas_menu.itemconfig(canvas_window, width=event.width)

canvas_menu.bind("<Configure>", resize_frame)
canvas_menu.configure(yscrollcommand=scrollbar_menu.set)

# MOSTRAR
canvas_menu.pack(side="left",fill="both",expand=True)

scrollbar_menu.pack(side="right",fill="y")
frame_contenido = tk.Frame(frame_principal, bg="#F8FBFD")
frame_contenido.pack(side="left", fill="both",expand=True)
frame_graficos = tk.Frame(frame_contenido,bg="#F8FBFD")
fig, ax = plt.subplots(figsize=(10,9))

canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
canvas.get_tk_widget().pack(fill="both",expand=True)

frame_graficos.pack(side="right",fill="both",expand=True)
frame_texto = tk.Frame(frame_contenido,bg="#F4F9FC",width=400)
frame_texto.pack(side="left",fill="both")
frame_texto.pack_propagate(False)
def boton(texto, comando, color):
    btn = tk.Button(frame_menu,text=texto,command=comando,height=2,font=('Arial', 10),bg=color,fg=COLOR_TEXTO,activebackground=color,activeforeground="white")
    btn.pack(fill='x',padx=5,pady=3)
    return btn

tk.Label(frame_menu,text="--- AEROPUERTOS ---",bg="#EBF5FB",fg="#1F618D",font=("Arial", 10, "bold")).pack(pady=5)
boton("Cargar aeropuertos", cargar_aeropuertos, COLOR_AEROPUERTOS)
boton("Gestionar aeropuertos",nuevo_aeropuerto,COLOR_AEROPUERTOS)
boton("Mostrar todos", mostrar_todos, COLOR_AEROPUERTOS)
boton("Mostrar Schengen", mostrar_schengen, COLOR_AEROPUERTOS)
boton("Mostrar No Schengen", mostrar_no_schengen, COLOR_AEROPUERTOS)
boton("Schengen vs No", grafico_tipo, COLOR_AEROPUERTOS)
boton("Mapa aeropuertos", mapa_aeropuertos, COLOR_AEROPUERTOS)

tk.Label(frame_menu,text="--- VUELOS ---",bg="#EBF5FB",fg="#1F618D",font=("Arial", 10, "bold")).pack(pady=5)
boton("Cargar vuelos", cargar_vuelos, COLOR_VUELOS)
boton("Gráfico llegadas", grafico_horas, COLOR_VUELOS)
boton("Vuelos >2000 km", vuelos_largos, COLOR_VUELOS)
boton("Mostrar aerolíneas", mostrar_botones_aerolineas, COLOR_VUELOS)
boton("Mapa vuelos", mapa_vuelos, COLOR_VUELOS)

tk.Label(frame_menu,text="--- TERMINALES ---",bg="#EBF5FB",fg="#1F618D",font=("Arial", 10, "bold")).pack(pady=5)
boton("Cargar terminales", cargar_terminales, COLOR_TERMINALES)
boton("Asignar Gates", asignar_gates, COLOR_TERMINALES)
boton("Mostrar ocupacion", mostrar_ocupacion, COLOR_TERMINALES)
boton("Plot ocupación",plot_ocupacion_terminales,COLOR_TERMINALES)
selector_frame = tk.Frame(frame_menu)
selector_frame.pack(pady=5)
# ----- HORA -----
hora_frame = tk.Frame(selector_frame)
hora_frame.pack(side="left", padx=10)
tk.Label(hora_frame,text="Hora").pack()
hora_var = tk.IntVar(value=12)
tk.Scale(hora_frame,from_=0,to=23,orient="horizontal",variable=hora_var,length=150,command=lambda v: plot_ocupacion_terminales()).pack()
# ----- TERMINAL -----
terminal_frame = tk.Frame(selector_frame)
terminal_frame.pack(side="left", padx=10)
tk.Label(terminal_frame,text="Terminal").pack()
terminal_var = tk.StringVar(value="T1")
tk.OptionMenu(terminal_frame,terminal_var,"T1","T2").pack()
frame_airlines = tk.Frame(frame_menu,bg="#EAEAEA")
frame_airlines.pack(pady=1)

tk.Label(frame_menu,text="--- VUELOS(V4) ---",bg="#EBF5FB",fg="#1F618D",font=("Arial", 10, "bold")).pack(pady=5)
boton("Cargar departures", cargar_departures, COLOR_V4)
boton("Merge movements", merge_movements, COLOR_V4)
boton("Plot ocupacion dia", plot_day, COLOR_V4)

tk.Label(frame_menu,text="--- BUSCAR AERONAVE ---",bg="#EBF5FB",fg="#1F618D",font=("Arial", 10, "bold")).pack(pady=5)
entry_aeronave = tk.Entry(frame_menu,width=20)
entry_aeronave.pack(padx=5,pady=2,fill="x")
tk.Button(frame_menu,text="Buscar Gate",command=buscar_aeronave,bg="#117A65",fg="white").pack(fill="x", padx=5,pady=3)
label_resultado = tk.Label(frame_menu,text="",bg="#EBF5FB",wraplength=250)
label_resultado.pack(padx=5,pady=5)

root.mainloop()
