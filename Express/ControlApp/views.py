import datetime,pytz

from django.shortcuts import render,redirect
import firebase_config

def indexPage(request):
    # return render(request,"ControlApp/index.html")
    return redirect("http://3.83.172.110:8001/control/campaigns")

campaignsArray=[]
famousArray=[]
notAddedFamous=[]
def campaignsPage(request):
     campaignsArray.clear()
     docs = firebase_config.firestore_client.collection('campaigns').order_by("start_time", direction=firebase_config.firestore.Query.DESCENDING).stream()
     for doc in docs:
         campaignsDict = doc.to_dict()
         start_time=datetime.datetime.fromtimestamp(campaignsDict['start_time'].timestamp(),pytz.timezone('Asia/Riyadh')).strftime("%m-%d-%Y")
         campaignsArray.append({"company":campaignsDict['company'],"name_ar": campaignsDict['name_ar'], "name_en": campaignsDict['name_en'], "link":campaignsDict['link'], "start_time":start_time, "end_time":"0", "famous":campaignsDict['famous']})
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
    notAddedFamous=[]
    campaign=firebase_config.firestore_client.collection("campaigns").document(str(request.GET.get('id'))).get().to_dict()
    campaign['start_time']=datetime.datetime.fromtimestamp(campaign['start_time'].timestamp(),pytz.timezone('Asia/Riyadh')).strftime("%m-%d-%Y %H:%M:%S")
    currentFamousArray=[]
    for k,v in campaign['famous'].items():
        famous=firebase_config.firestore_client.collection("famous").document(str(k)).get().to_dict()
        currentFamousArray.append({"name_en":str(k), "name_ar":famous['name_ar'], 'clicks':str(v)})
    famous=firebase_config.firestore_client.collection("famous").stream()
    for doc in famous:
        fam=doc.to_dict()
        if any(fam['name_en'] in d.values() for d in currentFamousArray):
            continue
        notAddedFamous.append({"name_en":fam['name_en'], "name_ar":fam['name_ar']})
    return render(request,"ControlApp/campaign_edit.html",{"campaign":campaign,"currentFamousArray":currentFamousArray, "notAddedFamous":notAddedFamous})

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