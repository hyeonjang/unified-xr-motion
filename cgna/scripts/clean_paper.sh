#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: clean_paper.sh [--remove-compiled-pdf] [--remove-submission-zip] [--dry-run]

Options:
  --remove-compiled-pdf  Also remove PDFs whose base name matches a local .tex file.
  --remove-submission-zip Also remove local .zip files.
  --dry-run              Print matched files without deleting.
  -h, --help             Show this help.
EOF
}

remove_compiled_pdf=0
remove_submission_zip=0
dry_run=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --remove-compiled-pdf)
      remove_compiled_pdf=1
      shift
      ;;
    --remove-submission-zip)
      remove_submission_zip=1
      shift
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

declare -A seen=()
declare -a targets=()

shopt -s nullglob
for file in *; do
  [[ -f "$file" ]] || continue
  case "$file" in
    *.aux|*.log|*.bbl|*.blg|*.fls|*.out|*.fdb_latexmk|*.synctex.gz|~\$*)
      if [[ -z "${seen[$file]:-}" ]]; then
        seen["$file"]=1
        targets+=("$file")
      fi
      ;;
  esac
done

if (( remove_compiled_pdf )); then
  for tex in *.tex; do
    [[ -f "$tex" ]] || continue
    pdf="${tex%.tex}.pdf"
    if [[ -f "$pdf" && -z "${seen[$pdf]:-}" ]]; then
      seen["$pdf"]=1
      targets+=("$pdf")
    fi
  done
fi

if (( remove_submission_zip )); then
  for zip_file in *.zip; do
    [[ -f "$zip_file" ]] || continue
    if [[ -z "${seen[$zip_file]:-}" ]]; then
      seen["$zip_file"]=1
      targets+=("$zip_file")
    fi
  done
fi
shopt -u nullglob

if [[ ${#targets[@]} -eq 0 ]]; then
  echo "No files matched cleanup rules."
  exit 0
fi

if (( dry_run )); then
  printf '%s\n' "${targets[@]}"
  echo "Matched: ${#targets[@]} file(s)"
  exit 0
fi

rm -f -- "${targets[@]}"
echo "Removed: ${#targets[@]}"
