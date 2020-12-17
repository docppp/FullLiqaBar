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
        self.assertEqual(ingredients.Ingredient.ingrType(), "Ingredient")
        self.assertEqual(ingredients.Alcohol.ingrType(), "Alcohol")
        self.assertEqual(ingredients.Filler.ingrType(), "Filler")
        self.assertEqual(ingredients.Addon.ingrType(), "Addon")

    def test_availableUnits(self):
        self.assertEqual(ingredients.Ingredient.availableUnits, ['ml', 'szt', 'g'])

    def test_unitValueInCreatedIngr(self):
        self.assertEqual(ingredients.Alcohol("name", 100).unit, "ml")
        self.assertEqual(ingredients.Filler("name", 100).unit, "ml")
        self.assertEqual(ingredients.Addon("name", 100, "szt").unit, "szt")


class TestRecipe(unittest.TestCase):

    xml_string = """<Recipe>
    <Name>Gin and Tonic</Name>
    <Ingredients>
        <Alcohol quantity="20" unit="ml">Gin</Alcohol>
        <Alcohol quantity="50" unit="ml">Gin2</Alcohol>
        <Filler quantity="80" unit="ml">Tonic</Filler>
        <Addon quantity="0.5" unit="szt">Limonka</Addon>
    </Ingredients>
</Recipe>"""
    name = "Gin and Tonic"
    alc = [ingredients.Alcohol("Gin", 20), ingredients.Alcohol("Gin2", 50)]
    fil = [ingredients.Filler("Tonic", 80)]
    add = [ingredients.Addon("Limonka", 0.5, "szt")]

    def test_listOfIngr(self):
        r = ingredients.Recipe(self.name, self.alc, self.fil, self.add)
        self.assertEqual(r.listOfIngr(), self.alc + self.fil + self.add)

    def test_listOfIngrNames(self):
        r = ingredients.Recipe(self.name, self.alc, self.fil, self.add)
        names = [x.name for x in (self.alc + self.fil + self.add)]
        self.assertEqual(r.listOfIngrNames(), names)

    def test_fromXmlString(self):
        r = ingredients.Recipe.fromXmlString(self.xml_string)
        self.assertEqual(r.name, "Gin and Tonic")
        self.assertEqual(str(r.listOfIngr()), str(self.alc + self.fil + self.add))

    def test_toXmlString(self):
        r = ingredients.Recipe(self.name, self.alc, self.fil, self.add)
        self.assertEqual(r.toXmlString(), self.xml_string)





if __name__ == '__main__':
    unittest.main()
