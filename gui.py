#Python Imports
import tkinter as tk
#Globalle Konstanzen
__version__ = "0.0.2"
ALIGN_LEFT = "0"
ALIGN_CENTER = "1"
def parse_geometry(geometry:str) -> tuple[int,int]:
    """
    Parst einen geometry String (WIDTHxHEIGHT+X+Y) in ein Tupel (WIDTH,HEIGHT) 
    """
    split=geometry.split("x")
    return (int(split[0]), split[1].split("+")[0])
def erstelle_Fenster(*widgets:dict, fenster_name:str = "Fenster", fenster_breite:int = 0, fenster_hoehe:int = 0, protocols:tuple[tuple[str, str]] = None, context:dict = None) -> tk.Tk:
    """
    Erstellt dynamisch ein Fenster in der Mitte des aktuellen Bildschirms.

    ACHTUNG: die Funktionen für Protokolle und Buttons muss man natürlich selber schreiben.\n
    für protocol und command wird automatisch ein lambda erstellt, an den beiden Stellen nur die Funktion mit Parameter übergeben

    Argumente:
        fenster_name - String: So wird das Fenster heißen
        fenster_breite - Integer: Breite des Fensters in Pixel, wenn nicht mitgegeben oder 0, oder nicht alles drauf passt, wird die Größe berechnet.
        fenster_hoehe - Integer: Höhe des Fensters in Pixel, wenn nicht mitgegeben oder 0, oder nicht alles drauf passt, wird die Größe berechnet.
        protocol - Tupel(String,String) Name des protokolls und Name der Funktion. die Funktion wird automatisch mit Lambda aufgerufen für Parameter
        widget - Dictionary - Für jedes Element auf dem Fenster von Oben bis unten ein Dictionary, dass das Element beschreibt
        context - Dictionary für Übergabe von benötigten Variablen oder Funktionen, die nicht im Modul sind.
    """
    fenster = tk.Tk()
    fenster.title = fenster_name
    min_breite = 0
    min_hoehe = 0
    elemente:tuple[tuple[tk.Widget,int]] = []
    if not protocols == None:
        for protocol in protocols:
            try:
                # funktionsname = protocol[2].__name__
                # if funktionsname not in globals():
                #     globals()[funktionsname] = protocol[2]
                procdict = {}
                einzel_argument = ""
                protocol_funktion = protocol[1].lstrip()
                for char in protocol_funktion:
                    if str(char).isalnum() or str(char) == "_":
                        einzel_argument += str(char)
                    elif einzel_argument != "":
                        if context and einzel_argument in context:
                            procdict[einzel_argument] = context[einzel_argument]
                        else:
                            procdict[einzel_argument] = eval(einzel_argument)
                        einzel_argument=""
                if not einzel_argument == "":
                    if context and einzel_argument in context:
                        procdict[einzel_argument] = context[einzel_argument]
                    else:
                        procdict[einzel_argument] = eval(einzel_argument)
                    einzel_argument=""
                fenster.protocol(protocol[0], lambda pc=protocol,pd=procdict: eval(pc[1], pd))    
            except Exception as e:
                print(f"Protokoll {protocol} für Fenster {fenster_name} konnte nicht erstellt werden: {e}")
    for widget in widgets:
        if not ("type" in widget): print(f"widget {widget} hat keinen Eintrag für Type")
        if widget["type"] == "space": 
            try: min_hoehe += int(widget["space"])
            except Exception as e: print(f"Fehler beim Space erstellen: {e}")
        elif widget["type"] == "label": 
            try:
                element = tk.Label(fenster, text = widget["text"])
                element_top=min_hoehe
                min_hoehe+=element.winfo_reqheight()
                if element.winfo_reqwidth()>min_breite:min_breite=element.winfo_reqwidth()
                if "align" in widget: align = widget["align"]
                else: align = ALIGN_CENTER
                elemente.append((element, element_top, align))
            except Exception as e:
                print(f"Fehler beim Label erstellen: {e}")
        elif widget["type"] == "button":
            try:
                # funktionsname = widget["function"].__name__
                # if funktionsname not in globals():
                #     globals()[funktionsname] = widget["function"]
                comdict = {}
                einzel_argument = ""
                command_funktion_string = widget["command"]
                command_funktion_string = command_funktion_string.lstrip()
                for char in command_funktion_string:
                    if str(char).isalnum() or str(char) == "_":
                        einzel_argument += str(char)
                    elif einzel_argument  != "":
                        if context and einzel_argument in context:
                            comdict[einzel_argument] = context[einzel_argument]
                        else:
                            comdict[einzel_argument] = eval(einzel_argument)
                        einzel_argument = ""
                if not einzel_argument == "":
                    if context and einzel_argument in context:
                        comdict[einzel_argument] = context[einzel_argument]
                    else:
                        comdict[einzel_argument] = eval(einzel_argument)
                einzel_argument=""
                element = tk.Button(fenster, text = widget["text"], command = lambda wc = widget["command"], cd = comdict: eval(wc, cd), width = widget["width"], height = widget["height"])
                element_top = min_hoehe
                min_hoehe += element.winfo_reqheight()
                if element.winfo_reqwidth() > min_breite: min_breite = element.winfo_reqwidth()
                if element.winfo_reqwidth() > min_breite: min_breite = element.winfo_reqwidth()
                if "align" in widget: align = widget["align"]
                elemente.append((element, element_top, align))
            except Exception as e:
                print(f"Fehler beim Button erstellen: {e}")
        else:
            print(f"{widget["type"]} ist kein gültuger Widget typ")
    if min_breite > fenster_breite:
        fenster_breite = min_breite
    if min_hoehe > fenster_hoehe:
        fenster_hoehe = min_hoehe
    for element in elemente:
        if element[2] == ALIGN_CENTER: element[0].place(x = (fenster_breite - element[0].winfo_reqwidth()) // 2, y = element[1])
        elif element[2] == ALIGN_LEFT: element[0].place(x = 0, y = element[1])
    fenster.geometry(f"{fenster_breite}x{fenster_hoehe}+{(fenster.winfo_screenwidth() - fenster_breite) // 2}+{(fenster.winfo_screenheight() - fenster_hoehe) // 2}")
    return fenster