import sqlite3
from sqlite3 import Error
from pathlib import Path


class Database():
    def __init__(self):
        """ creata a database connection to a SQLite database"""
        self.conn = None
        self.database_file = Path('./database.sqlite')
        if self.database_file.exists():
            try:
                self.conn = sqlite3.connect(str(self.database_file.absolute()))
                print(sqlite3.version)
            except Error as e:
                print(e)
        else:
            try:
                self.conn = sqlite3.connect(str(self.database_file.absolute()))
                print(sqlite3.version)
                self.populate_empty_database(self.conn)
            except Error as e:
                print(e)

    def get_database_conn(self):
        return self.conn

    def populate_empty_database(self):
        try:
            c = self.conn.cursor()
            sql_commands = ('''CREATE TABLE IF NOT EXISTS UserTeam(
                               TeamID INT UNSIGNED PRIMARY KEY,
                               TeamName VARCHAR(40) NOT NULL);''',
                            '''CREATE TABLE IF NOT EXISTS UserGroup(
                               GroupID INT UNSIGNED PRIMARY KEY,
                               GroupName VARCHAR(40) NOT NULL);''',
                            '''CREATE TABLE IF NOT EXISTS UserRole(
                               RoleID INT UNSIGNED PRIMARY KEY,
                               RoleName VARCHAR(40) NOT NULL);''',
                            '''CREATE TABLE IF NOT EXISTS Multipliers(
                               MulID BIGINT UNSIGNED PRIMARY KEY,
                               MulValue INT NOT NULL);''',
                            '''CREATE TABLE IF NOT EXISTS Gender(
                               GenderID INT(1) PRIMARY KEY,
                               GenderName VARCHAR(6) NOT NULL);''',
                            '''CREATE TABLE IF NOT EXISTS Category(
                               CategoryID INT PRIMARY KEY,
                               CategoryName VARCHAR(40) NOT NULL);''',
                            '''INSERT INTO Gender VALUES 
                               (0, "Female"),
                               (1, "Male");''',
                            '''CREATE TABLE IF NOT EXISTS Item(
                               ItemID BIGINT UNSIGNED PRIMARY KEY,
                               ItemName VARCHAR(40) NOT NULL,
                               ItemPrice DECIMAL(6,2) NOT NULL,
                               StartStock INT(5) NOT NULL,
                               SoldStock INT(5) NOT NULL,
                               CurrentStock INT(5) NOT NULL,
                               LostStock INT(5) NOT NULL,
                               Category INT(4),
                               FOREIGN KEY (Category) REFERENCES Category(CategoryID) ON DELETE SET NULL);''',
                            '''CREATE TABLE IF NOT EXISTS Users(
                               UserID INT(4) PRIMARY KEY,
                               UserName VARCHAR(40) NOT NULL,
                               Gender INT(1) NOT NULL,
                               Nickname VARCHAR(40),
                               UserRole UNSIGNED INT(4),
                               UserGroup UNSIGNED INT(4),
                               UserTeam UNSIGNED INT(4),
                               FOREIGN KEY (Gender) REFERENCES Gender(GenderID),
                               FOREIGN KEY (UserTeam) REFERENCES UserTeam(TeamID) ON DELETE SET NULL,
                               FOREIGN KEY (UserGroup) REFERENCES UserGroup(GroupID) ON DELETE SET NULL,
                               FOREIGN KEY (UserRole) REFERENCES UserRole(RoleID) ON DELETE SET NULL);''',
                            '''CREATE TABLE IF NOT EXISTS Transactions(
                               TransID UNSIGNED BIGINT(10) PRIMARY KEY,
                               UserID INT(4) NOT NULL,
                               Item UNSIGNED BIGINT(13) NOT NULL,
                               Multiplier INT(3) NOT NULL,
                               FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
                               FOREIGN KEY (Item) REFERENCES Item(ItemID)ON DELETE CASCADE);'''
                            )
            for command in sql_commands:
                c.execute(command)
            # TODO Make loop for multipliers 0-99
            self.conn.commit()
        except Error as e:
            print(e)
        return

    def get_username(self, ID):
        # Takes the ID of a user and gives the username of the given user
        c = self.conn.cursor()
        sql = '''SELECT UserName 
                 FROM Users
                 WHERE UID = ?
        '''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_nickname(self, ID):
        # Takes the ID of a user and gives the username of the given user
        c = self.conn.cursor()
        sql = '''SELECT Nickname
                 FROM Users
                 WHERE UserID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_product(self, ID):
        return

    # TODO Finish getters and create calculating functions for transactions and so forth
    def submit_transactions(self, transactions):
        return

