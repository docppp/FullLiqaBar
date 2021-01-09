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

    def __init__(self, db_path=path.join(".", "liquorBar.db"), new=False):
        print(f"Initializing BarmanShell with database located at {db_path}.")
        self.db = Database(path=db_path, new=new)
        if new:
            recipes = getRecipesFromAllFiles()
            for recipe in recipes:
                r = recipe["recipe"]
                f = recipe["file"]
                try:
                    self.db.addNewRecipe(r.name, f, ",".join(r.listOfIngrNames()))
                except DatabaseError:
                    continue

    def addNewRecipe(self, recipe_name, list_of_ingr):
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

        file_path = writeRecipeToFile(recipe_name, xml_string)

        try:
            self.db.addNewRecipe(recipe_name, file_path, ingr)
        except InterfaceError:
            return False
        except DatabaseError as e:
            print(e.message)
            return False

        print(f"SUCCESS: Recipe {recipe_name} added to database.")
        return True

    def addNewRecipeFromXml(self, xml_string):
        print("Adding new recipe from xml to database.")

        try:
            recipe = Recipe.fromXmlString(xml_string)
        except (TypeError, AttributeError, ParseError):
            print("ERROR: Cannot convert xml to recipe.")
            return False

        success = self.addNewRecipe(recipe.name, recipe.listOfIngr())

        if not success:
            print("ERROR: Could not add recipe from xml.")
            return False

        print("SUCCESS: Recipe added from xml to database.")
        return True

    def addBottleToShelf(self, bottle_name, bottle_qty):
        print(f"Adding new bottle {bottle_name} to database.")
        try:
            self.db.addNewBottle(bottle_name, bottle_qty)
        except DatabaseError as e:
            print(e.message)
            return False
        print(f"SUCCESS: Bottle {bottle_name} added to database.")
        return True

    def changeBottleByQty(self, bottle_name, qty):
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

    def getShelf(self):
        print("Getting bottles info.")
        try:
            bottles = self.db.getBottles()
        except InterfaceError:
            print("ERROR: Cannot get bottles info.")
            return False
        print(f"SUCCESS: Got bottles info: {bottles}")
        return bottles

    def getRecipes(self):
        print("Getting recipes info.")
        try:
            recipes = self.db.getRecipes()
        except InterfaceError:
            print("ERROR: Cannot get recipes info.")
            return False
        print(f"SUCCESS: Got recipes info.")
        return recipes


def writeRecipeToFile(recipe_name, xml_string):
    from os import path
    file_path = path.join("recipes", recipe_name + ".xml")
    try:
        f = open(file_path, "x")
        f.write(xml_string)
        f.close()
    except FileExistsError:
        print("WARNING: File already exists.")
        print("Checking if file content is the same.")
        f = open(file_path, "r")
        file_content = f.read()
        f.close()
        if file_content != xml_string:
            print("ERROR: File content is different.")
            return False
        print("File content is valid.")
    return file_path


def getRecipesFromAllFiles():
    from os import path, listdir
    recipes = []
    files = [path.join("recipes", f) for f in listdir("recipes")]
    print(f"Found {len(files)} recipe files.")

    for file in files:
        f = open(file, "r")
        content = f.read()
        f.close()
        try:
            recipes.append({"recipe": Recipe.fromXmlString(content),
                           "file": file})
        except (TypeError, AttributeError, ParseError):
            print(f"ERROR: Cannot convert {file} to recipe. Continuing.")

    print(f"Got {len(recipes)} valid recipes.")
    return recipes


# b = BarmanShell(db_path="db.sqlite3")
# print(b.getRecipes())
# b.getShelf()
