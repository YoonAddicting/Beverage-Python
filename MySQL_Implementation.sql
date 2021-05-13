CREATE DATABASE IF NOT EXISTS BeveragePython;
USE BeveragePython;

CREATE TABLE IF NOT EXISTS UserTeam(
	TeamID INT UNSIGNED PRIMARY KEY,
    TeamName VARCHAR(40) NOT NULL);
CREATE TABLE IF NOT EXISTS UserGroup(
	GroupID INT UNSIGNED PRIMARY KEY,
    GroupName VARCHAR(40) NOT NULL);
CREATE TABLE IF NOT EXISTS UserRole(
	RoleID INT UNSIGNED PRIMARY KEY,
    RoleName VARCHAR(40) NOT NULL);
CREATE TABLE IF NOT EXISTS Multipliers(
	MulID BIGINT UNSIGNED PRIMARY KEY,
    MulValue INT NOT NULL);
CREATE TABLE IF NOT EXISTS Gender(
	GenderID INT(1) PRIMARY KEY,
    GenderName VARCHAR(6) NOT NULL);
CREATE TABLE IF NOT EXISTS Category(
	CategoryID INT PRIMARY KEY,
    CategoryName VARCHAR(40) NOT NULL);
    
INSERT INTO Gender VALUES 
	(0, "Female"),
    (1, "Male");
    
INSERT INTO Multipliers (MulID, MulValue) VALUES 
	(820000000000, 0),
    (820000000001, 1),
    (820000000002, 2),
    (820000000003, 3),
    (820000000004, 4),
    (820000000005, 5),
    (820000000006, 6),
    (820000000010, 10),
    (820000000012, 12),
    (820000000015, 15),
    (820000000024, 24),
    (820000000030, 30);
    
CREATE TABLE IF NOT EXISTS Item(
	ItemID BIGINT(13) UNSIGNED PRIMARY KEY,
    ItemName VARCHAR(40) NOT NULL,
    ItemPrice DECIMAL(6,2) NOT NULL,
    StartStock INT(5) NOT NULL,
    SoldStock INT(5) NOT NULL,
    CurrentStock INT(5) NOT NULL,
    LostStock INT(5) NOT NULL,
    Category INT(4),
    FOREIGN KEY (Category) REFERENCES Category(CategoryID) ON DELETE SET NULL);

CREATE TABLE IF NOT EXISTS Users(
	UserID INT(4) PRIMARY KEY,
    UserName VARCHAR(40) NOT NULL,
    Gender INT(1) NOT NULL,
    Nickname VARCHAR(40),
    UserRole INT(4) UNSIGNED,
    UserGroup INT(4) UNSIGNED,
    UserTeam INT(4) UNSIGNED,
    FOREIGN KEY (Gender) REFERENCES Gender(GenderID),
    FOREIGN KEY (UserTeam) REFERENCES UserTeam(TeamID) ON DELETE SET NULL,
    FOREIGN KEY (UserGroup) REFERENCES UserGroup(GroupID) ON DELETE SET NULL,
    FOREIGN KEY (UserRole) REFERENCES UserRole(RoleID) ON DELETE SET NULL);
    
CREATE TABLE IF NOT EXISTS Transactions(
	TransID BIGINT(10) UNSIGNED PRIMARY KEY,
    UserID INT(4) NOT NULL,
    Item BIGINT(13) UNSIGNED NOT NULL,
    Multiplier INT(3) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE,
    FOREIGN KEY (Item) REFERENCES Item(ItemID)ON DELETE CASCADE);
    
    
INSERT INTO UserRole (RoleID, RoleName) VALUES 
	(1, "KABS"),
    (2, "Vektor"),
    (3, "Hyttebums"),
    (4, "Rus");
    
INSERT INTO UserGroup (GroupID, GroupName) VALUES
	(1, "Kalles Kaviar"),
    (2, "Adidas Aber"),
    (3, "Gulddamerne"),
    (4, "Næsehornene"),
    (5, "McBombers");
    
INSERT INTO UserTeam (TeamID, TeamName) VALUES
	(1, "S/M-KID"),
    (2, "NSA"),
    (3, "LiSE"),
    (4, "Medico"),
    (5, "SAS");
INSERT INTO Category VALUES
	(1, "Beer");
    
INSERT INTO Item VALUES
	(5740700301568, "Tuborg Julebryg Dåse", 5.00, 10, 0 , 10, 0, 1),
    (5740700301544, "Tuborg Grøn Dåse", 4.00, 10, 0 , 10, 0, 1);
    
INSERT INTO Users VALUES
	(1, "Jonas", 1, "Dr. Jones", 2, 1, 1),
    (2, "RockTown", 1, "QWABS", 1, 2, 1);
    
INSERT INTO Transactions (TransID, UserID, Item, Multiplier) VALUES
	(1, 1, 5740700301568, 3);

UPDATE Item
	SET CurrentStock = 7, SoldStock = 3
    WHERE ItemID = 5740700301544;
    
INSERT INTO Transactions (TransID, UserID, Item, Multiplier) VALUES
	(2, 2, 5740700301568, 10);
    
UPDATE Item
	SET CurrentStock = 0, SoldStock = 10
    WHERE ItemID = 5740700301568;
    
SELECT * FROM Transactions 
	WHERE UserID = 1;
SELECT * FROM Item;

SELECT UserID, SUM(Multiplier * ItemPrice)
FROM Transactions NATURAL JOIN Item
GROUP BY UserID;