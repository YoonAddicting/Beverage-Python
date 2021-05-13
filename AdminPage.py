import tkinter as tk

import StartPage
from Settings import *


class AdminPage(tk.Frame):
    def __init__(self, master, ID):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcome to the admin page", font=(None, 20)).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="General Settings",
                  command=lambda: master.switch_frame(GeneralSettings)).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Users",
                  command=lambda: master.switch_frame(UserSettings)).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Items",
                  command=lambda: master.switch_frame(ItemSettings)).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Barcode Export",
                  command=lambda: master.switch_frame(BarcodeExport)).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Payment",
                  command=lambda: master.switch_frame(PaymentSettings)).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="TransactionLog",
                  command=lambda: master.switch_frame(TransactionLog)).pack(side="top", fill="x", pady=5)

        tk.Button(self, text="Return to start page", command=lambda: master.switch_frame(StartPage.StartPage)).pack(side="top", fill="x", pady=5)