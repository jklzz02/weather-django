from django.db import models
    
class City(models.Model):
    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2)
    population = models.IntegerField()
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['country_code']),
        ]

    def __str__(self):
        return f"{self.name}, {self.country_code}"