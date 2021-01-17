import sqlite3


class Database(object):
    __DB_NAME = "liquorBar.db"

    def __init__(self, path="liquorBar.db",
                 conn=None, placeholder='?',
                 new=False, dummy=False):
        """
        :param path: physical location of database
        :param conn: override default sqlite3 connection if not None
        :param placeholder: symbol used for safe parameter substitution
        :param new: create recipes and shelf tables if new is True
        :param dummy: add dummy tag to db name for testing purposes if dummy is True
        """
        self.__DB_NAME = path if not dummy else path + "_dummy"
        self.conn = conn if conn is not None else sqlite3.connect(self.__DB_NAME)
        self.cur = self.conn.cursor()
        self.ph = placeholder
        if new:
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
        query = f"SELECT NAME FROM RECIPES WHERE NAME={self.ph}"
        name = self.cur.execute(query, (cocktail_name,))
        return True if name.fetchone() else None

    def isRecipePathExists(self, cocktail_path):
        query = f"SELECT PATH FROM RECIPES WHERE PATH={self.ph}"
        path = self.cur.execute(query, (cocktail_path,))
        return True if path.fetchone() else None

    def getRecipePath(self, cocktail_name):
        query = f"SELECT PATH FROM RECIPES WHERE NAME={self.ph}"
        path = self.cur.execute(query, (cocktail_name,)).fetchone()
        return path[0] if path else None

    def getRecipes(self):
        return self.cur.execute("SELECT NAME, INGR, PATH FROM RECIPES").fetchall()

    def addNewRecipe(self, cocktail_name, cocktail_path, cocktail_ingr=None):
        if self.isRecipeNameExists(cocktail_name):
            err = f'Cannot add to database. Cocktail with name {cocktail_name} already exists.'
            raise DatabaseError(err)
        if self.isRecipePathExists(cocktail_path):
            err = f'Cannot add to database. Cocktail with path {cocktail_path} already exists.'
            raise DatabaseError(err)
        if not cocktail_ingr:
            query = f"INSERT INTO RECIPES (NAME,PATH) VALUES ({self.ph}, {self.ph})"
            self.cur.execute(query, (cocktail_name, cocktail_path))
        else:
            query = f"INSERT INTO RECIPES (NAME,PATH,INGR) VALUES ({self.ph}, {self.ph}, {self.ph})"
            self.cur.execute(query, (cocktail_name, cocktail_path, cocktail_ingr))
        self.conn.commit()

    def deleteRecipe(self, cocktail_name):
        if not self.isRecipeNameExists(cocktail_name):
            err = f"Cannot remove from database. Cocktail with name {cocktail_name} does not exists."
            raise DatabaseError(err)
        query = f"DELETE FROM RECIPES WHERE NAME={self.ph}"
        self.cur.execute(query, (cocktail_name,))
        self.conn.commit()

    #
    # Shelf related
    #

    def isBottleOnShelf(self, bottle_name):
        query = f"SELECT NAME FROM SHELF WHERE NAME={self.ph}"
        name = self.cur.execute(query, (bottle_name,))
        return True if name.fetchone() else None

    def getBottleQty(self, bottle_name):
        query = f"SELECT QTY FROM SHELF WHERE NAME={self.ph}"
        qty = self.cur.execute(query, (bottle_name,)).fetchone()
        return qty[0] if qty else 0

    def getBottles(self):
        return self.cur.execute("SELECT NAME, QTY FROM SHELF").fetchall()

    def addNewBottle(self, bottle_name, bottle_qty):
        if self.isBottleOnShelf(bottle_name):
            err = f'Cannot add to database. Bottle with name {bottle_name} already exists.'
            raise DatabaseError(err)
        query = f"INSERT INTO SHELF (NAME, QTY) VALUES ({self.ph}, {self.ph})"
        self.cur.execute(query, (bottle_name, bottle_qty))
        self.conn.commit()

    def updateBottleQty(self, bottle_name, qty):
        if not self.isBottleOnShelf(bottle_name):
            err = f"Cannot update database. Bottle with name {bottle_name} does not exists."
            raise DatabaseError(err)
        bottle_qty = self.getBottleQty(bottle_name) + qty
        query = f"UPDATE SHELF SET QTY=? WHERE NAME={self.ph}"
        self.cur.execute(query, (bottle_qty, bottle_name))
        self.conn.commit()

    def deleteBottle(self, bottle_name):
        if not self.isBottleOnShelf(bottle_name):
            err = f"Cannot remove from database. Shelf does not contains {bottle_name}."
            raise DatabaseError(err)
        query = f"DELETE FROM SHELF WHERE NAME={self.ph}"
        self.cur.execute(query, (bottle_name,))
        self.conn.commit()


class DatabaseError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'DatabaseError, {self.message}'
        else:
            return f'DatabaseError has ben raised.'
