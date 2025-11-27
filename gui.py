#Python Imports
import tkinter as tk
#Globalle Konstanzen
__version__ = "0.0.3"
ALIGN_LEFT = "0"
ALIGN_CENTER = "1"
def parse_geometry(geometry:str) -> tuple[int,int]:
    """
    Parst einen geometry String (WIDTHxHEIGHT+X+Y) in ein Tupel (WIDTH,HEIGHT) 
    """
    split=geometry.split("x")
    return (int(split[0]), split[1].split("+")[0])
def erstelle_Fenster(widgets:list[dict], fenster_name:str = "Fenster", fenster_breite:int = 0, fenster_hoehe:int = 0, geometry_manager:str = "place", protocols:tuple[tuple[str, str]] = None, context:dict = None) -> tk.Tk:
    """
    Erstellt dynamisch ein Fenster in der Mitte des aktuellen Bildschirms.

    ACHTUNG: die Funktionen für Protokolle und Buttons muss man natürlich selber schreiben.\n
    für protocol und command wird automatisch ein lambda erstellt, an den beiden Stellen nur die Funktion mit Parameter übergeben

    Argumente:
        fenster_name - String: So wird das Fenster heißen
        fenster_breite - Integer: Breite des Fensters in Pixel, wenn nicht mitgegeben oder 0, oder nicht alles drauf passt, wird die Größe berechnet.
        fenster_hoehe - Integer: Höhe des Fensters in Pixel, wenn nicht mitgegeben oder 0, oder nicht alles drauf passt, wird die Größe berechnet.
        protocol - Tupel(String,String) Name des protokolls und Name der Funktion. die Funktion wird automatisch mit Lambda aufgerufen für Parameter
        widget - Dictionary-Liste - Für jedes Element auf dem Fenster von Oben bis unten ein Dictionary der Liste, dass das Element beschreibt
        context - Dictionary für Übergabe von benötigten Variablen oder Funktionen, die nicht im Modul sind.
    """
    fenster = tk.Tk()
    fenster.title(fenster_name)
    min_breite = 0
    min_hoehe = 0
    varlist = {}
    elemente:list[tk.Widget] = []
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
                element.element_top=min_hoehe
                min_hoehe+=element.winfo_reqheight()
                if element.winfo_reqwidth()>min_breite:min_breite=element.winfo_reqwidth()
                if "align" in widget: element.align = widget["align"]
                else: element.align = ALIGN_CENTER
                if "name" in widget:
                    element.name = widget["name"]
                elemente.append(element)
            except Exception as e:
                print(f"Fehler beim Label erstellen: {e}")
        elif widget["type"] == "listbox": 
            try:
                element = tk.Listbox(fenster)
                element.element_top=min_hoehe
                texte:list[str] = widget["text"]
                for text in texte:
                    element.insert("end", text)
                if "align" in widget: element.align = widget["align"]
                else: element.align = ALIGN_CENTER
                if "name" in widget:
                    element.name = widget["name"]
                if not "height" in widget:
                    element.configure(width=0) 
                elif len(texte) <  widget["height"]:
                    element.configure(width=0, height=len(texte))
                else:
                    element.configure(width=0, height=widget["height"])
                min_hoehe+=element.winfo_reqheight()
                elemente.append(element)
                if element.winfo_reqwidth() > min_breite: min_breite = element.winfo_reqwidth()
            except Exception as e:
                print(f"Fehler beim listbox erstellen: {e}")
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
                element.element_top = min_hoehe
                min_hoehe += element.winfo_reqheight()
                if element.winfo_reqwidth() > min_breite: min_breite = element.winfo_reqwidth()
                if "align" in widget: element.align = widget["align"]
                else: element.align = ALIGN_CENTER
                elemente.append(element)
            except Exception as e:
                print(f"Fehler beim Button erstellen: {e}")
        elif widget["type"] == "entry": 
            try:
                element = tk.Entry(fenster, width= widget["width"]) #if ("show" not in widget.keys()) else tk.Entry(fenster, width= widget["width"], show=widget["show"])
                if "show" in widget:
                    element.config({"show": widget["show"]})
                if "name" in widget:
                    element.name = widget["name"]
                element.element_top=min_hoehe
                min_hoehe+=element.winfo_reqheight()
                if element.winfo_reqwidth()>min_breite:min_breite=element.winfo_reqwidth()
                if "align" in widget: element.align = widget["align"]
                else: element.align = ALIGN_CENTER
                elemente.append(element)
            except Exception as e:
                print(f"Fehler beim Eingabefeld erstellen: {e}")
        elif widget["type"] == "radiobutton":
            try:
                if widget["variable"] not in varlist:
                    globals()[widget["variable"]] = tk.StringVar()
                    varlist[widget["variable"]] = globals()[widget["variable"]]
                  # Setze den Startwert von modus aus context, falls vorhanden
                if 'modus' in context:
                    varlist[widget["variable"]].set(context['modus'])  # Dynamischer Startwert aus context
                if 'command' in widget:
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
                    element = tk.Radiobutton(fenster, variable=varlist[widget["variable"]], value=widget["value"], text=widget["text"], command = lambda wc = widget["command"], cd = comdict: eval(wc, cd))
                else:
                    element = tk.Radiobutton(fenster, variable=varlist[widget["variable"]], value=widget["value"], text=widget["text"])
                element.element_top=min_hoehe
                min_hoehe+=element.winfo_reqheight()
                if element.winfo_reqwidth()>min_breite:min_breite=element.winfo_reqwidth()
                if "align" in widget: element.align = widget["align"]
                else: element.align = ALIGN_CENTER
                elemente.append(element)
            except Exception as e:
                print(f"Fehler beim radiobutton erstellen: {e}")
        else:
            print(f"{widget["type"]} ist kein gültuger Widget typ")
    min_breite += 10
    min_hoehe += 10
    if min_breite > fenster_breite:
        fenster_breite = min_breite
    if min_hoehe > fenster_hoehe:
        fenster_hoehe = min_hoehe
    for element in elemente:
        if geometry_manager == "place":
            if element.align == ALIGN_CENTER: element.place(x = (fenster_breite - element.winfo_reqwidth()) // 2, y = element.element_top)
            elif element.align == ALIGN_LEFT: element.place(x = 0, y = element.element_top)
        elif geometry_manager == "pack":
            if element.align == ALIGN_CENTER: element.pack(anchor=tk.CENTER)
            elif element.align == ALIGN_LEFT: element.pack(anchor=tk.W)
    x_pos = (fenster.winfo_screenwidth() - fenster_breite) // 2
    if x_pos < 0: x_pos = 0
    y_pos = (fenster.winfo_screenheight() - fenster_hoehe) // 2
    if y_pos < 0: y_pos = 0
    fenster.geometry(f"{fenster_breite}x{fenster_hoehe}+{x_pos}+{y_pos}")
    fenster.width = fenster_breite
    if len(varlist) == 0:
        return fenster
    else:
        return fenster, varlist