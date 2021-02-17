from django.shortcuts import render
from barmanshell.barmanshell import BarmanCopy
from math import ceil


def home_view(request, *args, **kwargs):
    context = {}
    return render(request, "base.html", context)


def myshelf_view(request, *args, **kwargs):
    if request.method == "GET":
        barman = BarmanCopy.useBarman(kwargs.get('barman'))
        shelf = barman.getShelf()

        context = {
            'bottle_list': shelf
        }
        return render(request, "shelf.html", context)

    if request.method == "POST":
        print(request)
        print(args)
        print(kwargs)
        return 1


def myshelf_edit_view(request, *args, **kwargs):
    if request.method == "GET":
        barman = BarmanCopy.useBarman(kwargs.get('barman'))
        bottle_qty = barman.db.getBottleQty(kwargs.get('bottle_name'))
        list_of_three = [(kwargs.get('bottle_name'), bottle_qty)]
        context = {'alc_group_by_three': list_of_three}
        return render(request, "shelf.html", context)


def myshelf_del_view(request, *args, **kwargs):
    if request.method == "GET":
        barman = BarmanCopy.useBarman(kwargs.get('barman'))
        bottle_qty = barman.db.getBottleQty(kwargs.get('bottle_name'))
        list_of_three = [(kwargs.get('bottle_name'), bottle_qty)]
        context = {'alc_group_by_three': list_of_three}
        return render(request, "shelf.html", context)
