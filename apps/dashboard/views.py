from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from apps.devices.models import ClientModel, DeviceModel, EventModel, InterfaceModel, SnapshotModel
from core.services.collector import CollectorService
from core.services.dashboard import DashboardMetricsService


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Render operational dashboard."""

    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        metrics = DashboardMetricsService().build_overview()
        context.update(metrics)
        return context


class DeviceListView(LoginRequiredMixin, TemplateView):
    """Render device list."""

    template_name = "dashboard/device_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["devices"] = (
            DeviceModel.objects.filter(id__isnull=False)
            .order_by("hostname", "id")
        )
        return context
    """Render device list."""

    template_name = "dashboard/device_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["devices"] = DeviceModel.objects.order_by("hostname")
        return context


class InterfaceListView(LoginRequiredMixin, TemplateView):
    """Render interface list."""

    template_name = "dashboard/interface_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["interfaces"] = (
            InterfaceModel.objects.select_related("device")
            .order_by("device__hostname", "name")
        )
        return context


class EventListView(LoginRequiredMixin, TemplateView):
    """Render event list."""

    template_name = "dashboard/event_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = EventModel.objects.select_related("device").order_by(
            "-occurred_at",
            "-id",
        )[:100]
        return context


class DeviceDetailView(LoginRequiredMixin, TemplateView):
    """Render device detail with current and historical data."""

    template_name = "dashboard/device_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = get_object_or_404(DeviceModel, pk=kwargs["pk"])

        snapshots = list(
            SnapshotModel.objects.filter(device=device)
            .prefetch_related("client_snapshots")
            .order_by("-timestamp", "-id")[:10]
        )
        events = EventModel.objects.filter(device=device).order_by("-occurred_at", "-id")[:20]
        clients = ClientModel.objects.filter(device=device, is_online=True).order_by("hostname", "mac")
        interfaces = device.interfaces.all().order_by("name")

        latest_snapshot = snapshots[0] if snapshots else None
        diff = latest_snapshot.payload.get("diff", {}) if latest_snapshot else {}

        history = []
        for snapshot in snapshots[:5]:
            summary = snapshot.payload.get("summary", {})
            history.append(
                {
                    "timestamp": snapshot.timestamp,
                    "clients": summary.get("online_clients", 0),
                    "interfaces": summary.get("interfaces", 0),
                }
            )

        context.update(
            {
                "device": device,
                "snapshots": snapshots,
                "events": events,
                "clients": clients,
                "interfaces": interfaces,
                "online_clients": clients.count(),
                "offline_clients": ClientModel.objects.filter(
                    device=device,
                    is_online=False,
                ).count(),
                "latest_diff": diff,
                "history_points": history,
            }
        )
        return context


class CollectDeviceView(LoginRequiredMixin, View):
    """Trigger manual collection for a device."""

    def post(self, request, pk: int):
        device = get_object_or_404(DeviceModel, pk=pk)
        result = CollectorService().collect_device(device.id)
        messages.success(
            request,
            (
                f"Coleta executada para {result['hostname']}. "
                f"Clientes={result['clients']} "
                f"Entraram={result['joined']} "
                f"Saíram={result['left']} "
                f"Alterados={result['changed']}."
            ),
        )
        return redirect("dashboard-device-detail", pk=device.id)