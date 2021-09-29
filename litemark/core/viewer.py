import tkinter as tk
import webbrowser
import pkgutil
import os
import os.path
from tkinter.font import Font
from litemark.core import scanner
from litemark.core.scanner import Element
from litemark.core.util import Tooltip
import pathlib
from litemark.core.style import Style


IMAGES_CACHE = []


class Viewer:
    def __init__(self, widget=None, root=None, style=None, on_browse=None):
        self._widget = widget
        self._root = root
        self._style = style
        self._on_browse = on_browse
        self._tokens = None
        self._anchors = {}
        self._setup()

    @property
    def widget(self):
        return self._widget

    @property
    def style(self):
        return self._style

    @property
    def root(self):
        return self._root

    @property
    def redirection(self):
        return self._redirection

    @redirection.setter
    def redirection(self, val):
        self._redirection = val

    @property
    def readonly(self):
        state = self._widget.cget("state")
        if state == tk.DISABLED:
            return True
        return False

    @readonly.setter
    def readonly(self, val):
        state = tk.NORMAL
        if val:
            state = tk.DISABLED
        self._widget.config(state=state)

    @property
    def tokens(self):
        return self._tokens

    def render(self, data, ignore=None):
        """data = string or tokens"""
        if isinstance(data, str):
            data = scanner.scan(data)
        if not data:
            return False
        self.clear()
        self._tokens = data
        if not ignore:
            ignore = tuple()
        elif not isinstance(ignore, tuple) and not isinstance(ignore, list):
            ignore = tuple((ignore, ))
        else:
            ignore = tuple(ignore)
        render(self, self._widget, self._tokens, ignore,
               self._style, self._anchors, self._root,
               self._on_browse)
        remove_empty_lines(self._widget)
        return True

    def open(self, path):
        with open(path, "r") as file:
            data = file.read
        self.render(data)

    def anchor(self, name):
        """name = heading"""
        try:
            self._widget.see(self._anchors[name.lower()])
        except KeyError as e:
            return False
        return True

    def clear(self):
        self._widget.config(state="normal")
        self._widget.delete("1.0", tk.END)
        self._anchors = {}
        self._tokens = None
        IMAGES_CACHE[:] = []

    def _setup(self):
        if not self._style:
            self._style = Style()
        if not isinstance(self._widget, tk.Text):
            raise WidgetError("Only tk.Text widget and subclasses are allowed")
        self._widget.config(state="normal")
        self._widget.bind("<Button-1>",
                          lambda e, widget=self._widget: widget.focus_set())
        self._widget.bind("<Destroy>",
                          lambda event: free_images_cache(), "+")
        self._widget.config(font=self._style.text_font,
                            background=self._style.text_background,
                            foreground=self._style.text_color)
        apply_tags(self._widget, self._style)


def render(viewer, widget, tokens, ignore,
           style, anchors, root, on_browse):
    for i, token in enumerate(tokens):
        if token.name == Element.CODEBLOCK:
            if token.data[0] in ignore:
                continue
        if token.name == "STRING":
            widget.insert(tk.END, token.data)
        elif token.name == Element.CODEBLOCK:
            insert_codeblock(widget, i, token.data, style)
        elif token.name == Element.HEADING:
            heading_level = token.data[0]
            title = token.data[1]
            cache = "{}_{}".format("#" * heading_level, title)
            cache = cache.replace(" ", "_")
            cache = cache.lower()
            anchors[cache] = widget.index(tk.INSERT)
            widget.insert(tk.END, title,
                          "heading_{}".format(heading_level))
        elif token.name == Element.BOLD:
            widget.insert(tk.END, token.data, "bold")
        elif token.name == Element.ITALIC:
            widget.insert(tk.END, token.data, "italic")
        elif token.name == Element.WARNING:
            widget.insert(tk.END, token.data, "warning")
        elif token.name == Element.OVERSTRIKE:
            widget.insert(tk.END, token.data, "overstrike")
        elif token.name == Element.IMAGE:
            insert_image(widget, i, token.data, root)
        elif token.name == Element.INTRALINK:
            insert_intralink(viewer, widget, i, token.data,
                             style, on_browse)
        elif token.name == Element.LINK:
            insert_link(viewer, widget, i, token.data, style, on_browse)
        else:
            raise TokenError("Invalid token '{}'".format(token.name))


