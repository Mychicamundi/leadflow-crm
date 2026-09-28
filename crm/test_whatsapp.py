import hashlib
import hmac
import json
from unittest.mock import patch
from django.test import SimpleTestCase
from django.urls import reverse
from .whatsapp_ai import generate_answer

class WhatsAppTests(SimpleTestCase):
    @patch.dict("os.environ", {"WHATSAPP_VERIFY_TOKEN": "example", "META_APP_SECRET": "test-secret"})
    def test_webhook_verification(self):
        url = reverse("whatsapp_webhook")
        response = self.client.get(url, {"hub.mode": "subscribe", "hub.verify_token": "example", "hub.challenge": "123"})
        self.assertEqual(response.content, b"123")
        self.assertEqual(self.client.post(url, data=b"{}", content_type="application/json").status_code, 403)

    @patch("crm.webhooks.send_whatsapp")
    @patch("crm.webhooks.generate_answer", return_value="Hola")
    @patch.dict("os.environ", {"META_APP_SECRET": "test-secret"})
    def test_signed_message(self, ai, send):
        body = json.dumps({"entry": [{"changes": [{"value": {"messages": [
            {"id": "unique-test-message", "from": "593999999999", "type": "text", "text": {"body": "Hola"}}
        ]}}]}]}).encode()
        signature = "sha256=" + hmac.new(b"test-secret", body, hashlib.sha256).hexdigest()
        response = self.client.post(reverse("whatsapp_webhook"), data=body, content_type="application/json", HTTP_X_HUB_SIGNATURE_256=signature)
        self.assertEqual(response.status_code, 200)
        ai.assert_called_once_with("Hola")
        send.assert_called_once_with("593999999999", "Hola")

    @patch("crm.whatsapp_ai.post_api", return_value={"output": [{"content": [{"type": "output_text", "text": "Respuesta"}]}]})
    @patch.dict("os.environ", {"OPENAI_API_KEY": "fake-test-key"})
    def test_openai_response(self, api):
        self.assertEqual(generate_answer("Pregunta"), "Respuesta")
