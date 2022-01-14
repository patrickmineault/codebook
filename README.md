# The Good Research Code Handbook source

This is the source for the Good Research Code Handbook, by Patrick Mineault. The website lives at [goodresearch.dev](https://goodresearch.dev). This book uses jupyterbook to build, with a highly customized theme based off of `tufte.css`.

## Reporting issues with the website

Please report any issues via the Issues tab.

## Building the book

Recreate the conda environment with:

`conda create --name cb --file environment.yml`

Run `jupyter-book build .` to build.

Use Run `jupyter-book build . --all` to force a full rebuild.

Use `netlify deploy -d _build/html --prod` to deploy.

## Building the book to PDF

Manually change `_config.yml` so the author name appears correctly:

`author: "Patrick Mineault"`

Use `jupyter-book build . --builder pdflatex` to build to PDF. [See here for the required environment](https://jupyterbook.org/advanced/pdf.html).

## Citing this book

<img data-toggle="modal" data-target="[data-modal='10.5281-zenodo.5796873']" src="https://zenodo.org/badge/398390273.svg" alt="10.5281/zenodo.5796873" />

Patrick J Mineault & The Good Research Code Handbook Community (2021). _The Good Research Code Handbook_. Zenodo. [doi:10.5281/zenodo.5796873](https://dx.doi.org/10.5281/zenodo.5796873)