def apply_tags(widget, style):
    font = Font(font=widget.cget("font"))
    actual_font_size = font.actual()["size"]
    # Heading
    font_heading_1 = Font(size=actual_font_size+6, weight="bold")
    font_heading_2 = Font(size=actual_font_size+5, weight="bold")
    font_heading_3 = Font(size=actual_font_size+4, weight="bold")
    font_heading_4 = Font(size=actual_font_size+3, weight="bold")
    font_heading_5 = Font(size=actual_font_size+2, weight="bold")
    font_heading_6 = Font(size=actual_font_size+1, weight="bold")
    widget.tag_configure("heading_1", font=font_heading_1,
                         foreground=style.heading_color,
                         spacing1=1, spacing3=5)
    widget.tag_configure("heading_2", font=font_heading_2,
                         foreground=style.heading_color,
                         spacing1=1, spacing3=5)
    widget.tag_configure("heading_3", font=font_heading_3,
                         foreground=style.heading_color,
                         spacing1=1, spacing3=5)
    widget.tag_configure("heading_4", font=font_heading_4,
                         foreground=style.heading_color,
                         spacing1=1, spacing3=5)
    widget.tag_configure("heading_5", font=font_heading_5,
                         foreground=style.heading_color,
                         spacing1=1, spacing3=5)
    widget.tag_configure("heading_6", font=font_heading_6,
                         foreground=style.heading_color,
                         spacing1=1, spacing3=5)
    # bold
    font_bold = Font(weight="bold")
    widget.tag_configure("bold", font=font_bold,
                         foreground=style.bold_color)
    # italic
    font_italic = Font(slant="italic")
    widget.tag_configure("italic", font=font_italic,
                         foreground=style.italic_color)
    # warning
    font_warning = Font()
    warning_color = style.warning_color if style.warning_color else "red"
    widget.tag_configure("warning", font=font_warning,
                         foreground=warning_color)
    # overstrike
    font_overstrike = Font(overstrike=1)
    widget.tag_configure("overstrike", font=font_overstrike,
                         foreground=style.overstrike_color)
    # codeblock-title
    widget.tag_configure("codeblock-title",
                         foreground=style.codeblock_title_color)
    # on_enter and on_leave event handlers
    on_enter = lambda event, widget=widget: widget.config(cursor="hand1")
    on_leave = lambda event, widget=widget: widget.config(cursor="")
    # bind hand icon to codeblock and link and intralink (enter vs leave)
    widget.tag_bind("codeblock", "<Enter>", on_enter, "+")
    widget.tag_bind("codeblock", "<Leave>", on_leave, "+")
    widget.tag_bind("link", "<Enter>", on_enter, "+")
    widget.tag_bind("link", "<Leave>", on_leave, "+")
    widget.tag_bind("intralink", "<Enter>", on_enter, "+")
    widget.tag_bind("intralink", "<Leave>", on_leave, "+")


def insert_link(viewer, widget, index, data, style, on_browse):
    title, location, description = data
    if on_browse:
        info = Info(viewer, widget, "link", location)
        location = on_browse(info)
        if not location:
            return
    title = title if title else location
    tag_name = "link_{}".format(index)
    widget.tag_configure(tag_name, foreground=style.link_color,
                         font=style.text_font)
    tooltip = Tooltip(widget, location)
    widget.tag_bind(tag_name, "<Enter>",
                    lambda e, widget=widget, tag_name=tag_name,
                    tooltip=tooltip:
                    on_enter_link(widget, tooltip), "+")
    widget.tag_bind(tag_name, "<Leave>",
                    lambda e, widget=widget, tag_name=tag_name,
                           tooltip=tooltip:
                    on_leave_link(widget, tooltip), "+")
    widget.tag_bind(tag_name, "<ButtonPress-1>",
                    lambda e, widget=widget, tag_name=tag_name:
                    on_button_press_1_link(widget, tag_name), "+")
    widget.tag_bind(tag_name, "<ButtonRelease-1>",
                    lambda e, widget=widget, tag_name=tag_name,
                           location=location:
                    on_button_release_1_link(widget, tag_name,
                                           location), "+")
    widget.tag_bind(tag_name, "<ButtonPress-3>",
                    lambda e, widget=widget, tag_name=tag_name:
                    on_button_press_3_link(widget, tag_name), "+")
    widget.tag_bind(tag_name, "<ButtonRelease-3>",
                    lambda e, widget=widget, tag_name=tag_name,
                    location=location:
                    on_button_release_3_link(widget, tag_name, location), "+")
    widget.insert(tk.END, title, ("link", tag_name))


