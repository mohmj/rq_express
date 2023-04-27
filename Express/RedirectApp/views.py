from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import firebase_config
from django_user_agents.utils import get_user_agent

#
# import firebase_admin
# from firebase_admin import firestore
# from firebase_admin import credentials
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
# firestore_client = firestore.client()


def RedirectFunction(request):
    user_agent = get_user_agent(request)
    famous = request.GET.get("famous") or "no famous assigned"
    website = request.GET.get("website")
    campaign=request.GET.get("campaign")
    platformUse=request.GET.get("platform")
    device=""
    if(user_agent.device.brand=="Apple"):
        device="apple"
    elif(user_agent.os.family=="Android"):
        device="android"
    else:
        device="else"

    firebase_config.firestore_client.collection("campaigns").document(campaign).set({
        "famous":{
            famous:{
                "views":{
                    "total":firebase_config.Increment(1),
                    device:firebase_config.Increment(1),
                    platformUse:{
                        device:firebase_config.Increment(1),
                        'total':firebase_config.Increment(1),
                    }
                }
            }
        }
    }, merge=True)
    return redirect(website)

def LoginPage(request):
    return render(request, "login_page.html")

def LoginPost(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    # auth.sign_in_with_email_and_password(email,password)
    # if(auth.current_user != None):
    #     return render(request,"home.html",{"message":"user logged in successfully",})
    return render(request,"home.html",{"message":"user failed login",})