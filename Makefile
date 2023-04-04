book: tmp/exports/book-complete.tex
	cd tmp/exports;pdflatex --shell-escape book-complete.tex;cd ../..
	cp tmp/exports/book-complete.pdf docs/_static/book.pdf

tmp/exports/book-complete.tex: $(wildcard docs/*.md) docs/_toc.yml assemble_book.py tmp
	python assemble_book.py

sphinx-book:
	jupyter-book build docs --all --builder latex

tmp:
	mkdir tmp

develop:
	jupyter-book config sphinx docs > docs/conf.py
	sphinx-autobuild docs _build/html -b html

build: $(wildcard *.md) clean
	jupyter-book build docs --all
	mv docs/_build _build
	python strip_js.py

clean:
	rm -rf _build

deploy:
	netlify deploy

.PHONY: clean build deploy develop book sphinx-book

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean       to remove all build, test, coverage and Python artifacts"
	@echo "  build       to build the book to HTML"
	@echo "  deploy      to deploy the book to netlify"
	@echo "  develop     to build the book and watch for changes"
	@echo "  book        to build the book in PDF via manual pipeline"
	@echo "  sphinx-book to build the book to PDF via sphinx-book pipeline"
	@echo "  help        to show this message"
