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
        list_of_three = []
        for i in range(ceil(len(shelf)/3)):
            list_of_three.append(shelf[i*3:i*3+3])
        context = {
            'alc_group_by_three': list_of_three
        }
        return render(request, "shelf.html", context)
