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
         campaignsDict['start_time']=datetime.datetime.fromtimestamp(campaignsDict['start_time'].timestamp(),pytz.timezone('Asia/Riyadh')).strftime("%m-%d-%Y")
         campaignsArray.append(campaignsDict)
     return render(request,"ControlApp/campaigns.html",{"campaignsArray":campaignsArray})


def createNewCampaign(request):
    return redirect(appConfig.appUrl+"campaigns/new")

def showCampaign(request):
    campaign = firebase_config.firestore_client.collection("campaigns").document(
        str(request.GET.get('id'))).get().to_dict()
    campaign['start_time'] = datetime.datetime.fromtimestamp(campaign['start_time'].timestamp(),
                                                             pytz.timezone('Asia/Riyadh')).strftime("%m-%d-%Y %H:%M:%S")

    notAddedFamous=[]
    currentFamousArray=[]
    viewstotal=0
    viewsApple=0
    viewsAndroid=0
    viewsElse=0
    for k,v in campaign['famous'].items():
        famous=firebase_config.firestore_client.collection("famous").document(str(k)).get().to_dict()
        totalViews=v['views']['total']
        viewstotal+=totalViews
        appleViews=v['views']['apple']
        viewsApple+=appleViews
        androidViews=v['views']['android']
        viewsAndroid+=androidViews
        elseDevicesViews=totalViews-androidViews-appleViews
        currentFamousArray.append({"name_en":str(k), "name_ar":famous['name_ar'], 'views':{
            'total':totalViews,
            'apple':appleViews,
            'android':androidViews,
            'else':elseDevicesViews,
            'snapchat':{
                'apple':v['views']['snapchat']['apple'],
                'android':v['views']['snapchat']['android'],
                'else':v['views']['snapchat']['else'],
                'total':v['views']['snapchat']['total'],
            },
            'instagram':{
                'apple':v['views']['instagram']['apple'],
                'android':v['views']['instagram']['android'],
                'else':v['views']['instagram']['else'],
                'total':v['views']['instagram']['total'],
            },
            'twitter': {
                'apple':v['views']['twitter']['apple'],
                'android':v['views']['twitter']['android'],
                'else':v['views']['twitter']['else'],
                'total':v['views']['twitter']['total'],
            },
            'tiktok':{
                'apple':v['views']['tiktok']['apple'],
                'android':v['views']['tiktok']['android'],
                'else':v['views']['tiktok']['else'],
                'total':v['views']['tiktok']['total'],
            },
            'youtube': {
                'apple':v['views']['youtube']['apple'],
                'android':v['views']['youtube']['android'],
                'else':v['views']['youtube']['else'],
                'total':v['views']['youtube']['total'],
            },
            'facebook': {
                'apple':v['views']['facebook']['apple'],
                'android':v['views']['facebook']['android'],
                'else':v['views']['facebook']['else'],
                'total':v['views']['facebook']['total'],
            },
        }})
    viewsElse = viewstotal - viewsApple - viewsAndroid
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
    famous_choose= {}
    print(famousArray)
    for item in famousArray:
        itemstatus=request.POST.get(item["name_en"])
        if (itemstatus == "checked"):
            famous_choose[item['name_en']] = {"views":{
                'apple':0,
                'android':0,
                'else':0,
                'total':0,
                'snapchat':{
                    'apple':0,
                    'android':0,
                    'else':0,
                    'total':0
                },
                'instagram':{
                    'apple':0,
                    'android':0,
                    'else':0,
                    'total':0
                },
                'twitter':{
                    'apple':0,
                    'android':0,
                    'else':0,
                    'total':0
                },
                'tiktok':{
                    'apple':0,
                    'android':0,
                    'else':0,
                    'total':0
                },
                'youtube':{
                    'apple':0,
                    'android':0,
                    'else':0,
                    'total':0
                },
                'facebook':{
                    'apple':0,
                    'android':0,
                    'else':0,
                    'total':0
                },
            }}
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

