---
name: djamedica
description: Memoria completa del proyecto Djamedica — sistema de gestión médica en Django puro. Usa esta skill siempre que trabajes en este proyecto, necesites entender su arquitectura, agregar features, corregir bugs, o recordar decisiones de diseño. Cubre modelos, vistas, permisos, validaciones, templates, scripts y el historial de fases.
---

# Djamedica — Memoria del proyecto

Sistema de gestión médica (citas, pacientes, doctores, especialidades) construido 100% en Django 5.x, sin FastAPI ni otros backends.

## Stack y configuraciones clave

- **Framework:** Django >=5.1,<6.0 (instalado 5.2.1)
- **DB:** SQLite para desarrollo local (`db.sqlite3`)
- **Auth model:** `AUTH_USER_MODEL = "users.User"` (AbstractUser con campo `role`)
- **Zona horaria:** `America/Guayaquil`, idioma `es-ec`
- **Login:** `LOGIN_URL = "/auth/login/"`, `LOGIN_REDIRECT_URL = "/panel/"`, `LOGOUT_REDIRECT_URL = "/auth/login/"`
- **Dependencias:** `Django>=5.1,<6.0`, `python-dotenv>=1.0,<2.0`
- **Entorno:** `.venv` con Python 3, scripts PowerShell en `scripts/`

## Estructura del proyecto

```text
djamedica/
├── manage.py
├── requirements.txt
├── .env / .env.example / .gitignore / .editorconfig
├── README.md
├── scripts/
│   ├── setup.ps1      # Crea .venv, instala deps, copia .env, migrate
│   ├── run.ps1        # runserver 127.0.0.1:8000
│   ├── test.ps1       # manage.py test
│   └── seed.ps1       # manage.py seed_initial_data
├── config/
│   ├── settings.py    # Configuración central
│   ├── urls.py        # Rutas raíz (admin + 6 apps)
│   ├── asgi.py / wsgi.py
├── apps/
│   ├── core/          # Home, health, dashboard, panel, login/logout, mixins, seed command, templatetags
│   ├── users/         # User (AbstractUser) con rol ADMIN|DOCTOR|STAFF
│   ├── specialties/   # Especialidades médicas
│   ├── patients/      # Pacientes con cédula/pasaporte
│   ├── doctors/       # Doctores (1:1 User, FK Specialty)
│   └── appointments/  # Citas médicas
└── templates/
    ├── base.html      # Layout base con nav, mensajes, CSS variables
    ├── registration/  # login.html, logged_out.html
    ├── core/          # home.html, panel.html
    ├── common/        # form.html, confirm_delete.html, pagination.html
    └── <app>/         # list.html, detail.html por cada app
```

## Modelos

### User (`apps/users/models.py`)
- Extiende `AbstractUser`
- `email` = unique, obligatorio
- `role` = ADMIN | DOCTOR | STAFF (default STAFF)
- `phone` = CharField blank

### Specialty (`apps/specialties/models.py`)
- `name` = unique, `description`, `is_active`, `created_at`
- `class Meta`: `ordering = ["name"]`, verbose_name = "Especialidad"

### Patient (`apps/patients/models.py`)
- `first_name`, `last_name` (obligatorios en clean)
- `document_type` = CEDULA | PASSPORT | OTHER, `document_number` = unique
- Validación de cédula ecuatoriana (módulo 10) en `clean()`
- `birth_date`, `sex` = M|F|O, `phone`, `email`, `address`
- `emergency_contact_name`, `emergency_contact_phone`
- `is_active`, `created_at`, `updated_at`
- `full_name` property

### Doctor (`apps/doctors/models.py`)
- `user` = OneToOneField(User, on_delete=PROTECT)
- `specialty` = FK(Specialty, on_delete=PROTECT)
- `professional_license` = unique, obligatorio
- `phone`, `office`, `bio`, `is_available`
- `clean()`: valida `user.role == DOCTOR`, `user.is_active`, `specialty.is_active`

### Appointment (`apps/appointments/models.py`)
- `patient` = FK(Patient, PROTECT), `doctor` = FK(Doctor, PROTECT), `specialty` = FK(Specialty, PROTECT)
- `scheduled_at` = DateTimeField, `duration_minutes` (10-240)
- `status` = SCHEDULED|CONFIRMED|COMPLETED|CANCELLED|NO_SHOW
- `reason` = obligatorio, `notes`, `created_by` = FK(User, SET_NULL)
- `clean()`: paciente activo, doctor disponible, especialidad activa, coincidencia doctor-especialidad, no solapamiento de horarios, estado coherente con fecha
- UniqueConstraint: `(doctor, scheduled_at)`

