from django.shortcuts import render
from .models import City
from .forms import CityForm

from environs import Env
from .functions import (
    get_coords_from_city,
    get_current_weather_data_from_coords,
    create_title_name,
    parse_current_weather_data,
)

env = Env()
env.read_env()

API_KEY = env.str("API_KEY")


def home_page_view(request):

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CityForm()
    cities = City.objects.all()
    weather_data_list = []
    data = {}
    for city in cities:
        weather_data = None
        coords = get_coords_from_city(API_KEY, city.name, city.country, city.state)
        if coords:
            data = get_current_weather_data_from_coords(
                API_KEY, "imperial", coords[0], coords[1]
            )
            if data:
                weather_data = parse_current_weather_data(data)
                weather_data["city_id"] = city.id
                weather_data["printed_name"] = create_title_name(
                    str(city), weather_data["name"]
                )
                weather_data_list.append(weather_data)

    context = {
        "all_data": data,
        "weather_data": weather_data_list,
        "form": form,
    }
    return render(request, "home.html", context)


def detail_view(request, id):
    obj = City.objects.get(id=id)
    context = {"id": id}
    context["name"] = obj.name
    context["lat"] = obj.lattitude
    context["lon"] = obj.longitude
    return render(request, "detail.html", context)
