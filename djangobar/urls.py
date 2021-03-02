"""djangoBar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import url
from django.db import connection
from barmanshell.barmanshell import BarmanShell
from myshelf.views import home_view
from myshelf.views import myshelf_view, myshelf_edit_view, myshelf_del_view
from recipe.views import recipe_view, recipe_detail_view

barman = BarmanShell.djangoParams(connection)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),

    path('myshelf/', myshelf_view, kwargs={'barman': barman}),
    path('myshelf/sort_name/', myshelf_view, kwargs={'barman': barman, 'sort': 'name'}),
    path('myshelf/sort_qty/', myshelf_view, kwargs={'barman': barman, 'sort': 'qty'}),
    path('myshelf/edit/<str:bottle_name>/', myshelf_edit_view, kwargs={'barman': barman}),
    path('myshelf/del/<str:bottle_name>/', myshelf_del_view, kwargs={'barman': barman}),

    path('recipes/', recipe_view, kwargs={'barman': barman}),
    path('recipes/<str:recipe_name>/', recipe_detail_view, kwargs={'barman': barman}),

    url(r'^favicon\.ico$', RedirectView.as_view(url='favicon.ico')),
]


