# Make it social

```{epigraph}

Maybe the real *good research code* is the friends we made along the way.

--Patrick Mineault
```

People think that programming is a solitary activity. Engineers, and software engineers in particular, are caricatured as socially inept basement-dwelling dweebs in popular culture. The reality is that programming is a highly social activity. At a place like Google, for instance, programmers are in constant contact with other programmers, through:

* readability reviews
* code reviews
* design reviews
* pair programming
* reading groups
* retreats
* performance reviews

This is how you get better at programming: by programming with people who are better at programming than you.

## Pair program

*Pair programming* is a very effective method of sharing knowledge through active practice. It's commonly used in industry. Two programmers collaborate actively on a programming task. In the traditional driver-and-navigator style, two programmers are physically co-located. One of them - the *driver* or co-pilot - physically types the code into the terminal or code editor. They think about micro-issues in the code (tactics): what goes into the body of a `for` loop, the syntax of the code, etc.

The *navigator* or co-pilot assist the driver in telling them what to write. They typically focus on macro issues: what a function should accomplish, how the code is structured, etc. They can also perform other tasks on a second laptop, for example looking up documentation. 

```{margin}
I wrote this book in part to become better at the skills I'm now teaching you. Teaching is a great way to learn.
```

Pair programming forces you to hone your communication skills. Nothing quite reveals your gaps in knowledge than trying to explain to someone what is going on with a piece of code. Sometimes, the people you're pairing with can immediately fill your gap in knowledge; in other cases, you can both learn about a new subject at the same time. Pair programming is especially effective at transmitting knowledge about under-documented systems. You may have explained to a new student in your lab how to perform mysterious experimental procedure X. The best way to transmit that knowledge is to have the student attempt to perform the procedure in front of you: active practice enhances learning.

```{margin}
I learned about Ctrl+Shift+R (reverse search in bash) through pair programming.
```

Finally, pair programming can help you learn someone's productivity shortcuts. Seeing somebody work comfortably in an unfamiliar environment is enlightening. I have seen programmers be productive in vim, and it is a sight to behold. 

To many, pair programming sounds like a nightmare. It's certainly *uncomfortable*. Things might go too slow or too fast for you, and it can be mentally draining. It's best to do it in short increments (e.g. one hour). In all cases, remember to turn your empathy up to 11, and be excellent to each other.

Although pair programming was traditionally done by physically co-located programmers, many find remote pair programming more comfortable. Screen sharing in Zoom works but can feel intrusive - imagine accidentally showing your inbox or IMs. Instead, you can use an IDE where you can see the other person's cursor. Some environments to do this:

* [VSCode Liveshare for in-IDE editing](https://code.visualstudio.com/blogs/2017/11/15/live-share)
* [DeepNote](https://deepnote.com/) and [cocalc](https://cocalc.com/) for jupyter notebooks
* [Replit](https://replit.com/) for pure Python in the browser

## Set up code review in your lab

Reading and critiquing other people's code is a great way to learn. *Code review* is the practice of peer reviewing other people's code. You can use [Github pull requests to give and receive line-by-line feedback on code](https://docs.github.com/en/enterprise-server@2.20/github/collaborating-with-issues-and-pull-requests/reviewing-proposed-changes-in-a-pull-request) asynchronously. Alternatively, you can set up a code review circle in your lab. It works like a lab meeting, but instead of doing presentations, you all read code and comment on it at once. Again, it's uncomfortable and awkward, but you can learn a lot this way.

## Participate in open source

Maybe your local environment isn't ideal for you to become better at programming. Perhaps you're the only person in your lab that programs. Becoming part of an open source project is a great way to find like-minded people you can learn from.

Joining an open source project doesn't have to be an all or none affair. You can dip your toe in by opening an issue on a software project that you use. Are people responsive? Are they nice? If yes, then you can increase your involvement by starting a pull request to add a feature to a project. Generally, it's better to open an issue first to tell people about your plans; many larger projects are careful not to introduce new features, because it increases the amount of long-term maintenance people need to do.

Sometimes, you can pick a moribund open source project and maintain it. And if something doesn't exist yet, you can start your own open source project. You will do everything wrong, but you will learn a ton.

## Find your community

In addition to projects, there are communities of programers that support each other. [Hacker spaces](https://wiki.hackerspaces.org/w/index.php) promote self-reliance through learning technical skills, which include fabrication, woodworking, sewing and programming. Many meetups exist, focused on Python, data science, deep learning, or more. Some groups are designed as safe spaces for underrepresented people, for example [PyLadies](https://www.pyladies.com/).

Finally, you can go on a programmer's retreat to deep dive into a tech, for example through the [Recurse Center](https://www.recurse.com/). This will put you in contact with many other like-minded people who are in different places in their learning journey. Creating that deep web of connections will be invaluable to making you feel connected to the community at large.

## Acknowledgements

I wouldn't have been able to write this book without the help of many people. They have made me a better programmer. Thanks first and foremost to Ella Batty for inviting me to give the workshop that inspired this book. Thanks to the reviewers, Tyler Sloan, Elizabeth DuPre and Martin Héroux who made this talk much better. Thanks to Ivan Savov for inspiring me to write in long form. 

This book was inspired by many other long-form books and tutorials. Check them out:

* Felienne Hermans. [The Programmer's Brain](https://www.manning.com/books/the-programmers-brain)
* Irving et al. [Research Software Engineering with Python](https://merely-useful.tech/py-rse/)
* The Turing Way Community. [The Turing Way: A Handbook for Reproducible Data Science](https://the-turing-way.netlify.app/welcome)
* [Software Carpentry lessons](https://software-carpentry.org/lessons/)

This book was generated by [jupyterbook](https://jupyterbook.org/), which builds on [Sphinx](https://www.sphinx-doc.org). The stylesheet is an adaptation of [`tufte.css`](https://edwardtufte.github.io/tufte-css/).

## Discussion

As we've seen throughout this book, there are many ways you can improve how you write code. However, one of the highest leverage actions you can take to improve your craft is to immerse yourself in a community of practice. Be excellent to each other, learn from each other and give back to the community 🌠🌈.

```{admonition} 5-minute exercise
Schedule a pair programming session with a lab mate.
```