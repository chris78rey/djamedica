# --- NUEVO: datos semilla de desarrollo ---
$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)

.\.venv\Scripts\python.exe manage.py seed_initial_data
# --- FIN NUEVO ---
