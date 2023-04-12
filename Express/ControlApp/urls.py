from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path('',views.indexPage),
    path('famousPage',views.famousPage),
    path('campaignsPage',views.campaignsPage),

]