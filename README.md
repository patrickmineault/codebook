# The Good Research Code Handbook source

This is the source for the Good Research Code Handbook, by Patrick Mineault. The website lives at [goodresearch.dev](https://goodresearch.dev). This book uses jupyterbook to build, with a highly customized theme based off of `tufte.css`.

## Reporting issues with the website

Please report any issues via the Issues tab.

## Building the book

[![Netlify Status](https://api.netlify.com/api/v1/badges/f0bcb2b1-3782-4a4b-8611-94f5412b4f76/deploy-status)](https://app.netlify.com/sites/fervent-carson-5a9d17/deploys)

Recreate the conda environment with:

`conda env create -n cb --file environment.yml`

Then `conda activate cb`.

Run `jupyter-book build .` to build.

Use Run `jupyter-book build . --all` to force a full rebuild.

The book can be visualized locally using a development server. Typically, I use `netlify dev` for this purpose.

To remove `thebe.js` includes (which causes a 500KB javascript file to be loaded), run `python strip_js.py` (a hack).

Use `netlify deploy -d _build/html --prod` to deploy.

_Note_: when you push a PR through Github, it will build a preview of your work through Netlify automatically. When I merge the PR, it will automatically deploy the built website to [goodresearch.dev](https://goodresearch.dev). See the badge above for build status.

## Building the book to PDF

The PDF of this book is built using LaTeX via CurveNote's MyST to tex conversion. As this feature is in alpha stage, there's an elaborate translation stage in `assemble_one_pager.py`. Because the CurveNote CLI is subject to change, make sure to use the exact version of the curvenote cli, `v0.8.2`, to build this.

Build using `make pdf`. This will create a number of temporary files and the final pdf will live in `tmp/exports/book-complete.pdf`.

## Citing this book

<img data-toggle="modal" data-target="[data-modal='10.5281-zenodo.5796873']" src="https://zenodo.org/badge/398390273.svg" alt="10.5281/zenodo.5796873" />

Patrick J Mineault & The Good Research Code Handbook Community (2021). _The Good Research Code Handbook_. Zenodo. [doi:10.5281/zenodo.5796873](https://dx.doi.org/10.5281/zenodo.5796873)
