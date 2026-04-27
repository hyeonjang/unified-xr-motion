#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: create_submission_zip.sh [options]

Options:
  -e, --entry-tex FILE   Entry TeX file (default: motiondag-submission.tex)
  -o, --output-zip FILE  Output ZIP filename (default: motiondag-paper-submission.zip)
      --rebuild          Rebuild entry TeX with latexmk before collecting inputs
      --include-pdf      Include generated entry PDF in ZIP if available
  -h, --help             Show this help
EOF
}

entry_tex="motiondag-submission.tex"
output_zip="motiondag-paper-submission.zip"
rebuild=0
include_pdf=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -e|--entry-tex)
      [[ $# -ge 2 ]] || { echo "Missing value for $1" >&2; exit 1; }
      entry_tex="$2"
      shift 2
      ;;
    -o|--output-zip)
      [[ $# -ge 2 ]] || { echo "Missing value for $1" >&2; exit 1; }
      output_zip="$2"
      shift 2
      ;;
    --rebuild)
      rebuild=1
      shift
      ;;
    --include-pdf)
      include_pdf=1
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

if ! command -v zip >/dev/null 2>&1; then
  echo "zip command not found. Please install zip." >&2
  exit 1
fi

resolve_path() {
  local path="$1"
  if command -v realpath >/dev/null 2>&1; then
    realpath "$path"
  else
    readlink -f "$path"
  fi
}

trim() {
  local s="$1"
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  printf '%s' "$s"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

entry_base="${entry_tex%.*}"
fls_path="$PROJECT_ROOT/$entry_base.fls"

if (( rebuild )) || [[ ! -f "$fls_path" ]]; then
  if ! command -v latexmk >/dev/null 2>&1; then
    echo "latexmk command not found. Please install latexmk." >&2
    exit 1
  fi
  echo "Building $entry_tex to refresh dependency list..."
  latexmk -pdf -interaction=nonstopmode -halt-on-error "$entry_tex"
fi

if [[ ! -f "$fls_path" ]]; then
  echo "Dependency file not found: $fls_path" >&2
  exit 1
fi

declare -A source_set=()

add_local_source_file() {
  local candidate="${1:-}"
  [[ -n "$candidate" ]] || return 0

  local resolved=""
  if [[ -f "$candidate" ]]; then
    resolved="$(resolve_path "$candidate")"
  elif [[ -f "$PROJECT_ROOT/$candidate" ]]; then
    resolved="$(resolve_path "$PROJECT_ROOT/$candidate")"
  else
    return 0
  fi

  [[ "$resolved" == "$PROJECT_ROOT"* ]] || return 0
  source_set["$resolved"]=1
}

add_local_source_file "$entry_tex"

while IFS= read -r line; do
  [[ "$line" == INPUT\ * ]] || continue
  raw="${line#INPUT }"
  raw="$(trim "$raw")"
  [[ -n "$raw" ]] || continue
  [[ -f "$raw" ]] || continue

  full="$(resolve_path "$raw")"
  [[ "$full" == "$PROJECT_ROOT"* ]] || continue

  lower_name="$(printf '%s' "$(basename "$full")" | tr '[:upper:]' '[:lower:]')"
  case "$lower_name" in
    *.aux|*.log|*.blg|*.fdb_latexmk|*.fls|*.synctex.gz|*.out|*.toc|*.lof|*.lot|*.bbl|*.bcf|*.run.xml)
      continue
      ;;
  esac

  source_set["$full"]=1
done < "$fls_path"

declare -a tex_files=()
for full in "${!source_set[@]}"; do
  [[ "$full" == *.tex ]] && tex_files+=("$full")
done

for tex_path in "${tex_files[@]}"; do
  stripped="$(sed -E 's/(^|[^\\])%.*/\1/' "$tex_path")"

  while IFS= read -r cmd; do
    [[ -n "$cmd" ]] || continue
    content="${cmd#\\bibliographystyle\{}"
    content="${content%\}}"
    IFS=',' read -r -a tokens <<< "$content"
    for token in "${tokens[@]}"; do
      token="$(trim "$token")"
      [[ -n "$token" ]] || continue
      if [[ "$token" == *.* ]]; then
        add_local_source_file "$token"
      else
        add_local_source_file "${token}.bst"
      fi
    done
  done < <(printf '%s\n' "$stripped" | grep -oE '\\bibliographystyle\{[^}]+\}' || true)

  while IFS= read -r cmd; do
    [[ -n "$cmd" ]] || continue
    content="${cmd#\\bibliography\{}"
    content="${content%\}}"
    IFS=',' read -r -a tokens <<< "$content"
    for token in "${tokens[@]}"; do
      token="$(trim "$token")"
      [[ -n "$token" ]] || continue
      if [[ "$token" == *.* ]]; then
        add_local_source_file "$token"
      else
        add_local_source_file "${token}.bib"
      fi
    done
  done < <(printf '%s\n' "$stripped" | grep -oE '\\bibliography\{[^}]+\}' || true)
done

if (( include_pdf )); then
  pdf_path="$PROJECT_ROOT/${entry_base}.pdf"
  if [[ -f "$pdf_path" ]]; then
    source_set["$(resolve_path "$pdf_path")"]=1
  else
    echo "Warning: requested --include-pdf but PDF not found: $pdf_path" >&2
  fi
fi

mapfile -t relative_paths < <(
  for full in "${!source_set[@]}"; do
    [[ "$full" == "$PROJECT_ROOT/"* ]] || continue
    printf '%s\n' "${full#"$PROJECT_ROOT"/}"
  done | sort -u
)

if [[ ${#relative_paths[@]} -eq 0 ]]; then
  echo "No files collected for submission zip." >&2
  exit 1
fi

zip_full="$PROJECT_ROOT/$output_zip"
zip_dir="$(dirname "$zip_full")"
mkdir -p "$zip_dir"
rm -f "$zip_full"

(
  cd "$PROJECT_ROOT"
  printf '%s\n' "${relative_paths[@]}" | zip -q "$output_zip" -@
)

if command -v stat >/dev/null 2>&1; then
  size_bytes="$(stat -c%s "$zip_full" 2>/dev/null || wc -c < "$zip_full")"
else
  size_bytes="$(wc -c < "$zip_full")"
fi

echo "Created: $zip_full"
echo "Size: $size_bytes bytes"
echo "Files: ${#relative_paths[@]}"
