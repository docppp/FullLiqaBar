from django.shortcuts import render
from barmanshell.barmanshell import BarmanShell
from django.http import HttpResponse



def home_view(request, *args, **kwargs):
    context = {}
    return render(request, "main.html", context)


def myshelf_view(request, *args, **kwargs):
    if request.method == "GET":
        #barman = BarmanShell(db_path="db.sqlite3")
        context = {}
        #alc = barman.getShelf()
        alc = "sdsd"
        return HttpResponse("<h1>" + str(alc) + "</h1>")
