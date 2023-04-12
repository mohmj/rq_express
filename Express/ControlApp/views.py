from django.shortcuts import render,redirect
import firebase_config

def indexPage(request):
    return render(request,"ControlApp/index.html")

def campaignsPage(request):
     # docs=firebase_config.firestore_client.collection("campaigns").stream
    return render(request,"ControlApp/campaigns.html")

def famousPage(request):
    return render(request,"ControlApp/famous.html")

