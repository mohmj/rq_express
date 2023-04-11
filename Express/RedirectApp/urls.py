from django.urls import path
from . import views

urlpatterns=[
    path('',views.RedirectFunction),
    path('login', views.LoginPage),
    path('loginPost', views.LoginPost)
]