from django.template.defaultfilters import title
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="page"),
    path("search_entry", views.search_entry, name="search_entry"),
]
