from django.db import models


class DeliveryRequest(models.Model):
    latitude_a = models.FloatField()
    longitude_a = models.FloatField()
    latitude_b = models.FloatField()
    longitude_b = models.FloatField()
    distance_km = models.FloatField(null=True, blank=True)
    cost_usd = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery from ({self.latitude_a}, {self.longitude_a}) to ({self.latitude_b}, {self.longitude_b})"
