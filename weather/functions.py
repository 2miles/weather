import requests
from datetime import datetime


def get_coords_from_city(API_key, name, country="", state="") -> list:
    """
    Makes an API call for a givin cities lattitude and longitude.
    state_code is optional for non-US locations.
    Returns a list of the respective coords.  If the city is not found return None.
    """
    coords = []
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={name},{state},{country}&limit=1&appid={API_key}"
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
