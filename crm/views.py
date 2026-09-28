from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import LeadForm
from .models import Activity, Lead

def owned(request):
    return Lead.objects.filter(owner=request.user)

@login_required
def dashboard(request):
    leads = owned(request)
    stages = [{"code": code, "name": name, "leads": leads.filter(stage=code)} for code, name in Lead.STAGES]
    context = {
        "total": leads.count(), "active": leads.exclude(stage="cerrado").count(),
        "won": leads.filter(stage="cerrado").aggregate(total=Sum("value"))["total"] or 0,
        "stages": stages, "tasks": Activity.objects.filter(lead__owner=request.user, done=False)[:6],
        "recent": leads[:6],
    }
    return render(request, "crm/dashboard.html", context)

@login_required
def lead_list(request):
    leads = owned(request)
    query = request.GET.get("q", "").strip()
    if query:
        leads = leads.filter(name__icontains=query)
    return render(request, "crm/leads.html", {"leads": leads, "query": query})

@login_required
def lead_create(request):
    form = LeadForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        lead = form.save(commit=False)
        lead.owner = request.user
        lead.save()
        messages.success(request, "Lead creado.")
        return redirect("lead_list")
    return render(request, "crm/form.html", {"form": form, "title": "Nuevo lead"})

@login_required
def lead_edit(request, pk):
    lead = get_object_or_404(owned(request), pk=pk)
    form = LeadForm(request.POST or None, instance=lead)
    if request.method == "POST" and form.is_valid():
        old_stage = lead.stage
        updated = form.save()
        if old_stage != updated.stage:
            stage_automation(updated)
        messages.success(request, "Lead actualizado.")
        return redirect("lead_list")
    return render(request, "crm/form.html", {"form": form, "title": "Editar lead"})

def stage_automation(lead):
    if lead.stage in ("contactado", "propuesta"):
        Activity.objects.create(
            lead=lead,
            title=f"Seguimiento automático: {lead.get_stage_display()} — {lead.name}",
            auto_generated=True,
        )

@login_required
@require_POST
def change_stage(request, pk):
    lead = get_object_or_404(owned(request), pk=pk)
    new_stage = request.POST.get("stage")
    if new_stage in dict(Lead.STAGES) and new_stage != lead.stage:
        lead.stage = new_stage
        lead.save(update_fields=["stage", "updated_at"])
        stage_automation(lead)
        messages.success(request, "Etapa actualizada; automatización aplicada.")
    return redirect("dashboard")

@login_required
@require_POST
def toggle_task(request, pk):
    task = get_object_or_404(Activity, pk=pk, lead__owner=request.user)
    task.done = not task.done
    task.save(update_fields=["done"])
    return redirect("dashboard")

@login_required
@require_POST
def assistant(request):
    # Asistente determinista: no se afirma integración con modelos de IA.
    question = request.POST.get("question", "").strip().lower()
    leads = owned(request)
    if "nuevo" in question:
        answer = f'Tienes {leads.filter(stage="nuevo").count()} leads nuevos.'
    elif "propuesta" in question:
        answer = f'Tienes {leads.filter(stage="propuesta").count()} oportunidades en propuesta.'
    elif "cerrad" in question or "venta" in question:
        answer = f'Has cerrado {leads.filter(stage="cerrado").count()} oportunidades.'
    elif "tarea" in question:
        answer = f'Tienes {Activity.objects.filter(lead__owner=request.user, done=False).count()} tareas pendientes.'
    else:
        answer = "Puedo consultar leads nuevos, propuestas, ventas cerradas o tareas pendientes. La integración con IA está prevista para una versión posterior."
    return render(request, "crm/assistant.html", {"question": request.POST.get("question", ""), "answer": answer})
