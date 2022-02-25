import pathlib
from tqdm import tqdm


def strip_js(filename, bad_lines):
    good_lines = []
    with open(filename, "r") as f:
        for line in f:
            is_bad = sum([bad_line in line for bad_line in bad_lines])
            if not is_bad:
                good_lines.append(line)

    text = "".join(good_lines)
    with open(filename, "w") as f:
        f.write(text)


if __name__ == "__main__":
    # Go through _build/html, and remove all extraneous javascript. This is all
    # very silly, but upgrading sphinx-book-theme's version to reject the bad js
    # is very annoying
    files = pathlib.Path("_build/html").glob("*.html")
    print(files)
    for f in tqdm(files):
        strip_js(f, ["thebe.js"])
