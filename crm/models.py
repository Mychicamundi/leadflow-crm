from django.conf import settings
from django.db import models
from django.utils import timezone

class Lead(models.Model):
    STAGES = [("nuevo", "Nuevo"), ("contactado", "Contactado"), ("propuesta", "Propuesta"), ("cerrado", "Cerrado")]
    SOURCES = [("web", "Sitio web"), ("instagram", "Instagram"), ("whatsapp", "WhatsApp"), ("referido", "Referido"), ("otro", "Otro")]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leads")
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    company = models.CharField(max_length=120, blank=True)
    source = models.CharField(max_length=20, choices=SOURCES, default="web")
    stage = models.CharField(max_length=20, choices=STAGES, default="nuevo")
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

class Activity(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="activities")
    title = models.CharField(max_length=180)
    due_at = models.DateTimeField(default=timezone.now)
    done = models.BooleanField(default=False)
    auto_generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["done", "due_at"]

    def __str__(self):
        return self.title
