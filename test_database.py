import sqlite3
import unittest
import database


class TestDatabaseRecipes(unittest.TestCase):

    db = None

    @classmethod
    def setUpClass(cls):
        cls.db = database.Database()
        cls.db.cur.execute("INSERT INTO RECIPES (NAME,PATH) \
                           VALUES ('obviously-dummy-cocktail', 'obviously-dummy-path');")
        cls.db.conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.db.cur.execute("DELETE FROM RECIPES WHERE NAME='obviously-dummy-cocktail';")
        cls.db.conn.commit()

    def test_databaseObjectConnects(self):
        self.assertTrue(isinstance(self.db.conn, sqlite3.Connection))

    def test_tableRecipesExists(self):
        table = self.db.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='RECIPES'")
        table_name = next(iter(table))[0]
        self.assertEqual(table_name, "RECIPES")

    def test_isRecipeNameExistsReturnValue(self):
        self.assertFalse(self.db.isRecipeNameExists("obviously-non-existing-cocktail"))
        self.assertTrue(self.db.isRecipeNameExists("obviously-dummy-cocktail"))

    def test_isRecipePathExistsReturnValue(self):
        self.assertFalse(self.db.isRecipePathExists("obviously-non-existing-path"))
        self.assertTrue(self.db.isRecipePathExists("obviously-dummy-path"))

    def test_getRecipePathReturnValue(self):
        path = self.db.getRecipePath("obviously-dummy-cocktail")
        path_none = self.db.getRecipePath("obviously-non-existing-cocktail")
        self.assertIsNone(path_none)
        self.assertEqual(path, "obviously-dummy-path")

    def test_addNewRecipeRaise(self):
        with self.assertRaises(database.DatabaseError):
            self.db.addNewRecipe("obviously-non-existing-cocktail", "obviously-dummy-path")
        with self.assertRaises(database.DatabaseError):
            self.db.addNewRecipe("obviously-dummy-cocktail", "obviously-non-existing-path")

    def test_addNewRecipe(self):
        name = "obviously-almost-existing-cocktail"
        path = "obviously-almost-existing-path"
        self.db.addNewRecipe(name, path)
        self.assertTrue(self.db.isRecipeNameExists(name))
        self.assertTrue(self.db.isRecipePathExists(path))
        self.db.cur.execute("DELETE FROM RECIPES WHERE NAME=?;", (name,))
        self.db.conn.commit()
        self.assertFalse(self.db.isRecipeNameExists(name))
        self.assertFalse(self.db.isRecipePathExists(path))

    def test_deleteRecipeRaise(self):
        with self.assertRaises(database.DatabaseError):
            self.db.deleteRecipe("obviously-non-existing-cocktail")

    def test_deleteRecipe(self):
        name = "obviously-almost-existing-cocktail"
        path = "obviously-almost-existing-path"
        self.db.addNewRecipe(name, path)
        self.assertTrue(self.db.isRecipeNameExists(name))
        self.assertTrue(self.db.isRecipePathExists(path))
        self.db.deleteRecipe(name)
        self.assertFalse(self.db.isRecipeNameExists(name))
        self.assertFalse(self.db.isRecipePathExists(path))


if __name__ == '__main__':
    unittest.main()
