
# Enough theory!

Let's de-couple CKA!

# Background on centered kernel alignment

Q: how can we compare how different brain areas and artificial neural networks represent the world?

A: Choose a standard battery of stimuli, measure responses across systems, compare the responses between the systems. Many approaches, including: 

* forward encoding models (e.g. ridge regression)
* canonical correlation analysis (CCA)
* representational similarity analysis (RSA). 

# CKA

[Kornblith et al. (2019)](https://arxiv.org/abs/1905.00414) propose a new method to compare representations. You can think of it as a generalization of the (square of the) Pearson correlation coefficient, but with matrices instead of vectors.

![Alignment between layers of two neural nets initialized with different seeds](../figures/cka_example.png){height=100px}

Importantly, CKA is not implemented in scipy or sklearn, github gives very few hits ^[1]... it's real research code!

[1] [There is an implementation in a notebook from authors](https://colab.research.google.com/github/google-research/google-research/blob/master/representation_similarity/Demo.ipynb)

# Centered kernel alignment

* We collect the responses of each system to our battery of $n$ stimuli into matrices $\mathbf{X}, \mathbf{Y}$. 
* $\mathbf{X}, \mathbf{Y}$ have shape $n x k$, $n x l$, and $k$ and $l$ are not necessarily the same.
* Center $\mathbf{X}, \mathbf{Y}$ so each column has 0 mean, then:

$$CKA(\mathbf X, \mathbf Y) = \frac{||\mathbf X^T \mathbf Y||_2^2}{||\mathbf X^T \mathbf X||_2 ||\mathbf Y^T \mathbf Y||_2}$$

* Min 0, max 1
* Check: if $\mathbf{X}$ and $\mathbf{Y}$ are one-dimensional, then $CKA = \rho( \mathbf X, \mathbf Y)^2$.


# Open discussion

Q: What's not ideal about this code? `research_code.cka_not_great.py`

# Pain points

* IO, computation and plotting are all in one big blob
* Solution: isolate the computation in its own function independent of IO
* Put the controller in the `main` function, hide behind `__name__ == "__main__"`
    * Avoids module variables in Python
    * Makes the code importable

# Live coding!

(the result is `cka_step2.py`)


A: 
# Demo

Let's code CKA tests. We will turn properties of CKA listed in the paper into tests.

# What we know about CKA

* Only makes sense if two matrices are the same size along the first dimension
* Pearson correlation: If $\mathbf{X}$ and $\mathbf{Y}$ are one-dimensional, then $CKA = \rho( \mathbf X, \mathbf Y)^2$.
* $CKA(\mathbf X, \mathbf X) = 1$

# Live coding

Note: to follow at home, look at `cka_step3.py` and `tests/test_cka_step3.py`.

# What else can we know about CKA? Let's read the paper!

* 2.1 _not_ invariant to non-isotropic scaling
* 2.2 invariant to rotations, $CKA(\alpha \mathbf{X U}, \beta \mathbf{Y V}) = CKA(\mathbf X, \mathbf Y)$

![Invariance to rotation](../figures/invariance_to_ortho.PNG){height=85px}

* 2.3 invariant to isotropic scaling, $CKA(\alpha \mathbf X, \beta \mathbf Y) = CKA(\mathbf X, \mathbf Y)$