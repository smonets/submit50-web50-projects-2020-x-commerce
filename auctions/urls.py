from django.urls import path

from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path('categories', views.categories, name="categories"),
    path('categories/<int:category_id>', views.category_items, name="category_items"),

]
