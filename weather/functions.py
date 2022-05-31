from django.http import Http404
import requests
from datetime import datetime
from environs import Env

env = Env()
env.read_env()

API_KEY = env.str("API_KEY")
DEBUG = env.bool("DEBUG")


def get_current_weather_data_from_coords(API_key, units, lat, lon) -> dict:
    """ "
    call for data from given lattitude and longitude. Returns dict of all data.
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


def get_coords_from_city(API_key, name, country="", state="") -> list:
    """
    Makes an API call for a givin cities lattitude and longitude.
    If the request fails, prints message to console (in debug mode), and returns None.
    If the city is not found return None.
    """
    coords = []
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={name},{state},{country}&limit=1&appid=asdf{API_key}"
    res = requests.get(url)
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if DEBUG:
            print("Error: " + str(e))
        return None
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
    except requests.exceptions.HTTPError as e:
        if DEBUG:
            print("Error: " + str(e))
        return None
    return data


def parse_current_weather_data(data: dict) -> dict:
    """
    Takes all the data returned from the current_weather_data_from_coords() and
    builds and formats a dict of specific key, values. If input dict is None, return None
    """
    if data == None:
        return None
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


def create_title_name(str1, str2) -> str:
    """
    Appends str2, in parentheses, to str1.
    """
    parts = str1.split(",")
    first_part = parts[0].strip()
    print(first_part.lower(), str2.lower())
    if first_part.lower() != str2.lower():
        return str1 + " (" + str2 + ")"
    return str1
