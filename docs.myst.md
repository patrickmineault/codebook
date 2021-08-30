# Write good docs

```{epigraph}

Documentation is a love letter that you write to your future self

--Damian Conway
```

Research code is written in spurts and fits. You will often put code aside for several months and focus your energy on experiments, passing quals or working on another project. When you come back to your original project, you will be lost. A little prep work by writing docs will help you preserve your knowledge over the long run.

## There are many kinds of documentation

When I say documentation, what comes to mind? For many people, *documenting code* is synonymous with *commenting code*. That's a narrow view of documentation. I take a larger view here - documentation is any meta-information that you write *about* the code. In that larger view, all of these are documentation:

* Single-line comments
* Multi-line comments
* Unit tests
* Docstrings at the top of functions
* Docstrings at the top of modules
* Makefiles
* Bash files
* README.md
* Usage documentation
* Tutorial jupyter notebooks on using the code
* Auto-generated documentation hosted on readthedocs
* Websites with tutorials

```{margin}
A unit test is meta-code which tells you the normative behaviour of other code. It's a kind of documentation. Woah.
```

My slightly unpopular opinion on this is that the two most useful subtypes of documentation are:

* *Executable documentation*. Jupyter notebooks that show you how to use the code, unit tests, makefiles, bash files, tutorial examples, etc.
* *Very high-level documentation*. Installation instructions, development instructions, design of the code, usage examples, links to papers, etc.

## Executable documentation is sustainable

```{epigraph}
Code is there to explain the comments to the computer

--Andy Harris
```

Executable documentation is documentation which is itself code. The great thing about executable documentation is that *it tends to stay up-to-date*. For instance, consider unit tests. Provided you run the unit tests on a regular basis and the tests pass, they code in the unit tests tell you how you *should* use the functions you created. If you can't remember how to use the code, you can always copy and paste the code from the unit tests - they are *usage* documentation. Textual documentation, on the other hand, can *lag* behind the code and become stale. **Inaccurate documentation is worse than no documentation**.

### Raise errors

```{epigraph}
Errors should never pass silently.

-- The Zen of Python
```

People don't read manuals. That includes *you*. What people do read are *error messages*. Consider the following function stub, which is meant to convolve two vectors together:

```
def conv(A, B, padding='valid'):
    """
    Convolves the 1d signals A and B.

    Args:
        A (np.array): a 1d numpy array
        B (np.array): a 1d numpy array
        padding (str): padding type (valid, mirror)

    Returns:
        (np.array) The convolution of two vectors.
    """
    pass
```

This is a fine docstring; it tells you how to use the code. Now consider the alternative function:

```
def conv(A, B, padding='valid'):
    assert A.ndim == 1, "A must be one dimensional"
    assert B.ndim == 1, "B must be one dimensional"
    if padding not in ('valid', 'mirror'):
        raise NotImplementedError(
            f"{padding} not implemented.")
    pass
```

This code does not tell you how to use it: it *yells* at you if you use it wrong. The first way relies on your good nature to read the docs; the second way *forces you* to use the code as it was intended. I would argue that the second is better. There are several ways to generate user errors:

