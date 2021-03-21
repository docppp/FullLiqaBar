from django.shortcuts import render, redirect
from barmanshell.barmanshell import BarmanCopy
from .models import ShelfForm


def home_view(request, *args, **kwargs):
    context = {}
    return render(request, "base.html", context)


def sort_shelf(shelf, sort):
    shelf.reverse()
    should_reverse = False

    if sort_shelf.prev_sort == sort:
        should_reverse = True
    sort_shelf.prev_sort = 'Default' if should_reverse else sort

    if sort == 'Sort by name':
        shelf.sort(key=lambda x: x[0], reverse=should_reverse)
    elif sort == 'Sort by quantity':
        shelf.sort(key=lambda x: x[1], reverse=not should_reverse)
    else:
        sort_shelf.prev_sort = 'Default'


sort_shelf.prev_sort = 'Default'


def myshelf_view(request, *args, **kwargs):
    barman = BarmanCopy.useBarman(kwargs.get('barman'))
    form = ShelfForm(request.POST or None)

    if request.method == "GET":
        shelf = barman.getShelf()

        sort_shelf(shelf, request.GET.get('sort'))

        context = {
            'bottle_list': shelf,
            'form': form
        }
        return render(request, "shelf.html", context)

    if request.method == "POST":
        if "button_delete" in request.POST:
            barman.deleteBottle(request.POST.get('button_delete'))
            return redirect("/myshelf/")

        if "button_add" in request.POST:
            bottles = [bottle[0] for bottle in barman.getShelf()]
            if form.is_valid() and form.cleaned_data.get("name") not in bottles:
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
