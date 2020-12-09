import sqlite3
from databaseErr import DatabaseError


class Database(object):
    __DB_NAME = "liquorBar.db"

    def __init__(self, dummy=None):
        if dummy:
            self.__DB_NAME = "liquorBar" + dummy + ".db"
        self.conn = sqlite3.connect(self.__DB_NAME)
        self.cur = self.conn.cursor()
        self.createTableRecipes()

    def __del__(self):
        self.conn.close()

    def close(self):
        self.conn.close()

    def createTableRecipes(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS RECIPES
                        (ID   INTEGER,
                         NAME TEXT    NOT NULL,
                         PATH TEXT    NOT NULL,
                         PRIMARY KEY(ID, NAME, PATH));''')
        self.conn.commit()

    def isRecipeNameExists(self, cocktail_name):
        path = self.cur.execute("SELECT NAME FROM RECIPES WHERE NAME=?", (cocktail_name,))
        return True if path.fetchone() else None

    def isRecipePathExists(self, cocktail_path):
        path = self.cur.execute(f"SELECT PATH FROM RECIPES WHERE PATH=?", (cocktail_path,))
        return True if path.fetchone() else None

    def getRecipePath(self, cocktail_name):
        path = self.cur.execute("SELECT PATH FROM RECIPES WHERE NAME=?", (cocktail_name,)).fetchone()
        return path[0] if path else None

    def addNewRecipe(self, cocktail_name, cocktail_path):
        if self.isRecipeNameExists(cocktail_name):
            err = f'Cannot add to database. Cocktail with name {cocktail_name} already exists.'
            raise DatabaseError(err)
        if self.isRecipePathExists(cocktail_path):
            err = f'Cannot add to database. Cocktail with path {cocktail_path} already exists.'
            raise DatabaseError(err)
        self.cur.execute("INSERT INTO RECIPES (NAME,PATH) VALUES (?, ?)", (cocktail_name, cocktail_path))
        self.conn.commit()

    def deleteRecipe(self, cocktail_name):
        if not self.isRecipeNameExists(cocktail_name):
            err = f"Cannot remove from database. Cocktail with name {cocktail_name} does not exists."
            raise DatabaseError(err)
        self.cur.execute("DELETE FROM RECIPES WHERE NAME=?;", (cocktail_name,))
        self.conn.commit()





