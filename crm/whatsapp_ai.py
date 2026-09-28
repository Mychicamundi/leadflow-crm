"""OpenAI Responses API and Meta WhatsApp Cloud API integration."""
import hashlib
import hmac
import json
import os
from urllib import request

def verify_signature(body, signature):
    secret = os.getenv("META_APP_SECRET", "")
    if not secret or not signature.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature[7:], expected)

def post_api(url, payload, token):
    req = request.Request(url, data=json.dumps(payload).encode(), headers={
        "Authorization": "Bearer " + token, "Content-Type": "application/json"
    }, method="POST")
    with request.urlopen(req, timeout=15) as response:
        return json.load(response)

def generate_answer(question):
    token = os.getenv("OPENAI_API_KEY", "")
    if not token:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    result = post_api("https://api.openai.com/v1/responses", {
        "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        "instructions": os.getenv("BOT_INSTRUCTIONS", "Eres un asistente de atención al cliente. Responde en español, breve y amablemente. No inventes precios, políticas ni disponibilidad; deriva preguntas desconocidas a una persona."),
        "input": question[:4000], "max_output_tokens": 220, "store": False
    }, token)
    answer = "\n".join(part.get("text", "") for item in result.get("output", [])
                       for part in item.get("content", []) if part.get("type") == "output_text").strip()
    if not answer:
        raise ValueError("AI response had no text")
    return answer

def send_whatsapp(recipient, answer):
    token = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    if not token or not phone_id:
        raise RuntimeError("WhatsApp credentials not configured")
    version = os.getenv("META_GRAPH_VERSION", "v23.0")
    return post_api(f"https://graph.facebook.com/{version}/{phone_id}/messages", {
        "messaging_product": "whatsapp", "recipient_type": "individual",
        "to": recipient, "type": "text",
        "text": {"preview_url": False, "body": answer[:4096]}
    }, token)
