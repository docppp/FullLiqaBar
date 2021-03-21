from sqlite3 import InterfaceError
from xml.etree.ElementTree import ParseError
from .database import Database, DatabaseError
from .ingredients import Recipe
from os import path

# TODO:
# getRecipeByIngr(ingr_name)
#     return all recipes when ingr_name appears
#
# getAvailableRecipes()
#     return all recipes where all alcohol are in shelf
#
# drinkCocktail(name)
#     remove alv qty from recipe in shelf db rows
#     return nothing


class BarmanShell:

    @classmethod
    def djangoParams(cls, conn):
        """
        Creates BarmanShell object adjusted for django.

        :param conn: must be connection from django.db module.
        :return: Initialized BarmanShell with recipes in db.
        """
        return cls(db_path="db.sqlite3", conn=conn, placeholder="%s", new=True)

    def __init__(self, db_path=path.join(".", "liquorBar.db"),
                 conn=None, placeholder='?', new=False):
        """
        :param db_path: physical location of used database.
        :param conn: override default sqlite3 connection if used.
        :param placeholder: override default sqlite3 placeholder if used.
        :param new: add all recipes found in recipe folder to database if True.
        """
        print(f"Initializing BarmanShell with database located at {db_path}.")
        self.db = Database(path=db_path, conn=conn, placeholder=placeholder, new=new)
        if new:
            self.recipes = self.getRecipesFromAllFiles()
            for recipe in self.recipes:
                r = recipe["recipe"]
                f = recipe["file"]
                try:
                    self.db.addNewRecipe(r.name, f, ",".join(r.listOfIngrNames()))
                except DatabaseError:
                    continue
        bottles = len(self.db.getBottles())
        recipes = len(self.db.getRecipes())
        print(f"BarmanShell initialized with {bottles} bottles and {recipes} recipes.")

    def addNewRecipe(self, recipe_name, list_of_ingr) -> bool:
        """
        :param recipe_name: recipe name
        :type recipe_name: str
        :param list_of_ingr: list of Ingredient objects.
        :type list_of_ingr: list[Ingredient]
        :return: True if success, otherwise False.
        """
        print(f"Adding recipe {recipe_name} to database.")

        alcohols = [x for x in list_of_ingr if x.ingrType == 'Alcohol']
        fillers = [x for x in list_of_ingr if x.ingrType == 'Filler']
        addons = [x for x in list_of_ingr if x.ingrType == 'Addon']

        try:
            recipe = Recipe(recipe_name, alcohols, fillers, addons)
            ingr = ",".join(recipe.listOfIngrNames())
            xml_string = recipe.toXmlString()
        except (TypeError, AttributeError):
            print("ERROR: Cannot convert to recipe.")
            return False

        file_path = self.writeRecipeToFile(recipe_name, xml_string)

        try:
            self.db.addNewRecipe(recipe_name, file_path, ingr)
        except InterfaceError:
            return False
        except DatabaseError as e:
            print(e.message)
            return False

        print(f"SUCCESS: Recipe {recipe_name} added to database.")
        return True

    def addBottleToShelf(self, bottle_name, bottle_qty) -> bool:
        """
        :param bottle_name: alcohol name
        :type bottle_name: str
        :param bottle_qty: alcohol quantity in milliliters
        :type bottle_qty: int
        :return: True if success, otherwise False.
        """
        print(f"Adding new bottle {bottle_name} to database.")
        try:
            self.db.addNewBottle(bottle_name, bottle_qty)
        except DatabaseError as e:
            print(e.message)
            return False
        print(f"SUCCESS: Bottle {bottle_name} added to database.")
        return True

    def changeBottleByQty(self, bottle_name, qty) -> bool:
        """
        :param bottle_name: bottle name to be changed
        :type bottle_name: str
        :param qty: value that qty is changed by
        :type qty: int
        :return: True if success, otherwise False.
        """
        print(f"Changing qty of {bottle_name} by {qty}.")
        try:
            self.db.updateBottleQty(bottle_name, qty)
        except DatabaseError as e:
            print(e.message)
            return False
        if self.db.getBottleQty(bottle_name) <= 0:
            print("Bottle qty drop to zero. Removing from shelf.")
            self.db.deleteBottle(bottle_name)
        return True

    def getShelf(self) -> list[tuple]:
        """
        :return: List of tuples (name, qty) if success, otherwise empty list
        """
        print("Getting bottles info.")
        try:
            bottles = self.db.getBottles()
        except InterfaceError:
            print("ERROR: Cannot get bottles info.")
            return []
        print(f"SUCCESS: Got bottles info: {bottles}")
        return bottles

    def deleteBottle(self, bottle_name) -> bool:
        """
        :param bottle_name: bottle name to be deleted\
        :type bottle_name: str
        :return: True if successfully deleted given bottle name, otherwise False
        """
        print(f"Deleting bottle {bottle_name}.")
        try:
            self.db.deleteBottle(bottle_name)
        except DatabaseError as e:
            print(e.message)
            return False
        return True

    def getRecipes(self) -> list[tuple]:
        """
        :return: List of tuples (id, name, path, ingr csv) if success, otherwise empty list
        """
        print("Getting recipes info.")
        try:
            recipes = self.db.getRecipes()
        except InterfaceError:
            print("ERROR: Cannot get recipes info.")
            return []
        print(f"SUCCESS: Got recipes info.")
        return recipes

    def checkRecipeReq(self, recipe) -> bool:
        """
        :param recipe: Recipe to be checked
        :type recipe: Recipe
        :return: True if shelf contains recipe's alcohols, otherwise False
        """
        for alc in recipe.alcohols:
            required = int(alc.qty)
            shelf = self.db.getBottleQty(alc.name)
            if shelf < required:
                return False
        return True

    @staticmethod
    def writeRecipeToFile(recipe_name, xml_string) -> str:
        """
        :param recipe_name: name of recipe, also name of file
        :type recipe_name: str
        :param xml_string: string with all recipe data
        :type xml_string: str
        :return: path of newly created file if success, False otherwise
        """
        file_path = path.join("recipes", recipe_name + ".xml")
        try:
            f = open(file_path, "x")
            f.write(xml_string)
            f.close()
        except FileExistsError:
            print("WARNING: File already exists.")
            print("Checking if file content is the same.")
            f = open(file_path, "r", encoding="utf-8")
            file_content = f.read()
            f.close()
            if file_content != xml_string:
                print("ERROR: File content is different.")
                return ""
            print("File content is valid.")
        return file_path

    @staticmethod
    def getRecipesFromAllFiles() -> list[dict[str, Recipe]]:
        """
        :return: List of dict with fields 'recipe':Recipe and 'file':str
        """
        from os import listdir
        recipes = []
        files = [path.join("recipes", f) for f in listdir("recipes")]
        print(f"Found {len(files)} recipe files.")

        for file in files:
            f = open(file, "r", encoding="utf-8")
            content = f.read()
            f.close()
            try:
                recipes.append({"recipe": Recipe.fromXmlString(content),
                               "file": file})
            except (TypeError, AttributeError, ParseError):
                print(f"ERROR: Cannot convert {file} to recipe. Continuing.")

        print(f"Got {len(recipes)} valid recipes.")
        return recipes


class BarmanCopy:
    @staticmethod
    def useBarman(barman) -> BarmanShell:
        """
        Workaround so ide knows the type of barman from dictionary

        :type barman: BarmanShell
        :return: the same barman as in input
        """
        return barman
