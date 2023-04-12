from django.shortcuts import render, redirect
from django.http import HttpRequest
import firebase_config

#
# import firebase_admin
# from firebase_admin import firestore
# from firebase_admin import credentials
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# firestore_client = firestore.client()


def RedirectFunction(request):
    famous = request.GET.get("famous") or "no famous assigned"
    website = "https://"+request.GET.get("website")
    campaign=request.GET.get("campaign")
    firebase_config.firestore_client.collection("campaigns").document(campaign).update({
        "famous":{famous:firebase_config.firestore.Increment(1)}
    })
    return redirect(website)
    # return render(request,"RedirectApp_index.html",{"famous":famous,"website":website})

def LoginPage(request):
    return render(request, "login_page.html")

def LoginPost(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    # auth.sign_in_with_email_and_password(email,password)
    # if(auth.current_user != None):
    #     return render(request,"home.html",{"message":"user logged in successfully",})
    return render(request,"home.html",{"message":"user failed login",})