from litemark.core import scanner
from litemark.core.scanner import Element
from litemark.core.viewer import Viewer, get_light_style
from litemark.core.style import Style
from litemark.core.util import center_window


__all__ = ["scan", "Element", "Viewer", "get_light_style", "Style"]


def scan(text):
    """Returns an iterator. If you need a list: list(scan(text))"""
    return scanner.scan(text)
