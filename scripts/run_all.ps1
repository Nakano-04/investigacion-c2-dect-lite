# Ejecutar validación completa - sin admin
# Uso: powershell -ExecutionPolicy Bypass -File .\run_all.ps1
$py = "$env:LOCALAPPDATA\Programs\Python\Launcher\py.exe"
if (-not (Test-Path $py)) { $py = "py" }
Write-Host "Tests..."
& $py -m unittest test_reglas -v
Write-Host "`nValidación completa..."
& $py validar_completa.py
Write-Host "`nComparación baselines..."
& $py comparar_reglas.py
Write-Host "`nEmulación timing..."
& $py emular_beaconing.py
Write-Host "`nRuido/proxy/TLS..."
& $py emular_ruido_proxy_tls.py
Write-Host "`nListo. Resultados en validacion_dinamica/ y fase2_dinamico/"
