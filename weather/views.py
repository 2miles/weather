from django.shortcuts import render
from .models import City
from .forms import CityForm

import requests
from datetime import datetime
from environs import Env

env = Env()
env.read_env()

API_KEY = env.str("API_KEY")


def home_page_view(request):
    def get_coords_from_city(
        API_key, city_name, country_code="", state_code=""
    ) -> list:
        """
        Makes an API call for a givin cities lattitude and longitude.
        state_code is optional for non-US locations.
        Returns a list of the respective coords.  If the city is not found return None.
        """
        coords = []
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit=1&appid={API_key}"
        res = requests.get(url)
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)
        data = res.json()
        try:
            lat, lon = data[0]["lat"], data[0]["lon"]
        except:
            return None
        coords.append(lat)
        coords.append(lon)
        return coords

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

    def parse_location(input: str) -> dict:
        """
        Converts comma seperated location string to dict. \\
        There are 3 cases: \\
        "Miami, FL, US" ->  {"city_code": "Miami", "state_code": "FL", "country_code": "US"} \\
        "Miami, US"     ->  {"city_code": "Miami", "country_code": "US"} \\
        "Miami"         ->  {"city_code": "Miami"}
        """
        codes_dict = {}
        codes = input.split(",")
        codes_dict["city_name"] = codes[0]
        if len(codes) > 2:
            codes_dict["state_code"] = codes[1]
            codes_dict["country_code"] = codes[2]
        elif len(codes) > 1:
            codes_dict["country_code"] = codes[1]
        return codes_dict

    def create_title_name(input_str: str, station_name: str) -> str:
        codes = input_str.split(",")
        if (codes[0]).lower() != station_name.lower():
            return (codes[0] + " (" + station_name + ")").title()
        return station_name.title()

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()
    form = CityForm()
    cities = City.objects.all()
    weather_data_list = []
    for city in cities:
        location_dict = parse_location(city.name)
        data = None
        weather_data = None
        coords = get_coords_from_city(API_KEY, **location_dict)
        if coords:
            data = get_current_weather_data_from_coords(
                API_KEY, "imperial", coords[0], coords[1]
            )
            weather_data = build_current_weather_data_dict(data)
        if data:
            city_name = create_title_name(city.name, weather_data["name"])
            weather_data["city_name"] = city_name
            weather_data_list.append(weather_data)

    context = {
        "all_data": data,
        "weather_data": weather_data_list,
        "form": form,
    }
    return render(request, "weather/home.html", context)
