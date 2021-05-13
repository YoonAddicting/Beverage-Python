import tkinter as tk
from tkinter.messagebox import showinfo
from pathlib import Path
import configparser

import AdminPage
import BeveragePython

class StartPage(tk.Frame):
    def __init__(self, master: tk.Tk, ID):
        # Initialize window
        tk.Frame.__init__(self, master)
        title_label = tk.Label(self, text="Welcome to Beverage-Python!", font=(None, 20))
        title_label.pack()
        barcode_label = tk.Label(self, text="Please enter a barcode...")
        barcode_label.pack(side="top", fill="x", pady=10)
        # Setup barcode variable for scanning barcodes
        self.barcode = ''
        #Setup keybindings
        self.bind('<F11>', self.auth_admin)
        self.bind('<Key>', self.get_key)
        # Grab focus
        self.focus_set()
        #tk.Button(self, text="Open admin panel", command=lambda: master.switch_frame(AdminPage.AdminPage)).pack(side="bottom")

    def auth_admin(self, event):
        if self.master.config.getboolean('DEFAULT','passwordenabled'):
            from tkinter import simpledialog
            password = simpledialog.askstring(title="Test", prompt="What thos?", show='*')
            if password != "AdminPassword": # TODO Perform Bcrypt check of password
                tk.messagebox.showerror("Invalid password", "Entered password was invalid!")
                self.focus_set()
            else:
                self.master.switch_frame(AdminPage.AdminPage)
        else:
            self.master.switch_frame(AdminPage.AdminPage)

    def get_key(self, event):
        if event.char in '0123456789':
            self.barcode += event.char
            # self.label['text'] = self.code

        elif event.keysym == 'Return':
            showinfo('Code', self.barcode)
            # TODO Create check that verifies if the given barcode belongs to a given user

            self.barcode = ''

class BuyPage(tk.Frame):
    def __init__(self, master: tk.Tk, ID):
        # Initialize window
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Please scan your items!", font=(None, 20)).pack()
        self.barcode = ''
