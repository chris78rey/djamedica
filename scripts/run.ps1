# --- NUEVO: ejecución local Django ---
$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)

.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
# --- FIN NUEVO ---
