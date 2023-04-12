from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
import firebase_config
# Create your views here.

famous_array=[]
def newCampaign(request):
    docs=firebase_config.firestore_client.collection('famous').stream()
    for doc in docs:
        famousDict=doc.to_dict()
        famous_array.append({"name_ar":famousDict['name_ar'],"name_en":famousDict['name_en']})
    return render(request,"CampaignsApp/new_campaign.html",{'famous_array':famous_array})

def createNewCampaign(request):
    name_arabic=request.POST.get('name_Arabic')
    name_english=request.POST.get('name_English')
    link=request.POST.get('link')
    famous_choose= {} # famous we choosed for this campaign .
    for item in famous_array:
        itemstatus=request.POST.get(item["name_en"])
        if(itemstatus=="checked"):
            # print(item["name_en"])
            famous_choose[item['name_en']]=0

    firebase_config.firestore_client.collection("campaigns").document(name_english).set({
        "name_ar":name_arabic,
        "name_en":name_english,
        "link":link,
        "start_time":firebase_config.firestore.SERVER_TIMESTAMP,
        "famous":famous_choose,
    })

    return HttpResponse("<h1> Campaign {} added successfully.".format(name_english))

