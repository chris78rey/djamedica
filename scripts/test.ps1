# --- NUEVO: pruebas Django ---
$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)

.\.venv\Scripts\python.exe manage.py test
# --- FIN NUEVO ---
