from django.shortcuts import render
import requests
from django.conf import settings
from .models import City
from .forms import CityForm

def index(request):
    WEATHER_API_KEY = settings.WEATHER_API_KEY
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid='+WEATHER_API_KEY

    cities = City.objects.all()

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json() 

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'index.html', context)
