from django.shortcuts import render
from barmanshell.barmanshell import getRecipesFromAllFiles
from barmanshell.ingredients import RecipeParser


def recipe_view(request, *args, **kwargs):
    if request.method == "GET":
        barman = kwargs.get('barman')
        recipes = getRecipesFromAllFiles()
        recipes.sort(key=lambda x: x['recipe'].name)
        recipes_html = [RecipeParser.toHtmlString(x['recipe']) for x in recipes]
        context = {
            'recipes': recipes_html
        }
        return render(request, "recipe.html", context)
