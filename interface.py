import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from collections import Counter
import os
import matplotlib.pyplot as plt
from collections import Counter
from Airport import LoadAirports, SetSchengen
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from aircraft import *
from LEBL import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

airports = []
aircrafts = []
bcn = LoadAirportStructure("VERSION 2/Terminals.txt")
print(bcn)
airlines_selected=[]
botones_visibles = False
grafico_horas_visible = False
grafico_tipo_visible = False
mostrar_todos_visible = False
fig = None
ax = None
canvas = None
def limpiar_panel(panel):

    for widget in panel.winfo_children():
        widget.destroy()

def limpiar_panel(panel):

    for widget in panel.winfo_children():
        widget.destroy()


def mostrar_grafico(fig, panel):

    limpiar_panel(panel)

    canvas = FigureCanvasTkAgg(fig, master=panel)

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )
def mostrar_texto(contenido):

    limpiar_panel(panel1)

    frame_texto = tk.Frame(panel1)

    frame_texto = tk.Frame(panel1)
    frame_texto.pack(fill="both", expand=True)

    scroll = tk.Scrollbar(frame_texto)
    scroll.pack(side="right", fill="y")
    global txt
    txt = tk.Text(frame_texto, yscrollcommand=scroll.set)
    txt.pack(fill="both", expand=True)

    scroll.config(command=txt.yview)

    txt.insert(tk.END, contenido)

def actualizar_contador():

    schengen = sum(1 for a in airports if a.schengen)
    no_schengen = len(airports) - schengen

    label_contador.config(
        text=f"Schengen: {schengen} | No Schengen: {no_schengen}"
    )

def cargar_aeropuertos():
    global airports

    ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    if ruta:
        airports = LoadAirports(ruta)

        for a in airports:
            SetSchengen(a)

        actualizar_contador()
        messagebox.showinfo("Info", f"Cargados: {len(airports)}")
def mostrar_todos():

    global mostrar_todos_visible

    # OCULTAR
    if mostrar_todos_visible:

        texto.delete("1.0", tk.END)

        mostrar_todos_visible = False

        return

    # MOSTRAR
    texto.delete("1.0", tk.END)

    for a in airports:
        texto.insert(tk.END, f"{a.code} | {a.latitude} | {a.longitude}\n")

    mostrar_todos_visible = True

def mostrar_schengen():

    texto = ""

    for a in airports:

        if a.schengen:

            texto += f"{a.code} | {a.lat} | {a.lon}\n"

    mostrar_texto(texto)


def mostrar_no_schengen():

    texto = ""

    for a in airports:

        if not a.schengen:

            texto += f"{a.code} | {a.lat} | {a.lon}\n"

    mostrar_texto(texto)

def mostrar_no_schengen():
    texto = ""
    for a in airports:
        if not a.schengen:
            texto += f"{a.code} | {a.lat} | {a.lon}\n"

    mostrar_texto(texto)




def mapa_aeropuertos():
    filename = "mapa_aeropuertos.kml"

    with open(filename, "w") as f:
        f.write("<kml><Document>\n")

        for a in airports:
            f.write(f"<Placemark><name>{a.code}</name>")
            f.write(f"<Point><coordinates>{a.lon},{a.lat},0</coordinates></Point>")
            f.write("</Placemark>\n")

        f.write("</Document></kml>")

    os.system(f"start {filename}")

def cargar_vuelos():
    def cargar_vuelos():
        global aircrafts

        ruta = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )

        if ruta:
            aircrafts = LoadArrivals(ruta)

            messagebox.showinfo(
                "Info",
                f"Vuelos cargados: {len(aircrafts)}"
            )
    global aircrafts

    if not airports:
        messagebox.showwarning("Error", "Carga aeropuertos primero")
        return

    ruta = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    if ruta:
        aircrafts = LoadArrivals(ruta, airports)
        messagebox.showinfo("Info", f"Vuelos cargados: {len(aircrafts)}")