def insert_codeblock(widget, index, data, style):
    title, code = data
    tag_name = "codeblock_{}".format(index)
    widget.tag_configure(tag_name, font=style.codeblock_font,
                         foreground=style.codeblock_color)
    widget.tag_bind(tag_name, "<Enter>",
                    lambda e, widget=widget, tag_name=tag_name:
                    on_enter_codeblock(widget), "+")
    widget.tag_bind(tag_name, "<Leave>",
                    lambda e, widget=widget, tag_name=tag_name:
                    on_leave_codeblock(widget), "+")
    widget.tag_bind(tag_name, "<ButtonPress-3>",
                    lambda e, widget=widget, tag_name=tag_name:
                    on_button_press_3_codeblock(widget, tag_name), "+")
    widget.tag_bind(tag_name, "<ButtonRelease-3>",
                    lambda e, widget=widget, tag_name=tag_name, code=code:
                    on_button_release_3_codeblock(widget, tag_name, code), "+")
    if title:
        cache_title = "{}\n".format(title)
        widget.insert(tk.END, cache_title, ("codeblock-title", "bold"))
    widget.insert(tk.END, code, ("codeblock", tag_name))


def insert_intralink(viewer, widget, index, data, style, on_browse):
    title, location, description = data
    if on_browse:
        info = Info(viewer, widget, "intralink", location)
        location = on_browse(info)
        if not location:
            return
    title = title if title else location
    tag_name = "intralink_{}".format(index)
    widget.tag_configure(tag_name, foreground=style.link_color,
                         font=style.text_font)
    tooltip = Tooltip(widget, location)
    widget.tag_bind(tag_name, "<Enter>",
                    lambda e, widget=widget, tag_name=tag_name,
                           tooltip=tooltip:
                    on_enter_link(widget, tooltip), "+")
    widget.tag_bind(tag_name, "<Leave>",
                    lambda e, widget=widget, tag_name=tag_name,
                           tooltip=tooltip:
                    on_leave_link(widget, tooltip), "+")
    widget.tag_bind(tag_name, "<ButtonPress-1>",
                    lambda e, widget=widget, tag_name=tag_name:
                    on_button_press_1_link(widget, tag_name), "+")
    widget.tag_bind(tag_name, "<ButtonRelease-1>",
                    lambda e, widget=widget, tag_name=tag_name,
                           viewer=viewer, location=location:
                    on_button_release_1_intralink(viewer, widget,
                                                  tag_name, location), "+")
    widget.tag_bind(tag_name, "<ButtonPress-3>",
                    lambda e, widget=widget, tag_name=tag_name:
                    on_button_press_3_link(widget, tag_name), "+")
    widget.tag_bind(tag_name, "<ButtonRelease-3>",
                    lambda e, widget=widget, tag_name=tag_name,
                           location=location:
                    on_button_release_3_link(widget, tag_name, location), "+")
    widget.insert(tk.END, title, ("intralink", tag_name))


def insert_image(widget, index, data, root):
    title, location, description = data
    title = title if title else description
    if ":" in location:
        package, res = location.split(":")
        img = pkgutil.get_data(package, res)
    else:
        if root:
            location = pathlib.PurePath(root, location)
        with open(location, "rb") as file:
            img = file.read()
    photo_image = tk.PhotoImage(data=img)
    widget.image_create(tk.END, image=photo_image)
    IMAGES_CACHE.append(photo_image)
    if title:
        widget.insert(tk.END, "\n"+title, "italic")


