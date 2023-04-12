from django.urls import path
from . import views

urlpatterns=[
    path('new',views.newCampaign),
    path('createNewCampaign',views.createNewCampaign)
]