from django.db import models

class TBCarsWeb(models.Model):
    carname = models.CharField(max_length=100, unique=True)
    carbrand = models.CharField(max_length=100)
    carmodel = models.CharField(max_length=100)
    carprice = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.carbrand} {self.carname}"
