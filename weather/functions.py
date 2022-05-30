import requests


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


def create_title_name(str1, str2) -> str:
    """
    Appends str2, in parentheses, to str1.
    """
    if str1.lower() != str2.lower():
        return (str1 + " (" + str2 + ")").title()
    return str2.title()
