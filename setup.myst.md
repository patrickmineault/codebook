# Set up your project

Setting up a project in an organized way is a great way to ensure that you will remain productive as your project grows. Here are the broad steps involved:

1. Pick a name and create a folder for your project
2. Initialize a git repository and sync to Github
3. Set up a virtual environment
4. Create a project skeleton
5. Install a project package

In addition, I've created a utility to make this as easy as possible.

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
---
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
If you don't use git very often, you might not like the idea of committing to git daily or multiple times per day. The git command line can feel like a formidable adversary; GUIs can ease you into it. I used to use the git command line exclusively. These days, I like to [use the git panel in VSCode](ide.myst). 
```

## Set up a virtual environment

```{epigraph}
Why do I use virtual Python environments? So I don't fuck up all my local shit.

--[Nick Wan](https://twitter.com/nickwan)
```


```{figure} figures/python_environment_2x.png
---
width: 492px
---
Python environments can be a real pain. From [xkcd.com](https://xkcd.com/1987/) by Randall Munroe.
```

Many novices starting out in Python use one big monolithic Python environment. Every package is `pip install`ed in that one environment. This will work great until they run into a dependency issue and they accidentally break their install. Getting back to a good state can take several tedious hours because there's no real documentation for what was installed for each project. 

The solution is to use a *virtual environment* to manage dependencies. Each virtual environment specifies which versions of software and packages a project uses. The specs can be different for different projects, and each virtual environment can be easily created, documented, duplicated or destroyed. You can use `conda`,  `pipenv`, `poetry`, `venv`, `virtualenv` or `asdf` - among other - to manage dependencies. Which one you prefer is a matter of personal taste and countless internet feuds. Here I present the `conda` workflow, which is particularly popular among the data science crowd.

### Conda

Conda serves as the de facto Python distribution for data science-centric Python. `conda` is both a package manager (something that installs package on your system) and a virtual environment manager (something that can swap out different combinations of packages and binaries - virtual environments - easily). 

[Once conda is installed](https://docs.conda.io/en/latest/miniconda.html) - for instance, through miniconda - you can create a new environment and activate it like so:

```console
~/Documents/codebook$ conda create --name codebook python=3.8
~/Documents/codebook$ conda activate codebook
```

From this point on, you can install packages through the conda installer like so:

```console
(codebook) ~/Documents/codebook$ conda install pandas numpy scipy matplotlib seaborn
```

To export a list of dependencies so you can easily recreate your environment, use the `export env` command:

```console
(codebook) ~/Documents/codebook$ conda export env > environment.yml
```

You can then commit `environment.yml` to document this environment. You can recreate the environment in question when needed - when you move to a different computer, for example - using:

```console
$ conda create --name recoveredenv --file environment.yml
```

```{admonition} Can I use both pip and conda?

A big point of confusion is how conda interacts with `pip`. For conda:

* Conda is both a package manager and a virtual environment manager
* Conda can install big, complicated-to-install, non-Python software, like `gcc`
* Not all Python packages are installable through conda

For pip:

* pip is just a package manager
* pip only installs Python packages
* pip can install every package on PyPI in additional to local packages

**You can use pip inside of a conda environment**. `conda` tracks which packages are pip installed and will include a special section in `environment.yml` for pip packages. [However, installing pip packages may negatively affect conda's ability to install packages correctly after the first pip install](https://www.anaconda.com/blog/using-pip-in-a-conda-environment). Therefore, people generally recommend installing conda packages first, then installing pip packages.
```

## Create a project skeleton

In many different programming frameworks - Ruby on Rails, React, etc. - people use a highly consistent directory structure from project to project. In Python, things are much less standardized. I went into a deep rabbit hole looking at different directory structures suggested by different projects, and came up with this consensus structure:

```{code}
├── docs
├── scripts
├── src
├── tests
└── .gitignore
└── environment.yml
└── README.md
```

`.gitignore` contains the list of files you want git to ignore, while `README.md` contains a short description of your project, including installation instructions. `environment.yml` contains the description of your conda environment.

The folders are organized as follows:

* `docs`: Where you put documentation, including Markdown and reStructuredText (reST). Calling it `docs` will make it easy to publish the docs through Github pages.
* `scripts`: Where you put scripts - Python and bash alike - as well as .ipynb notebooks.
* `src`: Contains reusable Python modules for your project. This is the kind of python code that you `import`
* `tests`: Where you put tests for your code. If you've never written formal tests before, don't worry, we'll cover these in a later lesson.

You can create this project structure manually using `mkdir` on the command line.

## Install a project package

```{warning}
Creating a project package is slightly annoying, but the payoff is quite substantial: you keep a clean project structure, paths are clean, your project is pip installable, etc.
```

You might notice a flaw in the preceding project structure. Let's say you create a reusable `lib.py` under the `src` folder, with a function `my_very_good_function`. How would you reference that function in `scripts/use_lib.py`? This doesn't work:

```pycon
>>> from ..code.lib import my_very_good_function
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: attempted relative import with no known parent package
```

You have two options, change your Python path, or create an installable package. I don't recommend directly changing the Python path, but I write it here anyway because you will encounter it and it will be confusing if not covered here.

### Change your Python path (not recommended)

You can put the `src` folder on your Python path. You can [append the `src` folder to the system variable PYTHONPATH when bash starts up (in ~/.bashrc)](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html). You might alternatively dynamically append to the system path from Python, via:

```{code}
import sys
sys.path.append('/home/me/Documents/codebook/src')

from code.lib import my_very_good_function
```

The disadvantage is that this tends to be pretty brittle. You have to hardcode the name of folders in multiple places. If they move, you will break your package. It won't work on another computer with different paths, so it will make it hard to share your project with colleagues. Furthermore, dynamic paths don't play well with IDEs like vscode that can only look in the static environment. 

### Create a pip-installable package (recommended)

This is the more scalable solution. [The packaging ecosystem in Python can feel frankly daunting](https://packaging.python.org/guides/), but creating a locally pip installable package only involves a few steps.

#### 1. Create a `setup.py` file

Create a `setup.py` file in the root of your project. Here's a minimal setup file:

```
from setuptools import find_packages, setup

setup(
    name='code',
    packages=find_packages(),
)
```

#### 2. Create a `__init__.py__` file

Create an empty `__init__.py` file under the `src` directory. This will allow the `find_packages` function find the package.

```console
(codebook) ~/Documents/codebook $ touch src/__init__.py
```

Your files should now look like:

```
├── doc
├── scripts
├── src
│   └── __init__.py
├── tests
├── .gitignore
└── setup.py
```

#### 3. `pip install` your package

Now comes the fun part, installing the package. You can do so using:

```console
(codebook) ~/Documents/codebook $ pip install -e .
```

`.` indicates that we're installing the package in the current directory. `-e` means that the package is editable, which means that if you change the files inside the `src` folder, you don't need to re-install the package for your changes to be picked up.

#### 4. Use the package

Once the package is locally installed, it can be easily used regardless of which directory you're in. For instance:

```
(codebook) ~/Documents/codebook $ echo "print('hello world')" > src/test.py
(codebook) ~/Documents/codebook $ cd scripts
(codebook) ~/Documents/codebook/scripts $ python
>>> import src.test
hello world
```

#### 5. Add to `.gitignore`

Installing the package locally will create folders for Python's internal use. To prevent accidentally committing these files, you can add the following line to `.gitignore`:

`*.egg-info`

#### 6. (optional) Change the name of the package

Note that the name of the folder, `src`, becomes the name of the package. If you'd like to rename the package, for example to `cb`, change the name of the folder and reinstall the like so:

```
(codebook) ~/Documents/codebook $ mv src cb
(codebook) ~/Documents/codebook $ pip install -e .
```

## Use the true-neutral cookiecutter

If doing all this for every new project sounds like a lot of work, you can save yourself some time using the true-neutral cookiecutter, which creates a project skeleton using the template I showed above. Cookiecutter generates project folders from templates. You can install it in the base conda environment with:

```
(base) ~/Documents $ pip install cookiecutter
```

To create the `codebook` folder with all its subfolders and setup.py, simply use the following:

```
(base) ~/Documents $ cookiecutter gh:patrickmineault/true-neutral
```

This will create an instance of the `true-neutral` project skeleton (hosting on my github here). Follow the prompts and it will create the folder structure above, including the setup file. Next, sync to your own remote repository following the github instructions, and pip install the package you've created for yourself.

## Discussion

Using structured projects linked to git will help your long-term memory. Using a project template will allow you to instantly understand how files are laid out months after you've last worked on that project. Using a virtual environment will allow you to recreate that environment in the far future. And git will give you a time machine to work with.

As an added bonus, if you can make it easy for future *you* to use your project, you will make it easier for *other people* to use it as well. 



