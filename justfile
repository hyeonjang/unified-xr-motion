# Justfile for building LaTeX documents with Tectonic.
# Usage from nvim: <leader>jj (pick recipe) or <leader>jr (free-form args).
#   just build          -> build the default document (main.tex -> main.pdf)
#   just build mini     -> build mini.tex
#   just build cgna/motiondag
#   just watch          -> rebuild on save
#   just clean          -> remove build artifacts
# Run recipes through PowerShell (Windows). 'just' defaults to 'sh', which
# isn't on PATH here -> "could not find the shell: program not found".

set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]

tectonic := "C:/tectonic/tectonic.exe"
main := "main-rebuttal"

# Build a .tex file (default: main). Pass a name without the .tex extension.
build doc=main:
    {{ tectonic }} -X compile --keep-logs --synctex "{{ doc }}.tex"

# Rebuild automatically whenever the source changes.
watch doc=main:
    {{ tectonic }} -X watch

# List available recipes.
default:
    @just --list

# Remove generated PDFs and Tectonic intermediates.
clean:
    Get-ChildItem -Path . -Include *.pdf,*.synctex.gz,*.log,*.aux,*.bbl,*.bcf,*.run.xml,*.out,*.toc -File -ErrorAction SilentlyContinue | Remove-Item -Force
