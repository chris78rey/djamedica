# --- NUEVO: preparación del entorno Django ---
$ErrorActionPreference = "Stop"

Set-Location (Split-Path -Parent $PSScriptRoot)

if (-not (Test-Path ".venv")) {
    py -3 -m venv .venv
}

.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip.exe install -r requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}

.\.venv\Scripts\python.exe manage.py migrate

Write-Host "Entorno Django preparado correctamente."
# --- FIN NUEVO ---
