[CmdletBinding(SupportsShouldProcess = $true)]
param(
  [switch]$RemoveCompiledPdf,
  [switch]$RemoveSubmissionZip
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

$targets = Get-ChildItem -Path $projectRoot -File -Force | Where-Object {
  $name = $_.Name.ToLowerInvariant()
  $name.EndsWith(".aux") -or
  $name.EndsWith(".log") -or
  $name.EndsWith(".bbl") -or
  $name.EndsWith(".blg") -or
  $name.EndsWith(".fls") -or
  $name.EndsWith(".out") -or
  $name.EndsWith(".fdb_latexmk") -or
  $name.EndsWith(".synctex.gz") -or
  $_.Name.StartsWith("~$")
}

if ($RemoveCompiledPdf) {
  foreach ($tex in Get-ChildItem -Path $projectRoot -File -Filter "*.tex") {
    $pdfPath = Join-Path $projectRoot ($tex.BaseName + ".pdf")
    if (Test-Path $pdfPath -PathType Leaf) {
      $targets += Get-Item $pdfPath
    }
  }
}

if ($RemoveSubmissionZip) {
  $targets += Get-ChildItem -Path $projectRoot -File -Filter "*.zip" -ErrorAction SilentlyContinue
}

$targets = $targets | Sort-Object FullName -Unique

if (-not $targets) {
  Write-Host "No files matched cleanup rules."
  return
}

$removed = 0
foreach ($file in $targets) {
  if ($PSCmdlet.ShouldProcess($file.FullName, "Remove")) {
    Remove-Item -LiteralPath $file.FullName -Force
    $removed++
  }
}

Write-Host ("Removed: {0}" -f $removed)
