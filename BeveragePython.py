import tkinter as tk
from pathlib import Path

from StartPage import StartPage
import configuration
import Database


class BeveragePython(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # Load config file

        self.config_file = Path('./conf.ini')
        if self.config_file.exists():
            self.config = configuration.open_config_file(self.config_file)
        else:
            self.config = configuration.create_default_config(self.config_file)
        self.geometry('480x320')
        self._frame = None
        self.switch_frame(StartPage)
        # Fullscreen check
        if self.config.getboolean('DEFAULT', 'Fullscreen') == True:
            self.attributes("-fullscreen", True)
        self.database = Database.Database()

    def switch_frame(self, frame_class, ID=None):
        """ Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self,ID)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def get_config(self):
        return self.config

    def set_config(self, config):
        self.config = config
