# The Good Research Code Handbook source

This is the source for the Good Research Code Handbook, by Patrick Mineault. The website lives at [goodresearch.dev](https://goodresearch.dev). This book uses jupyterbook to build, with a highly customized theme based off of `tufte.css`.

## Reporting issues with the website

Please report any issues via the Issues tab.

## Building the book

Recreate the conda environment with:

`conda env create --file environment.yaml --name cb`

Run `jupyter-book build .` to build.

Use `netlify deploy --prod` to deploy.

## Citing this book

<img data-toggle="modal" data-target="[data-modal='10.5281-zenodo.5796873']" src="https://zenodo.org/badge/398390273.svg" alt="10.5281/zenodo.5796873" />

Patrick J Mineault & The Good Research Code Handbook Community (2021). *The Good Research Code Handbook*. Zenodo. [doi:10.5281/zenodo.5796873](https://dx.doi.org/10.5281/zenodo.5796873)
