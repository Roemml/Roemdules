import sys
import os
import pygame
def get_exepath(file:str) -> str:
    """
    Ermitteln des HauptprogrammPfads.\n
    Parameter file ist daher __file__
    """
    if getattr(sys, 'frozen', False):  # wenn mit PyInstaller "eingefroren"
        # sys.executable ist dann die .exe-Datei
        return os.path.dirname(sys.executable)
    else:
        # normale Python-Ausführung: Skriptdatei
        return os.path.dirname(os.path.abspath(file))
def get_Surface_map(sprite:pygame.Surface):
    """
    Ermittelt eine 3-dimensionale Liste aus einem Image\n
    Dimension 1: y-Wert des Sprites\n
    Dimension 2: x-Wert des Sprites\n
    Dimension 3: Farbe an demPunkt
    """
    image_sring = pygame.image.tostring(sprite,"RGB")
    colors = []
    color_line = []
    color = []
    for i in range(len(image_sring)):
        color.append(image_sring[i])
        if i % 3 == 2:
            color_line.append(tuple(color))
            color = []
            if (i+1)% (sprite.get_rect().width * 3) == 0:
                colors.append(tuple(color_line))
                color_line = []
    return tuple(colors)