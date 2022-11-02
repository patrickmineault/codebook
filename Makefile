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
