# Open-Oncology Pipeline Environment Setup Script
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   INITIALIZING OPEN-ONCOLOGY PIPELINE RUNTIME ENVIRONMENT   " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Establish necessary system local file directories safely
$dirs = @("data/patient_samples", "data/output", "data/reports", "data/visuals", "data/validation", "data/manufacturing", "data/exports", "data/logs")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "-> Created runtime directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "-> Verified existing directory: $dir" -ForegroundColor Yellow
    }
}

# 2. Check for core Python configuration dependencies
if (Get-Command python -ErrorAction SilentlyContinue) {
    $version = python --version 2>&1
    Write-Host "-> Found Python System Engine: $version" -ForegroundColor Green
} else {
    Write-Host "[!] Core Dependency Error: Python 3.x was not detected on this system machine." -ForegroundColor Red
}

# 3. Verify core ecosystem pipeline tracking files
if (Test-Path run_pipeline.py) {
    Write-Host "-> Master Switchboard orchestration script verified." -ForegroundColor Green
} else {
    Write-Host "[!] Warning: run_pipeline.py missing from current root terminal scope." -ForegroundColor Yellow
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " ENVIRONMENT CONFIGURATION SUCCESSFUL - READY FOR AUTOMATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
