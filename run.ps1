$ErrorActionPreference = "Stop"

$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCommand) {
    $pythonCommand = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $pythonCommand) {
    throw "Python was not found. Install Python 3.11+ and run this script again."
}

& $pythonCommand.Source -c "import uvicorn" 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "Uvicorn is not installed for this Python interpreter. Run: $($pythonCommand.Source) -m pip install -r requirements.txt"
}

& $pythonCommand.Source -m uvicorn backend.main:app --reload
