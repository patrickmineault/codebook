# The coding brain

```{admonition} Optional
This section is completely optional - feel free to skip to the next section
```

What makes coding uniquely difficult? Coding is hard on your memory. This book's theme is that **writing good research code is about freeing your memory**. Neuroscientists distinguish different subtypes of memory, and coding strongly depends on two subtypes:

* Working memory
* Long-term memory

Let's look at how these two types of memory are involved during programming.

## Working memory

```{admonition} Reflection
What do you think coding looks like in the brain?
```

The term *programming language* makes it seem that reading code is like reading a book - albeit a very obtuse book. Neuroscientists have looked at what circuits are engaged when people read code.  [Ivanova and colleagues at MIT](https://elifesciences.org/articles/58906) measured brain activity while people read Python code in the scanner - and scratch Jr., a visual programming language. They found that activations didn't overlap much with conventional language and speech areas. 

Instead, they found high overlap with the **multiple-demand system** - a network of areas typically recruited during math, logic and problem solving. The multiple-demand system is also involved in **working memory**, a type of memory that can hold information for a short amount of time. You may have heard that people can only hold up to 7 items in working memory - for instance, the digits of a phone number. This idea was popularized by the Harvard psychologist George Miller in the 1950's. While there's debate about the exact number of items we can remember in the short term, neuroscientists generally agree that our working memory capacity is very limited.

Programming involves juggling in your mind many different pieces of information: the definition of the function you want to write, the name of variables you defined, the boundary conditions of the `for` loop you're writing, etc. If you have too many details to juggle, eventually you will forget about one detail, and you will have to slowly reconstruct that detail from context. Do that enough times, and you will completely cease to make progress. Your working memory is very precious indeed.

### Saving our working memory

One of our strongest weapons against overloading our working memory is *convention*. Conventions mean that you don't have to remember details in your working memory. For example, let's say you want to call a helper function that splits a url into its constituent parts. You might instinctively know that the function to call is `split_url` and not `splitUrl` or `splitURL` or `URLSplitterFactory().do`. That's because Python has a convention that says that you separate words with underscores (snake case) and not with changes in case (camel case). If you abide by the convention, you've just saved yourself a working memory slot. To be clear, it's a completely arbitrary convention: JS uses the opposite convention (camel case) and it works fine. 

We'll see many more examples of organizing code such that it saves our working memory:

* Writing small functions
* Writing functions with low number of side effects
* Writing decoupled functions
* Following the Python style guide to the letter
* Using an auto-formatter

```{important}
Your working memory is precious, save it!
```

## Long-term memory

