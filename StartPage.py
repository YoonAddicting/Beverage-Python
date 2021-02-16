import tkinter as tk
from tkinter.messagebox import showinfo

import AdminPage


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        title_label = tk.Label(self, text="Welcome to Beverage-Python!", font=(None,20))
        title_label.pack()
        barcode_label = tk.Label(self, text="Please enter a barcode...")
        self.barcode = ''
        barcode_label.pack(side="top", fill="x", pady=10)
        self.bind('<F11>', self.auth_admin)
        self.bind('<Key>', self.get_key)
        self.focus_set()
        tk.Button(self, text="Open admin panel", command=lambda: master.switch_frame(AdminPage.AdminPage)).pack(
            side="bottom")

    def auth_admin(self, event):
        from tkinter import simpledialog
        password = simpledialog.askstring(title="Test", prompt="What thos?", show='*')
        if(password != "AdminPassword"):
            tk.messagebox.showerror("Invalid password", "Entered password was invalid!")
        else:
            self.master.switch_frame(AdminPage.AdminPage)

    def get_key(self, event):
        if event.char in '0123456789':
            self.barcode += event.char
            # self.label['text'] = self.code

        elif event.keysym == 'Return':
            showinfo('Code', self.barcode)
            # TODO Create check that verifies if the given barcode belongs to a given user

            # self.code = "Code entered: " + self.code
            # self.label['text'] = self.code
            self.barcode = ''