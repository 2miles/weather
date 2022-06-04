from re import T
from django.db import models
from django.urls import reverse
from .functions import get_coords_from_city
from environs import Env

env = Env()
env.read_env()

API_KEY = env.str("API_KEY")


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=2, blank=True)
    country = models.CharField(max_length=2, blank=True)
    lattitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        full_name = self.name
        if self.state != "":
            full_name = f"{self.name}, {self.state}"
        elif self.country != "" and self.state == "":
            full_name = f"{self.name}, {self.country}"
        print(full_name)
        return full_name

    def clean(self):
        if self.lattitude == None or self.longitude == None:
            coords = get_coords_from_city(API_KEY, self.name, self.country, self.state)
            self.lattitude = coords[0]
            self.longitude = coords[1]

    def get_absolute_url(self):
        return reverse("city_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = "cities"
