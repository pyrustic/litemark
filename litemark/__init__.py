from tkinter.font import Font
from litemark.core import scanner
from litemark.core.scanner import Element
from litemark.core.viewer import Viewer
from litemark.core.style import Style
from litemark.core.util import center_window


def scan(text):
    return list(scanner.scan(text))


def get_default_style():
    style = Style()
    style.text_font = Font(family="DejaVu Sans", size=11)
    style.codeblock_font = Font(family="DejaVu Sans Mono", size=11)
    style.text_color = "#404040"
    style.text_color = "#505050"
    style.bold_color = "#707070"
    style.link_color = "blue"
    style.reference_color = "blue"
    style.heading_color = "#4D4D4D"
    style.heading_color = "#656565"
    style.heading_color = "#404040"
    style.heading_color = "#505050"
    style.codeblock_color = "#9A9A00"
    style.codeblock_title_color = "#B0B016"
    return style