def grafico_horas():

    global grafico_horas_visible
    global ax
    global canvas

    if not aircrafts:
        messagebox.showwarning("Error", "Carga vuelos primero")
        return

    # SI EL GRÁFICO YA ESTÁ VISIBLE -> OCULTAR
    if grafico_horas_visible:

        ax.clear()

        ax.axis("off")

        canvas.draw()

        grafico_horas_visible = False

        return

    # MOSTRAR GRÁFICO
    ax.clear()

    horas = [0] * 24

    for a in aircrafts:

        hora = int(a.hour)

        if 0 <= hora < 24:
            horas[hora] += 1

    ax.bar(range(24), horas)

    ax.set_title("Llegadas por hora")
    ax.set_xlabel("Hora")
    ax.set_ylabel("Número de vuelos")

    ax.axis("on")

    canvas.draw()

    grafico_horas_visible = True

def grafico_aerolineas():
    def grafico_aerolinea_individual(airline):

        cantidad = 0

        for a in aircrafts:
            if a.airline == airline:
                cantidad += 1

        plt.figure(figsize=(5, 5))

        plt.bar([airline], [cantidad])

        plt.xlabel("Aerolínea")
        plt.ylabel("Número de vuelos")
        plt.title(f"Vuelos de {airline}")

        plt.show()


    if not aircrafts:
        messagebox.showwarning("Error", "Carga vuelos primero")
        return

    fig = PlotAirlines(aircrafts)

    mostrar_grafico(fig, panel2)

def grafico_tipo():

    global grafico_tipo_visible
    global ax1
    global canvas1

    if not airports:
        messagebox.showwarning("Error", "Carga vuelos primero")
        return

    # OCULTAR
    if grafico_tipo_visible:

        ax1.clear()

        ax1.axis("off")

        canvas1.draw()

        grafico_tipo_visible = False

        return

    # CONTAR
    schengen = 0
    no_schengen = 0

    for a in airports:
        if a.schengen:
            schengen += 1
        else:
            no_schengen += 1

    ax1.clear()

    nombres = ["Schengen", "No Schengen"]
    valores = [schengen, no_schengen]

    colores = ["blue", "pink"]

    ax1.bar(nombres, valores, color=colores)

    ax1.set_title("Schengen vs No Schengen")

    ax1.axis("on")

    canvas1.draw()

    grafico_tipo_visible = True

def vuelos_largos():
    vuelos = LongDistanceArrivals(aircrafts)

    texto = "Vuelos >2000 km:\n\n"
    for v in vuelos[:30]:
        texto += f"{v.id} - {v.origin}\n"

    mostrar_texto(texto)


def mapa_vuelos():
    MapFlights(aircrafts)
    os.system("start flights.kml")

def actualizar_grafico_aerolineas():

    global ax
    global canvas

    ax.clear()

    if not airlines_selected:

        ax.axis("off")

        canvas.draw()

        return

    ax.axis("on")

    nombres = []
    valores = []

    for airline in airlines_selected:

        contador = 0

        for a in aircrafts:
            if a.airline == airline:
                contador += 1

        nombres.append(airline)
        valores.append(contador)

    ax.bar(nombres, valores)

    ax.set_title("Aerolíneas seleccionadas")
    ax.set_xlabel("Aerolínea")
    ax.set_ylabel("Número de vuelos")

    canvas.draw()

def seleccionar_aerolinea(airline):

    global airlines_selected

    if airline not in airlines_selected:
        airlines_selected.append(airline)

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

    if airline in airlines_selected:
        airlines_selected.remove(airline)
    else:
        airlines_selected.append(airline)

    actualizar_grafico_aerolineas()

def mostrar_botones_aerolineas():

    global botones_visibles

    if not aircrafts:
        messagebox.showwarning("Error", "Carga vuelos primero")
        return

    # SI YA ESTÁN VISIBLES -> OCULTAR
    if botones_visibles:

        for widget in frame_airlines.winfo_children():
            widget.destroy()

        frame_airlines.pack_forget()

        botones_visibles = False

        return

    # SI NO ESTÁN VISIBLES -> MOSTRAR
    airlines = sorted(set(a.airline for a in aircrafts))

    fila = 0
    columna = 0

    for airline in airlines:

        btn = tk.Button(
            frame_airlines,
            text=airline,
            width=8,
            command=lambda a=airline: seleccionar_aerolinea(a)
        )

        btn.grid(row=fila, column=columna, padx=2, pady=2)

        columna += 1

        if columna > 10:
            columna = 0
            fila += 1

    frame_airlines.pack(
        pady=10
    )
    botones_visibles = True

