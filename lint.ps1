# lint.ps1 – Spustí Pylint pro Django projekt a uloží výstup s historií

# Nastavení cesty k projektu a výstupní složce
$projectPath = @("myproject/myproject", "myproject/myapp", "myproject/manage.py")
$outputDir = "PYLINT"

# Nastav PYTHONPATH tak, aby rootem byl myproject/
$env:PYTHONPATH = "myproject"

# Vytvoř složku, pokud neexistuje
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Vytvoř timestamp a výstupní soubor
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$outputFile = "$outputDir\pylint_$timestamp.txt"

# Spusť Pylint a výstup pošli zároveň do konzole i do souboru
pylint $projectPath `
    --load-plugins=pylint_django `
    --django-settings-module=myproject.myproject.settings `
    --output-format=text `
    --rcfile=myproject/.pylintrc 2>&1 |
    Tee-Object -FilePath $outputFile
