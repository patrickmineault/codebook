pdf: tmp/exports/book-complete.tex
	cd tmp/exports; pdflatex --shell-escape book-complete.tex; pdflatex --shell-escape book-complete.tex; cd ../..
	cp tmp/exports/book-complete.pdf _static/book.pdf

tmp/exports/book-complete.tex: $(wildcard docs/*.md) docs/_toc.yml assemble_onepager.py tmp
	python assemble_onepager.py

tmp:
	mkdir tmp

develop:
	jupyter-book config sphinx docs > conf.py
	sphinx-autobuild docs _build/html -b html

build: $(wildcard *.md)
	jupyter-book build docs --all
	mv docs/_build _build
	python strip_js.py

deploy:
	netlify deploy
