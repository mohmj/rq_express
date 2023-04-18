import datetime,pytz

from django.shortcuts import render,redirect

import appConfig
import firebase_config

from django.http import HttpResponse

def indexPage(request):
    # return render(request,"ControlApp/index.html")
    return redirect(appConfig.appUrl+"control/campaigns")

campaignsArray=[]
famousArray=[]
notAddedFamous=[]
campaign={}
def campaignsPage(request):
     campaignsArray.clear()
     docs = firebase_config.firestore_client.collection('campaigns').order_by("start_time", direction=firebase_config.firestore.Query.DESCENDING).stream()
     for doc in docs:
         campaignsDict = doc.to_dict()
         start_time=datetime.datetime.fromtimestamp(campaignsDict['start_time'].timestamp(),pytz.timezone('Asia/Riyadh')).strftime("%m-%d-%Y")
         campaignsArray.append({"company":campaignsDict['company'],"name_ar": campaignsDict['name_ar'], "name_en": campaignsDict['name_en'], "link":campaignsDict['link'], "start_time":start_time, "end_time":"0", "famous":campaignsDict['famous']})
     return render(request,"ControlApp/campaigns.html",{"campaignsArray":campaignsArray})


def createNewCampaign(request):
    return redirect(appConfig.appUrl+"campaigns/new")

def showCampaign(request):
    notAddedFamous=[]
    campaign=firebase_config.firestore_client.collection("campaigns").document(str(request.GET.get('id'))).get().to_dict()
    campaign['start_time']=datetime.datetime.fromtimestamp(campaign['start_time'].timestamp(),pytz.timezone('Asia/Riyadh')).strftime("%m-%d-%Y %H:%M:%S")
    currentFamousArray=[]
    viewstotal=0
    viewsApple=0
    viewsAndroid=0
    viewsElse=0
    for k,v in campaign['famous'].items():
        famous=firebase_config.firestore_client.collection("famous").document(str(k)).get().to_dict()
        totalViews=v["views"]
        viewstotal+=totalViews
        appleViews=0
        androidViews=0
        if "Apple" in v["device"]:
            appleViews = int(v['device']['Apple'])
            viewsApple+=appleViews
        if "Android" in v['OS']:
            androidViews = v['OS']['Android']
            viewsAndroid+=androidViews
        elseDevicesViews=totalViews-androidViews-appleViews
        viewsElse=viewstotal-viewsApple-viewsAndroid
        currentFamousArray.append({"name_en":str(k), "name_ar":famous['name_ar'], 'views':{
            'total':totalViews,
            'apple':appleViews,
            'android':androidViews,
            'else':elseDevicesViews
        }})
    famous=firebase_config.firestore_client.collection("famous").stream()
    for doc in famous:
        fam=doc.to_dict()
        if any(fam['name_en'] in d.values() for d in currentFamousArray):
            continue
        notAddedFamous.append({"name_en":fam['name_en'], "name_ar":fam['name_ar']})
    return render(request,"ControlApp/campaign_show.html",{"campaign":campaign,"currentFamousArray":currentFamousArray, "notAddedFamous":notAddedFamous, "views":{
        "total":viewstotal,
        "apple":viewsApple,
        "android":viewsAndroid,
        "else":viewsElse,
    }})

def editCampaign(request):
    famousArray.clear()
    campaign = firebase_config.firestore_client.collection("campaigns").document(str(request.GET.get('id'))).get().to_dict()
    famous = firebase_config.firestore_client.collection("famous").stream()
    for doc in famous:
        fam=doc.to_dict()
        if fam['name_en'] in campaign['famous'].keys():
            continue
        else:
            famousArray.append({"name_ar":fam['name_ar'], "name_en":fam['name_en']})
    return render(request,"ControlApp/campaign_edit.html",{"famousArray":famousArray, "campaign":campaign})

def updateCampaign(request):
    id=request.GET.get("id")
    famous_choose: dict[str, {str, int}] = {}
    print(famousArray)
    for item in famousArray:
        itemstatus=request.POST.get(item["name_en"])
        if (itemstatus == "checked"):
            famous_choose[item['name_en']] = {"views": 0, "Browser": {}, "OS": {}, "device": {}}
    print(famous_choose)
    firebase_config.firestore_client.collection("campaigns").document(id).set({
       "famous":famous_choose
    },merge=True)
    return redirect(appConfig.appUrl+"control/campaigns")

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
    return redirect(appConfig.appUrl+"famous/new")