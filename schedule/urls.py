from rest_framework.routers import DefaultRouter
from schedule import views
from django.urls import path, include
from .views import (
    PublicCarrierListView,
    PublicLineListView,
    PublicStopListView,
    PublicTimetableListView,
    stops_near_location
)


router = DefaultRouter()
router.register(r'carriers', views.CarrierViewSet)
router.register(r'stops', views.StopViewSet)
router.register(r'lines', views.LineViewSet)
router.register(r'timetables', views.TimetableViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('public/carriers/', PublicCarrierListView.as_view(), name='public-carrier-list'),
    path('public/carriers/<int:carrier_id>/lines/', PublicLineListView.as_view(), name='public-line-list'),
    path('public/lines/<int:line_id>/stops/', PublicStopListView.as_view(), name='public-stop-list'),
    path('public/stops/<int:stop_id>/timetables/', PublicTimetableListView.as_view(), name='public-timetable-list'),
    path('public/stops/nearby/', stops_near_location, name='stops-near-location'),
]
