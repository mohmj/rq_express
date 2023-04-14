import datetime

from django.shortcuts import render,redirect
import firebase_config

def indexPage(request):
    # return render(request,"ControlApp/index.html")
    return redirect("http://3.83.172.110:8001/control/campaigns")

campaignsArray=[]
famousArray=[]
def campaignsPage(request):
     campaignsArray.clear()
     docs = firebase_config.firestore_client.collection('campaigns').order_by("start_time", direction=firebase_config.firestore.Query.DESCENDING).stream()
     for doc in docs:
         campaignsDict = doc.to_dict()
         campaignsArray.append({"company":campaignsDict['company'],"name_ar": campaignsDict['name_ar'], "name_en": campaignsDict['name_en'], "link":campaignsDict['link'], "start_time":"00/00/0000", "end_time":"0", "famous":campaignsDict['famous']})
     return render(request,"ControlApp/campaigns.html",{"campaignsArray":campaignsArray})

def showCampaign(request):

    # id=request.POST.get("id")
    # print("The id: "+id)
    campaignData=firebase_config.firestore_client.collection("campaigns").document("sinjar_eid").get()
    print("The type is"+str(type(campaignData)))
    return (request,"ControlApp/campaign_show",{"campaign":campaignData})

def createNewCampaign(request):
    return redirect("http://3.83.172.110:8001/campaigns/new")

def editCampaign(request):
    return "a"

def famousPage(request):
    famousArray.clear()
    docs = firebase_config.firestore_client.collection('famous').stream()
    for doc in docs:
        famousDict = doc.to_dict()
        famousArray.append({"name_ar": famousDict['name_ar'],
                               "name_en": famousDict['name_en'], "snapchat": famousDict['snapchat'],
                               "instagram": famousDict['instagram'],"twitter": famousDict['twitter'],})
    return render(request,"ControlApp/famous.html",{"famousArray":famousArray})

def addNewFamous(request):
    return redirect("http://3.83.172.110:8001/famous/new")