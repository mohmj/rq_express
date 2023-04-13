from django.urls import path
from . import views

urlpatterns=[
    path('',views.indexPage),
    path('campaigns', views.campaignsPage),
    path('famous', views.famousPage),
    path('campaigns/campaignShow',views.showCampaign),
]