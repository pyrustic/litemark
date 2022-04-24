This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).

[Usage](#usage) | [Installation](#installation)

# Litemark

`Litemark` is a lightweight `Markdown` dialect originally created to be the markup language for the [Codegame Platform](https://github.com/pyrustic/codegame) project.
When you run `litemark` from the command line interface without any arguments, the `Litemark Viewer` opens and displays the rendered demo.


<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/litemark-rendered.png" alt="Figure" width="668">
    <p align="center">
    <i> Litemark demo rendered in the Litemark Viewer </i>
    </p>
</div>

<br>

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/litemark-plain-text.png" alt="Figure" width="700">
    <p align="center">
    <i> litemark-demo.md (plain text) </i>
    </p>
</div>

## Usage
The name `Litemark` refers to both the markup language and the distribution package.

The distribution package comes with an API, a command line interface, and a graphical viewer.
### API
It is easy to break an arbitrary plain text into a flat list of tokens:
```python
import litemark


plain_text = """Hello *World* ! Visit the [repository](https://github.com/pyrustic/litemark) !"""

for token in litemark.scan(plain_text):
    # a token instance is a named tuple with 2 fields: name and data 
    print(token)
```
The output:
```
Token(name='STRING', data='Hello ')
Token(name='BOLD', data='World')
Token(name='STRING', data=' ! Visit the ')
Token(name='LINK', data=('repository', 'https://github.com/pyrustic/litemark', ''))
Token(name='STRING', data=' !')
```
The formal names of the tokens are defined in `litemark.Element`:
```python
class Element:
    CODEBLOCK = "CODEBLOCK"
    HEADING = "HEADING"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    WARNING = "WARNING"
    OVERSTRIKE = "OVERSTRIKE"
    IMAGE = "IMAGE"
    INLINK = "INLINK"
    LINK = "LINK"
    STRING = "STRING"
```
The token's `data` field represents a string for all elements except the following:
- **Element.CODEBLOCK**: 2-tuple (str-title, str-content)
- **Element.HEADING**: 2-tuple (int-level, str-content)
- **Element.IMAGE**: 3-tuple (str-inline, str-path, str-alt)
- **Element.INLINK**: 3-tuple (str-inline, str-path, str-alt)
- **Element.LINK**: 3-tuple (str-inline, str-URL, str-alt)

### Command line interface
To open `litemark-demo.md` in the graphical `Viewer`:
```bash
$ litemark
```

To open a specific `litemark` file in the graphical `Viewer`:
```bash
$ cd /path/to/root
$ litemark my-file.md
```

**Note:**
> Litemark is created for use in a desktop application. Thus, the Litemark Scanner assumes that the images referenced in a litemark document are relative to the `root` directory. The `root` directory is simply the current working directory. For this reason, you must first do a `cd` (change directory) to the root before rendering a document.

### Graphical Viewer
It is easy to embed a `Litemark Viewer` in your Python desktop app:
```python
import litemark
import tkinter as tk

root_directory = "/home/alex/demo"
litemark_filename = "/home/alex/demo/document.md"

# your GUI
gui = tk.Tk()
gui.geometry("500x500+0+0")

# let's embed a Litemark Viewer in this GUI

# -- text widget
text_widget = tk.Text(gui)
text_widget.pack(expand=1, fill=tk.BOTH)

# -- the viewer instance
viewer = litemark.Viewer(widget=text_widget, root=root_directory)
viewer.open(litemark_filename)
viewer.readonly = True

# done !
gui.mainloop()
```

This is a work in progress. A reference documentation will be released soon.

## Installation

### Install for the first time
```bash
pip install litemark
```

### Upgrade
```bash
pip install litemark --upgrade --upgrade-strategy eager
```

## Related projects
- [Codegame Platform](https://github.com/pyrustic/codegame): create, distribute, and run codegames
- [shared](https://github.com/pyrustic/shared): library to store, expose, read, and edit collections of data


This is a work in progress...
