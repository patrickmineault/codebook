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

# Write decoupled code

```{epigraph}

Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it.

-- Kernighan's law [^Kernighan]
```

[^kernighan]: Brian Kernighan is a Canadian computer scientist who contributed to the development of Unix and co-authored the first book on the C programming language.

Code which does a little bit of everything at once is hard to work with. Reasoning about a function which reads inputs, does math, calls a remote server and writes outputs in a tightly coupled bundle can easily become overwhelming: there's too many moving pieces to keep in your head. Here, I show how you can spot tightly coupled code and iteratively improve it.

## Code smells and spaghetti code

A code smell is an issue with the source code of a program that indicates there might be some larger underlying issue. For example [^wikipedia]:

[^wikipedia]: Many of these and more are mentioned in the [Wikipedia article on code smells](https://en.wikipedia.org/wiki/Code_smell).

- _Mysterious names_: variables have names which don't indicate their function
- _Magic numbers_: unique values with unexplained meaning
- _Duplicated code_: large portions of duplicated code with small tweaks
- _Uncontrolled side effects and variable mutations_: code is written so that it's unclear where and when variables are changed (more on this later)
- _Large functions_: big, unwieldy functions that do a little bit of everything
- _High cyclomatic complexity_: lots of nested ifs and for loops
- _Globals_: Using globals for things that don't strictly need to be global
- _Embedded configuration_: paths and filenames are hardcoded in ways that the code is not portable to to another computer

```{margin}
*Cyclomatic complexity* is the number of linearly independent paths (e.g. branches of an if statement) in a function
```

When code has a lot of code smells, it can become brittle to the point of becoming hard or impossible to change. At that point, your productivity goes to zero. Such code is often deemed _spaghetti code_, code so tightly wound that when you pull on one strand, the entire thing unravels.

```{margin}
It is a sad fact that delicious, delicious carbs have such a negative connotation in programming circles.
```

```{figure} figures/spaghetti-code.png
---
width: 450px
figclass: boxed
---
Spaghetti code. From Brown et al. (1998), AntiPatterns. Notice the late 90's clipart. Spaghetti code has been around for a long time
```

## What does spaghetti code look like?

I wanted to find an example of real-life spaghetti code, without being mean-spirited. `wave_clus` is a piece of software that runs in Matlab which is very useful to neuroscientists, and which I've personally used and appreciated. It's used to tease out signals from different neurons. Here's [an excerpt from real code from a function](https://github.com/csn-le/wave_clus/blob/master/wave_clus.m#L964):

```matlab
function isi_reject_button_Callback(hObject, eventdata, handles,developer_mode)
set(hObject,'value',1);
b_name = get(gcbo,'Tag');
cn = str2double(regexp(b_name, '\d+', 'match'));

eval(['set(handles.isi' int2str(cn) '_accept_button,''value'',0);'])
main_fig = findobj( 0, 'type', 'figure', 'tag', 'wave_clus_figure');
USER_DATA = get(main_fig,'userdata');
classes = USER_DATA{6};
if cn == 3
    if nnz(classes==3)==0
        nlab = imread('filelist_wc.xlj','jpg');
        figure('color','k'); image(nlab); axis off; set(gcf,'NumberTitle','off');
    end
end
```

The fact that it's Matlab code can help us to evaluate this code with a little bit of distance - a beginner's mindset, if you will. We see many different code smells:

- Parsing a magic integer (`cn`) from the name of a component
- Using magic numbers (`USER_DATA{6}`, `classes==3`)
- Using globals (`USER_DATA`)
- Mixing input and output (`imread` and `figure`)
- A nested if statement which could be flattened out
- Using `eval`

The problem with spaghetti code is not that it doesn't work, is that it's _inscrutable_ and _brittle_.

```{margin}
Sometimes code is so brittle that it's impossible to modify to run on a modern system. This is why every lab has a machine running ancient software in a backroom somewhere with a sticky note written DO NOT UPGRADE.
```

## Making code better

Now that we've seen real world bad code, let's consider what makes good code.

### Separate concerns

Great code exhibits _separation of concerns_:

- a function does one thing
- a module assembles functions which all work towards the same goal
- a class mostly modifies its own members rather than other objects

For instance, your data loading function should just load data, and your computation function should just compute. Each function should be small and should stand on its own. If a function is longer than a screen's worth of code (80 columns, 40 lines), it's usually a good sign it's time to split it off into two. **Make small functions**.

### Learn to identify and use pure functions

When novices are introduced to Python functions, they usually start with pure functions. Pure functions follow the _canonical data flow_:

- the inputs come from the arguments
- the outputs are returned with the `return` statement

For instance, this function which adds two numbers together follows the canonical data flow:

```{code-cell}
def add_two_nums(num0, num1):
    return num0 + num1
```

```{margin}
A stateless function doesn't have persistent state that carries over from call to call. A function which uses a global has state.
```

This function is also _deterministic_, and _stateless_. This is the computational analogue of a mathematical function. You can think of them as unchanging black boxes: you put stuff in, computation happens, you get a result out, and neither the input or the black box gets changed. Because of this, pure functions are easy to reason about - they are the best kind of function. _If something that you write makes sense as a pure function_, write it that way.

### Avoid side effects

Some languages enforce using pure functions: they are functional programming languages. Python, however, is a multi-paradigm programming language: you can write functional code, object-oriented code, imperative code, and mix and match as desired. While this flexibility allows us to use the right tool for each job, it offers numerous possibilities to shoot yourself in the foot.

Much Python code uses non-pure functions with _side effects_, which can be hard to reason about. A _side effect_ is anything that happens outside the canonical data flow from arguments to return, including:

- modifying a global
- modifying a static local variable
- modifying an argument
- doing IO, including printing to the console, drawing on the screen or calling a remote server

For instance, consider this function which reverses a list:

```{code-cell}
def reversi(arr):
    """Reverses a list."""
    for i in range(len(arr) // 2):
        arr[-i - 1], arr[i] = arr[i], arr[-i - 1]
    return arr
```

```{margin}
You can reverse a list directly with `arr[::-1]`, but we don't use this primitive here for the sake of illustration.
```

This function has a side effect: it modifies its argument `arr`. In Python and many other languages, arguments of complex types like lists, dictionaries and objects are passed by reference, which means they can be modified by the function. That breaks the normal data flow - the arguments are also returns!

In the base Python library, a function which modifies its argument returns `None`. For instance, the function `sort` sorts its input argument, modifies it in place, and returns `None`. This function has a side effect, but it's obvious: if a function returns `None`, yet does useful work, it must have a side effect. When we both modify an argument and return it, we break this convention and confuse the Python reader. We can fix this by returning `None` in our function (good), or returning an entirely new list (better):

````{tabbed} good
```
def reversi(arr):
    """Reverses a list."""
    for i in range(len(arr) // 2):
        arr[-i - 1], arr[i] = arr[i], arr[-i - 1]
    return None
```
````

````{tabbed} better
```
def reversi(arr):
    """Reverses a list."""
    reved = []
    for i in range(len(arr)):
        reved.append(arr[len(arr) - 1 - i])
    return reved
```
````

Functions with side effects can be hard to reason about: you often need to understand their internals and state in order to use them properly. They're also harder to test. **Not every function with side effects is problematic, however**. My pragmatic advice is to first learn to spot and understand pure functions. Then organize your code so that many functions are pure, and those that are not are well-behaved.

```{figure} figures/pure-impure.svg
---
width: 500px
figclass: boxed
---
Shrinking the amount of impure functions in your code will make it easier to reason about. Graphic [inspired by CodeRefinery](https://cicero.xyz/v3/remark/0.14.0/github.com/coderefinery/modular-code-development/master/talk.md/#10).
```

For instance:

- Write functions which modify their arguments, or return values, but not both
- Concentrate your IO in their own functions rather than sprinkling them throughout the code
- Use classes to encapsulate state rather than using stateful functions and globals. Python classes use the convention that private variables, which shouldn't be modified from outside, start with an `_`. For example, `self._x` denotes a class member `_x` which should be managed by the class itself [^convention].

[^convention]: Python doesn't restrict outside access to private class variables; it's just a convention to use `_` as a prefix.

### Make your code more Pythonic

```{epigraph}
If it ain't broke, fix it till it is.

-- [Steve Porter](https://www.youtube.com/channel/UCfOrKQtC1tDfGf_fFVb8pYw)
```

Sometimes, code smells come from a lack of knowledge about the language. _Reading other people's code_, _pair programming_, and _reading programming books_ can help fine tune your knowledge of a programming language and get out of this local minimum.

#### Move away from Matlab idioms

Some common issues are caused by using an idiom from another programming language in Python, where it doesn't translate. Many people using the Python data science ecosystem either come from a Matlab background, or were trained by someone who came from a Matlab background. As a consequence, they'll tend to write Matlab-like code, for example:

_Using magic columns numbers to index into a numpy array_. Matlab has a matrix type that it uses for many things. You might use the tenth column of a matrix to store a timestamp, which creates hard-to-read code. Dataframes are more appropriate to store parallel data. In 3 months from now, `A.timestamp` will be far clearer than `A[:, 10]`. [You can learn the basics of `pandas` in a weekend](https://github.com/jvns/pandas-cookbook), and it's a great time investment.

_Using unnamed dimensions in numpy_. Similarly, tensors with multiple dimensions can pose problems. If you have a mini-batch of images you're preparing for a deep learning pipeline, did the dimensions go `batch_size x channels x height x width`, or `batch_size x width x height x channels`? [xarray](http://xarray.pydata.org/en/stable/) and [named tensors in pytorch](https://pytorch.org/docs/stable/named_tensor.html) give you named dimensions, which will reduce your confusion down the line.

_Using bespoke casting for string formatting_. Python has a great string formatting method since version 3.6: [the f-string](https://realpython.com/python-f-strings/). Generating a file name for a checkpoint with `f"{model_name}_{iteration}.pkl"` is more intuitive and readable than `model_name + '_' + str(iteration) + '.pkl'`.

_Avoiding for loops_. You may have been taught to avoid for loops as much as possible in Matlab by vectorizing everything. However, this often sacrifices readability. Tricky indexing may look clever, but can be next to impossible to debug. Because Python has a different performance profile than Matlab, some Matlab-specific optimizations won't make your code faster. For instance, unlike Matlab vectors, Python lists are very cheap to grow. Appending to a list in a for loop and then turning that list into a numpy array in a single call has little performance overhead compared to preallocating.

To be clear, modern Matlab doesn't have to be written this way: for instance, Matlab has a capable dataframe class. But a lot of people that come from Matlab still use old Matlab idioms. I have three more tutorials for you if you come from a Matlab background to ease your transition [[1]](https://xcorr.net/2020/02/21/transitioning-away-from-matlab/) [[2]](https://xcorr.net/2020/02/29/orienting-yourself-through-python/) [[3]](https://xcorr.net/2020/03/04/rewriting-matlab-code-in-python/).

## Put it all together

Let's introduce a small-scale example that we will make progressively better. We want to write a function which does three things:

- Loads a file
- Counts the words in the files
- Writes the counted words to an output file.

We might code that as:

```{code-cell}
def count_words_in_file(in_file, out_file):
    counts = {}
    with open(in_file, 'r') as f:
        for l in f:
            # Split words on spaces.
            W = l.lower().split(' ')
            for w in W:
                if w != '':
                    if w in counts:
                        counts[w] += 1
                    else:
                        counts[w] = 0

    with open(out_file, 'w') as f:
        for k in counts.keys():
            f.write( k + ","+ str(counts[k]) + "\n")
```

Can you spot the code smells in the previous code?

```{dropdown} ⚠️ Spoilers

Here are some code smells in this example:

* Using one-character variable names.
* Using lots of nested for and if statements (6 levels of indent)
* Using bespoke string formatting
* Mixing IO and computation

```

### Split IO and computation

Let's start by splitting IO and computation.

```{code-cell}
def count_words(text):
    # Split words on spaces.
    counts = {}
    W = text.lower().split(' ')
    for w in W:
        if w != '':
            if w in counts:
                counts[w] += 1
            else:
                counts[w] = 0

    return counts

def count_words_in_file(in_file, out_file):
    with open(in_file, 'r') as f:
        counts = count_words(f.read())

    with open(out_file, 'w') as f:
        for k in counts.keys():
            f.write( k + ","+ str(counts[k]) + "\n")
```

`count_words` is now a pure function - it takes in a string and returns a dict, and it has no side effects. This isolation can make it a little easier to notice bugs in the function. Indeed, if we run the code on a few test strings, we notice that this function does not work as expected.

```pycon
>>> count_words("hello world")
{'hello': 0, 'world': 0}
>>> count_words("hello world\n\nhello")
{'hello': 0, 'world\n\nhello': 0}
```

We have an off-by-one error in counts, and we are also not correctly dealing with newline characters. Let's fix this.

```{code-cell}
def count_words(text):
    # Split words on spaces.
    counts = {}
    W = text.lower().replace('\n', ' ').split(' ')
    for w in W:
        if w != '':
            if w in counts:
                counts[w] += 1
            else:
                counts[w] = 1

    return counts
```

Now:

```pycon
>>> count_words("hello world")
{'hello': 1, 'world': 1}
>>> count_words("hello world\n\nhello")
{'hello': 2, 'world': 1}
```

Not only have we improved the _legibility_ of the code, we have improved its _correctness_.

### Decrease the amount of nesting

Our code has too many levels of nesting. One underlying cause is that we have two branches for when a key of dictionary exists and when it doesn't. Python has a collection in its standard library specifically built to deal with this: `collections.defaultdict`.

```{code-cell}
import collections

def count_words(text):
    # Split words on spaces.
    counts = collections.defaultdict(int)
    W = text.lower().replace('\n', ' ').split(' ')
    for w in W:
        if w != '':
            counts[w] += 1

    return counts
```

```{margin}
`collections.defaultdict(int)` creates a dict with a default integer value of 0.
```

The other level of nesting is due to detecting empty words, `w != ''`. We can decrease the nesting of the counting code by skipping to the next iteration upon encountering an empty word:

```{code-cell}
import collections

def count_words(text):
    # Split words on spaces.
    counts = collections.defaultdict(int)
    W = text.lower().replace('\n', ' ').split(' ')
    for w in W:
        if w == '':
            continue
        counts[w] += 1

    return counts
```

However, the root of the problem is that there can be multiple space characters next to each other - this creates empty words. One solution is to replace multiple spaces with one space. With regular expressions, this can be done in one line:

```{code-cell}
import collections
import re

def count_words(text):
    # Split words on spaces.
    counts = collections.defaultdict(int)
    W = re.sub(r"\s+", " ", text.lower()).split(' ')
    for w in W:
        counts[w] += 1

    return counts
```

`re.sub(r"\s+", " ", ...)` finds one or more instances of consecutive whitespace characters (including spaces, newlines and tabs), and replaces them with exactly one space. You could argue that this is less readable than the original version. Regular expressions can certainly be cryptic. However, from a feature perspective, this is an improvement because it deals with tabs and newlines properly.

```pycon
>>> count_words("hello   world\n\n\tworld")
defaultdict(int, {'hello': 1, 'world': 2})
```

Improving code will require us to make many judgement calls like this. Should we prefer features over cleanliness of code? There's no one true solution!

### Improving legibility

We can improve legibility further by using descriptive names and using f-strings. The finalized code can be compared with the old code side-by-side.

````{tabbed} Improved
```python
import collections
import re

def count_words(text):
    """Split words on spaces."""
    counts = collections.defaultdict(int)
    words = re.sub(r"\s+", " ", text.lower()).split(' ')
    for word in words:
        counts[word] += 1
    return counts

def count_words_in_file(in_file, out_file):
    with open(in_file, 'r') as f:
        counts = count_words(f.read())

    with open(out_file, 'w') as f:
        for word, count in counts.items():
            f.write(f"{word},{count}\n")
```
````

````{tabbed} Original
```
def count_words_in_file(in_file, out_file):
    counts = {}
    with open(in_file, 'r') as f:
        for l in f:
            # Split words on spaces.
            W = l.lower().split(' ')
            for w in W:
                if w != '':
                    if w in counts:
                        counts[w] += 1
                    else:
                        counts[w] = 0

    with open(out_file, 'w') as f:
        for k in counts.keys():
            f.write( k + ","+ str(counts[k]) + "\n")
```
````

It's not perfect, but it's an improvement over the original in terms of legibility, correctness and feature set.

## Discussion

Decoupled code is something we all strive towards. Yet, code often has a natural tendency to become more and more tightly wound over time until it becomes an unmanageable mess. The strategies in this chapter will help you to identify code smells and correct them.

Pure functions are easier to reason about, because they're stateless - that saves your working memory when you're reading code. Code that follows Python's idioms is also easier on your working memory: when you see a line of code that is a familiar pattern, you can see the entire line as one chunk rather than multiple disparate bits. That takes one working memory slot rather than several.

Changing existing code is not without its dangers, however. Perhaps we will make a mistake and introduce a bug in our code! How can we check that our improved code still does the correct thing? We'll cover this in the next chapter on testing.

```{admonition} 5-minute exercise
Take a long function in a script you currently are working on, and split it in two. What challenges did you face?
```
