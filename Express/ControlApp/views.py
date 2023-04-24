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
    return redirect(appConfig.appUrl+"control/campaigns/campaignShow?id="+id)

def famousPage(request):
    famousArray.clear()
    docs = firebase_config.firestore_client.collection('famous').stream()
    for doc in docs:
        famousDict = doc.to_dict()
        famousArray.append({"name_ar": famousDict['name_ar'],
                               "name_en": famousDict['name_en'], "snapchat": famousDict['snapchat'],
                               "instagram": famousDict['instagram'],"twitter": famousDict['twitter'],})
    return render(request,"ControlApp/famous.html",{"famousArray":famousArray})

def showFamous(request):
    campaignsArray.clear()
    id=request.GET.get('id')
    views={"total":0,"apple":0,"android":0,"else":0}
    famous=firebase_config.firestore_client.collection("famous").document(id).get().to_dict()
    campaigns=firebase_config.firestore_client.collection("campaigns").order_by("start_time", direction=firebase_config.firestore.Query.DESCENDING).stream()
    for campaign in campaigns:
        camp=campaign.to_dict()
        for k,v in camp['famous'].items():
            if k==id:
                dic={"name_en":camp['name_en'],"name_ar":camp['name_ar'],"company":camp['company'],"link":camp['link'],
                     "views_total":int(camp['famous'][id]['views']),
                     }
                views['total']+=dic['views_total']
                if "Apple" in camp['famous'][id]["device"]:
                    dic['views_apple'] = int(camp['famous'][id]["device"]['Apple'])
                    views['apple']+=dic['views_apple']
                else:
                    dic['views_apple'] =0
                if "Android" in camp['famous'][id]['OS']:
                    dic['views_android'] = int(camp['famous'][id]['OS']['Android'])
                    views['android']+=dic['views_android']
                else:
                    dic['views_android'] = 0
                dic['views_else']=dic['views_total']-dic['views_apple']-dic['views_android']
                views['else']+=dic['views_else']
                campaignsArray.append(dic)
                break

    return render(request,"ControlApp/famous_show.html",{"famous":famous,"campaigns":campaignsArray, "views":views})

def editFamous(request):
    id=str(request.GET.get('id'))
    famous=firebase_config.firestore_client.collection('famous').document(id).get().to_dict()
    return render(request,"ControlApp/famous_edit.html",{"famous":famous})

def updateFamous(request):
    id=str(request.GET.get('id'))
    firebase_config.firestore_client.collection("famous").document(id).set({
       "snapchat":str(request.POST.get('snapchat')),
       "instagram": str(request.POST.get('instagram')),
       "twitter": str(request.POST.get('twitter')),
    },merge=True)
    return render(request,"ControlApp/famous.html")

def addNewFamous(request):
    return render(request,"FamousApp/new_famous.html")

def returnHomeControl():
    return render(appConfig.appUrl+"control")

