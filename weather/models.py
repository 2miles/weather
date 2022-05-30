from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=2, blank=True)
    country = models.CharField(max_length=2, blank=True)

    def __str__(self) -> str:
        full_name = self.name
        if self.state != "":
            full_name = f"{self.name}, {self.state}"
        elif self.country != "" and self.state == "":
            full_name = f"{self.name}, {self.country}"
        print(full_name)
        return full_name

    class Meta:
        verbose_name_plural = "cities"