## Sistema de permisos

### Roles disponibles
- **ADMIN**: acceso total (usuarios, especialidades, pacientes, doctores, citas)
- **STAFF**: CRUD de pacientes y citas; solo lectura en doctores; sin acceso a users/specialties
- **DOCTOR**: solo lectura en pacientes/doctores/citas (filtrado a sus propias citas); sin acceso a users/specialties

### Mixins de permisos (`apps/core/mixins.py`)
- `AdminRequiredMixin` → solo ADMIN
- `StaffOrAdminRequiredMixin` → ADMIN + STAFF
- `ClinicalAccessRequiredMixin` → ADMIN + STAFF + DOCTOR
- `DeleteSuccessMessageMixin` → añade mensaje de éxito al eliminar

### Mixins de admin (`apps/core/admin_mixins.py`)
- `AdminOnlyAdminMixin` → solo ADMIN en Django Admin
- `StaffOrAdminAdminMixin` → ADMIN + STAFF en Django Admin

### Matriz de acceso a vistas manage/

| App | ADMIN | STAFF | DOCTOR | Anónimo |
|---|---|---|---|---|
| `users/manage/` | CRUD | ❌ 403 | ❌ 403 | 🔒 403 |
| `specialties/manage/` | CRUD | ❌ 403 | ❌ 403 | 🔒 403 |
| `patients/manage/` | CRUD | CRUD | 👁️ solo lectura | 🔒 403 |
| `doctors/manage/` | CRUD | 👁️ solo lectura | 👁️ solo lectura | 🔒 403 |
| `appointments/manage/` | CRUD | CRUD | 👁️ filtrado | 🔒 403 |

### Menú de navegación
- ADMIN/superuser ve: Panel, **Usuarios**, **Especialidades**, Pacientes, Doctores, Citas
- STAFF/DOCTOR ve: Panel, Pacientes, Doctores, Citas (sin Usuarios ni Especialidades)
- El menú está en `templates/base.html` y oculta enlaces según rol para evitar 403 innecesarios.

## Endpoints

### JSON (públicos, sin auth)
| Ruta | Descripción |
|---|---|
| `/health/` | `{"status":"ok","app":"djamedica","framework":"django"}` |
| `/dashboard/` | Conteos: users, specialties, patients, doctors, appointments |
| `/users/` | Lista JSON de usuarios (top 20) |
| `/users/summary/` | Resumen: total, admins, doctors, staff, active |
| `/specialties/` | Lista JSON de especialidades |
| `/specialties/summary/` | Resumen: total, active, inactive |
| `/patients/` | Lista JSON de pacientes |
| `/patients/summary/` | Resumen: total, active, inactive |
| `/doctors/` | Lista JSON de doctores |
| `/doctors/summary/` | Resumen: total, available, unavailable |
| `/appointments/` | Lista JSON de citas |
| `/appointments/summary/` | Resumen por estado |

### Web (requieren auth en su mayoría)
| Ruta | Descripción |
|---|---|
| `/` | Home pública |
| `/auth/login/` | Login HTML |
| `/auth/logout/` | Logout (POST) |
| `/panel/` | Dashboard con métricas reales, próximas citas, carga por especialidad |
| `/users/manage/` | CRUD usuarios con filtros y paginación |
| `/users/manage/<id>/` | Detalle usuario |
| `/specialties/manage/` | CRUD especialidades con filtros |
| `/specialties/manage/<id>/` | Detalle especialidad |
| `/patients/manage/` | CRUD pacientes con filtros |
| `/patients/manage/<id>/` | Detalle paciente |
| `/doctors/manage/` | CRUD doctores con filtros |
| `/doctors/manage/<id>/` | Detalle doctor |
| `/appointments/manage/` | CRUD citas con 6 filtros (q, status, doctor, specialty, date_from, date_to) |
| `/appointments/manage/<id>/` | Detalle cita |

## Fases del proyecto

### Fase 1 — Base Django
- `manage.py`, `config/settings.py`, `config/urls.py`, `apps/core/`
- Home, health endpoint, tests básicos
- Git init, remote origin github.com/chris78rey/djamedica.git

