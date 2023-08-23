from django.urls import path
from . import views

app_name = "news"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:news_id>/", views.detail, name="detail"),
    path("add/", views.add, name="add"),
    path("<int:news_id>/edit/", views.NewsEditView.as_view(), name="edit_news"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("<int:news_id>/delete-news/", views.delete_news, name="delete_news"),
    path("<int:news_id>/delete-comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),

    path("api/", views.api_index, name="api_index"),
    path("api/news", views.api_post, name="api_post"),
    # path("api/news/<int:pk>/", views.api_news_detail, name="api_news_detail"),
    path("api/news/<int:pk>/", views.NewsDetailView.as_view(), name="api_news_detail"),
    path("api/news/", views.NewsList.as_view(), name="api_news_list"),
]