from django.shortcuts import render, redirect
from django.http import HttpRequest

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