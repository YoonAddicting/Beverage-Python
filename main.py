import tkinter as tk

from StartPage import StartPage

class BeveragePython(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('480x320')
        self._frame = None
        self.switch_frame(StartPage)
        self.attributes("-fullscreen", False)
        # TODO: Create check that if it is initial launch (if db file isn't present in folder)
        # TODO: Initialize DB

    def switch_frame(self, frame_class):
        """ Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()



if __name__ == "__main__":
    win = BeveragePython()
    win.mainloop()
