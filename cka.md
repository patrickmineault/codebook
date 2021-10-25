
# Example: Testing code

Let's put some of the ideas we learned in a practical example. This example implements a computational method called CKA which was introduced [in a paper](https://arxiv.org/abs/1905.00414). Importantly, CKA is not already implemented in scipy or sci-kit learn or in any other pip installable package: we're flying solo[^caveat]. 

[^caveat]: [There is an implementation in a notebook from the authors](https://colab.research.google.com/github/google-research/google-research/blob/master/representation_similarity/Demo.ipynb). 

Does this make you nervous? It should! It's easy to make a mistake in a computational pipeline and get the wrong results. With the structured approach that I've introduced in this handbook, you can work with far more confidence.

```{note}
This example is math-heavy. I have another example that deals with less purely mathematical things next.
```

## Background on centered kernel alignment

We're going to implement centered kernel alignment (CKA) and apply it on test data. Because I wanted the method not to be implemented already in a major Python package, it had to be pretty obscure. I don't expect anyone reading this to have already heard of CKA, so a quick intro is in order. In brief, *CKA is a way to compare two matrices, in the same way that Pearson's correlation can compare two vectors*, with applications to studying the brain and neural nets.

### Background

Deep artificial neural nets perform fabulous feats, whether it's detecting objects in images or translating speech to text. Neuroscientists often wondered whether or not these neural nets do their work in ways similar to the brain. To answer this question, they've created methods that rely on the same core recipe: 

1. pick a battery of stimuli
2. measure the response of a brain to the battery of stimuli (in a MRI scanner, let's say)
2. measure the response of a deep neural net to the battery of stimuli. 

If the two sets of responses are similar, that means the brain and the deep neural net are aligned in some sense. We collect the responses into two matrices, $X$ and $Y$ which are of size NxK and NxL, respectively; N is the number of stimuli. Then the game is to compare the two matrices $X$ and $Y$. CKA is a metric introduced in Kornblith et al. (2019) that can be used to compare two matrices which has some nice properties. 

### Definition

CKA is defined as:

$$CKA(\mathbf X, \mathbf Y) = \frac{||\mathbf X^T \mathbf Y||_2^2}{||\mathbf X^T \mathbf X||_2 ||\mathbf Y^T \mathbf Y||_2}$$

The columns $X$ and $Y$ are centered. $|| \cdot ||_2$ is the Frobenius norm, the root of the sum of squares of the entries. 

When the CKA is 0, the two representations are different, when it's 1, the two representations are similar. You might notice that the formula resembles Pearson's correlation:

$$r_{xy} =\frac{\sum ^n _{i=1}(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum ^n _{i=1}(x_i - \bar{x})^2} \sqrt{\sum ^n _{i=1}(y_i - \bar{y})^2}}$$

In fact, CKA is the square of the Pearson's correlation when $X$ and $Y$ are vectors. You can thus think of the CKA as a generalization of Pearson's correlation for matrices.

## Initial implementation

Based off of the definition above, we can implement a working version of CKA with the following code. In `cka_step1.py`:

```python
import numpy as np

def cka(X, Y):
    # Implements linear CKA as in Kornblith et al. (2019)

    # Center X and Y
    X -= X.mean(axis=0)
    Y -= Y.mean(axis=0)

    # Calculate CKA
    XTX = X.T.dot(X)
    YTY = Y.T.dot(Y)
    YTX = Y.T.dot(X)

    return (YTX ** 2).sum() / np.sqrt((XTX ** 2).sum() * (YTY ** 2).sum())
```

Now, is this function *correct*? In these ten lines of code, there's a lot of trickiness going on:

* This function centers the columns of $X$... or does it? Should it remove `X.mean(axis=1)$` instead?
* Is this function pure? Does it change its arguments $X$ and $Y$?
* In the last line: is this the correct definition of the Frobenius norm? Or are we off by a squaring factor?

Indeed, a lot can go wrong in implementing this short function. Let's write down some test to reassure ourselves that this function does what it needs to do.

## Writing our first test

The first test is the identity test: the CKA of a matrix with itself is 1, just like with Pearson's correlation. Let's write the identity test as part of a test suite.

Let's code CKA tests. We will turn properties of CKA listed in the paper into tests. In `cka_step1.py`, we write:

```python
from cka import cka
import numpy as np

def test_identity():
    # Create a random matrix and check it is perfectly correlated with itself.
    X = np.random.randn(100, 2)
    assert cka(X, X) == 1.0
```

Great! Now we can run our test suite with pytest:

```console
(cb) ~/Documents/codebook_examples/cka$ pytest .
============================= test session starts ==============================
platform linux -- Python 3.8.11, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /home/pmin/Documents/codebook_examples/cka
plugins: anyio-3.3.0
collected 1 item

test_cka.py F                                                            [100%]

=================================== FAILURES ===================================
________________________________ test_identity _________________________________

    def test_identity():
        # Create a random matrix and check it is perfectly correlated with itself.
        X = np.random.randn(100, 2)
>       assert cka(X, X) == 1.0
E       assert 0.9999999999999994 == 1.0
```

Here we've run into one of the tricky bits about running numberical code -  numerical instability. When 1.0 is very close to 0.9999999999999994, but it's not exactly equal. We can replace our test with a more lenient one. Numpy's `np.testing.assert_allclose` can test that two arrays are close enough to each other entry-wise::

```python
def test_identity_lenient():
    # Create a random matrix and check it is perfectly correlated with itself.
    X = np.random.randn(100, 2)
    np.testing.assert_allclose(cka_start(X, X), 1.0)
```

And now we find the tests pass. Let's add one more test to the mix: a matrix and itself are perfectly correlated, *regardless of the order of their columns*. We can make a new test for that.

```python
def test_column_swaps():
    # Check that a matrix is perfectly correlated with itself even with column swaps.
    X = np.random.randn(100, 2)
    c = cka_start(X[:, [0, 1]], X[:, [1, 0]])
    np.testing.assert_allclose(c, 1.0)
```

And now the tests pass:

```console
(cb) $ pytest .
(cb) pmin@wintop:~/Documents/codebook_examples/cka$ pytest .
============================= test session starts ==============================
platform linux -- Python 3.8.11, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /home/pmin/Documents/codebook_examples/cka
plugins: anyio-3.3.0
collected 2 items

test_cka_step1.py ..                                                     [100%]

```

## Checking centering

Now let's add more tests - namely that CKA that we're doing centering correctly. It shouldn't matter how columns are centered. Let's add a test to this effect.

```
def test_centering():
    # Check that a matrix is perfectly correlated with itself even with adding column offsets
    X = np.random.randn(100, 2)
    Xp = X.copy()
    Xp[:, 1] += 1.0

    c = cka(X, Xp)
    np.testing.assert_allclose(c, 1.0)
```

Run it in pytest - it works! That means we did the centering correctly. Indeed, we correctly removed `X.mean(axis=0)` from `X` and `Y.mean(axis=0)` from `Y`. But wait a minute - when we center in our function, do we change the original matrix? We can add a test to check that:

```
(cb) ~/Documents/codebook_examples/cka$ pytest .
============================= test session starts ==============================
platform linux -- Python 3.8.11, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /home/pmin/Documents/codebook_examples/cka
plugins: anyio-3.3.0
collected 4 items

test_cka_step1.py ...F                                                   [100%]

=================================== FAILURES ===================================
__________________________________ test_pure ___________________________________

    def test_pure():
        # Check that a function doesn't change the original matrices
        X = np.random.randn(100, 2)
        Xp = X.copy()
        Xp[:, 1] += 1.0

        Xp_original = Xp.copy()
        c = cka(X, Xp)
>       np.testing.assert_allclose(Xp_original[:, 1], Xp[:, 1])
E       AssertionError:
E       Not equal to tolerance rtol=1e-07, atol=0
```

We see that this function modifies its argument. If you scroll back up to the `cka` definition, you can see that we used the `-=` in-place assignment operator - that caused the original matrix to change. If this tripped you up - don't worry! I was very confused by this as well. This line changes the original memory:

```
X -= X.mean(axis=0)
```

But this line doesn't:

```
X = X - X.mean(axis=0)
```

Who knew! This kind of subtle semantic difference can really trip you up. We can  clarify the intent of the code using `copy()` to identicate that we don't want to change the original array: this way, the function's intent is very clear. In `cka_step2.py`, we write the function a different way:

```
import numpy as np

def cka(X, Y):
    # Implements linear CKA as in Kornblith et al. (2019)
    X = X.copy()
    Y = Y.copy()

    # Center X and Y
    X -= X.mean(axis=0)
    Y -= Y.mean(axis=0)

    # Calculate CKA
    XTX = X.T.dot(X)
    YTY = Y.T.dot(Y)
    YTX = Y.T.dot(X)

    return (YTX ** 2).sum() / np.sqrt((XTX ** 2).sum() * (YTY ** 2).sum())
```

Now we copy our old tests into `test_cka_step2.py`, and the issue is fixed:

```
(cb) ~/Documents/codebook_examples/cka$ pytest test_cka_step2.py
============================= test session starts ==============================
platform linux -- Python 3.8.11, pytest-6.2.5, py-1.10.0, pluggy-1.0.0
rootdir: /home/pmin/Documents/codebook_examples/cka
plugins: anyio-3.3.0
collected 4 items

test_cka_step2.py ....                                                   [100%]
```

## More properties

CKA has several more properties which we can test. Many of these are listed in the paper:

* the CKA is the square of the Pearson's correlation when $X$ and $Y$ are vectors.
* the CKA is insensitive to rotations
* the CKA is insensitive to scaling the entire matrix
* the CKA is sensitive to scaling different columns differently

Here, it becomes useful to create a few helper functions to generate sample signals: matrices made of sinusoids. We'll remove our reliance on random data: it's generally good practice to have *deterministic* tests. Non-deterministic tests that sometimes work and sometimes don't are *flaky*, and they can be a pain. Let's put it all together:

```python
from cka_step2 import cka
import numpy as np
import pytest

def _get_one():
    X = np.cos(.1 * np.pi * np.arange(10)).reshape((-1, 1))
    Y = np.cos(2 + .07 * np.pi * np.arange(10)).reshape((-1, 1))
    return X, Y

def _get_multi():
    X = np.cos(.1 * np.pi * np.arange(10).reshape((-1, 1)) * np.linspace(.5, 1.5, num=3).reshape((1, -1)))
    Y = np.cos(.5 + .07 * np.pi * np.arange(10).reshape((-1, 1)) * np.linspace(.7, 1.3, num=4).reshape((1, -1)))
    return X, Y

def test_identity_lenient():
    """Create a random matrix and check it is perfectly correlated with itself."""
    X, _ = _get_multi()
    np.testing.assert_allclose(cka(X, X), 1.0)

def test_column_swaps():
    """Check that a matrix is perfectly correlated with itself even with column swaps."""
    X, _ = _get_multi()
    c = cka(X[:, [0, 1]], X[:, [1, 0]])
    np.testing.assert_allclose(c, 1.0)

def test_centering():
    """Check that a matrix is perfectly correlated with itself even with adding column offsets."""
    X, _ = _get_multi()
    Xp = X.copy()
    Xp[:, 1] += 1.0

    c = cka(X, Xp)
    np.testing.assert_allclose(c, 1.0)

def test_pure():
    """Check that a function doesn't change the original matrices."""
    X, _ = _get_multi()
    Xp = X.copy()
    Xp[:, 1] += 1.0

    Xp_original = Xp.copy()
    c = cka(X, Xp)
    np.testing.assert_allclose(Xp_original[:, 1], Xp[:, 1])

def test_corr():
    """The CKA of two vectors is the square of the correlation coefficient"""
    X, Y = _get_one()
    c1 = cka(X, Y)
    c2 = np.corrcoef(X.squeeze(), Y.squeeze())[0, 1] ** 2
    np.testing.assert_allclose(c1, c2)

def test_isoscaling():
    """CKA is insensitive to scaling by a scalar"""
    X, Y = _get_multi()
    c1 = cka(X, Y)
    c2 = cka(2.0 * X, - 1 * Y)
    np.testing.assert_allclose(c1, c2)

def test_rotation():
    """CKA is insensitive to rotations"""
    X, Y = _get_multi()
    X0 = X[:, :2]
    X0p = X0 @ np.array([[1, -1], [1, 1]]) / np.sqrt(2)
    c1 = cka(X0, Y)
    c2 = cka(X0p, Y)
    np.testing.assert_allclose(c1, c2)

def test_no_iso():
    """CKA is sensitive to column scaling"""
    X, Y = _get_multi()
    X0 = X[:, :2]
    X0p = X0 @ np.array([[1, 1], [10, 1]])
    c1 = cka(X0, Y)
    c2 = cka(X0p, Y)
    assert abs(c1 - c2) > .001
```

It's starting to get quite long! For numeric code, it's not unusual that the test code should be several times longer than the code it's testing. Indeed, when you introduce a new numerical method, you might spend days testing it on different inputs to check that it gives reasonable outputs. Testing takes this common practice and formalizes it. Now, you can rest assured that the code works as intended.

## Dealing with wide matrices

Before we add more features to the code, it's important to make sure that what is already there is correct. It's all to easy to build too much in a vacuum, and we are left debugging a giant chunk of code. 

In our case, a nice feature we might want is the ability to deal with wide matrices. The implementation we have works well for tall, skinny matrices - but neural nets are generally over-parametrized and frequently have big intermediate representations. So we'd like the ability to deal with wide matrices. The paper introduces another method to compute the CKA with wide matrices which is far more memory efficient. We can change our implementation to deal with these larger matrices efficiently - and of course, add more tests to make sure we didn't mess up anything! Tests are what allow us to move with confidence. Take a look at the final version of the code to see how we can test that our code works as expected.

## Final thoughts

We've gone through a complex example of testing numerical code. We build infrastructure to test the code, found a gnarly bug, and were able to expand our code to deal with new conditions. In the end, we could be confident that our code is correct. 