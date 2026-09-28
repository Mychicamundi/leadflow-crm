# Initial migration for LeadFlow CRM.
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Lead",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(blank=True, max_length=40)),
                ("company", models.CharField(blank=True, max_length=120)),
                ("source", models.CharField(choices=[("web", "Sitio web"), ("instagram", "Instagram"), ("whatsapp", "WhatsApp"), ("referido", "Referido"), ("otro", "Otro")], default="web", max_length=20)),
                ("stage", models.CharField(choices=[("nuevo", "Nuevo"), ("contactado", "Contactado"), ("propuesta", "Propuesta"), ("cerrado", "Cerrado")], default="nuevo", max_length=20)),
                ("value", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="leads", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Activity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("due_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("done", models.BooleanField(default=False)),
                ("auto_generated", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("lead", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="activities", to="crm.lead")),
            ],
            options={"ordering": ["done", "due_at"]},
        ),
    ]
