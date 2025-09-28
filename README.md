# cortexsys_todo

A **Django** Todo application (with optional **Django REST Framework**) built around two apps: `accounts` and `tasks`.

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Prerequisites](#prerequisites)
* [Project Structure](#project-structure)
* [Quickstart (Local, no Docker)](#quickstart-local-no-docker)
* [Environment Configuration (.env)](#environment-configuration-env)
* [PostgreSQL Setup (Local)](#postgresql-setup-local)
* [Common Commands](#common-commands)
* [Admin Panel](#admin-panel)
* [API (Sample Endpoints)](#api-sample-endpoints)
* [Testing](#testing)
* [Troubleshooting](#troubleshooting)
* [License](#license)
* [Contributing](#contributing)

---

## Overview

This repository contains a minimal Todo app implemented with Django. It separates concerns into two Django apps:

* `accounts`: user management (optionally a custom user model).
* `tasks`: CRUD for tasks (todos) and related logic.

> The exact URLs and serializers may differ based on your implementation. Adjust this README to match your code if needed.

---

## Features

* Django project with clear app boundaries (`accounts`, `tasks`).
* PostgreSQL as the primary database.
* Admin interface for quick content inspection.
* (Optional) Django REST Framework (DRF) for API endpoints.

---

## Tech Stack

* **Python**: 3.11+
* **Django**: 4.2+
* **PostgreSQL**: 14+
* **Django REST Framework** (optional)

---

## Prerequisites

* Python 3.11+ installed and available on PATH
* `pip` and (recommended) `virtualenv`
* A running local PostgreSQL server

> This guide does **not** use Docker. If you prefer containers, you can add Docker later, but it is intentionally excluded here.

---

## Project Structure

```text
cortexsys_todo/
├─ cortexsys_todo/            # Project settings & URLs
│  ├─ settings.py
│  ├─ urls.py
│  └─ asgi.py / wsgi.py
├─ accounts/                  # User-related models/views
│  ├─ models.py
│  ├─ admin.py
│  ├─ serializers.py (if using DRF)
│  └─ urls.py / views.py
├─ tasks/                     # Todo-related models/views
│  ├─ models.py
│  ├─ admin.py
│  ├─ serializers.py (if using DRF)
│  └─ urls.py / views.py
├─ manage.py
├─ requirements.txt
└─ README.md
```

---

## Quickstart (Local, no Docker)

1. Create and activate a virtual environment

```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Create a `.env` file in the project root (see the next section for all keys).

4. Apply migrations and run the server

```bash
python manage.py migrate
python manage.py createsuperuser   # create an admin user
python manage.py runserver         # http://127.0.0.1:8000/
```

> If you plan to use a **custom user model**, make sure `AUTH_USER_MODEL = "accounts.User"` (or your specific model) is correctly set in `settings.py` **before** running migrations.

---

## Environment Configuration (.env)

Create a `.env` file with content like this:

```env
# Django
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Local PostgreSQL)
POSTGRES_DB=cortexsys_todo
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

In `settings.py`, read these values using `os.getenv`. Example:

```python
import os

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "cortexsys_todo"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}
```

Also ensure the apps are registered:

```python
INSTALLED_APPS = [
    # ...
    "accounts",
    "tasks",
    "rest_framework",  # if DRF is used
]
```

---

## PostgreSQL Setup (Local)

### Option A: Already installed locally

* Ensure the PostgreSQL service is running.
* Create a database and (optionally) a dedicated user that matches `.env`.

**Linux/macOS (psql):**

```bash
psql -U postgres
CREATE DATABASE cortexsys_todo;
-- Optional: create a separate user
CREATE USER cortex_user WITH PASSWORD 'strong_password';
GRANT ALL PRIVILEGES ON DATABASE cortexsys_todo TO cortex_user;
```

**Windows (psql via installed binaries):**

```powershell
# Example path; adjust version as needed
"C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres
CREATE DATABASE cortexsys_todo;
```

### Option B: Using an existing local cluster

* If you already have a DB named differently, update your `.env` accordingly.

> Make sure port `5432` is not blocked by another service.

---

## Common Commands

```bash
# Make migrations for apps
python manage.py makemigrations accounts tasks

# Apply migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver 0.0.0.0:8000

# Open Django shell
python manage.py shell
```

---

## Admin Panel

After starting the server, visit `/admin` and log in with the superuser you created.
Ensure your models are registered in each app’s `admin.py`, for example:

```python
from django.contrib import admin
from .models import Task
admin.site.register(Task)
```

---

## API (Sample Endpoints)

> Your actual routes may vary depending on `urls.py` and DRF configuration.

* **Auth / Accounts** (if implemented):

  * `POST /api/auth/register/` — register a new user
  * `POST /api/auth/login/` — login and receive token/session
  * `GET /api/users/me/` — get current user profile

* **Tasks**:

  * `GET /api/tasks/` — list tasks (filter/search if available)
  * `POST /api/tasks/` — create a task
  * `GET /api/tasks/{id}/` — retrieve a task
  * `PUT/PATCH /api/tasks/{id}/` — update a task
  * `DELETE /api/tasks/{id}/` — delete a task

**Sample payload (create task):**

```json
{
  "title": "Buy milk",
  "description": "2L whole milk",
  "is_done": false,
  "due_date": "2025-10-01"
}
```

---

## Testing

If you have tests defined:

```bash
python manage.py test
```

---

## Troubleshooting

* **Models not visible in Django Admin**

  * Is each app listed in `INSTALLED_APPS`?
  * Are models registered in `admin.py`?
  * Have you applied migrations?

* **`KeyError: 'accounts'` during `makemigrations` or run**

  * Is the `accounts` app installed?
  * If using a custom user model, is `AUTH_USER_MODEL` correctly set (e.g., `accounts.User`) **before** initial migrations?

* **PostgreSQL connection errors**

  * Verify `.env` values (HOST/PORT/USER/PASSWORD/DB).
  * Ensure the Postgres service is running and listening on `5432`.
  * On Windows, if you see `System error 5 has occurred. Access is denied.`, run the terminal as **Administrator** or manage the service from *Services* (services.msc).

---

## License

MIT (or your preferred license). Add or edit the `LICENSE` file accordingly.

---

## Contributing

PRs and issues are welcome. Before opening a PR:

1. Lint/format your code.
2. Ensure tests pass.
3. Update the README if behavior changes.
