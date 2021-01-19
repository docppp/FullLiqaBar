from django.shortcuts import render
from barmanshell.barmanshell import BarmanCopy


def recipe_view(request, *args, **kwargs):
    if request.method == "GET":
        barman = BarmanCopy.useBarman(kwargs.get('barman'))
        barman.recipes.sort(key=lambda x: x['recipe'].name)
        ids = [x[0] for x in barman.getRecipes()]
        recipes_html = [x['recipe'].toHtmlString() for x in barman.recipes]
        allowed = [barman.checkRecipeReq(x['recipe']) for x in barman.recipes]

        context = {
            'recipes': zip(ids, recipes_html, allowed)
        }
        return render(request, "recipe.html", context)


def recipe_detail_view(request, *args, **kwargs):
    if request.method == "GET":
        barman = BarmanCopy.useBarman(kwargs.get('barman'))
        recipe = barman.db.getRecipeById(kwargs.get('recipe_id'))
        context = {'recipe': recipe}
        return render(request, "recipe_detail.html", context)
