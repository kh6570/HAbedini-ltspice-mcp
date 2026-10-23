# In the name of God, the Most Gracious, the Most Merciful
# Add the ltspice MCP server without removing other servers such as qspice.
param(
    [string]$WorkspaceRoot = (Join-Path $env:USERPROFILE "Desktop\ltspice-mcp-test"),
    [string]$LtspiceExe = "",
    [ValidateSet("Cursor", "VSCode", "Both")]
    [string]$Clients = "Both"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    py -3.12 -m venv (Join-Path $RepoRoot ".venv")
}
$core = $null
if ($env:MCP_CORE_PATH -and (Test-Path (Join-Path $env:MCP_CORE_PATH "src\mcp_app_core\__init__.py"))) {
    $core = $env:MCP_CORE_PATH
} else {
    $parent = Split-Path -Parent $RepoRoot
    $found = @()
    foreach ($dir in Get-ChildItem -Path $parent -Directory -ErrorAction SilentlyContinue) {
        $marker = Join-Path $dir.FullName "src\mcp_app_core\__init__.py"
        if ((Test-Path -LiteralPath $marker) -and ($dir.FullName -ne $RepoRoot)) {
            $found += $dir.FullName
        }
    }
    if ($found.Count -eq 1) {
        $core = $found[0]
        $env:MCP_CORE_PATH = $core
    }
}
& $VenvPython -m pip install -e $RepoRoot
if ($core) {
    & $VenvPython -m pip install -e $core --no-deps
}

if (-not $LtspiceExe) {
    $candidates = @(
        (Join-Path $env:ProgramFiles "LTC\LTspiceXVII\XVIIx64.exe"),
        (Join-Path $env:ProgramFiles "ADI\LTspice\LTspice.exe"),
        (Join-Path $env:LOCALAPPDATA "Programs\ADI\LTspice\LTspice.exe")
    )
    $LtspiceExe = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}
if (-not $LtspiceExe) {
    throw "LTspice was not found. Re-run with -LtspiceExe."
}

New-Item -ItemType Directory -Force -Path $WorkspaceRoot | Out-Null

$entry = @{
    type = "stdio"
    command = $VenvPython
    args = @("-u", "-m", "ltspice_mcp", "--workspace-root", $WorkspaceRoot, "--log-level", "error")
    env = @{
        LTSPICE_EXE = $LtspiceExe
        LTSPICE_LOG_LEVEL = "error"
    }
}
$entryPath = Join-Path $env:TEMP "ltspice-mcp-entry.json"
$json = $entry | ConvertTo-Json -Depth 5
$utf8 = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($entryPath, $json, $utf8)

$merge = Join-Path $PSScriptRoot "merge_user_mcp_json.py"
if ($Clients -eq "Cursor" -or $Clients -eq "Both") {
    & $VenvPython $merge (Join-Path $env:USERPROFILE ".cursor\mcp.json") "mcpServers" "ltspice-mcp" $entryPath
}
if ($Clients -eq "VSCode" -or $Clients -eq "Both") {
    & $VenvPython $merge (Join-Path $env:APPDATA "Code\User\mcp.json") "servers" "ltspice-mcp" $entryPath
}

& $VenvPython -m ltspice_mcp --describe --ltspice-exe $LtspiceExe --workspace-root $WorkspaceRoot --log-level error | Out-Null
Write-Output "ltspice-mcp entry merged. Restart the IDE. qspice entries were not removed."
