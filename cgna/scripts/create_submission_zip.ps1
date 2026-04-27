param(
  [string]$EntryTex = "motiondag-submission.tex",
  [string]$OutputZip = "motiondag-paper-submission.zip",
  [switch]$Rebuild,
  [switch]$IncludePdf
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $projectRoot
try {
  $entryBase = [System.IO.Path]::GetFileNameWithoutExtension($EntryTex)
  $flsPath = Join-Path $projectRoot "$entryBase.fls"

  if ($Rebuild -or -not (Test-Path $flsPath)) {
    Write-Host "Building $EntryTex to refresh dependency list..."
    & latexmk -pdf -interaction=nonstopmode -halt-on-error $EntryTex
    if ($LASTEXITCODE -ne 0) {
      throw "latexmk failed while building $EntryTex"
    }
  }

  if (-not (Test-Path $flsPath)) {
    throw "Dependency file not found: $flsPath"
  }

  $rootFull = (Resolve-Path $projectRoot).Path
  $zipFull = Join-Path $projectRoot $OutputZip

  # Generated/build artifacts to exclude from the source bundle.
  $excludeExt = @(
    ".aux", ".log", ".blg", ".fdb_latexmk", ".fls", ".synctex.gz",
    ".out", ".toc", ".lof", ".lot", ".bbl", ".bcf", ".run.xml"
  )

  $sourceSet = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
  function Add-LocalSourceFile {
    param([string]$Candidate)
    if ([string]::IsNullOrWhiteSpace($Candidate)) { return }
    $trimmed = $Candidate.Trim()
    $resolved = $null

    if (Test-Path $trimmed -PathType Leaf) {
      $resolved = (Resolve-Path $trimmed).Path
    } else {
      $joined = Join-Path $projectRoot $trimmed
      if (Test-Path $joined -PathType Leaf) {
        $resolved = (Resolve-Path $joined).Path
      }
    }

    if ($null -eq $resolved) { return }
    if (-not $resolved.StartsWith($rootFull, [System.StringComparison]::OrdinalIgnoreCase)) { return }
    $null = $sourceSet.Add($resolved)
  }

  # Always include the entry tex.
  $entryFull = (Resolve-Path (Join-Path $projectRoot $EntryTex)).Path
  $null = $sourceSet.Add($entryFull)

  # Pull inputs from latexmk recorder file.
  Get-Content $flsPath | ForEach-Object {
    if ($_ -notlike "INPUT *") { return }
    $raw = $_.Substring(6).Trim()
    if ([string]::IsNullOrWhiteSpace($raw)) { return }
    if (-not (Test-Path $raw)) { return }
    if (-not (Test-Path $raw -PathType Leaf)) { return }

    $full = (Resolve-Path $raw).Path
    if (-not $full.StartsWith($rootFull, [System.StringComparison]::OrdinalIgnoreCase)) { return }

    $ext = [System.IO.Path]::GetExtension($full).ToLowerInvariant()
    if ($excludeExt -contains $ext) { return }

    $null = $sourceSet.Add($full)
  }

  # Ensure bibliography sources and bibliography style are included.
  $texFiles = $sourceSet | Where-Object {
    [System.IO.Path]::GetExtension($_).Equals(".tex", [System.StringComparison]::OrdinalIgnoreCase)
  }
  foreach ($texPath in $texFiles) {
    Get-Content $texPath | ForEach-Object {
      $line = $_ -replace '(?<!\\)%.*$', ''

      [regex]::Matches($line, '\\bibliographystyle\{([^}]*)\}') | ForEach-Object {
        foreach ($style in $_.Groups[1].Value.Split(',')) {
          $token = $style.Trim()
          if ([string]::IsNullOrWhiteSpace($token)) { continue }
          if ([System.IO.Path]::GetExtension($token)) {
            Add-LocalSourceFile $token
          } else {
            Add-LocalSourceFile ($token + ".bst")
          }
        }
      }

      [regex]::Matches($line, '\\bibliography\{([^}]*)\}') | ForEach-Object {
        foreach ($db in $_.Groups[1].Value.Split(',')) {
          $token = $db.Trim()
          if ([string]::IsNullOrWhiteSpace($token)) { continue }
          if ([System.IO.Path]::GetExtension($token)) {
            Add-LocalSourceFile $token
          } else {
            Add-LocalSourceFile ($token + ".bib")
          }
        }
      }
    }
  }

  if ($IncludePdf) {
    $pdfPath = Join-Path $projectRoot "$entryBase.pdf"
    if (Test-Path $pdfPath) {
      $null = $sourceSet.Add((Resolve-Path $pdfPath).Path)
    } else {
      Write-Warning "Requested -IncludePdf but PDF not found: $pdfPath"
    }
  }

  $relativePaths = $sourceSet | ForEach-Object {
    $_.Substring($rootFull.Length).TrimStart('\', '/')
  } | Sort-Object -Unique

  if ($relativePaths.Count -eq 0) {
    throw "No files collected for submission zip."
  }

  if (Test-Path $zipFull) {
    Remove-Item $zipFull -Force
  }

  Add-Type -AssemblyName System.IO.Compression
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  $zipArchive = [System.IO.Compression.ZipFile]::Open($zipFull, [System.IO.Compression.ZipArchiveMode]::Create)
  try {
    foreach ($rel in $relativePaths) {
      $src = Join-Path $projectRoot $rel
      # Zip format expects forward slashes for path separators.
      $entryName = $rel -replace '\\', '/'
      [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
        $zipArchive,
        $src,
        $entryName,
        [System.IO.Compression.CompressionLevel]::Optimal
      ) | Out-Null
    }
  }
  finally {
    if ($null -ne $zipArchive) {
      $zipArchive.Dispose()
    }
  }

  $zipInfo = Get-Item $zipFull

  Write-Host "Created:" $zipInfo.FullName
  Write-Host ("Size: {0:N0} bytes" -f $zipInfo.Length)
  Write-Host ("Files: {0}" -f $relativePaths.Count)
}
finally {
  Pop-Location
}
