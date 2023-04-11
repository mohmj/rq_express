from django.shortcuts import render, redirect
from pyrebase import pyrebase


def redirect(request):
    famous = request.GET.get("famous") or "no famous assigned"
    website = request.GET.get("website") or "no website assigned"
    return render(request,"RedirectApp_index.html",{"famous":famous,"website":website})
