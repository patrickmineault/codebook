# The Good Research Code Handbook source

This is the source for the Good Research Code Handbook, by Patrick Mineault. The website lives at [goodresearch.dev](https://goodresearch.dev). This book uses jupyterbook to build, with a highly customized theme based off of `tufte.css`.

## Reporting issues with the website

Please report any issues via the Issues tab.

## Building the book

Recreate the conda environment with:

`conda create --name cb --file environment.yml`

Run `jupyter-book build .` to build.

Use `netlify deploy --prod` to deploy.
