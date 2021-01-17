from django.shortcuts import render
from barmanshell.barmanshell import getRecipesFromAllFiles
from math import ceil


def recipe_view(request, *args, **kwargs):
    if request.method == "GET":
        recipes = getRecipesFromAllFiles()
        tryhtml = "<h1>Hello</h1>"
        context = {'try': tryhtml}
        print(recipes)
        return render(request, "recipe.html", context)
