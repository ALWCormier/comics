from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.db import models
from django.conf import settings
from .forms import LoginForm
from .models import Comic, Series, Artist

from comicgeeks import Comic_Geeks
import ast
import os
from unidecode import unidecode
import pandas as pd


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('/')

        return render(request, 'login.html', {'form': form})


def home_view(request):

    if not request.user.is_authenticated:
        return redirect("/login")
    context = {}

    comics = Comic.objects.filter(users__id=request.user.id)
    series = Series.objects.filter(comic__in=comics).order_by("name")

    series_to_comic_map = {}
    for item in series:
        series_to_comic_map[item] = list(Comic.objects.filter(series=item).order_by("number"))

    context["series_list"] = series_to_comic_map

    return render(request, 'home.html', context)


def add_view(request, series_id=""):

    if not request.user.is_authenticated:
        return redirect("/login")

    # these are parameters intended to be passed to context
    results = []
    series_html = ""
    series_data = []

    if not series_id:

        if request.method == "POST":

            # set up API client
            client = Comic_Geeks()
            client.login("alwcormier", ".b!zEA5NLKj-2Ke")

            # is using search bar, using query to get series from API
            if "search" in request.POST:
                qstring = request.POST.get("search")
                series_list = client.search_series(qstring)
                i = 0
                for item in series_list:
                    # limit to only 10 results
                    if i > 19:
                        break
                    series = client.series_info(item.series_id)
                    try:
                        results.append({"name": series.name, "cover": series.cover, "number": series.start_year,
                                        "id": item.series_id})
                    except:
                        i -= 1
                        continue
                    i += 1
            # otherwise, post request means get issues
            else:
                qstring = request.POST.get("series_id")
                series = client.series_info(qstring)
                issues = series.issues
                series_html = series.name
                series_data = [series_html, qstring]
                for item in issues:
                    results.append({"cover": item.cover, "number": item.number,
                                    "variants": item.variant_covers, "id": item.issue_id})

    context = {"series": series_html, "series_data": series_data, "results": results}

    return render(request, 'add.html', context)


def record_view(request):

    if request.method == "POST" and request.user.is_authenticated:

        databundle = request.POST.get("issue_data")
        databundle = ast.literal_eval(databundle)
        series_cgid = int(databundle["series_cgid"])

        # check is series already exists
        if not Series.objects.filter(cgid=series_cgid):
            client = Comic_Geeks()
            client.login("alwcormier", ".b!zEA5NLKj-2Ke")
            new_series = client.series_info(series_cgid)
            series_data = [new_series.name, new_series.start_year, series_cgid, new_series.cover]
            series_obj = Series.objects.create_series(series_data)
        else:
            series_obj = Series.objects.filter(cgid=series_cgid)[0]

        comicdata = {"name": f"{databundle['name']} #{databundle['number']}", 'number': databundle['number'], "image": databundle["cover"],
                     "comic_geeks_code": databundle["issue_cgid"]}
        variant_data = request.POST.get("variant")
        # adding a comic with a variant cover, replace default image and such
        if variant_data != "Default":
            variant_data = ast.literal_eval(variant_data)
            comicdata["name"] = variant_data[0]
            comicdata["image"] = variant_data[1]

            # get artist name
            df = pd.read_excel(os.sep.join([settings.MEDIA_ROOT, "DC_Creators.xlsx"]))
            names_list = df["Names"]
            artist_name = ""
            for name in names_list:
                if name in unidecode(variant_data[0]):
                    artist_name = name
            # check if artist exists in the database
            artist_qset = Artist.objects.filter(name=artist_name)
            if not artist_qset:
                artist = Artist.objects.create(name=artist_name)
                comicdata["artist"] = artist
            else:
                comicdata["artist"] = artist_qset[0]

        Comic.objects.create_comic(comicdata, request.user, series_obj)

        return JsonResponse({"status": "success", "id": databundle["issue_cgid"]})
    else:
        print("something ain't right")
        return JsonResponse({'status': 'failure'})


def remove_view(request):
    if request.method == "POST" and request.user.is_authenticated:

        issue_id = request.POST.get("delete")
        issue_obj = Comic.objects.filter(id=issue_id)[0]
        issue_obj.users.remove(request.user)
        issue_obj.save()
        return JsonResponse({"status": "success", "id": issue_id})

    else:
        return JsonResponse({"status": "failure"})
