from django.shortcuts import render, redirect
import sys
from django.http import HttpRequest
# from pyrebase import pyrebase
firebaseConfig = {
  "apiKey": "AIzaSyA0G9sz2UgL2JonD2bdRSPoaW1hLvvhrHE",
  "authDomain": "rq-express-dev.firebaseapp.com",
  "projectId": "rq-express-dev",
  "storageBucket": "rq-express-dev.appspot.com",
  "messagingSenderId": "841781456816",
  "appId": "1:841781456816:web:b702055f9fd74f83c8b075",
  "measurementId": "G-YKEL44CZEH"
}

# firebase=pyrebase.initialize_app(firebaseConfig)
# auth=firebase.auth()
def RedirectFunction(request):
    # famous = request.GET.get("famous") or "no famous assigned"
    website = request.GET.get("website") or "https://google.com"
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