from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ExtendedUserCreationForm, CustomPasswordResetForm
from django.contrib.auth import authenticate, login,logout
from .models import leket_DB
import pandasql as ps
import pandas as pd
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


import csv
from . import algorithm_functions


@login_required
@csrf_exempt
def LeketIsraelApp(request):
    if request.method == 'POST':
        # Redirect to a success page
        return redirect('HomePage')
    else:
        # Render the form page
        return render(request, 'main.html')

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def results(request):
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    shmita_year = request.GET.get('shmita-year')
    weather_conditions = request.GET.get('weather-conditions')
    amount_rain = request.GET.get('amount-rain')
    epidemic = request.GET.get('epidemic')
    war = request.GET.get('war')
    print("printing the GET request in results:", request.GET)

    with open('results.csv', newline='') as csvfile:
        data = list(csv.DictReader(csvfile))
    print(data)
    return render(request, 'results.html', {'data': data, 'start_date': start_date, 'end_date': end_date,
                                            'shmita_year': shmita_year,
                                            'weather_conditions': weather_conditions,
                                            'amount_rain': amount_rain,
                                            'epidemic': epidemic, 'war': war})
@login_required
def HomePage(request):
    template = loader.get_template('HomePage.html')
    if not request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, 'Please login to access this page.')
    locations = leket_DB.objects.values_list('leket_location', flat=True).distinct()

    all_records = leket_DB.objects.all()
    record_values = all_records.values()
    df = pd.DataFrame.from_records(record_values)

    q2 = """
      SELECT distinct type
      FROM df
      GROUP BY type
      HAVING count(*) > 500
    """
    df1 = ps.sqldf(q2, locals())
    type = df1['type'].tolist()

    napa_name = leket_DB.objects.values_list('napa_name', flat=True).distinct()

    return render(request, 'HomePage.html', {'locations': locations, 'type':type, 'napa_name':napa_name})


def my_view(request):
    with open('results.csv', newline='') as csvfile:
        data = list(csv.DictReader(csvfile))
    print(data)
    return render(request, 'results.html', {'data': data})


def signup(request):
    if request.method == "POST":
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = ExtendedUserCreationForm()
    return render(request, "registration/signup.html", {"form":form})


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and User.objects.filter(username=username).exists() and user.check_password(password):
            login(request, user)
            return LeketIsraelApp(request)

        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'registration/login.html')

def custom_logout(request):
    logout(request)
    return redirect('login')


from urllib.parse import unquote
import json
def check_original(request):
    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    location = request.GET.get('location')
    chag = request.GET.get('chag')
    type = request.GET.get('type')
    napa_name = request.GET.get('napa_name')

    function = algorithm_functions.run(end_date, location, chag, type, napa_name)
    if len(function[0]) == 0:
        shmita_val = ("כן" if function[1] == 1 else "לא")
        return render(request, 'results.html', {'start_date': start_date,
                                              'end_date': end_date,
                                              'location':location,
                                              'chag':chag,
                                              'type':type,
                                              "No data": function,
                                              'shmita_val':shmita_val})

    df = function[0]
    image_base64 = function[1]
    shmita_val = function[2]
    leket_location_prediction = function[3]
    shmita_val = ("כן" if shmita_val == 1 else "לא")

    return render(request, 'results.html', {'df': df,
                                          'start_date':start_date,
                                          'end_date':end_date,
                                          'location': location,
                                          'chag': chag,
                                          'type': type,
                                          'image_base64':image_base64,
                                          'shmita_val':shmita_val,
                                          'leket_location_prediction':leket_location_prediction
                                          })


def results(request):
    end_date = request.GET.get('end-date')
    location = request.GET.get('location')
    chag = request.GET.get('chag')
    type = request.GET.get('type')
    napa_name = request.GET.get('napa_name')

    function = algorithm_functions.run(end_date, location, chag, type, napa_name)
    if len(function[0]) == 0:
        shmita_val = ("כן" if function[1] == 1 else "לא")
        return render(request, 'results.html', {'end_date': end_date,
                                              'napa_name':napa_name,
                                              'chag':chag,
                                              'type':type,
                                              "No data": function,
                                              'shmita_val':shmita_val})

    df = function[0]
    shmita_val = function[1]
    leket_location_arr = function[3]
    leket_location_prediction = function[2]
    shmita_val = ("כן" if shmita_val == 1 else "לא")

    data_list = leket_location_prediction.to_dict('records')
    paginator = Paginator(data_list, 10)
    page = request.GET.get('page',1)
    page_obj = paginator.get_page(page)
    nums = [i for i in range(1,page_obj.paginator.num_pages+1)]

    return render(request, 'results.html', {'df': df,
                                          'end_date':end_date,
                                          'napa_name': napa_name,
                                          'chag': chag,
                                          'type': type,
                                          'shmita_val':shmita_val,
                                          'leket_location_prediction_html':leket_location_prediction.to_html(),
                                          'leket_location_prediction_df': leket_location_prediction,
                                          'page_obj': page_obj,
                                          'nums':nums,
                                          'leket_location_arr':leket_location_arr
                                          })

from django.http import HttpResponse

def show_image(request, leket_location, type, chag, end_date, location_pred):
    # Generate the image based on the image_id
    decoded_leket_location = unquote(leket_location)
    location_image_base64, farmers_mean_image_base64, message_base64 = algorithm_functions.create_an_image(decoded_leket_location, type, chag, end_date, location_pred)
    if message_base64 == 'There is data':
        return render(request, 'image_show.html', {'location_image_base64':location_image_base64, 'farmers_mean_image_base64':farmers_mean_image_base64})
    else:
        return render(request, 'image_show.html', {'message_base64':message_base64})
