---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Write good docs

```{epigraph}

Documentation is a love letter that you write to your future self.

--Damian Conway
```

Research code is written in spurts and fits. You will often put code aside for several months and focus your energy on experiments, passing qualifying exams or working on another project. When you come back to your original project, you will be lost. A little prep work by writing docs will help you preserve your knowledge over the long run.

## There are many kinds of docs

When I say documentation, what comes to mind? For many people, *documenting code* is synonymous with *commenting code*. That's a narrow view of documentation. I take a larger view here - documentation is any meta-information that you write *about* the code. In that larger view, all of these are documentation:

* Single-line comments
* Multi-line comments

```{margin}
A unit test is meta-code which tells you the normative behavior of other code. It's a kind of documentation. Woah.
```

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


My slightly unpopular opinion on this is that the two most useful subtypes of documentation are:

* *Executable documentation*. Jupyter notebooks that show you how to use the code, unit tests, makefiles, bash files, tutorial examples, etc.
* *Very high-level documentation*. Installation instructions, development instructions, design of the code, usage examples, links to papers, etc.

## Executable docs are sustainable

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

```{code-cell}
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

```{code-cell}
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

### Create executable docstrings

You can add testable snippets of Python inside of docstrings. These snippets serve both as documentation and as executable tests. Consider our trusty `fib` function. We could write a docstring like this:

```{code-cell}
def fib(x):
    """Calculate the x'th Fibonacci number.

    Usage:
        >>> [fib(x) for x in range(6)]
        [0, 1, 1, 2, 3, 5]
    """
    if x % 1 != 0 or x < 0:
        raise NotImplementedError('fib(x) only defined on non-negative integers.')
    cache = {}
    def fib_inner(x):
        nonlocal cache
        if x in cache:
            return cache[x]
        if x == 0:
            return 0
        elif x == 1:
            return 1
        else:
            val = fib_inner(x - 1) + fib_inner(x - 2)
            cache[x] = val
            return val
    return fib_inner(x)
```

The `>>>` chevrons have a special meaning to test runners: it means that the code should be executed and the output compared to the expected output. We can check that the inline tests run with our trusty `pytest`:

```console
~/Documents/codebook/src $ pytest --doctest-modules
================================= test session starts ==================================
platform linux -- Python 3.8.8, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /home/pmin/Documents/codebook
plugins: anyio-3.1.0
collected 1 item                                                                       

fib.py .                                                                         [100%]

================================== 1 passed in 0.03s ===================================
```

The docstring thus both acts as documentation for the human *and* for the machine. Pretty slick! Docstring tests and standalone unit tests can be mixed and matched as desired. To keep the readability to a maximum, put shorter unit tests in docstrings and longer unit tests in standalone test suites.

### Keep configuration separate and obvious

To use a new package or to install an existing software project on a different computer, you often to change paths and other configuration. What if that configuration is spread across dozens of files? You're in for a bad time. Preferably, there should be one and only one location where you can find configuration options. A Pythonic way of doing this is to create a `conf.py` file which contains your configuration items. For instance:

```
# URL of the endpoint for the remote API
remote_endpoint = "https://example.com/v2/api"

# Location of the trained model
trained_model = "./assets/trained_model.ckpt"
```

Then, you can import this configuration whenever you need it with:

```
import conf
print(conf.trained_model)
```

Be careful not to overuse this mechanism - `conf` essentially acts as a global variable. Keep your configuration file terse and don't use conf in your reusable modules that might be used outside of the context of your current project.

### Document console programs

Let's say that you write a Python script that reads arguments from the command line. How will you know how to use this program in several months? Console programs written through the `argparse` library are *self-documenting*: they can tell you how to use them.

Let's say you create a command line program `train_net.py` that trains a neural net. Perhaps this training script takes in four arguments: model type, number of iterations, input directory, output directory. Here's how you can write that:

```{margin}
Real training scripts for neural nets can take dozens of parameters. [Here's an example](https://github.com/patrickmineault/your-head-is-there-to-move-you-around/blob/main/train_net.py#L677).
```

```{code-cell}
import argparse

def main(args):
    # TODO(pmin): Implement a neural net here.
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train a neural net")

    parser.add_argument("--model", required=True, help="Model type (resnet or alexnet)")
    parser.add_argument("--niter", type=int, default=1000, help="Number of iterations")
    parser.add_argument("--in_dir", required=True, help="Input directory with images")
    parser.add_argument("--out_dir", required=True, help="Output directory with trained model")

    args = parser.parse_args()
    main(args)
```

Then, at the command line:

```shell
$ python train_net.py -h
usage: train_net.py [-h] --model MODEL [--niter NITER] --in_dir IN_DIR --out_dir OUT_DIR

Train a neural net

optional arguments:
  -h, --help         show this help message and exit
  --model MODEL      Model type (resnet or alexnet)
  --niter NITER      Number of iterations
  --in_dir IN_DIR    Input directory with images
  --out_dir OUT_DIR  Output directory with trained model
```

