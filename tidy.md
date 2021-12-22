# Keep things tidy

```{epigraph}
Does it spark joy?

--Marie Kondo
```

Keeping things consistent and tidy will free your working memory from having to remember extraneous information like variable names and paths.

## Use the style guide

Generally, Python uses:

- Snake case for variables and module: `variable_name`, `my_module.py`
- Camel case for class name: `MyClass`
- Camel case with spaces for jupyter notebook: `Analyze Brain Data.ipynb`

You might know that Python generally uses 4 spaces for indentation, and that files are expected to be at most 80 columns long. These and many other elements of style are written in [PEP 8](https://www.python.org/dev/peps/pep-0008/). Code that adheres to style tends to be easier to read.

```{margin}
Big software companies like Google [have their own coding style guide](https://google.github.io/styleguide/pyguide.html). Even Guido von Rossum, inventor of Python, had to follow Google's style guide when he was working at Google.
```

Reading style guides is nobody's idea of a good time, but thankfully tools exist to help you maintain good coding style. If you prefer to eventually learn the rules, you can install `flake8` or `pylint`. Both tools are _linters_ - detectors of bad style - which allow you to find and correct common deviations from the style guide. The ideal place to use the linter is inside of an IDE, [for example VSCode](vscode). It's also possible to use linters from the command line.

A more radical way to impose style is to use a _code formatter_. A linter suggests fixes which you implement yourself; a formatter fixes issues automatically whenever you save a file. `black` [imposes consistent Python style](https://github.com/psf/black), and has plugins for all the popular IDEs. `black` is particularly useful to run on old code with haphazard style; run it once to upgrade code to a standard format.

## Delete dead code

```{figure} figures/final.doc.gif
---
width: 450px
---
Dead code is a liability. From "Piled Higher and Deeper" by Jorge Cham. [www.phdcomics.com](https://www.phdcomics.com)
```

Code that gets developed over time can accumulate lots of dead ends and odds and ends. After a while, the majority of the code in your project might be dead: code that never gets called. You know who hates dead code? You, in three months. Navigating a project that contains stale or incorrect code can waste a huge amount of time. Whenever you're about to put aside a project for a long time - for instance, after submitting a manuscript - _clean up dead code_. Delete dead code from the main branch. With git and github, you have access to a time machine, so you can always revert if you mess up.

If you're not used to this workflow, you might be scared of messing something up. You can download an archive of the repo before the cleanup to reassure yourself. If you've been diligent about committing and pushing code to Github, however, deleting dead code is a safe process. [`vulture` can help you find dead code in your codebase](https://github.com/jendrikseipp/vulture). Unit tests can help you verify that your codebase will still run after you eliminate dead code -- we will cover this in a later lesson.

## Keep jupyter notebooks tidy

```{epigraph}
If you use notebooks to develop software, you are probably using the wrong tool.

-- [Yihui Xie](https://yihui.org/en/2018/09/notebook-war/)
```

Jupyter notebooks present a special challenge to keep tidy because of their inherently nonlinear nature. It's commonplace for long-running notebooks to accumulate lots of cruft: dead cells, out-of-date analyses, inaccurate commentary. Moreover, it takes a lot of discipline to put imports and functions at the start of notebooks. They don't play well with source control, so it can be hard to track down what has changed from one version of a notebook to another.

```{figure} figures/jupyter.svg
---
width: 500px
---
Jupyter notebooks are very good at literate programming - play to their strengths by focusing your jupyter notebooks on mixing explanations, text and graphics.
```

My [_somewhat_ controversial advice](https://news.ycombinator.com/item?id=18336202) is to keep IO, long-running pipelines, and functions and classes out of jupyter notebooks. Jupyter notebooks excel at literate programming - mixing code, textual explanations, and graphics. If you focus the scope of your jupyter notebooks to literate programming, you'll reduce the amount of cruft that you will need to clean up. As a side benefit, you'll be able to develop more software inside of an IDE - like VSCode or PyCharm - which has a deeper understanding of your code and supports powerful multi-file search - and you'll be well on your way to develop testable code.

```{tip}
When you start a jupyter notebook, write 3-5 bullet points on what you want the analysis to accomplish. You'd be surprised how much this prevents notebooks from getting out of hand.
```

### Make sure your notebooks run top to bottom

[Pimentel et al. (2021)](https://link.springer.com/article/10.1007/s10664-021-09961-9#Sec18) found that only about 25% of jupyter notebooks scraped from GitHub ran from top to bottom without error. When you have context, it might only take a couple of minutes to re-order the cells and fix the errors; in several months, you could waste days on this.

Therefore, before you commit a notebook to git, get into the habit of _restarting the kernel and running all_. Often, you will find that the notebook will not run top to bottom; fix the underlying error, and _restart and run all_ until your notebook runs again. If it's impractical to restart a notebook because you have a long-running pipeline in a cell, and executing the whole notebook takes a long time, move the relevant code outside the notebook and into a separate script. As a rule of thumb, a jupyter notebook _should run from top to bottom in a minute or less_.

### Be productive mixing modules and notebooks

It can be difficult to co-develop a notebook and a module side-by-side, because whenever you change the module you will need to reload the library, often by restarting the kernel. Using these two magics - special commands recognized by jupyter - will ensure that the module is automatically reloaded in jupyter whenever the module code is changed.

```python
%load_ext autoreload
%autoreload 2
```

Now, it will feel uncomfortable to move away from jupyter notebooks for some workflows. You might be used to writing small snippets of code and then interact with it immediately to see whether it works - moving the code to a module means you can't use it in this very immediate fashion. We'll fix this discomfort later as we learn about [testing](testing).

### Refactor comfortably

Refactoring and cleaning up a notebook can be a pain in the jupyter environment: moving a cell across several screens is a pain. [`jupytext` can seamlessly translate between a regular jupyter notebook and a markdown-based textual representation](https://jupytext.readthedocs.io/en/latest/). In my opinion, refactoring and moving cells around is far easier in the text representation. Checking in the jupytext representation of a notebook to source control also makes it easy to compare different versions of the same analysis.

Move imports and function definitions to the top of your notebook. Look at Markdown headers and verify that they meaningfully summarize the analysis presented in that section. I find that it's better to write good headings and little long-form text at the start of an analysis, when the analysis still has a lot of room to shift, and to fill in the text later. Read the descriptions and check that they're up-to-date. Delete cells with obsolete analyses from the bottom of notebook - you can always recover them with source control if you've checked in the jupytext representation.

## Discussion

```{epigraph}
There should be one -- and preferably only one -- obvious way to do it.

-- [The Zen of Python](https://zen-of-python.info/there-should-be-one-and-preferably-only-one-obvious-way-to-do-it.html#13)
```

It's easy to mock style guides as pedantic nitpicking. After all, style, like spelling, is ultimately arbitrary. However, adhering to a standard style can help you preserve your working memory. Don't spend precious mental energy making lots of micro-decisions about variable names and how many spaces to put after a parenthesis: use the style guide. If there's an obvious way of doing things, do it that way.

The short term advantage of using consistent structure compounds over time. Once you've put aside a project for long enough, you will need to reacquaint yourself with it anew, and cruft and dead ends will no longer make sense. Maintaining good code hygiene will make your future self happy.

```{admonition} 5-minute exercise
Install `pylint` and run on a script you're currently working on. What did you learn?
```
