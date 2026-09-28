# LeadFlow CRM — MVP

MVP demostrativo de CRM construido con Python, Django, HTML y CSS. Permite iniciar sesión, gestionar clientes potenciales, actualizar un embudo de ventas, consultar indicadores y crear tareas automáticas de seguimiento.

> **Estado:** proyecto de demostración local. El asistente funciona con reglas, **no** con un modelo de inteligencia artificial. No incluye integración real con WhatsApp, plataformas externas de CRM ni envío de correos.

## Instalación

Requiere Python 3.11 o superior.

```bash
python -m venv .venv
```

En Windows: `.venv\Scripts\activate`; en macOS/Linux: `source .venv/bin/activate`.

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre http://127.0.0.1:8000/ y accede con el usuario creado. Para desarrollo local, copia `.env.example` a `.env` y modifica la clave secreta.

## Pruebas

```bash
python manage.py test
```

## Funciones incluidas

- Inicio de sesión protegido.
- Registro y edición de prospectos con datos comerciales.
- Embudo por etapas (Nuevo, Contactado, Propuesta, Cerrado).
- Dashboard con totales y tareas pendientes.
- Tarea automática al cambiar una oportunidad a Contactado o Propuesta.
- Asistente de consultas basado en reglas (sin IA real).
- Separación de información por usuario en la interfaz.

## Pendiente para producción

Revisar permisos del administrador, configurar PostgreSQL, HTTPS y secretos de entorno; integrar APIs verificadas y añadir pruebas de seguridad y carga. Usa únicamente datos ficticios para esta demostración.
