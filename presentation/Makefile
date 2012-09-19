TITLE=homopres

default: $(TITLE).tex
	#latex -no-shell-escape homo.tex
	#sage homo.sagetex.sage
	latex $(TITLE)
	#bibtex homo
	#latex homo
	#latex homo
	dvips $(TITLE).dvi
	ps2pdf $(TITLE).ps

clean: 
	rm -rf $(TITLE).aux $(TITLE).dvi $(TITLE).log $(TITLE).nav $(TITLE).out $(TITLE).ps $(TITLE).snm $(TITLE).toc


veryclean: clean
	rm -rf $(TITLE).pdf
