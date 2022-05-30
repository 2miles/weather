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

    def clean(self):
        cleaned_data = super(ModelForm, self).clean()
        coords = get_coords_from_city(API_KEY, **cleaned_data)
        if coords == None:
            raise ValidationError("Not a valid location")
        return cleaned_data
