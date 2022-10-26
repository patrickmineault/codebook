pdf: tmp/exports/book-complete.tex
	cd tmp/exports; pdflatex --shell-escape book-complete.tex; cd ../..

tmp/exports/book-complete.tex: $(wildcard *.md) _toc.yml assemble_onepager.py
	python assemble_onepager.py