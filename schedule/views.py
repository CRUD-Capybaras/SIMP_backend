from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from .models import Carrier, Stop, Line, Timetable
from .serializers import CarrierSerializer, StopSerializer, LineSerializer, TimetableSerializer

from django.db.models import F, Func, FloatField, Value
from django.db.models.functions import ACos, Cos, Radians, Sin


class CarrierViewSet(viewsets.ModelViewSet):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    permission_classes = [IsAdminUser]


class StopViewSet(viewsets.ModelViewSet):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    permission_classes = [IsAdminUser]


class LineViewSet(viewsets.ModelViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer
    permission_classes = [IsAdminUser]


class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAdminUser]


class PublicCarrierListView(generics.ListAPIView):
    queryset = Carrier.objects.all()
    serializer_class = CarrierSerializer
    permission_classes = [AllowAny]


class PublicLineListView(generics.ListAPIView):
    serializer_class = LineSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        carrier_id = self.kwargs['carrier_id']
        return Line.objects.filter(carrier_id=carrier_id)


class PublicStopListView(generics.ListAPIView):
    serializer_class = StopSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        line_id = self.kwargs['line_id']
        return Stop.objects.filter(line_id=line_id)


class PublicTimetableListView(generics.ListAPIView):
    serializer_class = TimetableSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        stop_id = self.kwargs['stop_id']
        return Timetable.objects.filter(stop_id=stop_id).order_by('time')


class Haversine(Func):
    function = ''
    template = """
    (6371 * acos (
    cos ( radians(%(latitude)s) )
    * cos( radians( latitude ) )
    * cos( radians( longitude ) - radians(%(longitude)s) )
    + sin ( radians(%(latitude)s) )
    * sin( radians( latitude ) )
    ))"""
    output_field = FloatField()

    def __init__(self, latitude, longitude, **extra):
        super().__init__(**extra)
        self.extra['latitude'] = latitude
        self.extra['longitude'] = longitude


@extend_schema(
    parameters=[
        OpenApiParameter(name='latitude', description='Latitude of the location', required=True, type=OpenApiTypes.FLOAT),
        OpenApiParameter(name='longitude', description='Longitude of the location', required=True, type=OpenApiTypes.FLOAT),
        OpenApiParameter(name='distance', description='Search radius in km', required=False, type=OpenApiTypes.FLOAT, default=1.0),
        OpenApiParameter(name='carriers', description='Comma-separated list of carrier IDs to filter by', required=False, type=OpenApiTypes.STR),
    ],
    responses={200: StopSerializer(many=True)}
)
@api_view(['GET'])
def stops_near_location(request):
    latitude = request.query_params.get('latitude')
    longitude = request.query_params.get('longitude')
    distance = float(request.query_params.get('distance', 1))
    carriers = request.query_params.get('carriers')

    if not latitude or not longitude:
        return Response({'detail': 'Latitude and longitude are required parameters.'}, status=status.HTTP_400_BAD_REQUEST)

    latitude = float(latitude)
    longitude = float(longitude)

    stops = Stop.objects.annotate(
        distance=Haversine(
            latitude,
            longitude,
        )
    )

    if carriers:
        carrier_ids = [int(id) for id in carriers.split(',')]
        stops = stops.filter(line__carrier_id__in=carrier_ids)

    stops = stops.filter(distance__lt=distance).order_by('distance')

    serializer = StopSerializer(stops, many=True)
    return Response(serializer.data)
