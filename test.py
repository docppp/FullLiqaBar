import sqlite3
import unittest
import database
import os
import ingredients


class TestDatabaseRecipes(unittest.TestCase):

    db = None
    dummy = 'Dummy'

    @classmethod
    def setUpClass(cls):
        cls.db = database.Database(cls.dummy)
        cls.db.cur.execute("INSERT INTO RECIPES (NAME,PATH) \
                           VALUES ('obviously-dummy-cocktail', 'obviously-dummy-path');")
        cls.db.conn.commit()

    @classmethod
    def tearDownClass(cls):
        cls.db.cur.execute("DELETE FROM RECIPES;")
        cls.db.conn.commit()
        cls.db.close()
        os.remove("liquorBar" + cls.dummy + ".db")

    def test_1databaseObjectConnects(self):
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

    def test_changesCommits(self):
        db_checker = database.Database(self.dummy)
        name = "obviously-almost-existing-cocktail"
        path = "obviously-almost-existing-path"
        self.db.addNewRecipe(name, path)
        self.assertTrue(db_checker.isRecipeNameExists(name))
        self.assertTrue(db_checker.isRecipePathExists(path))
        self.db.deleteRecipe(name)
        self.assertFalse(db_checker.isRecipeNameExists(name))
        self.assertFalse(db_checker.isRecipePathExists(path))
        db_checker.close()


class TestIngredients(unittest.TestCase):

    def test_ingredientClassName(self):
        self.assertEqual(ingredients.Ingredient.className(), "Ingredient")

    def test_availableUnits(self):
        self.assertEqual(ingredients.Ingredient.availableUnits, ['ml', 'szt', 'g'])

    def test_xmlParserHelperFunctions(self):
        xml_string = "<Alcohol qty='1000' unit='ml'>Alcohol Name</Alcohol>"
        self.assertEqual(ingredients.XmlParser._XmlParser__getClassFromTag(xml_string), "Alcohol")
        self.assertEqual(ingredients.XmlParser._XmlParser__getQtyFromTag(xml_string), "1000")
        self.assertEqual(ingredients.XmlParser._XmlParser__getUnitFromTag(xml_string), "ml")
        self.assertEqual(ingredients.XmlParser._XmlParser__getNameFromTag(xml_string), "Alcohol Name")

    def test_xmlParserStringFormat(self):
        alc = ingredients.Alcohol("Alcohol Name", 1000)
        alc_xml = ingredients.XmlParser(alc).xml_string
        alc_str = "<Alcohol qty='1000' unit='ml'>Alcohol Name</Alcohol>"
        self.assertEqual(alc_xml, alc_str)

        fil = ingredients.Filler("Filler Name", 100)
        fil_xml = ingredients.XmlParser(fil).xml_string
        fil_str = "<Filler qty='100' unit='ml'>Filler Name</Filler>"
        self.assertEqual(fil_xml, fil_str)

        add = ingredients.Addon("Addon Name", 30, "g")
        add_xml = ingredients.XmlParser(add).xml_string
        add_str = "<Addon qty='30' unit='g'>Addon Name</Addon>"
        self.assertEqual(add_xml, add_str)

    def test_xmlParserFromString(self):
        alc_str = "<Alcohol qty='1000' unit='ml'>Alcohol Name</Alcohol>"
        alc = ingredients.Alcohol("Alcohol Name", 1000)
        alc_from_xml = ingredients.XmlParser(alc_str).ingr
        self.assertEqual(alc.name, alc_from_xml.name)
        self.assertEqual(alc.qty, alc_from_xml.qty)
        self.assertEqual(alc.unit, alc_from_xml.unit)

    def test_xmlParserRaises(self):
        # something went wrong here. FIXIT
        pass


if __name__ == '__main__':
    unittest.main()
