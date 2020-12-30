import sqlite3
from databaseErr import DatabaseError


class Database(object):
    __DB_NAME = "liquorBar.db"

    def __init__(self, dummy=None):
        if dummy:
            self.__DB_NAME = "liquorBar" + dummy + ".db"
        self.conn = sqlite3.connect(self.__DB_NAME)
        self.cur = self.conn.cursor()
        self.__createTableRecipes()
        self.__createTableShelf()

    def __del__(self):
        self.conn.close()

    def __createTableShelf(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS SHELF
                        (ID   INTEGER,
                         NAME TEXT     NOT NULL,
                         QTY  INTEGER  NOT NULL,
                         PRIMARY KEY(ID, NAME));''')
        self.conn.commit()

    def __createTableRecipes(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS RECIPES
                        (ID   INTEGER,
                         NAME TEXT     NOT NULL,
                         PATH TEXT     NOT NULL,
                         INGR TEXT,
                         PRIMARY KEY(ID, NAME, PATH));''')
        self.conn.commit()

    def close(self):
        self.conn.close()

    #
    # Recipe related
    #

    def isRecipeNameExists(self, cocktail_name):
        name = self.cur.execute("SELECT NAME FROM RECIPES WHERE NAME=?", (cocktail_name,))
        return True if name.fetchone() else None

    def isRecipePathExists(self, cocktail_path):
        path = self.cur.execute(f"SELECT PATH FROM RECIPES WHERE PATH=?", (cocktail_path,))
        return True if path.fetchone() else None

    def getRecipePath(self, cocktail_name):
        path = self.cur.execute("SELECT PATH FROM RECIPES WHERE NAME=?", (cocktail_name,)).fetchone()
        return path[0] if path else None

    def addNewRecipe(self, cocktail_name, cocktail_path, cocktail_ingr=None):
        if self.isRecipeNameExists(cocktail_name):
            err = f'Cannot add to database. Cocktail with name {cocktail_name} already exists.'
            raise DatabaseError(err)
        if self.isRecipePathExists(cocktail_path):
            err = f'Cannot add to database. Cocktail with path {cocktail_path} already exists.'
            raise DatabaseError(err)
        if not cocktail_ingr:
            self.cur.execute("INSERT INTO RECIPES (NAME,PATH) VALUES (?, ?)", (cocktail_name, cocktail_path))
        else:
            self.cur.execute("INSERT INTO RECIPES (NAME,PATH,INGR) VALUES (?, ?, ?)",
                             (cocktail_name, cocktail_path, cocktail_ingr))
        self.conn.commit()

    def deleteRecipe(self, cocktail_name):
        if not self.isRecipeNameExists(cocktail_name):
            err = f"Cannot remove from database. Cocktail with name {cocktail_name} does not exists."
            raise DatabaseError(err)
        self.cur.execute("DELETE FROM RECIPES WHERE NAME=?;", (cocktail_name,))
        self.conn.commit()

    #
    # Shelf related
    #

    def isBottleOnShelf(self, bottle_name):
        name = self.cur.execute("SELECT NAME FROM SHELF WHERE NAME=?", (bottle_name,))
        return True if name.fetchone() else None

    def getBottleQty(self, bottle_name):
        qty = self.cur.execute("SELECT QTY FROM SHELF WHERE NAME=?", (bottle_name,)).fetchone()
        return qty[0] if qty else 0

    def getBottles(self):
        return self.cur.execute("SELECT NAME, QTY FROM SHELF").fetchall()

    def addNewBottle(self, bottle_name, bottle_qty):
        if self.isBottleOnShelf(bottle_name):
            err = f'Cannot add to database. Bottle with name {bottle_name} already exists.'
            raise DatabaseError(err)
        self.cur.execute("INSERT INTO SHELF (NAME, QTY) VALUES (?, ?)", (bottle_name, bottle_qty))
        self.conn.commit()

    def updateBottleQty(self, bottle_name, qty):
        if not self.isBottleOnShelf(bottle_name):
            err = f"Cannot update database. Bottle with name {bottle_name} does not exists."
            raise DatabaseError(err)
        bottle_qty = self.getBottleQty(bottle_name) + qty
        self.cur.execute("UPDATE SHELF SET QTY=? WHERE NAME=?", (bottle_qty, bottle_name))
        self.conn.commit()

    def deleteBottle(self, bottle_name):
        if not self.isBottleOnShelf(bottle_name):
            err = f"Cannot remove from database. Shelf does not contains {bottle_name}."
            raise DatabaseError(err)
        self.cur.execute("DELETE FROM SHELF WHERE NAME=?;", (bottle_name,))
        self.conn.commit()
