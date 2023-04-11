from django.shortcuts import render, redirect
# from pyrebase import pyrebase


def redirect(request):
    famous = request.GET.get("famous") or "no famous assigned"
    website = request.GET.get("website") or "no website assigned"
    return render("test working correctly, {0} & {1}".format(famous,website))
