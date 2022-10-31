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
title: "Write good documentation"
exports:
  - format: tex
    logo: false
    template: ../templates/plain_latex_book_chapter
    output: exports/docs.tex
---

# Document your code

```{epigraph}

Documentation is a love letter that you write to your future self.

--Damian Conway
```

When I say documentation, what comes to mind? For many people, _documenting code_ is synonymous with _commenting code_. That's a narrow view of documentation. I take a larger view here - documentation is any meta-information that you write _about_ the code. In that larger view, all of these are documentation:

- Single-line comments
- Multi-line comments

```{margin}
A unit test is meta-code which tells you the normative behavior of other code. It's a kind of documentation. Woah.
```

- Unit tests
- Docstrings at the top of functions
- Docstrings at the top of modules
- Makefiles
- Bash files
- README.md
- Usage documentation
- Tutorial jupyter notebooks on using the code
- Auto-generated documentation hosted on readthedocs
- Websites with tutorials

In this chapter, I'll talk about documenting small units of code - functions and modules. I will cover things that are not conventionally considered documentation, but that nevertheless clarify how to use code. In the next section, I'll discuss documenting larger units of code - programs, projects and pipelines.

## Raise errors

```{epigraph}
Errors should never pass silently.

-- The Zen of Python
```

People don't read manuals. That includes _you_. What people do read are _error messages_. Consider the following function stub, which is meant to convolve two vectors together:

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

This code does not tell you how to use it: it _yells_ at you if you use it wrong. The first way relies on your good nature to read the docs; the second way _forces you_ to use the code as it was intended. I would argue that the second is better [^combine]. There are several ways to generate user errors:

[^combine]: You can combine raising errors and write good docstrings.

- `assert`: When an assert doesn't pass, it raises an `AssertionError`. You can optionally add an error message at the end.
- `NotImplementedError`, `ValueError`, `NameError`: [Commonly used, generic errors](https://docs.python.org/3/library/exceptions.html) you can raise. I probably overuse `NotImplementedError` compared to other types.
- Type hints: Python 3 has type hints, and you can optionally enforce type checking using decorators with [`enforce`](https://github.com/RussBaz/enforce) or [`pytypes`](https://pypi.org/project/pytypes/). Type checking is a bit controversial because it goes against Python's dynamic nature. It depends on your use case: if you like them, use them.

The unit tests that we discussed last chapter are another mechanism through which you can raise errors - not in the main code path of your code, but in a secondary path that you run through the `pytest` command line.

## Write in-line comments

```{epigraph}
Don’t comment bad code - rewrite it.
-- Kernighan & Plaugher, cited by Robert Martin in [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
```

In-line comments are often used to explain away bad code; you'd be better off rewriting the code rather than to explain the mess. Instead, aim to write code so that it needs few in-line comments. For instance, this code snippet uses meaningless variables names, so we have to explain its function in a comment:

```python
# Iterate over lines
for l in L:
    pass
```

Instead, we can clarify the code by using more meaningful variable names:

```python
for line in lines:
    pass
```

Before commenting in-line on a piece of code, ask yourself: could I write this in a way that the code is self-explanatory? Then change your code to achieve that. You can then reserve in-line comments to give context that is not readily available in the code itself. There are some essential things you should comment in-line:

- _References to papers_ with page numbers and equation numbers (e.g. see Mineault et al. (2011), Appendix equation 2 for definition)
- _Explanations of tricky code_, and why you wrote it the way you did, and why it does the thing that it does
- _TODOs_. Your Python editor recognizes special `TODO` comments and will highlight them.

```
# TODO(pmin): Implement generalization to non-integer numbers
```

You can similarly highlight code that needs to be improved with `FIXME`.

## Write docstrings

Python uses multi-line strings - docstrings - to document individual functions. Docstrings can be read by humans directly. They can be also be read by machines to create HTML documentation, so they're particularly useful if your code is part of a publicly available package. There are three prevalent styles of docstrings:

```{margin}
[Sphinx](https://www.sphinx-doc.org/en/master/) is the standard way to generate HTML documentation in Python. Sphinx is very powerful - this book is generated by jupyterbook, which uses sphinx to do its job!
```

- [reST (reStructuredText)](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)
- [Google style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
- [Numpy style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html)

reST is more prevalent because it's the default in Sphinx, but I think the Google style is easier to read for humans and I prefer it. Here's how you would document a function which counts the number of occurrences of a line:

````{tabbed} Google-style
```
def count_line(f, line):
    """
    Counts the number of times a line occurs. Case-sensitive.

    Arguments:
        f (file): the file to scan
        line (str): the line to count

    Returns:
        int: the number of times the line occurs.
    """
    num_instances = 0
    for l in f:
        if l.strip() == line:
            num_instances += 1

    return num_instances
```
````

````{tabbed} Numpy-style
```
def count_line(f, line):
    """
    Counts the number of times a line occurs. Case-sensitive.

    Parameters
    ----------
    f: file
        the file to scan
    line: str
        the line to count

    Returns
    -------
    int
        the number of times the line occurs.
    """
    num_instances = 0
    for l in f:
        if l.strip() == word:
            num_instances += 1

    return num_instances
```
````

````{tabbed} reST
```
def count_word(f, line):
    """
    Counts the number of times a line occurs. Case-sensitive.

    :param f: the file to scan
    :type f: file
    :param line: the line to count
    :type line: str
    :returns: the number of times the line occurs.
    :rtype: int
    """
    num_instances = 0
    for l in f:
        if l.strip() == line:
            num_instances += 1

    return num_instances
```
````

Docstrings for this function will appear in the REPL and in jupyter notebook when you type `help(count_word)` - they will also be parsed and displayed in IDEs like vscode and PyCharm.

See which style of docstring you prefer and stick to it. Autodocstring, an extension in vscode, can you help you [automatically generate a docstring stub](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring). It uses the Google style by default.

```{warning}
Docstrings can age poorly. When your arguments change, it's easy to forget to change the docstring accordingly. I prefer to wait until later in the development process when function interfaces are stable to start writing docstrings.
```

## Publish docs on Readthedocs

```{margin}
Sphinx can auto-generate docs from Google and Numpy-style docstrings [with a plugin](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html).
```

You know those sweet static docs that you see on readthedocs? You can generate this kind of documentation from docstrings using Sphinx. [There's a great tutorial to get you started](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html), but in essence getting basic generated docs is a matter of typing 4 commands:

```shell
pip install sphinx
cd docs
sphinx-quickstart
make html
```

[Uploading the docs to readthedocs](https://docs.readthedocs.io/en/stable/tutorial/index.html#importing-the-project-to-read-the-docs) (or Github pages or netlify) is a one-command affair. Docs which focus exclusively on usage (what arguments to use, their types, the returns) are of pretty limited use by themselves. They're powerful when combined with high-level instructions, tutorials and walkthroughs. We'll cover how to write these in the next chapter.

## Discussion

Good documentation helps maintain the long-term memory of a project. Very tricky code must be documented with care so that the memory of its intent and implementation is preserved. However, if you have a choice between documenting tricky code and refactoring the code so that it's less tricky, you'll often find that refactoring code pays off over the long term. Similarly, it's often more productive to write unit tests that lock in how the code works than to explain how the code _should_ work in words. Document code that needs to be documented, improve the code that can be improved, and develop the wisdom to tell them apart.

```{admonition} 5-minute exercise
Write a docstring for a function you've worked on.
```