def cargar_terminales():

    global bcn

    ruta = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt")]
    )

    if ruta:

        bcn = LoadAirportStructure(ruta)

        if bcn is None:

            messagebox.showerror(
                "Error",
                "No se pudo cargar terminales"
            )

        else:

            messagebox.showinfo(
                "Info",
                "Terminales cargadas correctamente"
            )

def asignar_gates():

    global bcn

    texto = ""

    for a in aircrafts:

        gate = AssignGate(bcn, a)

        if gate == -1:

            texto += f"{a.id} -> SIN GATE\n"

        else:

            texto += (
                f"{a.id} | "
                f"{a.airline} | "
                f"{gate}\n"
            )

    mostrar_texto(texto)

def mostrar_ocupacion():

    global bcn

    if bcn is None:

        messagebox.showwarning(
            "Error",
            "Carga terminales primero"
        )

        return

    info = GateOccupancy(bcn)

    texto = ""

    for linea in info:

        texto += linea + "\n"

    mostrar_texto(texto)

ventana = tk.Tk()
frame_principal = tk.Frame(ventana)
frame_principal.pack(fill="both", expand=True)

# PANEL IZQUIERDO → BOTONES

frame_menu = tk.Frame(frame_principal, width=250, bg="#EAEAEA")
frame_menu.pack(side="left", fill="y")
frame_menu.pack_propagate(False)

frame_contenido = tk.Frame(frame_principal, bg="white")
frame_contenido.pack(side="right", fill="both", expand=True)

frame_airlines = tk.Frame(ventana)
frame_airlines.pack(pady=10)

# GRID PRINCIPAL
frame_contenido.rowconfigure(0, weight=1)
frame_contenido.rowconfigure(1, weight=1)

frame_contenido.columnconfigure(0, weight=1)
frame_contenido.columnconfigure(1, weight=1)

# PANEL SUPERIOR IZQUIERDO
panel1 = tk.Frame(frame_contenido, bg="white", bd=2, relief="groove")
fig1 = Figure(figsize=(5,5), dpi=100)

ax1 = fig1.add_subplot(111)

ax1.axis("off")

canvas1 = FigureCanvasTkAgg(fig1, master=panel1)

canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

canvas1.draw()
panel1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# PANEL SUPERIOR DERECHO
panel2 = tk.Frame(frame_contenido, bg="white", bd=2, relief="groove")
panel2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
fig = Figure(figsize=(6,5), dpi=100)

ax = fig.add_subplot(111)
ax.axis("off")

canvas = FigureCanvasTkAgg(fig, master=panel2)

canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

canvas.draw()

# PANEL INFERIOR (MAPAS)
panel3 = tk.Frame(frame_contenido, bg="white", bd=2, relief="groove")
panel3.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)


def boton(texto, comando):
    return tk.Button(
        frame_menu,
        text=texto,
        command=comando,
        width=25,
        height=2,
        font=("Arial", 10)
    )

tk.Label(frame_menu, text="--- AEROPUERTOS ---").pack(pady=5)
boton("Cargar aeropuertos", cargar_aeropuertos).pack(pady=3)
boton("Mostrar todos", mostrar_todos).pack(pady=3)
boton("Mostrar Schengen", mostrar_schengen).pack(pady=3)
boton("Mostrar No Schengen", mostrar_no_schengen).pack(pady=3)
boton("Schengen vs No", grafico_tipo).pack(pady=3)
boton("Mapa aeropuertos", mapa_aeropuertos).pack(pady=5)

label_contador = tk.Label(frame_menu, text="Schengen: 0 | No Schengen: 0")
label_contador.pack(pady=10)

tk.Label(frame_menu, text="--- VUELOS ---").pack(pady=5)
boton("Cargar vuelos", cargar_vuelos).pack(pady=3)
boton("Gráfico llegadas", grafico_horas).pack(pady=3)
boton("Gráfico aerolíneas", seleccionar_aerolinea)
boton("Vuelos >2000 km", vuelos_largos).pack(pady=3)
boton("Mostrar aerolíneas", mostrar_botones_aerolineas).pack(pady=3)
boton("Mapa vuelos", mapa_vuelos).pack(pady=5)

tk.Label(frame_menu, text="--- TERMINALES ---").pack(pady=5)
boton("Cargar terminales", cargar_terminales).pack(pady=3)
boton("Asignar Gates", asignar_gates).pack(pady=3)
boton("Mostrar ocupacion", mostrar_ocupacion).pack(pady=3)

ventana.mainloop()