### Fase 2 — Apps de negocio
- 5 apps: users, specialties, patients, doctors, appointments
- Modelos con relaciones, admin registrado, endpoints JSON summary/list
- `AUTH_USER_MODEL = "users.User"`

### Fase 3 — Auth, CRUD HTML y roles
- Login/logout con `django.contrib.auth.views`
- `RoleRequiredMixin` y jerarquía de permisos
- `CreateView`, `UpdateView`, `DeleteView`, `ListView` en todas las apps
- Templates: `base.html`, `common/form.html`, `common/confirm_delete.html`, list.html por app
- Restricciones en admin con `AdminOnlyAdminMixin` y `StaffOrAdminAdminMixin`

### Fase 4 — Filtros, paginación, mensajes y seed
- Filtros GET en todos los listados (búsqueda, selects, fechas)
- `paginate_by = 10` en todos los ListView
- `SuccessMessageMixin` y `DeleteSuccessMessageMixin` en todas las operaciones
- `query_transform` templatetag para preservar filtros en paginación
- `manage.py seed_initial_data` + `scripts/seed.ps1`
- Nav responsive con CSS variables, cards con números grandes
- Panel con acciones rápidas condicionales por rol
- `DoctorForm` excluye users ya asignados; `AppointmentForm` con datetime-local y `created_by` automático

### Fase 5 — Detalle, validaciones y métricas
- `DetailView` en todas las apps con templates `detail.html`
- Panel enriquecido: 10 cards de métricas + próximas citas + completadas recientes + carga por especialidad
- Validación de cédula ecuatoriana (módulo 10) en `Patient.clean()`
- `Doctor.clean()`: user rol DOCTOR, user activo, specialty activa, licencia obligatoria
- `Appointment.clean()`: paciente activo, doctor disponible, specialty activa, coincidencia doctor-especialty, duración 10-240 min, no solapamiento, coherencia estado/fecha
- `UserCreateForm.clean_email()` y `UserUpdateForm.clean_email()`: email único y obligatorio

## Comandos útiles

```powershell
# Preparar entorno
powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1

# Ejecutar servidor
powershell -ExecutionPolicy Bypass -File .\scripts\run.ps1

# Correr tests (16 tests)
powershell -ExecutionPolicy Bypass -File .\scripts\test.ps1

# Cargar datos semilla
powershell -ExecutionPolicy Bypass -File .\scripts\seed.ps1

# Crear superusuario manual
.\.venv\Scripts\python.exe manage.py createsuperuser

# Shell Django
.\.venv\Scripts\python.exe manage.py shell

# Verificar sin migraciones pendientes
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

## Credenciales de desarrollo (seed)

```
admin       / Admin12345!     (ADMIN, superuser)
recepcion   / Staff12345!     (STAFF)
dr.cardenas / Doctor12345!    (DOCTOR, Cardiología)
dra.lopez   / Doctor12345!    (DOCTOR, Pediatría)
dr.suarez   / Doctor12345!    (DOCTOR, Medicina General)
```

## Datos semilla creados

- 5 usuarios (admin, recepcion, 3 doctores)
- 5 especialidades (Cardiología, Medicina General, Pediatría, Traumatología, Dermatología)
- 8 pacientes con cédula ecuatoriana
- 8 citas agendadas

## Principios de diseño

1. **Django puro** — sin FastAPI, sin mezcla de frameworks backend
2. **Estructura por apps** — cada dominio en su propia app bajo `apps/`
3. **Permisos granulares** — mixins reutilizables, no lógica dispersa
4. **Validaciones en el modelo** — `clean()` con `ValidationError` para integridad de negocio
5. **Endpoints JSON preservados** — las rutas `/users/`, `/patients/`, etc. nunca se rompen al agregar vistas web
6. **Crecimiento por fases** — cada fase agrega sin romper la anterior
7. **Rollback con Git** — commits semánticos, fácil revertir a cualquier fase

## Cuándo usar esta skill

Invoca esta skill cuando:
- Trabajes en el proyecto Djamedica (`G:\codex_projects\djamedica`)
- Necesites entender la arquitectura o el historial de decisiones
- Vayas a agregar una nueva app, modelo, vista o endpoint
- Depures un error de permisos, validación o rutas
- Necesites recordar credenciales, comandos o estructura de archivos
- El usuario pregunte "¿cómo funciona X en Djamedica?" o "¿qué hace Y?"
