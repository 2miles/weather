from django.shortcuts import render
from .models import City
from .forms import CityForm

import requests
from datetime import datetime
from environs import Env
from .functions import get_coords_from_city, create_title_name

env = Env()
env.read_env()

API_KEY = env.str("API_KEY")


def home_page_view(request):
    def get_current_weather_data_from_coords(API_key, units, lat, lon) -> dict:
        """
        Makes an API call for data from given lattitude and longitude. Returns dict of all data.
        If lat and long is not valid returns None
        """
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units={units}"
        res = requests.get(url)
        data = None
        try:
            res.raise_for_status()
            data = res.json()
        except:
            pass
        return data

    def build_current_weather_data_dict(data: dict) -> dict:
        """
        Takes all the data returned from the current_weather_data_from_coords() and
        builds and formats a dict of specific key, values.
        """
        weather_data = {}
        weather_data["name"] = data["name"]
        weather_data["description"] = data["weather"][0]["description"].capitalize()
        weather_data["icon"] = data["weather"][0]["icon"]
        weather_data["temp"] = str(round(data["main"]["temp"])) + " F"
        weather_data["humidity"] = str(data["main"]["humidity"]) + "%"
        weather_data["windspeed"] = str(round(data["wind"]["speed"])) + " mph"
        weather_data["sunrise"] = datetime.fromtimestamp(
            data["sys"]["sunrise"] + data["timezone"]
        ).strftime("%I:%M %p")
        weather_data["sunset"] = datetime.fromtimestamp(
            data["sys"]["sunset"] + data["timezone"]
        ).strftime("%I:%M %p")
        return weather_data

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
    form = CityForm()
    cities = City.objects.all()
    weather_data_list = []
    for city in cities:
        data = None
        weather_data = None
        coords = get_coords_from_city(API_KEY, city.name, city.country, city.state)
        data = get_current_weather_data_from_coords(
            API_KEY, "imperial", coords[0], coords[1]
        )
        weather_data = build_current_weather_data_dict(data)
        weather_data["printed_name"] = create_title_name(
            city.name, weather_data["name"]
        )
        weather_data_list.append(weather_data)

    context = {
        "all_data": data,
        "weather_data": weather_data_list,
        "form": form,
    }
    return render(request, "weather/home.html", context)
