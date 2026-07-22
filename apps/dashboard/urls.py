from django.urls import path

from apps.dashboard.views import (
    CollectDeviceView,
    DashboardHomeView,
    DeviceDetailView,
    DeviceListView,
    EventListView,
    InterfaceListView,
)

urlpatterns = [
    path("", DashboardHomeView.as_view(), name="dashboard-home"),
    path("", DashboardHomeView.as_view(), name="dashboard-index"),
    path("devices/", DeviceListView.as_view(), name="dashboard-device-list"),
    path("interfaces/", InterfaceListView.as_view(), name="dashboard-interfaces"),
    path("events/", EventListView.as_view(), name="dashboard-events"),
    path("devices/<int:pk>/", DeviceDetailView.as_view(), name="dashboard-device-detail"),
    path(
        "devices/<int:pk>/collect/",
        CollectDeviceView.as_view(),
        name="dashboard-collect-device",
    ),
]