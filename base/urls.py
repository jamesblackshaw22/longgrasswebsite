from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("create-field/", views.createField, name="create-field"),
    path("join-field/", views.joinField, name="join-field"),
    path("create-indecision/", views.createIndecision, name="create-indecision"),
    path("<str:room_code>/", views.home, name="home"),
    # path("create-status/"),
]
