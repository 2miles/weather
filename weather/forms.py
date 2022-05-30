from django.forms import ModelForm, TextInput, ValidationError
from .models import City
from .functions import get_coords_from_city
from environs import Env

env = Env()
env.read_env()

API_KEY = env.str("API_KEY")


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ["name", "state", "country"]
        widgets = {
            "name": TextInput(attrs={"class": "input", "placeholder": "Detroit"}),
            "state": TextInput(
                attrs={"class": "input", "placeholder": "MI (optional)"}
            ),
            "country": TextInput(
                attrs={"class": "input", "placeholder": "US (optional)"}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]
        name = name.title()
        return name

    def clean_state(self):
        if "state" in self.cleaned_data:
            state = self.cleaned_data["state"]
            state = state.upper()
        return state

    def clean_country(self):
        if "country" in self.cleaned_data:
            country = self.cleaned_data["country"]
            country = country.upper()
        if self.cleaned_data["state"] != "":
            country = "US"
        return country

    def clean(self):
        cleaned_data = super(ModelForm, self).clean()
        if cleaned_data["country"] == "":
            existing_city_count = City.objects.filter(name=cleaned_data["name"]).count()
            print(cleaned_data)
        else:
            existing_city_count = (
                City.objects.filter(name=cleaned_data["name"])
                .filter(state=cleaned_data["state"])
                .filter(country=cleaned_data["country"])
                .count()
            )
        print(existing_city_count)
        if existing_city_count > 0:
            raise ValidationError("That Location already exists in the database!")
        coords = get_coords_from_city(API_KEY, **cleaned_data)
        if coords == None:
            raise ValidationError("Not a valid location!")
        return cleaned_data