```{margin}
An example of a command line program which uses verbs is `git`. The verbs include `add`, `clone`, `commit`, `push`, etc. 
```

This is a powerful way of documenting usage. You can even create complex command-line programs that use *verbs* - subcommands - and you will get both general documentation and documentation about each verb. [See the argparse documentation for details](https://docs.python.org/3/library/argparse.html).


### Commit shell files

Speaking of command line programs, pipelines involving many steps should to be documented. Consider a long-running pipeline,  involving `train_net.py`. This pipeline starts with downloading images from the internet stored in an AWS S3 bucket; trains a neural net; then generates plots. The simplest way to document this pipeline is to create a shell file. In `pipeline.sh`, we have:

```shell
#!/bin/bash

# This will cause bash to stop executing the script if there's an error
set -e

mkdir assets

# Download files
aws s3 cp s3://examplebucket/images/ assets/images --recursive

# Train network
python scripts/train_net.py --model resnet --niter 100000 --in_dir assets/images --out_dir assets/trained_model

# Create output directory
mkdir docs/figures/

# Generate plots
python generate_plots.py --in_dir assets/trained_model --out_dir docs/figures/
```

This allows you to see, at a glance, how to use the code, and what's more, it runs. 

```{danger}
Bash is quirky - the syntax is awkward and it's pretty easy to shoot yourself in the foot. If you're going to write elaborate shell scripts,  use [`shellcheck`](https://github.com/koalaman/shellcheck), which will point out common mistakes in your code. Your favorite editor probably has a plugin for `shellcheck`.

Also, check out [Julia Evans' zine](https://wizardzines.com/zines/bite-size-command-line/) on bash - it's a life saver.
```

### Document pipelines with make

Scientific pipelines often take the shape of DAGs - directed acyclic graphs. This means, essentially, that programs flow from inputs to output in a directed fashion.  The `train_net` pipeline above simple DAG with 5 steps. Other DAGs can be more elaborate, for example the 12-step DAG which generates figures shown in Van Vliet (2020) [^VanVliet]:

[^VanVliet]: Van Vliet (2020). [Seven quick tips for analysis scripts in neuroimaging](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007358). PLOS Computational Biology.

```{figure} figures/pcbi.1007358.g002.PNG_L.png
---
figclass: boxed
---
DAG from Van Vliet (2020). CC-BY 4.0
```

Van Vliet (2020) recommends to use filenames which indicate a file's position in a DAG, for example `00_fetch_data.py`. One issue with this naming scheme, is that such scripts are not testable because they can't be `import`ed. You can instead start filenames with an underscore, for example `_00_fetch_data.py`, or with a prefix, `step_00_fetch_data.py`. 

You can document how all the steps of the DAG fit together with a bash file. As your pipelines grow, it can be painful to restart a pipeline that fails in the middle. This could lead to a proliferation of bash files corresponding to different subparts of your pipeline, and pretty soon you'll have a mess of shell scripts on your hands. 

You can use a more specialized build tool to build and document a pipeline. GNU `make` has been a standard tool for compiling code for several decades, and is becoming more adopted by the data science and research communities. A `Makefile` specifies both the inputs to each pipeline step and its outputs. To give you a flavor of what a `Makefile` looks like, this file implements the DAG to train a neural net and plot diagnostic plots:

```makefile
.PHONY: plot
plot: assets/trained_model docs/figures
    python generate_plots.py --in_dir assets/trained_model --out_dir docs/figures/

assets/trained_model: assets/images
    python scripts/train_net.py --model resnet --niter 100000 --in_dir assets/images --out_dir assets/trained_model

assets/images: assets
    aws s3 cp s3://examplebucket/images/ assets/images --recursive

assets docs/figures:
    mkdir assets
    mkdir docs/figures/
```

The plot can be created with `make plot`. The `Makefile` contains a complete description of the inputs and outputs to different scripts, and thus serves as a self-documenting artifact. [Software carpentry](https://swcarpentry.github.io/make-novice/) has an excellent tutorial on `make`. What's more, `make` only rebuilds what needs to rebuilt. In particular, if the network is already trained, `make` will detect it and won't retrain the network again, skipping ahead to the plotting task.

`make` uses a domain-specific language (DSL) to define a DAG. It might feel daunting to learn yet another language to document a pipeline. There are numerous alternatives to `make` that define DAGs in pure Python, including [`doit`](https://pydoit.org/). There are also more complex tools that can implement Python DAGs and run them in the cloud, including [`luigi`](https://github.com/spotify/luigi), [`airflow`](https://airflow.apache.org/), and [`dask`](https://docs.dask.org/en/latest/custom-graphs.html).

## Write high-level text docs

In addition to executable documentation, it's important to write proper textual documentation. The secret is that once you've writing good executable documentation, you won't have any textual docs to write. 

### Write comments

You may have gotten the impression that I'm discouraging you from writing conventional comments. Good comments certainly have their place. Here are some essential things you should comment in-line:

* *References to papers* with page numbers and equation numbers (e.g. see Mineault et al. (2011), Appendix equation 2 for definition)
* *Explanations of tricky code*, and why you wrote it the way you did, and why it does the thing that it does
* *TODOs*. Your Python editor recognizes special TODO comments and will highlight them.

```
# TODO(pmin): Implement generalization to non-integer numbers
```

### Write a `README.md`

`README.md` is the often first entry point to your code that you and others will see. What are some of the good elements in a good README?

* A one-sentence description of your project
* Installation instructions
* General orientation to the codebase and usage instructions
* Links to papers
* Links to extended docs
* License

Importantly, keep your README.md up-to-date.

### Generate docs from Markdown

Scientists are taught to generate long-form, formal texts in the form of research articles. Increasingly, they're also encouraged to have a social media presence to build a more informal communication style. In between these two extremes, there are many forms of semi-formal publication to communicate complex technical subjects. I'm going to call this category  *generated docs* for lack of a better umbrella term. This includes digital notes, blogs, wikis, static site generators, executable books and readthedocs-style documentation. Let's look at each of them in turn:

*Digital notes* might not strike you as publications, since they are primarily for you instead of others. However, if you have good note taking hygiene, your notes can be readable several months, perhaps even in a year from now, so they are a form of documentation. Digital notes apps include [notion](https://notion.so/) and [notable](https://notable.app/). You could even use vscode to write Markdown files that you push to Github.

```{margin}
I was blogging back when Google Reader existed. RIP. It never stops hurting.
```

*Blogs* are places where you can write long narrative articles about technical subjects. I am a big fan of blogs - [I've written over 200 articles on my blog over the last 13 years](https://xcorr.net). Earlier this year, I copied and pasted code that I had written in a blog post from 2009. Blogs can serve as an external long-term memory, and they can help you clarify your vague ideas to others (including yourself in the future). I use [Wordpress](https://wordpress.com), but these days people tend to prefer static generators including [Jekyll](https://jekyllrb.com/).

*Wikis* are helpful when content changes rapidly and several people need to collaborate on the same documents. Github offers a wiki in every repository.

*Static sites* are multi-page websites written in Markdown and translated to HTML by a command-line tool. Popular tools include [Jekyll](https://jekyllrb.com/) (used by Github pages) and [eleventy](https://eleventy.com/)

*Executable books* are digital books that can be executed directly in the browser. The book you're reading right now is one example 😱 Executable books can generated by [jupyterbook](https://jupyterbook.org/). Under the hood, jupyterbook uses sphinx.

*readthedocs-style documentation* is documentation derived from Python code and from extra written content. [Sphinx](https://www.sphinx-doc.org/en/master/) is the tool used to generate readthedocs-style docs. More on that later.

Back in the day, all these forms of publication were very different in form, employing different technical stacks and methods of publication. These days, the lines are increasingly blurred, and in practice they all work with more or less the same paradigm: you write text in Markdown or reST, use a command-line tool to generate static HTML, upload the generated HTML to a host such as Github Pages or netlify, and voila! -- the whole world can see your work. This increasing focus on Markdown means that it's possible to seamlessly move from one medium to another. For instance, I write notes on papers in notion - I then export those notes to markdown as stubs for my blog, for [pandoc slides](https://pandoc.org/MANUAL.html) or for jupyterbook. 

#### Publish docs on Readthedocs

So how do you generate those sweet static docs you see on readthedocs? Sphinx! [There's a great tutorial to get you started](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html), but in essence getting basic generated docs is a matter of typing 4 commands:

```shell
pip install sphinx
cd docs
sphinx-quickstart
make html
```

To write your docs in markdown, you need to install an extension and add one configuration item in `conf.py`. That's it! [Uploading the docs to readthedocs](https://docs.readthedocs.io/en/stable/tutorial/index.html#importing-the-project-to-read-the-docs) (or Github pages or netlify) is a one-command affair. 

## Discussion

```{epigraph}
Some things are in our control and others not. [...] If [a thing] concerns anything not in your control, be prepared to say that it is nothing to you. 

--Epictetus
```

Documentation contains the long-term memory of a project. When you're writing documentation, you're ensuring that your code will remain useful for a long time. Code should be self-documenting to a large degree. However, you will still need to write some textual documentation. 

You can take that occasion to reflect on your project. Sometimes, you'll find that it's more productive to rewrite bad code than to write complex explanations for it. At other times, especially at the very end of a project, refactoring will not be worth the effort, and you will have to let things go. As part of the documentation, you can write about how you could improve on your project. You can use a framing device device like *three lessons I learned in this project*. Learn from your mistakes and do better next time.

```{admonition} 5-minute exercise
Write a structured `README.md` file for a project you're working on.
```