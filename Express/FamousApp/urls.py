from django.urls import path
from . import views

urlpatterns=[
    path('new',views.newFamous),
    path('createFamous',views.createFamous)

]