import unittest
import database
import ingredients


class TestDatabase(unittest.TestCase):

    db = None

    @classmethod
    def setUpClass(cls):
        cls.db = database.Database(dummy=True)
        cls.db.cur.execute("INSERT INTO RECIPES (NAME, PATH) \
                           VALUES ('obviously-dummy-cocktail', 'obviously-dummy-path');")
        cls.db.cur.execute("INSERT INTO SHELF (NAME, QTY) \
                           VALUES ('obviously-dummy-bottle', 500);")
        cls.db.cur.execute("INSERT INTO SHELF (NAME, QTY) \
                            VALUES ('obviously-dummy-bottle2', 700);")
        cls.db.conn.commit()

    @classmethod
    def tearDownClass(cls):
        from os import remove
        cls.db.cur.execute("DELETE FROM RECIPES;")
        cls.db.cur.execute("DELETE FROM SHELF;")
        cls.db.conn.commit()
        cls.db.close()
        remove(database.Database._Database__DB_NAME + "_dummy")

    def test_checkIfAllMethodsAreCovered(self):
        test_members = list(TestDatabase.__dict__.keys())
        class_members = list(database.Database.__dict__.keys())
        check_for = ['test_' + x for x in class_members if not x.startswith('_')]
        are_covered = all(test in test_members for test in check_for)
        if not are_covered:
            diff = list(set(check_for)-set(test_members))
            print("Database functions that are not covered: ", diff)
            self.assertTrue(False)

    def test_isRecipeNameExists(self):
        self.assertFalse(self.db.isRecipeNameExists("obviously-non-existing-cocktail"))
        self.assertTrue(self.db.isRecipeNameExists("obviously-dummy-cocktail"))

    def test_isBottleOnShelf(self):
        self.assertFalse(self.db.isBottleOnShelf("obviously-non-existing-bottle"))
        self.assertTrue(self.db.isBottleOnShelf("obviously-dummy-bottle"))

    def test_isRecipePathExists(self):
        self.assertFalse(self.db.isRecipePathExists("obviously-non-existing-path"))
        self.assertTrue(self.db.isRecipePathExists("obviously-dummy-path"))

    def test_getRecipePath(self):
        path = self.db.getRecipePath("obviously-dummy-cocktail")
        path_none = self.db.getRecipePath("obviously-non-existing-cocktail")
        self.assertIsNone(path_none)
        self.assertEqual(path, "obviously-dummy-path")

    def test_getBottleQty(self):
        qty = self.db.getBottleQty("obviously-dummy-bottle")
        qty_none = self.db.getBottleQty("obviously-non-existing-bottle")
        self.assertEqual(qty_none, 0)
        self.assertEqual(qty, 500)

    def test_getRecipes(self):
        recipes = self.db.getRecipes()
        self.assertEqual(recipes, [('obviously-dummy-cocktail', None)])

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

    def test_addNewBottle(self):
        name = "obviously-almost-existing-bottle"
        self.db.addNewBottle(name, 500)
        self.assertTrue(self.db.isBottleOnShelf(name))
        self.db.cur.execute("DELETE FROM SHELF WHERE NAME=?;", (name,))
        self.db.conn.commit()
        self.assertFalse(self.db.isBottleOnShelf(name))

    def test_getBottles(self):
        bottles = self.db.getBottles()
        check = [('obviously-dummy-bottle', 500), ('obviously-dummy-bottle2', 700)]
        self.assertEqual(bottles, check)

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

    def test_deleteBottleRaise(self):
        with self.assertRaises(database.DatabaseError):
            self.db.deleteBottle("obviously-non-existing-bottle")

    def test_deleteBottle(self):
        name = "obviously-almost-existing-bottle"
        self.db.addNewBottle(name, 500)
        self.assertTrue(self.db.isBottleOnShelf(name))
        self.db.deleteBottle(name)
        self.assertFalse(self.db.isBottleOnShelf(name))

    def test_updateBottleQtyRaise(self):
        with self.assertRaises(database.DatabaseError):
            self.db.updateBottleQty("obviously-non-existing-bottle", 40)

    def test_updateBottleQty(self):
        name = 'obviously-dummy-bottle'
        previous_qty = self.db.getBottleQty(name)
        self.db.updateBottleQty(name, 40)
        new_qty = self.db.getBottleQty(name)
        self.assertEqual(previous_qty + 40, new_qty)
        self.db.updateBottleQty(name, -100)
        newest_qty = self.db.getBottleQty(name)
        self.assertEqual(previous_qty + 40 - 100, newest_qty)

    def test_changesCommits(self):
        db_checker = database.Database(dummy=True)
        name = "obviously-almost-existing-cocktail"
        path = "obviously-almost-existing-path"
        bottle = "obviously-almost-existing-bottle"
        self.db.addNewRecipe(name, path)
        self.db.addNewBottle(bottle, 500)
        self.assertTrue(db_checker.isRecipeNameExists(name))
        self.assertTrue(db_checker.isRecipePathExists(path))
        self.assertTrue(db_checker.isBottleOnShelf(bottle))
        self.db.deleteRecipe(name)
        self.db.deleteBottle(bottle)
        self.assertFalse(db_checker.isRecipeNameExists(name))
        self.assertFalse(db_checker.isRecipePathExists(path))
        self.assertFalse(db_checker.isBottleOnShelf(bottle))
        db_checker.close()

    def test_close(self):
        # must be here, so all methods from Database are covered
        pass


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
</Recipe>
"""
    name = "Gin and Tonic"
    alc = [ingredients.Alcohol("Gin", 20), ingredients.Alcohol("Gin2", 50)]
    fil = [ingredients.Filler("Tonic", 80)]
    add = [ingredients.Addon("Limonka", 0.5, "szt")]

    def test_checkIfAllMethodsAreCovered(self):
        test_members = list(TestRecipe.__dict__.keys())
        class_members = list(ingredients.Recipe.__dict__.keys())
        check_for = ['test_' + x for x in class_members if not x.startswith('_')]
        are_covered = all(test in test_members for test in check_for)
        if not are_covered:
            diff = list(set(check_for)-set(test_members))
            print("Recipe functions that are not covered: ", diff)
            self.assertTrue(False)

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
