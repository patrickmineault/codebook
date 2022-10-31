import collections
import yaml


template = r"""
\documentclass[letterpaper,twoside,openright]{scrbook}
\usepackage{hyperref}
\usepackage{datetime}
\usepackage{graphicx}
\usepackage{natbib}
\usepackage{framed}
\usepackage[utf8]{inputenc}
\usepackage{svg}

% Header stuff
\usepackage{scrlayer-scrpage}

\usepackage[top=80pt, bottom=80pt, left=80pt, right=80pt]{geometry}

\clearscrheadfoot
\ihead{\headmark}
\ohead{\pagemark}

\rofoot{Patrick Mineault}

% Use a smaller verbatim font to prevent overfull hboxes
\usepackage{etoolbox}
\makeatletter
\patchcmd{\@verbatim}
  {\verbatim@font}
  {\verbatim@font\small}
  {}{}
\makeatother

% Listing code
\usepackage{courier}
\usepackage{listings}
\lstdefinestyle{mystyle}{
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    frame=tB,
    aboveskip=16pt,
    belowskip=16pt,
    keepspaces=true,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=2
}

\lstset{style=mystyle}

\bibliographystyle{abbrvnat}

% colors for hyperlinks
\hypersetup{colorlinks=true, allcolors=blue}

\title{Good Research Code handbook}
\author{Patrick Mineault}

\begin{document}

\maketitle

\frontmatter

\setcounter{tocdepth}{\subsectiontocdepth}

\tableofcontents

[-FRONTMATTER-]

\mainmatter

[-CONTENT-]

\backmatter

[-BACKMATTER-]

\end{document}
"""


import subprocess


def clean_input(md):
    lines = []
    in_citation = False
    for line in md.split("\n"):
        if in_citation:
            if "```" in line:
                in_citation = False
            else:
                lines.append("> " + line)
        else:
            if "{epigraph}" in line:
                in_citation = True
            elif "{dropdown}" in line:
                lines.append(line.replace("dropdown", "admonition"))
            elif "{margin}" in line:
                lines.append(line.replace("{margin}", "{admonition} Note"))
            elif "{tabbed}" in line:
                lines.append(line.replace("{tabbed}", "{admonition}"))
            else:
                lines.append(line.replace("🌠", "").replace("🌈", ""))
    return "\n".join(lines)


def process_one(name):
    with open(f"{name}.md", "r") as f:
        md = f.read()

    md = clean_input(md)
    with open(f"tmp/{name}.md", "w") as f:
        f.write(md)

    process = subprocess.Popen(
        ["curvenote", "export", "tex", f"tmp/{name}.md"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    print(stderr.decode("utf-8"))
    with open(f"tmp/exports/{name}.tex", "r") as f:
        tex = f.read()
    return tex


def clean_output(book):
    lines = []
    in_code = False
    for line in book.split("\n"):
        if ".svg" in line and "includegraphics" in line:
            lines.append(line.replace("includegraphics", "includesvg"))
        elif "caption*" in line:
            lines.append(line.replace("caption*", "caption"))
        elif r"\begin{verbatim}" in line:
            lines.append(
                line.replace(
                    r"\begin{verbatim}", r"\begin{lstlisting}[language=Python]"
                )
            )
            in_code = True
        elif "\end{verbatim}" in line:
            lines.append(line.replace(r"\end{verbatim}", r"\end{lstlisting}"))
            in_code = False
        else:
            if in_code:
                lines.append(
                    line.replace("- -", "--")
                    .replace(" - ", "-")
                    .replace("true -neutral -cookiecutter", "true-neural-cookiecutter")
                )
            else:
                lines.append(line)

    return "\n".join(lines)


def assemble_onepager():
    with open("_toc.yml", "r") as f:
        toc = yaml.safe_load(f)
    print(toc)

    # Copy files
    process = subprocess.Popen(
        ["cp", "-r", "figures", "tmp"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    print(stderr.decode("utf-8"))

    book_parts = collections.defaultdict(str)

    book_parts["Intro"] += process_one("front-print")
    for part in toc["parts"]:
        for chapter in part["chapters"]:
            book_parts[part["caption"]] += process_one(chapter["file"])

    the_map = {
        "Intro": "[-FRONTMATTER-]",
        "Lessons": "[-CONTENT-]",
        "Extras": "[-BACKMATTER-]",
    }

    complete = template
    for k, v in the_map.items():
        part = clean_output(book_parts[k])
        complete = complete.replace(v, part)

    with open("tmp/exports/book-complete.tex", "w") as f:
        f.write(complete)


if __name__ == "__main__":
    assemble_onepager()
