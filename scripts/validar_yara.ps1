# Validar YARA contra artefactos de lab y set limpio
# Uso: .\validar_yara.ps1 -YaraExe "C:\tools\yara\yara.exe" -Reglas ".\reglas.yar" -LabDir ".\lab_artefactos" -LimpioDir ".\set_limpio"
# Solo escanea. No ejecuta muestras.

param(
    [string]$YaraExe = "$PSScriptRoot\tools\YARA\yara64.exe",
    [string]$Reglas = "$PSScriptRoot\reglas.yar",
    [string]$LabDir = "$PSScriptRoot\lab_artefactos",
    [string]$LimpioDir = "$PSScriptRoot\set_limpio"
)

function Test-Yara {
    param([string]$Dir, [string]$Label)
    if (-not (Test-Path $Dir)) {
        Write-Host "[$Label] Carpeta no encontrada: $Dir (se omite)" -ForegroundColor Yellow
        return
    }
    Write-Host "`n=== $Label : $Dir ==="
    & $YaraExe -r $Reglas $Dir
    if ($LASTEXITCODE -ne 0) { Write-Host "YARA devolvió código $LASTEXITCODE" -ForegroundColor Red }
}

Write-Host "Reglas: $Reglas"
Test-Yara -Dir $LabDir -Label "LAB"
Test-Yara -Dir $LimpioDir -Label "LIMPIO (falsos positivos)"

Write-Host "`nCriterio: LAB debe dar detecciones, LIMPIO idealmente 0."
Write-Host "Si LIMPIO da hits, ajusta reglas.yar y vuelve a medir."