* `assert`: When an assert doesn't pass, it raises an `AssertionError`. You can optionally add an error message at the end. 
* `NotImplementedError`, `ValueError`, `NameError`: [Commonly used, generic errors](https://docs.python.org/3/library/exceptions.html) you can raise. I probably overuse `NotImplementedError` compared to other types.
* Type hints: Python 3 has type hints, and you can optionally enforce type checking using decorators with [`enforce`](https://github.com/RussBaz/enforce) or [`pytypes`](https://pypi.org/project/pytypes/). Type checking is a bit controversial because it goes against Python's dynamic nature. It depends on your use case: if you like it, use it.

### Document console programs

Let's say that you write a Python script that reads arguments from the command line. How will you know how to use this program in several months? Console programs written through the `argparse` library are *self-documenting*: they can tell you how to use them.

Let's say you create a command line program `train_net.py` that trains a neural net. Perhaps this training script takes in two arguments: one for model type, one for number of iterations. Here's how you can write that:

```{margin}
Real training scripts for neural nets can take dozens of parameters. [Here's an example](https://github.com/patrickmineault/your-head-is-there-to-move-you-around/blob/main/train_net.py#L677).
```

```
import argparse

def main(args):
    # TODO(pmin): Implement a neural net here.
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train a neural net")

    parser.add_argument("--model", required=True, help="Model type (resnet or alexnet)")
    parser.add_argument("--niter", type=int, default=1000, help="Number of iterations")

    args = parser.parse_args()
    main(args)
```

Then, at the command line:

```shell
$ python train_net.py -h
usage: train_net.py [-h] --model MODEL [--niter NITER]

Train a neural net

optional arguments:
  -h, --help     show this help message and exit
  --model MODEL  Model type (resnet or alexnet)
  --niter NITER  Number of iterations
```

This is a powerful way of documenting usage. You can even create complex command-line programs that use *verbs* - subcommands - and you will get both general documentation and documentation about each verb. [See the argparse documentation for details](https://docs.python.org/3/library/argparse.html).

```{margin}
An example of a command line program which uses verbs is `git`. The verbs include `add`, `clone`, `commit`, `push`, etc.
```

### Commit you shell files



* References to papers
* Why you wrote tricky code the way you did instead of the obvious way
* TODOs (your Python editor will highlight these special comments)

```{.python}
# TODO(pmin): refactor this mess
```

* Usage, especially if other people will use your code.
* It's a gift from present you to future you

# Package docs

If you create a useful package, you can generate docs for it using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) and publish them on [readthedocs](https://readthedocs.org/).

# 

There are other many kinds of *documentation*

# `README.md`

![NMC3: We survived](../figures/readme.PNG){height=220px}

# Console usage

![NMC3: We survived](../figures/argparse.PNG){height=220px}

# Lab book & blogs

* I like [notion.so](https://notion.so) as a labbook
* Blog: jekyll hosted on Github pages or wordpress.com
* I have had a [wordpress.com blog](https://xcorr.net) for the last 12 years. Two weeks ago I copied and pasted from a blog post that I wrote in 2009.

# Dashboards

* If you have a project that relies on tracking and improving a metric, use a dashboard
    * Lots of machine learning projects are set up this way 
* Not only acts as a LTM, acts as an information radiator
* Many ways to do this (most of these are commercial cloud offerings with a free tier): 
    * [R Shiny](https://shiny.rstudio.com/)
    * [Streamlit](https://www.streamlit.io/)
    * [Panel](https://panel.holoviz.org/)
    * [Plotly dash](https://plotly.com/dash/)
    * [Google Data Studio](https://datastudio.google.com/u/0/)
    * [W&B](https://wandb.ai/)

# Sample dashboard

![NMA dashboard](../figures/dashboard.PNG){height=220px}

# Lesson 4

* Write documentation
* Write the right kind of documentation
* Save your long-term memory and offload it to digital store
* 5-minute exercise: make a `README.md` file and push it to Github

## Document entry points

When you pick a project back up after several months, you might not remember how to get the code to work. **Document a clear entry point** in your `README.md` file e.g.:

````markdown
This project counts words which rhyme with *orange*. Use it like so:

```
$ python orange_counter.py --file apples.txt
```
````

For more elaborate projects, you might need to run multiple scripts to complete an analysis. A lightweight option is to create a master shell file which can run the entire analysis end-to-end. For the orange counter example, we can create a bash file with an evocative name like `run_analysis.sh` which looks like this:

```
#!/bin/bash

# This will cause bash to stop executing the script if there's an error
set -e

# Download file
wget -O apples.txt http://www.example.com/apples.txt

# Count words
python orange_counter.py --file apples.txt --out counts.txt

# Create output directory
mkdir figures/

# Generate plots
python generate_plots.py --file counts.txt --out_dir figures/
```

```{danger}
Bash is quirky - the syntax is awkward and it's pretty easy to shoot yourself in the foot. If you're going to write elaborate shell scripts,  use [`shellcheck`](https://github.com/koalaman/shellcheck), which will point out common mistakes in your code. Your favorite editor probably has a plugin for shellcheck.

Also, check out [Julia Evans' zine](https://wizardzines.com/zines/bite-size-command-line/) on bash - it's a life saver.
```

## Document pipelines

Scientific pipelines often take the shape of DAGs - directed acyclic graphs. This means, essentially, that programs flow from inputs to output in a directed fashion.  The rhymes-with-orange example above is an example of a simple DAG with 4 steps. Other DAGs can be more elaborate, for example the 12-step DAG which generates figures shown in Van Vliet (2020) [^VanVliet]:

[^VanVliet]: Van Vliet (2020). [Seven quick tips for analysis scripts in neuroimaging](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007358). PLOS Computational Biology.

```{figure} figures/pcbi.1007358.g002.PNG_L.png
---
figclass: boxed
---
DAG from Van Vliet (2020). CC-BY 4.0
```

Van Vliet (2020) recommend to use filenames which indicate a file's position in a DAG, for example `00_fetch_data.py`. One issue with this naming scheme, is that such scripts are not testable because they can't be `import`ed. You can instead start filenames with an underscore, for example `_00_fetch_data.py`, or with a prefix, `step_00_fetch_data.py`. 

You can document how all the steps of the DAG fit together with a bash file, as in the previous section. One problem with using bash for long-running pipelines is that it can be painful to restart a pipeline that fails in the middle. This will lead to a proliferation of bash files corresponding to different subparts of your pipeline, and pretty soon you'll have a mess of shell scripts on your hands. 

You can use a more specialized build tool to build and document a pipeline. GNU `make` has been a standard tool for compiling code for several decades, and is becoming more adopted in data science and research. A `Makefile` specifies both the inputs to each pipeline step and its outputs. `make` keeps track of timestamps of intermediate files and only rebuilds what needs to rebuilt. To give you a flavor of what a `Makefile` looks like, this file implements the DAG for the orange counter:

```makefile
.PHONY: plot
plot: counts.txt generate_plots.py figures
    python generate_plots.py --file counts.txt --out_dir figures/

counts.txt: apples.txt orange_counter.py
    python orange_counter.py --file apples.txt --out counts.txt

apples.txt:
    wget -O apples.txt http://www.example.com/apples.txt

figures:
    mkdir figures
```

The plot can be created with `make plot`. The `Makefile` contains a complete description of the inputs and outputs to different scripts, and thus serves as a self-documenting artifact. [Software carpentries](https://swcarpentry.github.io/make-novice/) have an excellent tutorial on `make`.

`make` uses a domain-specific language (DSL) to define a DAG. It might feel daunting to learn yet another language to document a pipeline. There are numerous alternatives to `make` that define DAGs in pure Python, including [`doit`](https://pydoit.org/). There are also more complex tools that can implement Python DAGs and run them in the cloud, including [`luigi`](https://github.com/spotify/luigi), [`airflow`](https://airflow.apache.org/), and [`dask`](https://docs.dask.org/en/latest/custom-graphs.html).


# Decoupling configuration

* Keep your configuration our of your code
    * Use `argparse` to specify options via the command line
    * Keep configuration options located in an importable `config.py` file
    * Use `python-dotenv` to store secrets in a `.env` file
