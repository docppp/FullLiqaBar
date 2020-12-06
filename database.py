import sqlite3


class Database(object):
    __DB_NAME = "liquorBar.db"

    def __init__(self):
        self.connection = sqlite3.connect(self.__DB_NAME)
        self.cur = self.connection.cursor()
        self.createTableRecipes()

    def __del__(self):
        self.connection.close()

    def close(self):
        self.connection.close()

    def createTableRecipes(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS RECIPES
                        (ID   INTEGER,
                         NAME TEXT    NOT NULL,
                         PATH TEXT    NOT NULL,
                         PRIMARY KEY(ID, NAME, PATH));''')

    def getRecipePath(self, cocktail_name):
        path = self.cur.execute(f"SELECT PATH FROM RECIPES WHERE NAME='{cocktail_name}'")
        if path.fetchone() is None:
            return None
        return path.fetchone()[0]


# db = Database()
# db.cur.execute("INSERT INTO RECIPES (NAME,PATH) \
#       VALUES ('Paul', 'path');")
# c = db.cur.execute("SELECT PATH FROM RECIPES WHERE NAME='Paula'")
# db.connection.close()



