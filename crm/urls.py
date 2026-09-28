from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("leads/", views.lead_list, name="lead_list"),
    path("leads/new/", views.lead_create, name="lead_create"),
    path("leads/<int:pk>/edit/", views.lead_edit, name="lead_edit"),
    path("leads/<int:pk>/stage/", views.change_stage, name="change_stage"),
    path("tasks/<int:pk>/toggle/", views.toggle_task, name="toggle_task"),
    path("assistant/", views.assistant, name="assistant"),
]
