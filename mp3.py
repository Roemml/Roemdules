#Global Imports
import pygame
import threading
# Globale Variablen
__version__ = "0.0.2"
pygame.mixer.init()
class Music:
    stop__music_event:threading.Event = threading.Event()
    pause_music_event:threading.Event = threading.Event()
    resume_music_event:threading.Event = threading.Event()
    mp3_thread = None
    def _play_music(self, mp3_file, stop_music_event, pause_music_event, resume_music_event, volume) -> None:
        """
        Hintergrundmusik Spieler im Loop.
        """
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)  # Loop indefinitely
        while not stop_music_event.is_set():
            if pause_music_event.is_set():
                pygame.mixer.music.pause()
                pause_music_event.clear()
            elif resume_music_event.is_set():
                pygame.mixer.music.unpause()
                resume_music_event.clear()
            pygame.time.Clock().tick(10)  # Check the stop event periodically
        try:
            pygame.mixer.music.stop()
            # pygame.mixer.quit()
        except:
            pass
    def __init__(self, mp3_file:str, volume:float = 1) -> None:
        """
        Startet die Hintergrundmusik.
        """
        self.stop__music_event.clear()
        self.mp3_thread = threading.Thread(target = self._play_music, args = (mp3_file, self.stop__music_event, self.pause_music_event, self.resume_music_event, volume))
        self.mp3_thread.start()
    def end_music(self) -> None:
        """
        Beendet die Hintergrundmusik.
        """
        self.stop__music_event.set()
        self.mp3_thread.join()
    def pause_music(self) -> None:
        """
        Pausiert die Hintergrundmusik.
        """
        self.pause_music_event.set()
    def resume_music(self) -> None:
        """
        Hintergrundmusik wird wieder fortgesetzt.
        """
        self.resume_music_event.set()