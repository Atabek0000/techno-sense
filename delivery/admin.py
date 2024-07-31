import requests
from django.contrib import admin
import logging
from .models import DeliveryRequest

logger = logging.getLogger(__name__)


@admin.register(DeliveryRequest)
class DeliveryRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude_a', 'longitude_a', 'latitude_b', 'longitude_b', 'distance_km', 'cost_usd', 'created_at')
    search_fields = ('latitude_a', 'longitude_a', 'latitude_b', 'longitude_b')
    readonly_fields = ('distance_km', 'cost_usd', 'created_at')

    def save_model(self, request, obj, form, change):
        if not obj.distance_km or not obj.cost_usd:

            latitude_a = obj.latitude_a
            longitude_a = obj.longitude_a
            latitude_b = obj.latitude_b
            longitude_b = obj.longitude_b

            try:
                url = f"http://router.project-osrm.org/route/v1/driving/{longitude_a},{latitude_a};{longitude_b},{latitude_b}?overview=false"
                response = requests.get(url)
                data = response.json()

                if response.status_code == 200 and 'routes' in data:
                    distance = data['routes'][0]['distance'] / 1000
                    cost = distance * 5
                    obj.distance_km = distance
                    obj.cost_usd = cost
                    logger.info(f"Calculated distance: {distance} km, Cost: {cost} USD")
                else:
                    logger.error(f"Failed to get distance from API: {data}")
            except Exception as e:
                logger.exception("Exception occurred while calculating delivery cost")

        super().save_model(request, obj, form, change)

