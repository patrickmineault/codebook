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

(test)=

# Test your code

```{epigraph}
Most scientists who write software constantly test their code. That is, if you are a scientist writing software, I am sure that you have tried to see how well your code works by running every new function you write, examining the inputs and the outputs of the function, to see if the code runs properly (without error), and to see whether the results make sense. Automated code testing takes this informal practice, makes it formal, and automates it, so that you can make sure that your code does what it is supposed to do, even as you go about making changes around it. 

--[Ariel Rokem](https://github.com/uwescience/shablona)
```

Automated testing is one of the most powerful techniques that professional programmers use to make code robust. I think it should be taught in introductory Python classes for scientists - it's quite intuitive, and once you learn it, it will change the way you write code for the better.

## Testing to maintain your sanity

When you run an experiment and the results of the analysis don't make sense, you will go through a process of eliminating one potential cause after the other. You will investigate several hypotheses, including:

* the data is bad
* you're loading the data incorrectly
* your model is incorrectly implemented
* your model is inappropriate for the data
* the statistical test you used is inappropriate for the data distribution

Testing can help you maintain your sanity by decreasing the surface of things that might be wrong with your experiment. Good code yells loudly when something goes wrong. Imagine that you had an experimental setup that alerted you when you had a ground loop, or that would sound off when you use the wrong reagent, or that would text you when it's about to overheat - how many hours or days would you save?

## Testing by example

The easiest way to understand testing is to illustrate it with a specific example. The Fibonacci sequence is defined as:

$$F(x) \equiv F(x-1) + F(x-2)$$
$$F(0) \equiv 0 $$
$$F(1) \equiv 1 $$

