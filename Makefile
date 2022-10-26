pdf: tmp/exports/book-complete.tex
	cd tmp/exports; pdflatex --shell-escape book-complete.tex; cd ../..
	cp tmp/exports/book-complete.pdf _static/book.pdf

tmp/exports/book-complete.tex: $(wildcard *.md) _toc.yml assemble_onepager.py tmp
	python assemble_onepager.py

tmp:
	mkdir tmp

develop: 
	jupyter-book config sphinx . > conf.py
	sphinx-autobuild . _build/html -b html

build: $(wildcard *.md)
	jupyter-book build . --all
	python strip_js.py

deploy:
	