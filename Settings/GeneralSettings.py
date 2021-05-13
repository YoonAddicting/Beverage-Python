import tkinter as tk

import AdminPage


class GeneralSettings(tk.Frame):
    def __init__(self, master, ID):
        tk.Frame.__init__(self, master)
        title_label = tk.Label(self, text="Welcome to Beverage-Python!", font=(None, 20))
        title_label.pack()
        tk.Label(self, text="Welcome to the General Settings page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to Admin Page", command=lambda: master.switch_frame(AdminPage.AdminPage)).pack(
            side="bottom")