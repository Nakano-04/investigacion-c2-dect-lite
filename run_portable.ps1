# Wrapper portable sin admin — uso local
# Ejemplos:
#   .\run_portable.ps1 yara .\reglas.yar .\archivo
#   .\run_portable.ps1 olevba .\muestra.docm
#   .\run_portable.ps1 oleid .\muestra.docm
#   .\run_portable.ps1 pcap .\captura.pcap

param(
    [Parameter(Mandatory=$true)][string]$Tool,
    [Parameter(ValueFromRemainingArguments=$true)][string[]]$Args
)

$root = $PSScriptRoot
$python = Join-Path $PSScriptRoot "tools\PythonPortable\python.exe"
$yara = Join-Path $PSScriptRoot "tools\YARA\yara64.exe"

switch ($Tool.ToLower()) {
    "yara"     { & $yara @Args }
    "olevba"   { & $python -m oletools.olevba @Args }
    "oleid"    { & $python -m oletools.oleid @Args }
    "olemata"  { & $python -m oletools.olemeta @Args }
    "pcap"     { & $python (Join-Path $root "analizar_pcap_beacon.py") @Args }
    default    { Write-Host "Uso: yara | olevba | oleid | oelemeta | pcap"; exit 1 }
}
