import os
import sqlite3
from database import Database
from databaseErr import DatabaseError
from ingredients import Recipe, Alcohol, Filler, Addon


# TODO:
# addNewRecipe(recipe)
#   adds recipe as list of ingredients to db
#   return nothing
#
# addBottleToShelf(name, qty)
#   name is alcohol name
#   qty is bottle quantity
#   adds qty to proper row in shelf db
#   return nothing
#
# getShelf()
#     return list of pair alcohol, qty
#
# getRecipes()
#     return list of all recipes
#
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

    def __init__(self):
        self.db = Database()

    def addNewRecipe(self, recipe_name, list_of_ingr):
        print(f"Adding new recipe {recipe_name} to database.")

        if self.db.isRecipeNameExists(recipe_name):
            print(f"WARNING: Cocktail {recipe_name} already exists in database.")
            return False

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

        try:
            file_path = os.path.join("Recipes", recipe_name + ".xml")
            f = open(file_path, "x")
            f.write(xml_string)
            f.close()
        except FileExistsError:
            print("ERROR: Cannot create new recipe file.")
            return False

        try:
            self.db.addNewRecipe(recipe_name, file_path, ingr)
        except DatabaseError:
            print("ERROR: Cannot add recipe to database.")
            print("Removing newly added recipe file.")
            os.remove(file_path)
            return False

        print(f"SUCCESS: Recipe {recipe_name} added to database.")
        return True

    def addBottleToShelf(self, bottle_name, bottle_qty):
        print(f"Adding new bottle {bottle_name} to database.")
        try:
            self.db.addNewBottle(bottle_name, bottle_qty)
        except DatabaseError:
            print("ERROR: Cannot add bottle to database.")
            return False
        print(f"SUCCESS: Bottle {bottle_name} added to database.")
        return True

    def getShelf(self):
        print("Getting bottles info.")
        try:
            bottles = self.db.getBottles()
        except sqlite3.Error:
            print("ERROR: Cannot get bottles info.")
            return False
        print(f"SUCCESS: Got bottles info: {bottles}")
        return bottles




