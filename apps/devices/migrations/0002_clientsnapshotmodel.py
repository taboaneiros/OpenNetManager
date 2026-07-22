
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("devices", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClientSnapshotModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("mac", models.CharField(max_length=32)),
                ("ip", models.GenericIPAddressField(blank=True, null=True)),
                ("hostname", models.CharField(blank=True, default="", max_length=255)),
                ("signal", models.IntegerField(default=0)),
                ("rx", models.CharField(blank=True, default="", max_length=40)),
                ("tx", models.CharField(blank=True, default="", max_length=40)),
                ("is_online", models.BooleanField(default=True)),
                ("first_seen", models.DateTimeField(blank=True, null=True)),
                ("last_seen", models.DateTimeField(blank=True, null=True)),
                (
                    "device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="client_history",
                        to="devices.devicemodel",
                    ),
                ),
                (
                    "snapshot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="client_snapshots",
                        to="devices.snapshotmodel",
                    ),
                ),
            ],
            options={
                "ordering": ["hostname", "mac"],
                "verbose_name": "Client Snapshot",
                "verbose_name_plural": "Client Snapshots",
            },
        ),
    ]
