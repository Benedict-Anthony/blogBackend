from django.urls import path

from .views import CategoryView, CommentView, PostView, PostCRUDView

urlpatterns = [
    path("", PostView.as_view()),
    path("mutate/", PostCRUDView.as_view()),
    path("comment/", CommentView.as_view()),
    path("categories/", CategoryView.as_view()),
    path("mutate/<slug:slug>/", PostCRUDView.as_view()),
    path("<slug:slug>/", PostView.as_view()),
]