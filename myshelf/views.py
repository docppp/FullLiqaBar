from django.shortcuts import render, redirect
from barmanshell.barmanshell import BarmanCopy
from .models import ShelfForm


def home_view(request, *args, **kwargs):
    context = {}
    return render(request, "base.html", context)


def myshelf_view(request, *args, **kwargs):
    form = ShelfForm(request.POST or None)

    if request.method == "GET":
        barman = BarmanCopy.useBarman(kwargs.get('barman'))
        shelf = barman.getShelf()
        shelf.reverse()
        if kwargs.get('sort') == 'name':
            shelf.sort(key=lambda x: x[0])
        if kwargs.get('sort') == 'qty':
            shelf.sort(key=lambda x: x[1], reverse=True)

        context = {
            'bottle_list': shelf,
            'form': form
        }
        return render(request, "shelf.html", context)

    if request.method == "POST":
        if form.is_valid():
            form.save()
        return redirect("/myshelf/")


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
