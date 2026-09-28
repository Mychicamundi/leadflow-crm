# LeadFlow CRM — MVP

CRM demostrativo con Python y Django: autenticación, prospectos, embudo de ventas, dashboard, tareas automáticas y asistente interno basado en reglas.

## Nuevo: integración OpenAI + WhatsApp Cloud API

El webhook `/webhooks/whatsapp/` recibe mensajes de texto de WhatsApp, verifica la firma HMAC SHA-256 de Meta, solicita respuestas contextuales a la API Responses de OpenAI y envía las respuestas mediante la API oficial WhatsApp Cloud de Meta. Los mensajes repetidos se deduplican mediante la caché de Django. El asistente interno del dashboard sigue funcionando con reglas; la IA está integrada en el webhook.

**La integración es código funcional pendiente de configurar y validar extremo a extremo con cuentas reales.** No hay claves ni datos de clientes incluidos.

### Instalación

Requiere Python 3.11+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Copia .env.example a .env y cambia DJANGO_SECRET_KEY
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py test
```

### Configuración WhatsApp + OpenAI

1. Consigue tu propia clave de OpenAI y las credenciales de WhatsApp Cloud API en Meta Developers.
2. En tu archivo local `.env` configura `OPENAI_API_KEY`, `META_APP_SECRET`, `WHATSAPP_VERIFY_TOKEN`, `WHATSAPP_ACCESS_TOKEN` y `WHATSAPP_PHONE_NUMBER_ID`. No subas este archivo a GitHub.
3. Despliega Django con HTTPS y `DJANGO_DEBUG=0`, establece `DJANGO_ALLOWED_HOSTS` y registra `https://TU_DOMINIO/webhooks/whatsapp/` como webhook en Meta Developers. Usa el mismo token de verificación y suscribe el campo `messages`.
4. Prueba con un número de prueba de Meta. Respeta las reglas de consentimiento, ventana de atención y plantillas aprobadas de WhatsApp.

**Antes de producción:** mueve el procesamiento sincrónico a una cola de trabajos, utiliza Redis compartido para deduplicación, incorpora métricas y derivación a agentes humanos, y revisa privacidad y manejo de errores. No compartas datos personales con servicios de IA sin autorización adecuada. Las respuestas generadas pueden equivocarse.
