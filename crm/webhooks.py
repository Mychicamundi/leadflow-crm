"""Verified WhatsApp webhook. Use a durable queue and Redis in production."""
import json
import logging
import os
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .whatsapp_ai import generate_answer, send_whatsapp, verify_signature

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def whatsapp_webhook(request):
    if request.method == "GET":
        if (request.GET.get("hub.mode") == "subscribe"
                and os.getenv("WHATSAPP_VERIFY_TOKEN")
                and request.GET.get("hub.verify_token") == os.getenv("WHATSAPP_VERIFY_TOKEN")):
            return HttpResponse(request.GET.get("hub.challenge", ""))
        return HttpResponseForbidden("Invalid verification token")
    if not verify_signature(request.body, request.headers.get("X-Hub-Signature-256", "")):
        return HttpResponseForbidden("Invalid signature")
    try:
        payload = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            for message in change.get("value", {}).get("messages", []):
                if message.get("type") != "text" or not message.get("id") or not message.get("from"):
                    continue
                body = message.get("text", {}).get("body", "").strip()
                if not body:
                    continue
                key = "wa_event_" + message["id"]
                if not cache.add(key, "processing", timeout=86400):
                    continue
                try:
                    answer = generate_answer(body)
                    send_whatsapp(message["from"], answer)
                    cache.set(key, "sent", timeout=86400)
                except Exception:
                    cache.delete(key)
                    logger.exception("WhatsApp event failed")
                    return JsonResponse({"error": "Temporary failure"}, status=503)
    return JsonResponse({"status": "ok"})
