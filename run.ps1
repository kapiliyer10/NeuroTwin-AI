$ErrorActionPreference = "Stop"

$pythonCandidates = @(
    (Get-Command python -ErrorAction SilentlyContinue),
    (Get-Command py -ErrorAction SilentlyContinue)
)
$pythonCommand = $null
$previousErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Continue"

foreach ($candidate in $pythonCandidates) {
    if ($candidate) {
        & $candidate.Source -c "import uvicorn" 2>$null
        if ($LASTEXITCODE -eq 0) {
            $pythonCommand = $candidate
            break
        }
    }
}

$ErrorActionPreference = $previousErrorActionPreference

if (-not $pythonCommand) {
    throw "A working Python installation with Uvicorn was not found. Install Python 3.11+, then run: py -m pip install -r requirements.txt"
}

& $pythonCommand.Source -m uvicorn backend.main:app --reload
