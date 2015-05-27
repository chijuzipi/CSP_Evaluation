LATEX = /usr/bin/latex -halt-on-error
BIBTEX = /usr/bin/bibtex
DVI2PS = /usr/bin/dvips
PAPER = main
BIBFILE = main.bib
DISTDIR = dist
	
PS2PDF = /usr/bin/ps2pdf -dMaxSubsetPct=100 -dCompatibilityLevel=1.2 -dSubsetFonts=true -dEmbedAllFonts=true

TEXFILES = \
	*.tex \

all: $(PAPER).pdf

install: $(PAPER).pdf
	mkdir -p $(DISTDIR)
	cp $(PAPER).pdf $(DISTDIR)

$(PAPER).ps: $(PAPER).dvi
	$(LATEX) $(PAPER)
	$(BIBTEX) $(PAPER)
	$(LATEX) $(PAPER)
	$(LATEX) $(PAPER)
	$(DVI2PS) -P cmz -t letter -o $(PAPER).ps $(PAPER).dvi

$(PAPER).dvi: $(FIGS) $(TEXFILES)
	$(LATEX) $(PAPER)
	$(LATEX) $(PAPER)
	$(LATEX) $(PAPER)

$(PAPER).blg: $(BIBFILE)
	$(LATEX) $(PAPER)
	$(BIBTEX) $(PAPER)
	$(LATEX) $(PAPER)

$(PREPRINT).ps: $(PREPRINT).dvi
	$(DVI2PS) -P cmz -t letter -f $(PREPRINT).dvi > $(PREPRINT).ps

$(PREPRINT).dvi: $(FIGS) $(TEXFILES) $(PREPRINT).tex
	$(LATEX) $(PREPRINT)
	$(LATEX) $(PREPRINT)

%.pdf: %.ps
	$(PS2PDF) $<

clean:
	/bin/rm -f main.pdf *.dvi *.aux main.ps *~ *.log *.lot *.lof *.toc *.blg *.bbl
