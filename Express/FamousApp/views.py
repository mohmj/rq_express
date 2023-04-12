from django.shortcuts import render, redirect
import firebase_config

def newFamous(request):
    return render(request,"FamousApp/new_famous.html")

def createFamous(request):
    nameArabic=request.POST.get("name_Arabic")
    nameEnglish=request.POST.get("name_English")
    snapchat=request.POST.get("snapchat")
    instagram=request.POST.get("instagram")
    twitter=request.POST.get("twitter")

    firebase_config.firestore_client.collection("famous").document(nameEnglish).set({
        "name_ar":nameArabic,
        "name_en":nameEnglish,
        "snapchat":snapchat,
        "instagram":instagram,
        "twitter":twitter
    })
    return render(request,"FamousApp/new_famous.html")