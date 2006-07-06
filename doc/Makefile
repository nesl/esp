####################################################
#
# Makefile     : Documentation Makefile
#  
############################################################
DOCUMENT =	report

LATEX    =      latex
DVIPS    =      dvips
PDFLATEX =	pdflatex

default:        all

all: pdf

$(DOCUMENT).dvi dvi: $(DOCUMENT).tex 
	$(LATEX) $(DOCUMENT).tex
	$(LATEX) $(DOCUMENT).tex

$(DOCUMENT).pdf pdf:
	$(PDFLATEX) $(DOCUMENT).tex

clean:
	rm -f *.bak *.aux *.ps *.pdf *.dvi *.log *.toc *~

always:
	@:

.PHONY: always clean dvi ps pdf
