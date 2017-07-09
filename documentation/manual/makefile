SOURCE=hepstore

all:
	pdflatex $(SOURCE)
	makeindex $(SOURCE).idx -s StyleInd.ist
	biber $(SOURCE)
	pdflatex $(SOURCE)
	pdflatex $(SOURCE)

clean:
	rm -f $(SOURCE).pdf $(SOURCE).blg  $(SOURCE).ilg  $(SOURCE).aux  $(SOURCE).bbl  $(SOURCE).bcf  $(SOURCE).idx  $(SOURCE).ind  $(SOURCE).log  $(SOURCE).pdf  $(SOURCE).ptc  $(SOURCE).run.xml $(SOURCE).toc *~ part*/*~ 
