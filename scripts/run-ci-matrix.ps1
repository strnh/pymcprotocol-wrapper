# run-ci-matrix.ps1
# Usage: Open PowerShell in repo root and run: .\run-ci-matrix.ps1
# Requires Docker Desktop installed and running.

$pythonVersions = @("3.10", "3.11")
$pmcVersions = @("0.3.0", "latest")
$logsDir = Join-Path -Path $PWD -ChildPath "ci-logs"

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  Write-Error "docker コマンドが見つかりません。Docker Desktop をインストールして起動してください。"
  exit 1
}

if (-not (Test-Path $logsDir)) {
  New-Item -ItemType Directory -Path $logsDir | Out-Null
}

$summary = @()

foreach ($py in $pythonVersions) {
  foreach ($pmc in $pmcVersions) {
    $safePmc = $pmc -replace '\.', '_'
    $label = "py$($py)_pmc_$safePmc"
    $logFile = Join-Path $logsDir "$label.log"
    Write-Host "=== Running: Python $py, pymcprotocol $pmc -> log: $logFile ===" -ForegroundColor Cyan

    # Build inner bash command (runs inside container)
    $innerCmd = @"
apt-get update -qq && apt-get install -y -qq git build-essential && \
python -m venv .venv && . .venv/bin/activate && \
python -m pip install --upgrade pip setuptools wheel && \
if [ '$pmc' = 'latest' ]; then pip install -U pymcprotocol; else pip install pymcprotocol==$pmc; fi && \
pip install -r requirements-dev.txt && \
pip install -e . --no-deps && \
pytest -q
"@

    # Docker image tag
    $image = "python:$py-slim"

    # Prepare docker arguments array
    # Note: Use ${PWD} for current path; Docker Desktop with WSL2 handles path mapping.
    $dockerArgs = @(
      "run", "--rm",
      "-v", "${PWD}:/work",
      "-w", "/work",
      $image,
      "bash", "-lc", $innerCmd
    )

    # Run container and tee output to log file
    try {
      & docker @dockerArgs 2>&1 | Tee-Object -FilePath $logFile
      $exit = $LASTEXITCODE
    } catch {
      $_ | Out-File -FilePath $logFile -Append
      $exit = 1
    }

    if ($exit -eq 0) {
      Write-Host "SUCCESS: $label" -ForegroundColor Green
      $summary += [PSCustomObject]@{ combo = $label; result = "PASS"; log = $logFile }
    } else {
      Write-Host "FAIL: $label (exit code $exit)" -ForegroundColor Red
      $summary += [PSCustomObject]@{ combo = $label; result = "FAIL"; log = $logFile }
    }

    Write-Host ""
  }
}

# Print summary
Write-Host "=== SUMMARY ==="
$summary | Format-Table -AutoSize

Write-Host ""
Write-Host "ログは $logsDir に保存されています。問題があれば該当ログファイルを共有してください。"