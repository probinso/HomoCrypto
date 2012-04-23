
default: homo.tex
	# latex -no-shell-escape eposter.tex
	# sage eposter.sage
	latex -shell-escape homo.tex
	dvips homo.dvi
	ps2pdf homo.ps

clean: 
	rm -rf a0header.ps homo.aux  homo.dvi  homo.log homo.ps Makefile~

veryclean: clean
	rm -rf homo.pdf