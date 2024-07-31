import requests
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DeliveryRequestSerializer
from .models import DeliveryRequest
from django.conf import settings

logger = logging.getLogger(__name__)


class DeliveryCostView(APIView):
    def post(self, request):
        serializer = DeliveryRequestSerializer(data=request.data)
        if serializer.is_valid():
            latitude_a = serializer.validated_data['latitude_a']
            longitude_a = serializer.validated_data['longitude_a']
            latitude_b = serializer.validated_data['latitude_b']
            longitude_b = serializer.validated_data['longitude_b']

            try:
                url = settings.OSRM_API_URL.format(
                    longitude_a=longitude_a, latitude_a=latitude_a,
                    longitude_b=longitude_b, latitude_b=latitude_b
                )
                response = requests.get(url, timeout=settings.REQUEST_TIMEOUT)
                response.raise_for_status()  # Поднимет исключение для плохих кодов состояния

                data = response.json()

                if 'routes' in data:
                    distance = data['routes'][0]['distance'] / 1000
                    cost = distance * settings.DELIVERY_COST_PER_KM

                    # Сохранение данных в модель
                    DeliveryRequest.objects.create(
                        latitude_a=latitude_a,
                        longitude_a=longitude_a,
                        latitude_b=latitude_b,
                        longitude_b=longitude_b,
                        distance_km=distance,
                        cost_usd=cost
                    )

                    logger.info(f"Calculated distance: {distance} km, Cost: {cost} USD")
                    return Response({
                        'distance_km': distance,
                        'cost_usd': cost
                    })
                else:
                    logger.error(f"Failed to get distance from API: {data}")
                    return Response({'error': 'Failed to get distance from API'}, status=status.HTTP_400_BAD_REQUEST)
            except requests.exceptions.RequestException as e:
                logger.exception("Exception occurred while calculating delivery cost")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning(f"Invalid input data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
