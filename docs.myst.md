# Write good docs

## Document entry points

When you pick a project back up after several months, you might not remember how to get the code to work. **Document a clear entry point** in your `README.md` file e.g.:

````markdown
This project counts words which rhyme with *orange*. Use it like so:

```
$ python orange_counter.py --file apples.txt
```
````

For more elaborate projects, you might need to run multiple scripts to complete an analysis. A lightweight option is to create a master shell file which can run the entire analysis end-to-end. For the orange counter example, we can create a bash file with an evocative name like `run_analysis.sh` which looks like this:

```
#!/bin/bash

# This will cause bash to stop executing the script if there's an error
set -e

# Download file
wget -O apples.txt http://www.example.com/apples.txt

# Count words
python orange_counter.py --file apples.txt --out counts.txt

# Create output directory
mkdir figures/

# Generate plots
python generate_plots.py --file counts.txt --out_dir figures/
```

```{danger}
Bash is quirky - the syntax is awkward and it's pretty easy to shoot yourself in the foot. If you're going to write elaborate shell scripts,  use [`shellcheck`](https://github.com/koalaman/shellcheck), which will point out common mistakes in your code. Your favorite editor probably has a plugin for shellcheck.

Also, check out [Julia Evans' zine](https://wizardzines.com/zines/bite-size-command-line/) on bash - it's a life saver.
```

## Document pipelines

Scientific pipelines often take the shape of DAGs - directed acyclic graphs. This means, essentially, that programs flow from inputs to output in a directed fashion.  The rhymes-with-orange example above is an example of a simple DAG with 4 steps. Other DAGs can be more elaborate, for example the 12-step DAG which generates figures shown in Van Vliet (2020) [^VanVliet]:

[^VanVliet]: Van Vliet (2020). [Seven quick tips for analysis scripts in neuroimaging](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007358). PLOS Computational Biology.

```{figure} figures/pcbi.1007358.g002.PNG_L.png
---
figclass: boxed
---
DAG from Van Vliet (2020). CC-BY 4.0
```

Van Vliet (2020) recommend to use filenames which indicate a file's position in a DAG, for example `00_fetch_data.py`. One issue with this naming scheme, is that such scripts are not testable because they can't be `import`ed. You can instead start filenames with an underscore, for example `_00_fetch_data.py`, or with a prefix, `step_00_fetch_data.py`. 

You can document how all the steps of the DAG fit together with a bash file, as in the previous section. One problem with using bash for long-running pipelines is that it can be painful to restart a pipeline that fails in the middle. This will lead to a proliferation of bash files corresponding to different subparts of your pipeline, and pretty soon you'll have a mess of shell scripts on your hands. 

You can use a more specialized build tool to build and document a pipeline. GNU `make` has been a standard tool for compiling code for several decades, and is becoming more adopted in data science and research. A `Makefile` specifies both the inputs to each pipeline step and its outputs. `make` keeps track of timestamps of intermediate files and only rebuilds what needs to rebuilt. To give you a flavor of what a `Makefile` looks like, this file implements the DAG for the orange counter:

```makefile
.PHONY: plot
plot: counts.txt generate_plots.py figures
    python generate_plots.py --file counts.txt --out_dir figures/

counts.txt: apples.txt orange_counter.py
    python orange_counter.py --file apples.txt --out counts.txt

apples.txt:
    wget -O apples.txt http://www.example.com/apples.txt

figures:
    mkdir figures
```

The plot can be created with `make plot`. The `Makefile` contains a complete description of the inputs and outputs to different scripts, and thus serves as a self-documenting artifact. [Software carpentries](https://swcarpentry.github.io/make-novice/) have an excellent tutorial on `make`.

`make` uses a domain-specific language (DSL) to define a DAG. It might feel daunting to learn yet another language to document a pipeline. There are numerous alternatives to `make` that define DAGs in pure Python, including [`doit`](https://pydoit.org/). There are also more complex tools that can implement Python DAGs and run them in the cloud, including [`luigi`](https://github.com/spotify/luigi), [`airflow`](https://airflow.apache.org/), and [`dask`](https://docs.dask.org/en/latest/custom-graphs.html).