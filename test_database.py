import sqlite3
import unittest
import database


class TestDatabaseRecipes(unittest.TestCase):

    def setUp(self):
        self.db = database.Database()

    def test_databaseObjectConnects(self):
        self.assertTrue(isinstance(self.db.connection, sqlite3.Connection))

    def test_tableRecipesExists(self):
        table = self.db.cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='RECIPES'")
        table_name = next(iter(table))[0]
        self.assertEqual(table_name, "RECIPES")

    def test_getNonExistingRecipePathReturnNone(self):
        path = self.db.getRecipePath("obiusly-non-existing-cocktail")
        self.assertIsNone(path)


if __name__ == '__main__':
    unittest.main()
