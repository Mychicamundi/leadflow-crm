from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Activity, Lead

class CRMTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.a = User.objects.create_user("alice", password="safe-password-123")
        self.b = User.objects.create_user("bob", password="safe-password-123")
        self.lead = Lead.objects.create(owner=self.a, name="Cliente A")
    def test_login_required(self):
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 302)
    def test_owner_cannot_see_other_leads(self):
        self.client.force_login(self.b)
        self.assertNotContains(self.client.get(reverse("lead_list")), "Cliente A")
        self.assertEqual(self.client.get(reverse("lead_edit", args=[self.lead.pk])).status_code, 404)
    def test_stage_creates_automatic_task(self):
        self.client.force_login(self.a)
        response = self.client.post(reverse("change_stage", args=[self.lead.pk]), {"stage": "contactado"})
        self.assertEqual(response.status_code, 302)
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.stage, "contactado")
        self.assertTrue(Activity.objects.filter(lead=self.lead, auto_generated=True).exists())
    def test_other_user_cannot_change_stage(self):
        self.client.force_login(self.b)
        self.assertEqual(self.client.post(reverse("change_stage", args=[self.lead.pk]), {"stage": "cerrado"}).status_code, 404)
    def test_assistant_uses_only_owner_data(self):
        self.client.force_login(self.b)
        response = self.client.post(reverse("assistant"), {"question": "leads nuevos"})
        self.assertContains(response, "0 leads nuevos")
