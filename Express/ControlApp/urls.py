from django.urls import path
from . import views

urlpatterns=[
    path('',views.indexPage),
    path('campaigns', views.campaignsPage),
    path('campaigns/campaignShow',views.showCampaign),
    path('campaigns/newCampaign',views.createNewCampaign),
    path('campaigns/campaignShow',views.showCampaign),
    path('campaigns/campaignEdit', views.editCampaign),
    path('campaigns/campaignUpdate',views.updateCampaign),


    path('famous', views.famousPage),
    path('famous/newFamous', views.addNewFamous)
]