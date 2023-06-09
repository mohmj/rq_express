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
    path('campaigns/home',views.returnHomeControl),


    path('famous', views.famousPage),
    path('famous/newFamous', views.addNewFamous),
    path('famous/famousShow',views.showFamous),
    path('famous/famousEdit',views.editFamous),
    path('famous/famousUpdate',views.updateFamous)
]