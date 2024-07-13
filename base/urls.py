from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("post/<int:pk>", views.postdetail, name="post_detail"),
    path("search", views.searchresult, name="search_result"),
    path('sign-in', views.sign_in, name='sign_in'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('sign-out', views.sign_out, name='sign_out'),
    path("category/<str:pk>", views.category, name="category"),
    path('create', views.create_post, name='create_post'),
]

