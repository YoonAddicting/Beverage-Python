import tkinter as tk

import AdminPage


class UserSettings(tk.Frame):
    def __init__(self, master, ID):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Welcome to the User Settings page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Create user", command=lambda: master.switch_frame(CreateUser)).pack()
        tk.Button(self, text="Modify user", command=lambda: master.switch_frame(ModifyUser)).pack()
        tk.Button(self, text="Delete user", command=lambda: master.switch_frame(DeleteUser)).pack()
        tk.Button(self, text="Return to Admin Page", command=lambda: master.switch_frame(AdminPage.AdminPage)).pack(
            side="bottom")

class CreateUser(tk.Frame):
    def __init__(self, master, ID):
        tk.Frame.__init__(self, master)
        self.master = master
        # Get genders for dropdown
        genders = master.database.get_all_gender()
        # Get roles for dropdown
        roles = master.database.get_all_userrole()
        # Get groups for dropdown
        groups = master.database.get_all_usergroup()
        # Get teams for dropdown
        teams = master.database.get_all_userteam()
        c_gender = tk.StringVar(self)
        c_gender.set("Female")
        c_role = tk.StringVar(self)
        c_role.set("")
        c_group = tk.StringVar(self)
        c_group.set("")
        c_team = tk.StringVar(self)
        c_team.set("")
        title = tk.Label(self, text="Create a user.").grid(row=0, column=0)
        name = tk.Entry(self)
        gendermenu = tk.OptionMenu(self, c_gender, *[i[0] for i in genders])
        nickname = tk.Entry(self)
        rolemenu = tk.OptionMenu(self, c_role, "", *[i[0] for i in roles])
        groupmenu = tk.OptionMenu(self, c_group, "", *[i[0] for i in groups])
        teammenu = tk.OptionMenu(self, c_team, "", *[i[0] for i in teams])

        name_label = tk.Label(self, text="Name:").grid(row=1, column=0)
        gender_label = tk.Label(self, text="Gender:").grid(row=2, column=0)
        nickname_label = tk.Label(self, text="Nickname:").grid(row=3, column=0)
        role_label = tk.Label(self, text="Role:").grid(row=4, column=0)
        group_label = tk.Label(self, text="Group:").grid(row=5, column=0)
        team_label = tk.Label(self, text="Team:").grid(row=6, column=0)

        def goback():
            self.master.switch_frame(UserSettings)

        def createuser():
            gender_dict = dict(genders)
            gender_ID = (gender_dict[c_gender.get()])
            role_dict = dict(roles)
            role_dict[""] = None
            role_ID = (role_dict[c_role.get()])
            group_dict = dict(groups)
            group_dict[""] = None
            group_ID = (group_dict[c_group.get()])
            team_dict = dict(teams)
            team_dict[""] = None
            team_ID = (team_dict[c_team.get()])
            master.database.create_user(name.get(), gender_ID, nickname.get(), role_ID, group_ID, team_ID)


            goback()

        save_btn = tk.Button(self, text="Save and return", command=createuser).grid(row=7, column=1)
        return_btn = tk.Button(self, text="Go back without saving", command=goback).grid(row=7, column=0)

        name.grid(row=1, column=1)
        gendermenu.grid(row=2, column=1)
        nickname.grid(row=3, column=1)
        rolemenu.grid(row=4, column=1)
        groupmenu.grid(row=5, column=1)
        teammenu.grid(row=6, column=1)







class ModifyUser(tk.Frame):
    def __init__(self, master, ID):
        tk.Frame.__init__(self, master)
class DeleteUser(tk.Frame):
    def __init__(self, master, ID):
        tk.Frame.__init__(self, master)
