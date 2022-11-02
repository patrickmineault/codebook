---
title: How to read this book
exports:
  - format: tex
    logo: false
    template: ../templates/plain_latex_book_chapter
    output: exports/roadmap.tex
---

# Roadmap

This handbook covers practices and tools from big to small. We'll discuss how to write and organize modular code, how to write docs, how to make your code robust. We'll finally reveal the correct number of spaces to use to indent code [^four]. At the end of the main lessons, we'll go through an example project step-by-step.

This roadmap shows some of the concepts we'll cover in the book. Take stock of where you are now. Come back to this figure after you've read parts of this book: you'll be surprised how much you can learn in a few hours!

[^four]: [Four. Four is the correct number](https://www.python.org/dev/peps/pep-0008/).

```{figure} figures/concepts.svg
---
figclass: boxed
width: 100%
---
Some concepts we'll cover in this book. I've highlighted in green and blue different concepts which are relevant to short-term and to long-term memory, respectively: we'll discuss what that means in the next section. How many concepts are you familiar with now? How many do you know well?
```

## Conventions

This book uses a number of conventions throughout. The command line is indicated by a `$` prompt:

```
$ ls -al
```

The Python command prompt is indicated by `>>>`:

```
$ python
>>> import antigravity
```

Sometimes I will ask you a question, and will hide the answer behind a spoilers panel. For example, what is the answer to life, the universe, and everything?

```{dropdown} Spoilers
42
```

At the end of each main lesson, I ask you to put one of the lessons into practice through a 5-minute exercise. It looks like this:

```{admonition} 5-minute exercise
Brush your teeth.
```

## Code

This handbook refers to code in several repositories:

- [True neutral cookie cutter](https://github.com/patrickmineault/true-neutral-cookiecutter): `github.com/patrickmineault/true-neutral-cookiecutter`
- [CKA example](https://github.com/patrickmineault/codebook_examples/tree/main/cka): `github.com/patrickmineault/codebook_examples`
- [Zipf's law example project](https://github.com/patrickmineault/zipf/): `github.com/patrickmineault/zipf`
- [Source for the text of the book](https://github.com/patrickmineault/codebook): `github.com/patrickmineault/codebook`
- [Tweaked sphinx book theme](https://github.com/patrickmineault/sphinx-book-theme/): `patrickmineault/sphinx-book-theme`

You can use these as references when you're working on your own projects.

## Breaking the cycle of frustration

Learning to code is a lifelong journey. The upper ceiling on programming skills is very high. Much like cooking, coding can be done on a purely utilitarian basis, or it can be elevated to high art. [Professional programmers with decades of experience go on months-long retreats to acquire new skills](https://www.recurse.com/not-a-bootcamp). _A good frame_ for getting better at coding is to think of it as a _craft_. Reading this book is a great way to refine your craft through focused practice [^calnewport].

[^calnewport]: CS professor Cal Newport explores these themes in his book [So Good They Can't Ignore You](https://www.calnewport.com/books/so-good/).

When I talk to students about writing code, a lot of them describe feelings like:

- guilt
- shame
- cringe
- frustration

```{margin}
Julia Evans [has a lovely zine](https://wizardzines.com/comics/attitude-matters/) on dealing with frustrating bugs.
```

Much of that frustration comes from a mismatch between what you want to accomplish (a lot) and what you have the ability to accomplish (not as much as you'd like). Programming instruction often emphasizes _exploration_, embracing errors as learning opportunities, and encouraging you to let your imagination run free. This theory of change implies that you will learn a lot by simply programming a lot every day. You might then feel guilty and inadequate when you're not as proficient as you want after several years of daily programming.

In fact, unstructured exploration is a very inefficient way to learn a complex skill like programming. It's like expecting a student to rediscover calculus by themselves after teaching them the rudiments of algebra! Research shows that _structured instruction_---like the one in this book---is far more effective at teaching programming skills [^felienne]. You're taking the right step by reading this book!

[^felienne]: Felienne Hermans, [The Programmer's Brain](https://www.manning.com/books/the-programmers-brain) (2021).

## Our social contract

You might have experience talking about computer stuff with somebody more experienced, and left feeling discouraged. Perhaps they were dismissive, or snooty, or just kind of a jerk. It's an unfortunate tendency in our profession, and I want to break that cycle, because I think that this lack of _psychological safety_ can make it hard to become proficient at coding.

```{important}
This is a safe space. You're in a learning environment. There will be no tests. The advice I give here is non-binding and non-sanctimonious.
```

It's ok to write bad code when you're learning or you're in a hurry. You have deadlines! Remember to come back to the bad code and tidy it up after. Don't let the perfect be the enemy of the good. And remember, once you are empowered with this new knowledge, to be nice to beginners who are going through the same journey that you have.
