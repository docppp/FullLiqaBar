from django.shortcuts import render
from barmanshell.barmanshell import BarmanCopy, BarmanShell

recipes = BarmanShell.getRecipesFromAllFiles()
recipes.sort(key=lambda x: x['recipe'].name)


def recipe_view(request, *args, **kwargs):
    if request.method == "GET":
        barman = BarmanCopy.useBarman(kwargs.get('barman'))

        ids = [x[0] for x in barman.getRecipes()]
        recipes_html = [x['recipe'].toHtmlString() for x in recipes]
        allowed = [barman.checkRecipeReq(x['recipe']) for x in recipes]

        context = {
            'recipes': zip(ids, recipes_html, allowed)
        }
        return render(request, "recipe.html", context)


def recipe_detail_view(request, *args, **kwargs):
    if request.method == "GET":
        barman = BarmanCopy.useBarman(kwargs.get('barman'))
        context = kwargs
        return render(request, "recipe_detail.html", context)
