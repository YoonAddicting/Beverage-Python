import tkinter as tk

import StartPage


class AdminPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        title_label = tk.Label(self, text="Welcome to Beverage-Python!", font=(None, 20))
        title_label.pack()
        tk.Label(self, text="This is the admin page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page", command=lambda: master.switch_frame(StartPage.StartPage)).pack()