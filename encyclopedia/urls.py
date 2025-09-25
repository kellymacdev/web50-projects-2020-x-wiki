from django.template.defaultfilters import title
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.page, name="page"),
    path("search_entry", views.search_entry, name="search_entry"),
    #path("create_page", views.create_page, name="create_page"),
    path("create_entry", views.create_entry, name="create_entry"),
    path("wiki/<str:title>/edit", views.edit_entry, name="edit_entry"),
]
