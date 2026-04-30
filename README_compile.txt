UnifiedXRMotion EuroXR submission source package

Main source: main.tex
Compiled PDF: main.pdf
Bibliography: main.bbl is included for deterministic PDF builds; bib/references.bib and splncs04.bst are also included.
Figures used by main.tex are in figures/.

Suggested build:
  pdflatex main.tex
  bibtex main
  pdflatex main.tex
  pdflatex main.tex

If BibTeX is unavailable, keep main.bbl in this directory and run pdflatex main.tex twice.
