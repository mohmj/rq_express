from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
import firebase_config
# Create your views here.
def newCampaign(request):
    docs=firebase_config.firestore_client.collection('famous').stream()
    famous_array=[]
    for doc in docs:
        famousDict=doc.to_dict()
        famous_array.append({"name_ar":famousDict['name_ar'],"name_en":famousDict['name_en']})
    print(famous_array)
    return render(request,"CampaignsApp/new_campaign.html",{'famous_array':famous_array})

def createNewCampaign(request):
    name_arabic=request.POST.get('name_Arabic')
    name_english=request.POST.get('name_English')
    link=request.POST.get('link')
    firebase_config.firestore_client.collection("campaigns").document(name_english).set({
        "name_ar":name_arabic,
        "name_en":name_english,
        "link":link,
        "start_time":firebase_config.firestore.SERVER_TIMESTAMP
    })
    return HttpResponse("<h1> Campaign {} added successfully.".format(name_english))

