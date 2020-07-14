from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random"),
    path("add", views.add, name="add"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("<str:entry>", views.entry, name="entry")
]

