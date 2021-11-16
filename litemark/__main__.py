import tkinter as tk
import pkgutil
import sys
import os
import os.path
from tkinter.scrolledtext import ScrolledText
from litemark import Viewer, center_window, get_light_style


def set_root_style(root):
    root.option_add("*Text.highlightThickness", 0)
    root.option_add("*Text.borderWidth", 0)
    root.option_add("*Text.selectBackground", "#CCEBFF")
    root.option_add("*Text.inactiveSelectBackground", "#A8E1FF")
    root.option_add("*Scrollbar.troughColor", "white")
    root.option_add("*Scrollbar.activeBackground", "#E2E2E2")
    root.option_add("*Scrollbar.background", "#EFEFEF")
    root.option_add("*Scrollbar.highlightBackground", "gray")
    root.option_add("*Scrollbar.highlightColor", "gray")
    root.option_add("*Scrollbar.relief", "flat")
    root.option_add("*Scrollbar.highlightThickness", 0)
    root.option_add("*Scrollbar.borderWidth", 0)


def get_demo():
    """ Returns a tuple (root, basename) """
    home = os.path.expanduser("~")
    root = os.path.join(home, "PyrusticData", "litemark", "demo")
    document_filename = os.path.join(root, "litemark-demo.md")
    header_filename = os.path.join(root, "header.png")
    # root
    if not os.path.isdir(root):
        os.makedirs(root)
    # document
    if not os.path.isfile(document_filename):
        document_content = pkgutil.get_data("litemark", "demo/litemark-demo.md")
        with open(document_filename, "wb") as file:
            file.write(document_content)
    # header
    if not os.path.isfile(header_filename):
        header_content = pkgutil.get_data("litemark", "demo/header.png")
        with open(header_filename, "wb") as file:
            file.write(header_content)
    return root, "litemark-demo.md"


def get_document():
    """ Returns a tuple (root, document_data) """
    root = os.getcwd()
    try:
        basename = sys.argv[1]
    except IndexError as e:
        try:
            root, basename = get_demo()
        except Exception as e:
            print("Failed to load the demo")
            sys.exit(1)
    path = os.path.join(root, basename)
    if not os.path.isfile(path):
        print("The path argument isn't a file")
        sys.exit(1)
    with open(path, "r") as file:
        demo = file.read()
    return root, demo


def refresh(root, viewer):
    command = lambda root=root: root.title("Refreshing...")
    root.after(1, command)
    root_dir, data = get_document()
    viewer.render(data=data)
    viewer.readonly = True
    title = "Litemark Viewer | Pyrustic Open Ecosystem"
    command = lambda root=root, title=title: root.title(title)
    root.after(500, command)


def main():
    # root
    root = tk.Tk()
    root.geometry("666x600")
    root.config(background="white")
    root.title("Litemark Viewer | Pyrustic Open Ecosystem")
    set_root_style(root)
    # text widget
    text_widget = ScrolledText(root, width=0, height=0,
                               padx=10, pady=10, wrap="word")
    text_widget.pack(expand=1, fill=tk.BOTH)
    # viewer
    litemark_style = get_light_style()
    root_dir, data = get_document()
    viewer = Viewer(text_widget, root=root_dir, style=litemark_style)
    # render
    viewer.render(data)
    viewer.readonly = True
    # center window
    center_window(root)
    # bind refresh command
    command = (lambda e, root=root, text_widget=text_widget:
               refresh(root, viewer))
    root.bind("<F5>", command)
    # mainloop
    root.mainloop()


if __name__ == "__main__":
    main()
