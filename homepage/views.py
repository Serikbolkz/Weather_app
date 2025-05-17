from django.shortcuts import render, redirect
import requests
from django.conf import settings
from .models import City
from .forms import CityForm
from django.contrib import messages

def index(request):
    WEATHER_API_KEY = settings.WEATHER_API_KEY
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=' + WEATHER_API_KEY
    cities = City.objects.all()
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            api_response = requests.get(url.format(city_name)).json()  
            if api_response.get('main'):
                form.save()
                return redirect('index')
            else:
                messages.error(request,'City not found')
                return redirect('index')
        else:
            messages.error(request,'City already is shown')
            return redirect('index')
    else:
        form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city.name)).json()
        if city_weather.get('main'):
            weather = {
                'city': city.name,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon']
            }
            weather_data.append(weather)

    context = {
        'form': form, 
        'weather_data': weather_data
    }

    return render(request, 'index.html', context)


