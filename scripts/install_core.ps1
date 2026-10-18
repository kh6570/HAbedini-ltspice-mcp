# In the name of God, the Most Gracious, the Most Merciful
# Install mcp-app-core.
# Uses MCP_CORE_PATH when it points at a checkout. Otherwise uses the one
# neighboring checkout that contains src\mcp_app_core. If neither exists,
# pip clones https://github.com/kh6570/HAbedini-mcp-app-core.
param(
    [string]$CorePath = $env:MCP_CORE_PATH,
    [string]$CoreRepo = "https://github.com/kh6570/HAbedini-mcp-app-core.git"
)

$ErrorActionPreference = "Stop"
$ServerRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ServerRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "python"
}

if (-not ($CorePath -and (Test-Path (Join-Path $CorePath "src\mcp_app_core\__init__.py")))) {
    $parent = Split-Path -Parent $ServerRoot
    $found = @()
    foreach ($dir in Get-ChildItem -Path $parent -Directory -ErrorAction SilentlyContinue) {
        $marker = Join-Path $dir.FullName "src\mcp_app_core\__init__.py"
        if ((Test-Path -LiteralPath $marker) -and ($dir.FullName -ne $ServerRoot)) {
            $found += $dir.FullName
        }
    }
    if ($found.Count -eq 1) {
        $CorePath = $found[0]
    } else {
        $CorePath = ""
    }
}

if ($CorePath) {
    & $Python -m pip install -e $CorePath
    if ($LASTEXITCODE -ne 0) { throw "pip install of mcp-app-core failed" }
    Write-Output "installed mcp-app-core from $CorePath"
    Write-Output "Set MCP_CORE_PATH to that folder before pip install of this server."
    return
}

& $Python -m pip install "mcp-app-core @ git+$CoreRepo"
if ($LASTEXITCODE -ne 0) {
    throw "Could not clone mcp-app-core from $CoreRepo. Create that GitHub repository, or set MCP_CORE_PATH to a local checkout."
}
Write-Output "installed mcp-app-core from $CoreRepo"
