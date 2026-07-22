
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.viewsets import (
    ClientViewSet,
    CollectViewSet,
    DeviceViewSet,
    EventViewSet,
    InterfaceViewSet,
    SnapshotViewSet,
    SystemViewSet,
)

router = DefaultRouter()
router.register("devices", DeviceViewSet, basename="device")
router.register("clients", ClientViewSet, basename="client")
router.register("interfaces", InterfaceViewSet, basename="interface")
router.register("events", EventViewSet, basename="event")
router.register("snapshots", SnapshotViewSet, basename="snapshot")
router.register("system", SystemViewSet, basename="system")
router.register("collect", CollectViewSet, basename="collect")

urlpatterns = [
    path("", include(router.urls)),
]
