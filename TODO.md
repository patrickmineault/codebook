* Add more illustrations
* Color code high effort / low effort
* WOrk on transitions
* Get feedback from reviewers
* Integrate other resources
* Rework the basic template
* Consider adding CKA back into the mix
* Creating an accompanying repository for the book
* Give people a place to chat about the book
* Fix font changing on changing the page
* Make the code live
* Add to documentation the fact that it's easy to publish something through github

Read these resources:

* Come back to this: https://missing.csail.mit.edu/
* Very very good on PLOS: good enough practices https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510
* Lots of references in this one: https://handsonscicomp.readthedocs.io/en/latest/
* R centric: https://plain-text.co/
* Stuff I don't totally agree with: https://github.com/colaresi/ScientificComputationClass

A better template to start from:

* https://github.com/bvreede/good-enough-project

Pure vs impure and making code modular:

Coderefinery
(love the graphic)
* https://cicero.xyz/v3/remark/0.14.0/github.com/coderefinery/modular-code-development/master/talk.md/#10

Code along with an idea for an analysis:
https://coderefinery.github.io/modular-type-along/instructor-guide/

Kaytee's feedback
===

* split off docs into two sections
| However, I feel a bit of “gumminess” in getting to the “write good docs” section
* I find it easiest to follow an organization that clearly builds from single functions to modules to executable scripts or some similar build-up. 
* add more information about going from jupyter notebooks to a different kind of pipeline
* 
Add more code challenges
Level 1 challenge = replace print with assert. 
Level 2 challenge = write a test.py file for one of your smaller modules.

Ivan's feedback
===
docs.html

-> Very low-level documentation. Installation instructions, usage examples, development environment setup.
> % bcs needed to get you started (new user happy path)

- Very high-level documentation. Design documents, data models and system diagrams, links to papers, etc.
> % bcs needed to know the why? of the codebase --- for the how? and what? you read the source code

Cut doctests
~~Fix CSS bug on resizing~~
 ~~-> Show hamburger menu conditionally.~~
(temporary patch)