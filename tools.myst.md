# Use good tools

(vscode)=
## Choose an IDE

Integrated development environments (IDE) can help you develop faster and make it easy to implement some of the productivity tips I've discussed previously. Preferred IDEs change from year to year, as new editors become favored while others are shunned. Don't be surprised if in three years you'll be using a different IDE.

[I've evaluated many IDEs](https://xcorr.net/2013/04/17/evaluating-ides-for-scientific-python/), and overall, I like [vscode](https://code.visualstudio.com/) best. It's open source, free, and fast. It has very good integrated Python development tools, and it has an impressive array of plugins for almost any imaginable use case. Others recommend [PyCharm](https://www.jetbrains.com/pycharm/) - it's more targeted towards industry use cases, has best-in-class code understanding, and remains usable with large codebases. It's free for academics.

(wsl)=
## Use WSL on Windows

Windows' basic terminal lacks basic features. Powershell is powerful but it is very different from other platforms. For a while, the best way to get a Unix-style shell on Windows was to use the git bash tool. In my opinion, these days the best-in-class terminal to use on Windows is *Windows subsystem for Linux* (WSL). 

*WSL* is an emulation layer that allows you to run a full Linux kernel inside of a Windows terminal window. [Once installed](https://docs.microsoft.com/en-us/windows/wsl/install-win10), you can install any Linux OS you like - Ubuntu being the *de facto* standard. 

You won't be able to run GUI applications. However, many tools you'll want to use run webservers, for example jupyter - you'll be able to access these through your your normal Windows-based web browser, such as Chrome, Firefox or Edge. Your Linux installation will run in a virtual filesystem, which you can access through Windows explorer by typing `explorer` inside a WSL terminal. `code .` will fire up a version of vscode in your current directory.

