from rest_framework.routers import DefaultRouter
from schedule import views

router = DefaultRouter()
router.register(r'carriers', views.CarrierViewSet)
router.register(r'stops', views.StopViewSet)
router.register(r'lines', views.LineViewSet)
router.register(r'timetables', views.TimetableViewSet)

urlpatterns = router.urls
