from django.shortcuts import render, redirect

# Create your views here.
def newCampaign(request):
    return render(request,"CampaignsApp/new_campaign.html")