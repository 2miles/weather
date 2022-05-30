from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=2, blank=True)
    country = models.CharField(max_length=2, blank=True)

    def __str__(self) -> str:
        return self.name

    def clean(self):
        self.name = self.name.title()
        self.state = self.state.upper()
        self.country = self.country.upper()
        super(City, self).clean()

    class Meta:
        verbose_name_plural = "cities"
