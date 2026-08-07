[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$Owner = "univcorp2-ctrl",
    [string]$RepoName = "roblox-japanready-growth",
    [string]$LocalRoot = "G:\マイドライブ\AI_Agents\github\repos",
    [ValidateSet("private", "public", "internal")]
    [string]$Visibility = "private",
    [switch]$SkipPush
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Require-Command {
    param([Parameter(Mandatory)][string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

Require-Command git
Require-Command gh

& gh auth status | Out-Host
if ($LASTEXITCODE -ne 0) {
    throw "GitHub CLI is not authenticated. Run 'gh auth login' as Hiro, then rerun. Do not paste tokens into this script or logs."
}

$repoFullName = "$Owner/$RepoName"
$localPath = Join-Path $LocalRoot $RepoName

if (-not (Test-Path $LocalRoot)) {
    New-Item -ItemType Directory -Path $LocalRoot -Force | Out-Null
}

$repoExists = $false
& gh repo view $repoFullName --json nameWithOwner,isPrivate,url 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
    $repoExists = $true
}

if (-not $repoExists) {
    if ($PSCmdlet.ShouldProcess($repoFullName, "Create $Visibility GitHub repository")) {
        $visibilityFlag = "--$Visibility"
        & gh repo create $repoFullName $visibilityFlag --description "Roblox Japan launch service, prospect pipeline, and JapanReady Studio plugin" --disable-issues:$false --disable-wiki
        if ($LASTEXITCODE -ne 0) { throw "Failed to create GitHub repository: $repoFullName" }
    }
}

if (-not (Test-Path $localPath)) {
    if ($PSCmdlet.ShouldProcess($localPath, "Clone repository")) {
        & gh repo clone $repoFullName $localPath
        if ($LASTEXITCODE -ne 0) { throw "Failed to clone repository to $localPath" }
    }
}

Set-Location $localPath

$directories = @(
    ".github/workflows",
    "docs",
    "sales/outreach",
    "prospects/audits",
    "plugin/src",
    "plugin/tests",
    "schemas",
    "scripts",
    "outputs",
    "logs"
)

foreach ($directory in $directories) {
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
}

$gitignore = @'
.env
.env.*
!.env.example
*.token
*.key
*.pem
secrets/
credentials/
outputs/private/
logs/*secret*
.DS_Store
Thumbs.db
'@
Set-Content -Path ".gitignore" -Value $gitignore -Encoding utf8

$readme = @'
# Roblox JapanReady Growth

Sales validation, prospect evidence, and a privacy-first Roblox Studio localization-risk plugin.

Start with `AGENTS.md` and `docs/project-spec.md`. Do not place credentials, identity documents, tax information, banking information, Stripe data, session cookies, or customer secrets in this repository.
'@
Set-Content -Path "README.md" -Value $readme -Encoding utf8

$agents = @'
# AGENTS

Read the handoff source before work:
https://github.com/univcorp2-ctrl/ai-agent-handoff-hub/tree/feature/roblox-japanready-bootstrap/docs/projects/roblox-japanready

Mandatory order:
1. Read MASTER_AGENT_INSTRUCTIONS.md.
2. Read PROJECT_SPEC.md and ACCEPTANCE_CRITERIA.md.
3. Confirm official current Roblox documentation.
4. Implement the smallest testable scope.
5. Run Maker and independent Checker.
6. Update logs/execution-log.md and outputs/status.json.

Showrunner must not be automated. No browser bot, scraper, or scripted generation against Showrunner.
'@
Set-Content -Path "AGENTS.md" -Value $agents -Encoding utf8

$codex = @'
# CODEX

You are the implementation Maker. Build and test the Lite plugin only after project requirements are fixed. Keep scanner/rules/CSV logic separate from UI. No remote code, network, telemetry, obfuscation, or secrets. Run all available lint and tests. Do not self-approve; hand the frozen artifact to a separate Checker.
'@
Set-Content -Path "CODEX.md" -Value $codex -Encoding utf8

$log = @"
# Execution Log

- started_at: $(Get-Date -Format o)
- repository: $repoFullName
- local_path: $localPath
- phase: bootstrap
- status: initialized
- human_blocker: none
"@
Set-Content -Path "logs/execution-log.md" -Value $log -Encoding utf8

$status = [ordered]@{
    schema_version = 1
    project = "roblox-japanready-growth"
    phase = "bootstrap"
    status = "initialized"
    updated_at = (Get-Date -Format o)
    maker = $null
    checker = $null
    tests = @()
    artifacts = @()
    human_blockers = @()
} | ConvertTo-Json -Depth 6
Set-Content -Path "outputs/status.json" -Value $status -Encoding utf8

& git add .
& git status --short --branch | Out-Host

$hasChanges = -not [string]::IsNullOrWhiteSpace((& git status --porcelain | Out-String))
if ($hasChanges) {
    & git commit -m "Bootstrap Roblox JapanReady commercialization repository"
    if ($LASTEXITCODE -ne 0) { throw "Initial commit failed" }
}

if (-not $SkipPush) {
    if ($PSCmdlet.ShouldProcess($repoFullName, "Push bootstrap commit")) {
        & git branch -M main
        & git push -u origin main
        if ($LASTEXITCODE -ne 0) { throw "Push failed" }
    }
}

$repoUrl = (& gh repo view $repoFullName --json url --jq '.url').Trim()
Write-Host "BOOTSTRAP_COMPLETE"
Write-Host "Repository: $repoUrl"
Write-Host "Local path: $localPath"
Write-Host "Next: copy the handoff package, then run the independent requirements checker before implementation."
