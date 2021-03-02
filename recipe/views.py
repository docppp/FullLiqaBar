from django.shortcuts import render
from barmanshell.barmanshell import BarmanCopy


def recipe_view(request, *args, **kwargs):
    if request.method == "GET":
        barman = BarmanCopy.useBarman(kwargs.get('barman'))
        barman.recipes.sort(key=lambda x: x['recipe'].name)

        names = [x['recipe'].name for x in barman.recipes]
        recipes_html = [x['recipe'].toHtmlString() for x in barman.recipes]
        allowed = [barman.checkRecipeReq(x['recipe']) for x in barman.recipes]

        context = {'recipes': zip(names, recipes_html, allowed)}
        return render(request, "recipe.html", context)


def recipe_detail_view(request, *args, **kwargs):
    if request.method == "GET":
        barman = BarmanCopy.useBarman(kwargs.get('barman'))
        recipe = next((x['recipe'].toHtmlString() for x in barman.recipes
                       if x['recipe'].name == kwargs.get('recipe_name')), None)
        context = {'recipe': recipe}
        return render(request, "recipe_detail.html", context)
