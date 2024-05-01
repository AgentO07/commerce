from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_new_listing", views.create_new_listing, name="create_new_listing"),
    path("active_listing", views.active_listing, name="active_listing"),
    path("listing/<str:req_list>", views.listing, name="req_list"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:called_category>", views.category, name="category"),
    path("Users", views.Users, name="Users")
]
    