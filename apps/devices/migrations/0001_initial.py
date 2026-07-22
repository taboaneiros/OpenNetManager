from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DeviceModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("hostname", models.CharField(max_length=120)),
                ("vendor", models.CharField(max_length=80)),
                ("model", models.CharField(max_length=80)),
                ("firmware", models.CharField(blank=True, max_length=120)),
                ("serial", models.CharField(blank=True, max_length=120)),
                ("management_ip", models.GenericIPAddressField(unique=True)),
                ("status", models.CharField(default="unknown", max_length=32)),
                ("ssh_port", models.PositiveIntegerField(default=22)),
                ("ssh_username", models.CharField(blank=True, max_length=120)),
                ("ssh_password", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "devices"},
        ),
        migrations.CreateModel(
            name="SnapshotModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("timestamp", models.DateTimeField()),
                ("payload", models.JSONField()),
                ("duration", models.FloatField()),
                ("device", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="snapshots", to="devices.devicemodel")),
            ],
            options={
                "db_table": "snapshots",
                "ordering": ["-timestamp"],
            },
        ),
        migrations.CreateModel(
            name="InterfaceModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("status", models.CharField(max_length=32)),
                ("speed", models.CharField(blank=True, max_length=32)),
                ("device", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="interfaces", to="devices.devicemodel")),
            ],
            options={"db_table": "interfaces"},
        ),
        migrations.CreateModel(
            name="EventModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("severity", models.CharField(max_length=32)),
                ("message", models.TextField()),
                ("occurred_at", models.DateTimeField()),
                ("device", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="events", to="devices.devicemodel")),
            ],
            options={
                "db_table": "events",
                "ordering": ["-occurred_at"],
            },
        ),
        migrations.CreateModel(
            name="ClientModel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("mac", models.CharField(max_length=17)),
                ("ip", models.GenericIPAddressField(blank=True, null=True)),
                ("hostname", models.CharField(blank=True, max_length=255)),
                ("signal", models.IntegerField(default=0)),
                ("rx", models.CharField(blank=True, max_length=64)),
                ("tx", models.CharField(blank=True, max_length=64)),
                ("last_seen", models.DateTimeField(blank=True, null=True)),
                ("is_online", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("device", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="clients", to="devices.devicemodel")),
            ],
            options={"db_table": "clients"},
        ),
        migrations.AlterUniqueTogether(
            name="interfacemodel",
            unique_together={("device", "name")},
        ),
        migrations.AlterUniqueTogether(
            name="clientmodel",
            unique_together={("device", "mac")},
        ),
    ]
