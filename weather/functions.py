from time import strftime, time
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
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={name},{state},{country}&limit=1&appid={API_key}"
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if DEBUG:
            print("Error: " + str(e))
            print(res.json()["cod"], res.json()["message"])
        return None
    data = res.json()
    try:
        lat, lon = data[0]["lat"], data[0]["lon"]
    except:
        return None
    coords = []
    coords.append(lat)
    coords.append(lon)
    return coords


def get_current_weather_data_from_coords(API_key, units, lat, lon) -> dict:
    """
    Makes an API call for weather data from given lattitude and longitude. Returns dict of all data.
    If request returns a bad status, returns None
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units={units}"
    data = None
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if DEBUG:
            # print("Error: " + str(e))
            print(res.json()["cod"], res.json()["message"])
        return None
    data = res.json()
    return data

def get_forecast_from_coords(API_key, units, lat, lon) -> dict:
    """
    Makes an API call for forcast data from given lattitude and longitude. Returns dict of all data.
    If request returns a bad status, returns None
    """
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units={units}"
    data = None
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if DEBUG:
            # print("Error: " + str(e))
            print(res.json()["cod"], res.json()["message"])
        return None
    data = res.json()
    print(data)
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

def parse_forecast_data(data: dict) -> list:
    """
    Takes all the data returned from the get_forcast_from_coords() and
    builds and formats a list of dicts with specific key, values. If input dict is None, return None
    """
    def day_of_week(seconds_epoc, timezone) -> str:
        return datetime.fromtimestamp(seconds_epoc + timezone).strftime("%A")

    def time_of_day(seconds_epoc, timezone) -> str:
        return datetime.fromtimestamp(seconds_epoc + timezone).strftime("%-I%p")

    if data == None:
        return None
    forecast_list = [dict() for i in range(40)]
    timezone = data["city"]["timezone"]
    for i in range(40):

        # forecast_list[i]['time'] = data['list'][i]["dt"]
        epoc_time = data['list'][i]['dt']
        week = day_of_week(epoc_time, timezone)
        day = time_of_day(epoc_time, timezone)
        # forecast_list[i]['date'] = data['list'][i]['dt_txt']
        forecast_list[i]['icon'] = data['list'][i]["weather"][0]['icon']
        forecast_list[i]['description'] = data['list'][i]["weather"][0]['description']
        forecast_list[i]['temp'] = data['list'][i]["main"]['temp']
        forecast_list[i]['humidity'] = data['list'][i]["main"]['humidity']
        forecast_list[i]['feels_like'] = data['list'][i]["main"]['feels_like']
        forecast_list[i]['day_of_week'] = week
        forecast_list[i]['time_of_day'] = day
    # weather_data = {}
    # weather_data["name"] = data["name"]
    # weather_data["description"] = data["weather"][0]["description"].capitalize()
    # weather_data["icon"] = data["weather"][0]["icon"]
    # weather_data["temp"] = str(round(data["main"]["temp"])) + " F"
    # weather_data["humidity"] = str(data["main"]["humidity"]) + "%"
    # weather_data["windspeed"] = str(round(data["wind"]["speed"])) + " mph"
    # weather_data["sunrise"] = datetime.fromtimestamp(
    #     data["sys"]["sunrise"] + data["timezone"]
    # ).strftime("%I:%M %p")
    # weather_data["sunset"] = datetime.fromtimestamp(
    #     data["sys"]["sunset"] + data["timezone"]
    # ).strftime("%I:%M %p")
    return forecast_list



def create_title_name(str1, str2) -> str:
    """
    Appends str2, in parentheses, to str1 if
    """
    parts = str1.split(",")
    first_part = parts[0].strip()
    print(first_part.lower(), str2.lower())
    if first_part.lower() != str2.lower():
        return str1 + " (" + str2 + ")"
    return str1