def create_image_tile(parent, img, index):
    # canvas
    photo_image = tk.PhotoImage(data=img)
    parent.image_create(tk.END, image=photo_image)
    try:
        parent.image
    except AttributeError as e:
        parent.images = []
    finally:
        parent.images.append(photo_image)


def open_website(url, widget):
    command = lambda: webbrowser.open(url, new=2)
    widget.after(1, command)


def update_clipboard(widget, data):
    widget.clipboard_clear()
    widget.clipboard_append(data)


def button_press_effect(widget, tag_name):
    font = Font(font=widget.tag_cget(tag_name, "font"))
    actual = font.actual()
    actual["underline"] = 1
    font = Font(**actual)
    widget.tag_configure(tag_name, font=font)


def button_release_effect(widget, tag_name):
    font = Font(font=widget.tag_cget(tag_name, "font"))
    actual = font.actual()
    actual["underline"] = 0
    font = Font(**actual)
    widget.tag_configure(tag_name, font=font)


def on_enter_link(widget, tooltip):
    tooltip.show()
    widget.config(cursor="hand1")


def on_leave_link(widget, tooltip):
    tooltip.cancel()
    widget.config(cursor="")


def on_button_press_1_link(widget, tag_name):
    font = Font(font=widget.tag_cget(tag_name, "font"))
    actual = font.actual()
    actual["underline"] = 1
    font = Font(**actual)
    widget.tag_configure(tag_name, font=font)


def on_button_release_1_link(widget, tag_name, location):
    font = Font(font=widget.tag_cget(tag_name, "font"))
    actual = font.actual()
    actual["underline"] = 0
    font = Font(**actual)
    widget.tag_configure(tag_name, font=font)
    open_website(location, widget)


def on_button_release_1_intralink(viewer, widget, tag_name, location):
    font = Font(font=widget.tag_cget(tag_name, "font"))
    actual = font.actual()
    actual["underline"] = 0
    font = Font(**actual)
    widget.tag_configure(tag_name, font=font)
    viewer.anchor(location)


def on_enter_codeblock(widget):
    widget.config(cursor="hand1")


def on_leave_codeblock(widget):
    widget.config(cursor="")


def on_button_press_3_link(widget, tag_name):
    font = Font(font=widget.tag_cget(tag_name, "font"))
    actual = font.actual()
    actual["underline"] = 1
    font = Font(**actual)
    widget.tag_configure(tag_name, font=font)


def on_button_release_3_link(widget, tag_name, location):
    update_clipboard(widget, location)
    font = Font(font=widget.tag_cget(tag_name, "font"))
    actual = font.actual()
    actual["underline"] = 0
    font = Font(**actual)
    widget.tag_configure(tag_name, font=font)


def on_button_press_3_codeblock(widget, tag_name):
    font = Font(font=widget.tag_cget(tag_name, "font"))
    actual = font.actual()
    actual["underline"] = 1
    font = Font(**actual)
    widget.tag_configure(tag_name, font=font)


def on_button_release_3_codeblock(widget, tag_name, code):
    update_clipboard(widget, code)
    font = Font(font=widget.tag_cget(tag_name, "font"))
    actual = font.actual()
    actual["underline"] = 0
    font = Font(**actual)
    widget.tag_configure(tag_name, font=font)


def remove_empty_lines(widget):
    cursor = widget.index(tk.END)
    line, _ = cursor.split(".")
    line = int(line)
    while True:
        if line == 1:
            break
        pos = "{}.0".format(line)
        cache = widget.get(pos, tk.END)
        if cache.isspace() or cache == "":
            widget.delete(pos, tk.END)
        else:
            break
        line -= 1


def free_images_cache():
    IMAGES_CACHE[:] = []


class Info:
    def __init__(self, viewer, widget, element, location):
        self.viewer = viewer
        self.widget = widget
        self.element = element
        self.location = location


class Error(Exception):
    pass


class WidgetError(Error):
    pass


class TokenError(Error):
    pass
