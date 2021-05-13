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
                self.populate_empty_database()
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
            self.generate_multipliers()
            self.conn.commit()
        except Error as e:
            print(e)
        return

    # Category Getters
    def get_category_name(self, ID):
        # Takes the ID of a category and returns the name of the category
        c = self.conn.cursor()
        sql = '''SELECT CategoryName
                 FROM Category
                 WHERE CategoryID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_all_categories(self):
        # Returns a list of all categories and their corresponding IDs
        c = self.conn.cursor()
        sql = '''SELECT CategoryName, CategoryID
                 FROM Category'''
        c.execute(sql)
        return c.fetchall()

    def generate_new_categoryid(self):
        # TODO Figure out a method to detect any holes in the sequence of IDs
        # Generates a new unique categoryID and returns it
        c = self.conn.cursor()
        sql = '''SELECT MAX(CategoryID)
                 FROM Category'''
        c.execute(sql)
        res = c.fetchall()
        if res[0][0] is None:
            return 0
        else:
            return res[0][0]+1

    # Category Setters
    def create_category(self, name):
        # Creates a new category with the given name
        c = self.conn.cursor()
        sql = '''INSERT INTO Category VALUES
                 (?, ?);'''
        category_id = self.generate_new_categoryid()
        c.execute(sql, (category_id, name,))

    def rename_category(self, id, name):
        # Renames a category with the given ID
        c = self.conn.cursor()
        sql = '''UPDATE Category
                 SET CategoryName = ?
                 WHERE CategoryID = ?'''
        c.execute(sql, (name, id,))

    def remove_category(self, id):
        c = self.conn.cursor()
        sql = '''DELETE FROM Category
                 WHERE CategoryID = ?'''
        c.execute(sql, (id,))

    # Gender Getters
    def get_gender(self, ID):
        # Takes the ID of a category and returns the name of the category
        c = self.conn.cursor()
        sql = '''SELECT GenderName
                 FROM Gender
                 WHERE GenderID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_all_gender(self):
        # Returns a list of all transactions
        c = self.conn.cursor()
        sql = '''SELECT GenderName, GenderID
                 FROM Gender'''
        c.execute(sql)
        return c.fetchall()

    # Item Getters
    def get_item(self, ID):
        # Takes the ID of a product and returns the name of the product
        c = self.conn.cursor()
        sql = '''SELECT ItemName
                 FROM Item
                 WHERE ItemID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_item_all_details(self, ID):
        # Takes the ID of a product and returns all details about the product
        c = self.conn.cursor()
        sql = '''SELECT *
                 FROM Item
                 WHERE ItemID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res

    def get_item_price(self, ID):
        # Takes the ID of a product and returns the price of the product
        c = self.conn.cursor()
        sql = '''SELECT ItemPrice
                         FROM Item
                         WHERE ItemID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_item_startstock(self, ID):
        # Takes the ID of a product and returns the StartStock of the product
        c = self.conn.cursor()
        sql = '''SELECT StartStock
                 FROM Item
                 WHERE ItemID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_item_soldstock(self, ID):
        # Takes the ID of a product and returns the SoldStock of the product
        c = self.conn.cursor()
        sql = '''SELECT SoldStock
                 FROM Item
                 WHERE ItemID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_item_currentstock(self, ID):
        # Takes the ID of a product and returns the CurrentStock of the product
        c = self.conn.cursor()
        sql = '''SELECT CurrentStock
                 FROM Item
                 WHERE ItemID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_item_loststock(self, ID):
        # Takes the ID of a product and returns the LostStock of the product
        c = self.conn.cursor()
        sql = '''SELECT LostStock
                 FROM Item
                 WHERE ItemID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_item_category(self, ID):
        # Takes the ID of a product and returns the category of the product
        c = self.conn.cursor()
        sql = '''SELECT Category
                 FROM Item
                 WHERE ItemID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_all_item(self):
        # Returns a list of tuples with the (ItemID, ItemName) of all the items.
        c = self.conn.cursor()
        sql = '''SELECT ItemID, ItemName
                 FROM Item'''
        c.execute(sql)
        res = c.fetchall()
        return res

    # Item setters

    def generate_item_id(self):
        c = self.conn.cursor()
        sql = '''SELECT MAX(ItemID)
                         FROM Item
                         WHERE ItemID LIKE '99%';'''
        # TODO Verify doesn't overlap with userID or Multipliers
        c.execute(sql)
        res = c.fetchall()
        if res[0][0] is None:
            return 9900000000000
        else:
            return res[0][0]+1

    def create_item(self, name, price, startstock, ID=None, category=None):
        c = self.conn.cursor()
        sql = '''INSERT INTO Item VALUES
                         (?, ?, ?, ? ,? ,?, ?, ?);'''
        if ID is None:
            ID = self.generate_item_id()
        c.execute(sql, (ID, name, price, startstock, 0, startstock, 0, category))

    def update_item(self, ID, name, price, startstock, soldstock, currentstock, loststock, category, oldID=None):
        # Updates all fields of the Item, assumes that all arguments are given except for oldID.
        # If ID needs to be updated, then oldID needs to be given.
        c = self.conn.cursor()
        sql = '''UPDATE Item
                 SET ItemID = ?,
                     ItemName = ?,
                     ItemPrice = ?,
                     StartStock = ?,
                     SoldStock = ?,
                     CurrentStock = ?,
                     LostStock = ?,
                     Category = ?
                     WHERE ItemID = ?'''
        if oldID is None:
            c.execute(sql, (ID, name, price, startstock, soldstock, currentstock, loststock, category, ID))
        else:
            c.execute(sql, (ID, name, price, startstock, soldstock, currentstock, loststock, category, oldID))

    def remove_item(self, ID):
        # Removes an item with the given ID.
        c = self.conn.cursor()
        sql = '''DELETE FROM Item WHERE ItemID = ?'''
        c.execute(sql, (ID,))

    # Multiplier getters
    def get_multiplier(self, ID):
        # Takes the ID of a multiplier and returns the value
        c = self.conn.cursor()
        sql = '''SELECT MulValue
                 FROM Multipliers
                 WHERE MulID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    # Multiplier setters
    def generate_multipliers(self):
        # Generates multipliers for values 0-100
        c = self.conn.cursor()
        sql = '''INSERT INTO Multipliers VALUES
                 (?, ?)'''
        multipliers = []
        for i in range(0, 101):
            multipliers.append((970000000000+i, i))
        c.executemany(sql, multipliers)

    # Transaction getters
    def get_all_transactions(self):
        # Returns a list of all transactions
        c = self.conn.cursor()
        sql = '''SELECT *
                 FROM Transactions'''
        c.execute(sql)
        return c.fetchall()

    # User Group Getters
    def get_usergroup(self, ID):
        # Takes the ID of a UserGroup and returns the name
        c = self.conn.cursor()
        sql = '''SELECT GroupID
                 FROM UserGroup
                 WHERE GroupID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_all_usergroup(self):
        c = self.conn.cursor()
        sql = '''SELECT GroupName, GroupID
                 FROM UserGroup'''
        c.execute(sql)
        return c.fetchall()

    def generate_new_groupid(self):
        # TODO Figure out a method to detect any holes in the sequence of IDs
        # Generates a new unique GroupID and returns it
        c = self.conn.cursor()
        sql = '''SELECT MAX(GroupID)
                 FROM UserGroup'''
        c.execute(sql)
        res = c.fetchall()
        if res[0][0] is None:
            return 0
        else:
            return res[0][0]+1

    # User Group setters
    def create_usergroup(self, name):
        # Creates a new usergroup with the given name
        c = self.conn.cursor()
        sql = '''INSERT INTO UserGroup VALUES
                 (?, ?);'''
        usergroup_id = self.generate_new_groupid()
        c.execute(sql, (usergroup_id, name,))

    def rename_usergroup(self, id, name):
        # Renames a usergroup with the given ID
        c = self.conn.cursor()
        sql = '''UPDATE UserGroup
                 SET GroupName = ?
                 WHERE GroupID = ?'''
        c.execute(sql, (name, id,))

    def remove_usergroup(self, id):
        # Removes a given usergroup
        c = self.conn.cursor()
        sql = '''DELETE FROM UserGroup
                 WHERE GroupID = ?'''
        c.execute(sql, (id,))

    # User Role Getters
    def get_userrole(self, ID):
        # Takes the ID of a UserRole and returns the name
        c = self.conn.cursor()
        sql = '''SELECT RoleName
                 FROM UserRole
                 WHERE RoleID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_all_userrole(self):
        c = self.conn.cursor()
        sql = '''SELECT RoleName, RoleID
                 FROM UserRole'''
        c.execute(sql)
        return c.fetchall()

    def generate_new_roleid(self):
        # TODO Figure out a method to detect any holes in the sequence of IDs
        # Generates a new unique roleID and returns it
        c = self.conn.cursor()
        sql = '''SELECT MAX(RoleID)
                 FROM UserRole'''
        c.execute(sql)
        res = c.fetchall()
        if res[0][0] is None:
            return 0
        else:
            return res[0][0]+1

    # User Role setters
    def create_userrole(self, name):
        # Creates a new userrole with the given name
        c = self.conn.cursor()
        sql = '''INSERT INTO UserRole VALUES
                 (?, ?);'''
        userrole_id = self.generate_new_roleid()
        c.execute(sql, (userrole_id, name,))

    def rename_userrole(self, id, name):
        # Renames a userrole with the given ID
        c = self.conn.cursor()
        sql = '''UPDATE UserRole
                 SET RoleName = ?
                 WHERE RoleID = ?'''
        c.execute(sql, (name, id,))

    def remove_userrole(self, id):
        # Removes a given userrole
        c = self.conn.cursor()
        sql = '''DELETE FROM UserRole
                 WHERE RoleID = ?'''
        c.execute(sql, (id,))

    # User Team Getters
    def get_userteam(self, ID):
        # Takes the ID of a UserTeam and returns the name
        c = self.conn.cursor()
        sql = '''SELECT TeamName
                 FROM UserTeam
                 WHERE TeamID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_all_userteam(self):
        c = self.conn.cursor()
        sql = '''SELECT TeamName, TeamID
                 FROM UserTeam'''
        c.execute(sql)
        return c.fetchall()

    def generate_new_teamid(self):
        # TODO Figure out a method to detect any holes in the sequence of IDs
        # Generates a new unique teamID and returns it
        c = self.conn.cursor()
        sql = '''SELECT MAX(TeamID)
                 FROM UserTeam'''
        c.execute(sql)
        res = c.fetchall()
        if res[0][0] is None:
            return 0
        else:
            return res[0][0]+1

    # User Team setters
    def create_userteam(self, name):
        # Creates a new userteam with the given name
        c = self.conn.cursor()
        sql = '''INSERT INTO UserTeam VALUES
                 (?, ?);'''
        userteam_id = self.generate_new_teamid()
        c.execute(sql, (userteam_id, name,))

    def rename_userteam(self, id, name):
        # Renames a userteam with the given ID
        c = self.conn.cursor()
        sql = '''UPDATE UserTeam
                 SET TeamName = ?
                 WHERE TeamID = ?'''
        c.execute(sql, (name, id,))

    def remove_userteam(self, id):
        # Removes a given userteam
        c = self.conn.cursor()
        sql = '''DELETE FROM UserTeam
                 WHERE TeamID = ?'''
        c.execute(sql, (id,))

    # User Getters
    def get_username(self, ID):
        # Takes the ID of a user and returns the username
        c = self.conn.cursor()
        sql = '''SELECT UserName
                 FROM Users
                 WHERE UserID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_user_gender(self, ID):
        # Takes the ID of a user and returns the gender
        c = self.conn.cursor()
        sql = '''SELECT Gender
                 FROM Users
                 WHERE UserID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_nickname(self, ID):
        # Takes the ID of a user and returns the nickname
        c = self.conn.cursor()
        sql = '''SELECT Nickname
                        FROM Users
                        WHERE UserID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_user_role(self, ID):
        # Takes the ID of a user and returns the userrole
        c = self.conn.cursor()
        sql = '''SELECT UserRole
                        FROM Users
                        WHERE UserID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_user_group(self, ID):
        # Takes the ID of a user and returns the usergroup
        c = self.conn.cursor()
        sql = '''SELECT UserGroup
                        FROM Users
                        WHERE UserID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_user_team(self, ID):
        # Takes the ID of a user and returns the userteam
        c = self.conn.cursor()
        sql = '''SELECT UserTeam
                        FROM Users
                        WHERE UserID = ?'''
        c.execute(sql, (ID,))
        res = c.fetchall()
        return res[0][0]

    def get_userinfo(self, ID):
        # Takes the ID of a user and returns all of the user info
        c = self.conn.cursor()
        sql = '''SELECT *
                        FROM Users
                        WHERE UserID = ?'''
        c.execute(sql, (ID,))
        return c.fetchall()

    def get_all_users(self):
        # Returns a list of tuples of (UserID, UserName)
        c = self.conn.cursor()
        sql = '''SELECT UserID, UserName
                    FROM Users'''
        c.execute(sql)
        return c.fetchall()

    # User Setters
    def generate_new_userid(self):
        # TODO Figure out a method to detect any holes in the sequence of IDs
        # Generates a new unique userid and returns it
        c = self.conn.cursor()
        sql = '''SELECT MAX(UserID)
                 FROM Users'''
        c.execute(sql)
        res = c.fetchall()
        if res[0][0] is None:
            return 0
        else:
            return res[0][0]+1

    def create_user(self, name, gender, nickname=None, role=None, group=None, team=None):
        c = self.conn.cursor()
        sql = '''INSERT INTO Users VALUES 
                    (?, ?, ?, ?, ?, ? ,?)'''
        user_id = self.generate_new_userid()
        c.execute(sql, (user_id, name, gender, nickname, role, group, team))
        self.conn.commit()

    def update_user(self, ID, name, gender, nickname=None, role=None, group=None, team=None, oldID=None):
        c = self.conn.cursor()
        sql = '''UPDATE Users
                    SET UserID = ?,
                    UserName = ?,
                    Gender = ?,
                    Nickname = ?,
                    UserRole = ?,
                    UserGroup = ?,
                    UserTeam = ?
                    WHERE UserID = ?'''
        if oldID is None:
            c.execute(sql, (ID, name, gender, nickname, role, group, team, ID))
        else:
            c.execute(sql, (ID, name, gender, nickname, role, group, team, oldID))
        self.conn.commit()

    def remove_user(self, ID):
        c = self.conn.cursor()
        sql = '''DELETE FROM Users
                    WHERE UserID = ?'''
        c.execute(sql, (ID,))

    # TODO Finish getters and create calculating functions for transactions and so forth

    def submit_transactions(self, transactions):
        # Get a list of tuples with transactions as (UserID, ItemID, Multiplier) and submit them to the
        # database and update the item with sold and current stock
        c = self.conn.cursor()
        # Get max transaction
        sql = '''SELECT MAX(TransID)
                 FROM Transactions'''
        c.execute(sql)
        max_trans = c.fetchall()[0][0]

        # Make new list with the IDs of transactions
        actual_transactions = []
        for transaction in transactions:
            actual_transactions.append((max_trans + 1, transaction[0], transaction[1], transaction[2]))
            max_trans += 1

        # executemany in transactions
        sql = '''INSERT INTO Transactions VALUES
                    (?, ?, ?, ?)'''
        c.executemany(sql, actual_transactions)

        # Update individual items
        for transaction in transactions:
            cur_stock = self.get_item_currentstock(transaction[1])
            sold_stock = self.get_item_soldstock(transaction[1])

            sql = '''UPDATE Item 
                        SET CurrentStock = ?,
                            SoldStock = ?
                        WHERE ItemID = ?'''
            c.execute(sql, (cur_stock-transaction[2], sold_stock+transaction[2], transaction[1]))
