from django.shortcuts import render, redirect
from pyrebase import pyrebase
import firebase_admin
from firebase_admin import firestore
firebaseConfig = {
  "apiKey": "AIzaSyA0G9sz2UgL2JonD2bdRSPoaW1hLvvhrHE",
  "authDomain": "rq-express-dev.firebaseapp.com",
  "projectId": "rq-express-dev",
  "storageBucket": "rq-express-dev.appspot.com",
  "messagingSenderId": "841781456816",
  "appId": "1:841781456816:web:b702055f9fd74f83c8b075",
  "measurementId": "G-YKEL44CZEH"
};
def redirect(request):
    famous = request.GET.get("famous") or "no famous assigned"
    website = request.GET.get("website") or "https://google.com"
    return redirect(website)
    # return render(request,"RedirectApp_index.html",{"famous":famous,"website":website})
