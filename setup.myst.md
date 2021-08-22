# Set up your project

Setting up a project in an organized way is a great way to ensure that you will remain productive as your project grows. Here are the broad steps involved:

1. Pick a name and create a folder for your project
2. Initialize a git repository and sync to Github
3. Set up a virtual environment
4. Create a project skeleton
5. (optional) Install a project package

## Pick a name and create a folder for your project

When you start a project, you will need to decide how to structure it. As an academic, a project will tend to naturally map to one paper. Therefore, **one project = one paper = one folder = one git repository** is a generally a good default structure.

```{warning}
You might want to create extra standalone projects for tools you re-use across different papers
```

Pick a short and descriptive name for your project and create a folder in your Documents folder. For instance, when I created this project, the first step was to run:

```{code}
~/Documents $ mkdir codebook
```

## Initialize a git repository and sync to Github

Since git is such a core tool to manage code-heavy projects, I recommend that you set up git next. The way I prefer to do this is by going to [Github](https://github.com) and clicking the big green **New** button to create a new repository. I name the remote the same as my local folder and hit **Create Repository**.

```{figure} figures/github-repo.png
width: 313px
---
The big green New button.
```

I then follow Github's instructions to initialize the repo. In `~/Documents/codebook`, I run:

```{code}
echo "# codebook" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/patrickmineault/codebook.git
git push -u origin main
```

```{note}
I've never attempted to remember these commands. I always just copy and paste.
```

From then on, you can commit anywhere between a few times a day to a few times per week, depending on how the project is going. Try to make the git commit messages meaningful and to group related changes together. A changelist with 100 changed files and a message "update" is not that helpful when you're trying to track when a bug was introduced several months after the fact.

```{note}
If you don't use git very often, you might not like the idea of committing to git daily or multiple times per day. The git command line can feel like a formidable adversary; GUIs can ease you into it. I used to use the git command line exclusively. These days, I like to [use the git panel in VSCode](ide.myst:vscode). 
```

## Set up a virtual environment

```{epigraph}
Why do I use virtual Python environments? So I don't fuck up all my local shit.

--[Nick Wan](https://twitter.com/nickwan)
```


```{figure} figures/python_environment_2x.png
width: 492px
---
Python environments can be a real pain. From [xkcd.com](https://xkcd.com/1987/) by Randall Munroe.
```

Many novices starting out in Python use one big monolithic Python environment. Every package is `pip install`ed in that one environment. This will work great until they run into a dependency issue and they accidentally break their install. Getting back to a good state can take several tedious hours because there's no real documentation for what was installed for each project. 

The solution is to use a *virtual environment* to manage dependencies. Each virtual environment specifies which versions of software and packages a project uses. The specs can be different for different projects, and each virtual environment can be easily created, documented, duplicated or destroyed. You can use one of `conda`,  `pipenv` or `poetry` to manage dependencies. Which one you prefer is a matter of personal taste. Here I present the `conda` workflow.

### Conda

Conda serves as the de facto Python distribution for data science-centric Python. `conda` is both a package manager (something that installs package on your system) and a virtual environment manager (something that can swap out different combinations of packages easily). 

Once conda is installed, you can create a new environment and activate it:

```{code}
~/Documents/codebook$ conda create --name codebook python=3.8
~/Documents/codebook$ conda activate codebook
```

From this point on, you can install packages through the conda installer like so:

```{code}
(codebook) ~/Documents/codebook$ conda install pandas numpy scipy matplotlib seaborn
```

To export a list of dependencies so you can easily recreate your environment, use the `export env` command:

```{code}
(codebook) ~/Documents/codebook$ conda export env > environment.yml
```

You can then commit `environment.yml` to document this environment. You can recreate the environment in question when needed - when you move to a different computer, for example - using:

```{code}
$ conda create --name recoveredenv --file environment.yml
```

```{admonition} What's the difference between pip and conda? Can I use both?

A big point of confusion is how conda interacts with `pip`. For conda:

* Conda is both a package manager and a virtual environment manager
* Conda can install big, complicated-to-install, non-Python software, like `gcc`
* Not all Python packages are installable through conda

For pip:

* pip is just a package manager
* pip generally only installs Python packages
* pip can install every package on PyPI in additional to local packages

**You can use pip inside of a conda environment**. `conda` tracks which packages are pip installed and will include a special section in `environment.yml` for pip packages. [However, installing pip packages may negatively affect conda's ability to install packages correctly after the first pip install](https://www.anaconda.com/blog/using-pip-in-a-conda-environment). Therefore, people generally recommend installing conda packages first, then installing pip packages.
```

## Create a project skeleton

In many different programming frameworks - Ruby on Rails, React, etc. - people use a highly consistent directory structure from project to project. In Python, things are much less standardized. I went into a deep, deep rabbit hole looking at different directory structures suggested by different projects, and I come up with this consensus structure:

```{code}
├── code
├── docs
├── scripts
├── tests
└── .gitignore
└── environment.yml
└── README.md
```

`.gitignore` contains the list of files you want git to ignore, while `README.md` contains a short description of your project, including installation instructions. `environment.yml` contains the description of your conda environment.

The folders are organized as follows:

* `code`: Contains reusable Python modules for your project. This is the kind of python code you `import`
* `docs`: Where you put documentation, including Markdown and reStructuredText (reST). Calling it `docs` will make it easy to publish the docs through Github pages.
* `scripts`: Where you put scripts - Python and bash alike - as well as notebooks.
* `tests`: Where you put tests for your code. You might not have ever written formal tests, but don't worry, we'll cover these in a later lesson.

## Install a project package

You might notice a flaw in the preceding project structure. Let's say you create a reusable `lib.py` under the `code` folder, with a function `my_very_good_function`. How would you reference that function in `scripts/use_lib.py`? This doesn't work:

```{code}
from ..code.lib import my_very_good_function
```

```{code}
$ python scripts/use_lib.py
Traceback (most recent call last):
  File "use_lib.py", line 1, in <module>
    from ..code.lib import my_very_good_function
ImportError: attempted relative import with no known parent package
```

You have two options, change your Python path, or create an installable package.

### Change your Python path (not recommended)

You can put the `code` folder on your Python path. You can [append the `code` folder to the system variable PYTHONPATH when bash starts up (in ~/.bashrc)](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html). You might alternatively dynamically append to the system path from Python, via:

```{code}
import sys
sys.path.append('/home/me/Documents/codebook/code)

from code.lib import my_very_good_function
```

The disadvantage is that this tends to be pretty brittle. You have to hardcode the name of folders in multiple places. If they move, you will break your package. It won't work on another computer with different paths. 

### Create a pip-installable package (recommended)

This is the more scalable solution. The packaging ecosystem in Python can feel frankly daunting, but creating a locally pip installable package only involves a few steps.