[The first few items in the Fibonacci sequence](https://oeis.org/A000045) are:

$$F = 0, 1, 1, 2, 3, 5, 8, 13, 21, \ldots$$

Let's write up a naive implementation of this.

```{code-cell}
def fib(x):
    if x <= 2:
        return 1
    else:
        return fib(x - 1) + fib(x - 2)
```

Let's say that a colleague brings you this code and asks you to check that the code they've written up works. How would check whether this code works?

````{dropdown} ⚠️ Spoilers
You could run this code on the command line with different inputs and check that the code works as expected. For instance, you expect that:

```pycon
>>> fib(0)
0
>>> fib(1)
1
>>> fib(2)
1
>>> fib(6)
8
>>> fib(40)
102334155
```

You could also run the code with bad inputs, to check whether the code returns meaningful errors. For example, the sequence is undefined for negative numbers or non-integers.
````

Informal testing can be done in an interactive computing environment, like the `ipython` REPL or a jupyter notebook. Run the code, check the output, repeat until the code works right -- it's a workflow you've probably used as well.

### Lightweight formal tests with `assert`

One issue with informal tests is that they often have a short shelf life. Once the code is written and informal testing is over, you don't have a record of that testing - you might even discard the tests you wrote in jupyter! We can make our tests stick with `assert`. 

`assert` is a special statement in Python that throws an error whenever the statement is false. For instance, 

```
>>> assert 1 == 0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError
```

Notice that there are no parentheses between `assert` and the statement. `assert` is great for inline tests, for example checking whether the shape or a matrix is as expected after permuting its indices. 

We can also assemble multiple assert operations to create a lightweight test suite. You can hide your asserts behind an `__name__ == '__main__'` statement, so that they will only run when you directly run a file. Let's write some tests in `fib.py`:

```{code-cell}
:tags: ["raises-exception"]
def fib(x):
    if x <= 2:
        return 1
    else:
        return fib(x - 1) + fib(x - 2)

if __name__ == '__main__':
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(6) == 8
    assert fib(40) == 102334155
    print("Tests passed")
```

Now we can run the tests from the command line:

```console
$ python fib.py
Traceback (most recent call last):
  File "fib.py", line 8, in <module>
    assert fib(0) == 0
AssertionError
```

We see our test suite fail immediately for `fib(0)`. We can fix up the boundary conditions of the code, and run the code again. We repeat this process until all our tests pass. Let's look at the fixed up code:

```{code-cell}
def fib(x):
    if x == 0:
        return 0
    if x == 1:
        return 1
    else:
        return fib(x - 1) + fib(x - 2)

if __name__ == '__main__':
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(6) == 8
    assert fib(40) == 102334155
    print("Tests passed")
```

While the first few tests pass, the last one hangs for a long time. What's going on here?

### Refactoring with confidence with tests

Our `fib(N)` function hangs for a large value of `N` because it spawns a lot of repeated computation. `fib(N)` calls both `fib(N-1)` and `fib(N-2)`. In turn, `fib(N-1)` calls `fib` twice, and so on and so forth. Therefore, the time complexity of this function scales exponentially with $2^N$ - it's very slow.

We can re-implement this function so that it keeps a record of previously computed values. One straightforward way of doing this is with a global cache. **We keep our previously implemented tests**, and rewrite the function:

```{code-cell}
cache = {}
def fib(x):
    global cache
    if x in cache:
        return cache[x]
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        val = fib(x - 1) + fib(x - 2)
        cache[x] = val
        return val

if __name__ == '__main__':
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(6) == 8
    assert fib(40) == 102334155
    print("Tests passed")
```

Running this new and improved script, we see:

```console
$ python fib.py
Tests passed
```

Hurray! We can be confident that our code works as expected. What if we want to refactor our code so that it doesn't use globals? Not a problem, we keep the tests around, and we rewrite the code to use an inner function:

```{code-cell}
def fib(x):
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

if __name__ == '__main__':
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(6) == 8
    assert fib(40) == 102334155
    print("Tests passed")
```

Running the module again, our tests still pass! Testing helps us refactor with confidence because we can immediately tell whether we've introduced new bugs in our code.

### Testing pure functions

With pure functions, such as `fib`, we can readily come up with ways to test whether the code works or not. We can check:

* *Correctness for typical inputs*, e.g. $F(5) = 5$
* *Edge cases*, e.g. $F(0) = 0$
* *Errors* with bad input, e.g. $F(-1)$ → *error*
* *Functional goals are achieved*, e.g. that the function works for large numbers

Pure functions don't require elaborate setups to test properly, and indeed they have some of the highest *bang for you buck* when it comes to testing. If in your current workflow, you would have manually checked whether a procedure yielded reasonable results, write a test for it. 

```{tip}
If something caused a bug, write a test for it. 70% of bugs are old bugs that keep reappearing.
```

### Testing with a test suite

Testing with `assert` hidden behind `__name__ == '__main__'` works great for small-scale testing. However, once you have a lot of tests, it starts to make sense to group them into a *test suite* and run them with a *test runner*. There are two main frameworks to run unit tests in Python, `pytest` and `unittest`. `pytest` is the more popular of the two, so I'll cover that here.

Writing a test suite for pytest is a matter of taking our previous unit tests and putting them in a separate file, wrapping them in functions which start with `test_`. In `tests/test_fib.py`, we write:

```
from src.fib import fib
import pytest

def test_typical():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(6) == 8
    assert fib(40) == 102334155

def test_edge_case():
    assert fib(0) == 0

def test_raises():
    with pytest.raises(NotImplementedError):
        fib(-1)

    with pytest.raises(NotImplementedError):
        fib(1.5)
```

Notice that pytest primarily relies on the `assert` statement to do the heavy lifting. `pytest` also offers extra functionality to deal with special test cases. `pytest.raises` creates a context manager to verify that a function raises an expected exception.

Running the `pytest` utility from the command line, we find:

```console
$ pytest test_fib.py
...
    def fib_inner(x):
        nonlocal cache
        if x in cache:
            return cache[x]
>       if x == 0:
E       RecursionError: maximum recursion depth exceeded in comparison

../src/fib.py:7: RecursionError
============================= short test summary info =============================
FAILED test_fib.py::test_raises - RecursionError: maximum recursion depth exceed...
=========================== 1 failed, 2 passed in 1.18s ===========================
```

Notice how informative the output of pytest is compared to our homegrown test suite. `pytest` informs us that two of our tests passed - `test_typical` and `test_edge_case` - while the last one failed. Calling our `fib` function with a negative argument or a non-integer argument will make the function call itself recursively with negative numbers - it never stops! Hence,  Python eventually will generate a `RecursionError`. However, our tests are expecting a `NotImplementedError` instead! Our test correctly detected that the code has this odd behavior. We can fix it up like so:

```{code-cell}
def fib(x):
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

Now we can run tests again.

```console
$ pytest test_fib.py 
=============================== test session starts ===============================
platform linux -- Python 3.8.8, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /home/pmin/Documents/codebook
plugins: anyio-3.1.0
collected 3 items                                                                 

test_fib.py ...                                                             [100%]

================================ 3 passed in 0.02s ================================
```

They pass! 

## Testing non-pure functions and classes

I claimed earlier that *pure functions* are the easiest to test. Let's see what we need to do to test non-pure functions. For a *nondeterministic* function, you can usually give the random seed or random variables needed by the function as arguments, turning the nondeterministic function into a deterministic one. For a *stateful* function, we need to additionally test that:

* *Postconditions are met*, that is, the internal state of the function or object is changed in the expected way by the code

Classes are stateful, so we'll need to inspect their state after calling methods on them to make sure they work as expected. For example, consider this Chronometer class:

```{code-cell}
import time

class Chronometer:
    def start(self):
        self.t0 = time.time()

    def stop(self):
        return time.time() - self.t0
```

We might want to check that the `t0` variable is indeed set by the `start` method.

For a function with *I/O side effects*, we'll need to do a little extra work to verify that it works. We might need to create mock files to check whether inputs are read properly and outputs are as expected. `io.StringIO` and the `tempfile` module can help you create these mock objects. For instance, suppose we have a function `file_to_upper` that takes in an input and an output filename, and turns every letter into an uppercase:

```{code-cell}
def file_to_upper(in_file, out_file):
    fout = open(out_file, 'w')
    with open(in_file, 'r') as f:
        for line in f:
            fout.write(line.upper())
    fout.close()
```

Writing a test for this is a little tortured:

```{code-cell}
import tempfile
import os

def test_upper():
    in_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    out_file = tempfile.NamedTemporaryFile(delete=False)
    out_file.close()
    in_file.write("test123\nthetest")
    in_file.close()
    file_to_upper(in_file.name, out_file.name)
    with open(out_file.name, 'r') as f:
        data = f.read()
        assert data == "TEST123\nTHETEST"
    os.unlink(in_file.name)
    os.unlink(out_file.name)
```

With remote calls and persistent storage, testing can rapidly become quite complex. 

## A hierarchy of tests

What we've been focused on so far are *unit tests*. Unit tests test a *unit* of code, for example, a function. However, there are many different kinds of tests that people use. 

* *Static tests*: your editor parses and runs your code as you write it to figure out if it will crash
* *Inline asserts*: test whether intermediate computations are as expected
* *Unit tests*: test whether one function or unit of code works as expected
* *Docstring tests*: unit tests embedded in docstrings
* *Integration tests*: test whether multiple functions work correctly together
* *Smoke tests*: test whether a large piece of code crashes at an intermediate stage
* *Regression tests*: tests whether your code is working the way you expect to
* *End-to-end tests*: literally a robot clicking buttons to figure out if your application works as expected

The point is not to overwhelm you with the possibilities, but to give you a glossary of testing so you know what to look for when you're ready to dig deeper.

## Write lots of tiny unit tests

My proposal to you is modest:

1. Isolate numeric code. 
2. Make numeric functions pure if practical. 
3. Write tests for the numeric code
4. Write tests for the critical IO code

You're going to get a lot of bang for your buck by writing unit tests - inline asserts and regression tests are also high payoff-to-effort. Aim for each unit test to run in 1 ms. The faster each test runs, the better for your working memory. More than 5 seconds and you'll be tempted to check your phone.

What do you think is the ideal ratio of test code to real code?

```{dropdown} ⚠️ Spoilers
There's no ideal number per say, but 1:1 to 3:1 is a commonly quoted range for library code. For one-off code, you can usually get away with less test coverage. For more down-to-earth applications, 80% test coverage is a common target. [You can use the `Coverage.py` package to figure out your test coverage](https://coverage.readthedocs.io/en/coverage-5.3.1/).
```

## Now you're playing with power

Testing is the key to refactor with confidence. Let's say that your code looks ugly, and you feel like it's time to refactor. 

1. Lock in the current behavior of your code with regression tests
1. Check that the tests pass
1. Rewrite the code to be tidy
1. Correct the code
1. Iterate until tests pass again

You can call `pytest` with a specific filename to run one test suite. For a larger refactor, you can run all the tests in the current directory with:

```
$ pytest .
```

If you want, you can even integrate this workflow into github by running tests every time you push a commit! This is what's called *continuous integration*. It's probably overkill for a small-scale project, but know that it exists.

## Discussion

Writing tests is not part of common scientific practice yet, but I think it deserves a higher place in scientific programming education. 

Testing allows you to decrease the uncertainty surface of your code. With the right tests, you can convince yourself that parts of your code are *correct*, and that allows you to concentrate your debugging efforts. Keeping that uncertainty out of your head saves your working memory, and debugging will be faster and more efficient. At the same time, code with tests is less stressful to refactor, so you will be able to continuously improve your code so that it doesn't slide towards an unmanageable mess of spaghetti.

Testing is not an all-or-none proposition: you can start writing lightweight inline tests in your code today. Find a commented out `print` statement in your code. Can you figure out how to replace it with an `assert`?

```{admonition} 5-minute exercise
Find a commented out `print` statement in your code and transform it into an `assert`.
```