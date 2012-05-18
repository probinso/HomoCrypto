
default: homo.tex
	#latex -no-shell-escape homo.tex
	#sage homo.sagetex.sage
	latex homo
	#bibtex homo
	#latex homo
	#latex homo
	dvips homo.dvi
	ps2pdf homo.ps

clean: 
	rm -rf a0header.ps homo.aux  homo.dvi  homo.log homo.ps Makefile~

veryclean: clean
	rm -rf homo.pdf
