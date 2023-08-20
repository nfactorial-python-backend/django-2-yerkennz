from django.urls import path
from . import views

app_name = "news"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:news_id>/", views.detail, name="detail"),
    path("add/", views.add, name="add"),
    path("<int:news_id>/edit/", views.NewsEditView.as_view(), name="edit_news"),
]