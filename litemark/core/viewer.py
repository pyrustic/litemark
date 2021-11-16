import tkinter as tk
import webbrowser
import pkgutil
import pathlib
from tkinter.font import Font
from litemark.core import scanner
from litemark.core.scanner import Element
from litemark.core.util import Tooltip
from litemark.core.style import Style


IMAGES_CACHE = []


def get_light_style():
    style = Style()
    # default style
    style.text_color = "#303030"
    style.text_font_family = "DejaVu Sans"
    style.text_font_size = 11
    style.text_font_weight = "normal"
    style.text_font_slant = "roman"
    # heading style
    style.heading_color = "#454545"
    style.heading_font_family = None
    style.heading_font_size = None
    style.heading_font_weight = "bold"
    style.heading_font_slant = None
    # bold style
    style.bold_color = "#505050"
    style.bold_font_family = None
    style.bold_font_size = None
    style.bold_font_weight = "bold"
    style.bold_font_slant = None
    # italic style
    style.italic_color = None
    style.italic_font_family = None
    style.italic_font_size = None
    style.italic_font_weight = None
    style.italic_font_slant = "italic"
    # warning style
    style.warning_color = "red"
    style.warning_font_family = None
    style.warning_font_size = None
    style.warning_font_weight = None
    style.warning_font_slant = None
    # overstrike color
    style.overstrike_color = None
    style.overstrike_font_family = None
    style.overstrike_font_size = None
    style.overstrike_font_weight = None
    style.overstrike_font_slant = None
    # link color
    style.link_color = "blue"
    style.link_font_family = None
    style.link_font_size = None
    style.link_font_weight = None
    style.link_font_slant = None
    # inlink style
    style.inlink_color = "blue"
    style.inlink_font_family = None
    style.inlink_font_size = None
    style.inlink_font_weight = None
    style.inlink_font_slant = None
    # codeblock title style
    style.codeblock_title_color = "#B0B016"
    style.codeblock_title_font_family = None
    style.codeblock_title_font_size = None
    style.codeblock_title_font_weight = "bold"
    style.codeblock_title_font_slant = None
    # codeblock style
    style.codeblock_color = "#9A9A00"
    style.codeblock_font_family = "DejaVu Sans Mono"
    style.codeblock_font_size = 11
    style.codeblock_font_weight = None
    style.codeblock_font_slant = None
    return style


def get_dark_style():  # TODO: implement the dark style
    return get_light_style()


class Viewer:
    def __init__(self, widget=None, root=None,
                 style=get_light_style(), on_browse=None):
        self._widget = widget
        self._root = root
        self._style = style if style else get_light_style()
        self._on_browse = on_browse
        self._tokens = None
        self._anchors = {}
        self._setup()

    @property
    def widget(self):
        return self._widget

    @property
    def root(self):
        return self._root

    @property
    def style(self):
        return self._style

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

    def render(self, data):
        """data = string or tokens"""
        ignore = None  # TODO: delete all mentions of ignore !
        if isinstance(data, str):
            data = scanner.scan(data)
        if not data:
            return False
        readonly_cache = self.readonly
        self.clear()
        define_tags(self._widget, self._style)
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
        self.readonly = readonly_cache
        return True

    def open(self, path):
        with open(path, "r") as file:
            data = file.read()
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
        for tag in self._widget.tag_names():
            self._widget.tag_delete(tag)
        self._widget.delete("1.0", tk.END)
        self._anchors = {}
        self._tokens = None
        IMAGES_CACHE[:] = []

    def _setup(self):
        self._style = setup_style(self._style)
        if not isinstance(self._widget, tk.Text):
            raise WidgetError("Only tk.Text widget and subclasses are allowed")
        self._widget.config(state="normal")
        self._widget.bind("<Button-1>",
                          lambda e, widget=self._widget: widget.focus_set())
        self._widget.bind("<Destroy>",
                          lambda event: free_images_cache(), "+")
        font = Font(family=self._style.text_font_family,
                    size=self._style.text_font_size,
                    weight=self._style.text_font_weight,
                    slant=self._style.text_font_slant)
        self._widget.config(font=font,
                            foreground=self._style.text_color)


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
        elif token.name == Element.INLINK:
            insert_inlink(viewer, widget, i, token.data,
                             style, on_browse)
        elif token.name == Element.LINK:
            insert_link(viewer, widget, i, token.data, style, on_browse)
        else:
            raise TokenError("Invalid token '{}'".format(token.name))


def define_tags(widget, style):
    text_font_size = style.text_font_size
    # Heading
    heading_1_font = Font(size=text_font_size+6)
    heading_2_font = Font(size=text_font_size+5)
    heading_3_font = Font(size=text_font_size+4)
    heading_4_font = Font(size=text_font_size+3)
    heading_5_font = Font(size=text_font_size+2)
    heading_6_font = Font(size=text_font_size+1)
    for font in (heading_1_font, heading_2_font,
                 heading_3_font, heading_4_font,
                 heading_5_font, heading_6_font):
        font.config(family=style.heading_font_family,
                    weight=style.heading_font_weight,
                    slant=style.heading_font_slant)
    for tag, font in (("heading_1", heading_1_font),
                      ("heading_2", heading_2_font),
                      ("heading_3", heading_3_font),
                      ("heading_4", heading_4_font),
                      ("heading_5", heading_5_font),
                      ("heading_6", heading_6_font)):
        widget.tag_configure(tag, font=font,
                             foreground=style.heading_color,
                             spacing1=1, spacing3=7)
    # bold
    bold_font = Font(family=style.bold_font_family,
                     size=style.bold_font_size,
                     weight=style.bold_font_weight,
                     slant=style.bold_font_slant)
    widget.tag_configure("bold", font=bold_font,
                         foreground=style.bold_color)
    # italic
    italic_font = Font(family=style.italic_font_family,
                       size=style.italic_font_size,
                       weight=style.italic_font_weight,
                       slant=style.italic_font_slant)
    widget.tag_configure("italic", font=italic_font,
                         foreground=style.italic_color)
    # warning
    warning_font = Font(family=style.warning_font_family,
                        size=style.warning_font_size,
                        weight=style.warning_font_weight,
                        slant=style.warning_font_slant)
    widget.tag_configure("warning", font=warning_font,
                         foreground=style.warning_color)
    # overstrike
    overstrike_font = Font(family=style.overstrike_font_family,
                           size=style.overstrike_font_size,
                           weight=style.overstrike_font_weight,
                           slant=style.overstrike_font_slant,
                           overstrike=1)
    widget.tag_configure("overstrike", font=overstrike_font,
                         foreground=style.overstrike_color)
    # codeblock-title
    codeblock_title_font = Font(family=style.codeblock_title_font_family,
                                size=style.codeblock_title_font_size,
                                weight=style.codeblock_title_font_weight,
                                slant=style.codeblock_title_font_slant)
    widget.tag_configure("codeblock-title", font=codeblock_title_font,
                         foreground=style.codeblock_title_color,
                         spacing1=1, spacing3=3)
    # on_enter and on_leave event handlers
    on_enter = lambda event, widget=widget: widget.config(cursor="hand1")
    on_leave = lambda event, widget=widget: widget.config(cursor="")
    # bind hand icon to codeblock and link and inlink (enter vs leave)
    widget.tag_bind("codeblock", "<Enter>", on_enter, "+")
    widget.tag_bind("codeblock", "<Leave>", on_leave, "+")
    widget.tag_bind("link", "<Enter>", on_enter, "+")
    widget.tag_bind("link", "<Leave>", on_leave, "+")
    widget.tag_bind("inlink", "<Enter>", on_enter, "+")
    widget.tag_bind("inlink", "<Leave>", on_leave, "+")


def insert_link(viewer, widget, index, data, style, on_browse):
    title, location, description = data
    if on_browse:
        info = Info(viewer, widget, "link", location)
        location = on_browse(info)
        if not location:
            return
    title = title if title else location
    tag_name = "link_{}".format(index)
    font = Font(family=style.link_font_family,
                size=style.link_font_size,
                weight=style.link_font_weight,
                slant=style.link_font_slant)
    widget.tag_configure(tag_name, foreground=style.link_color,
                         font=font)
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
    font = Font(family=style.codeblock_font_family,
                size=style.codeblock_font_size,
                weight=style.codeblock_font_weight,
                slant=style.codeblock_font_slant)
    widget.tag_configure(tag_name, font=font,
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


def insert_inlink(viewer, widget, index, data, style, on_browse):
    title, location, description = data
    if on_browse:
        info = Info(viewer, widget, "inlink", location)
        location = on_browse(info)
        if not location:
            return
    title = title if title else location
    tag_name = "inlink_{}".format(index)
    font = Font(family=style.inlink_font_family,
                size=style.inlink_font_size,
                weight=style.inlink_font_weight,
                slant=style.inlink_font_slant)
    widget.tag_configure(tag_name, foreground=style.link_color,
                         font=font)
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
                    on_button_release_1_inlink(viewer, widget,
                                                  tag_name, location), "+")
    widget.tag_bind(tag_name, "<ButtonPress-3>",
                    lambda e, widget=widget, tag_name=tag_name:
                    on_button_press_3_link(widget, tag_name), "+")
    widget.tag_bind(tag_name, "<ButtonRelease-3>",
                    lambda e, widget=widget, tag_name=tag_name,
                           location=location:
                    on_button_release_3_link(widget, tag_name, location), "+")
    widget.insert(tk.END, title, ("inlink", tag_name))


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


def on_button_release_1_inlink(viewer, widget, tag_name, location):
    font = Font(font=widget.tag_cget(tag_name, "font"))
    actual = font.actual()
    actual["underline"] = 0
    font = Font(**actual)
    widget.tag_configure(tag_name, font=font)
    # move to
    path = ""
    anchor = ""
    if "#" in location:
        for char in location:
            if char == "#" or anchor:
                anchor += char
            else:
                path += char
    else:
        path = location
    if path:
        viewer.open(path)
    if anchor:
        viewer.anchor(anchor)


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


def setup_style(style):
    # heading style
    if not style.heading_color:
        style.heading_color = style.text_color
    if not style.heading_font_family:
        style.heading_font_family = style.text_font_family
    if not style.heading_font_size:
        style.heading_font_size = style.text_font_size
    if not style.heading_font_weight:
        style.heading_font_weight = style.text_font_weight
    if not style.heading_font_slant:
        style.heading_font_slant = style.text_font_slant
    # bold style
    if not style.bold_color:
        style.bold_color = style.text_color
    if not style.bold_font_family:
        style.bold_font_family = style.text_font_family
    if not style.bold_font_size:
        style.bold_font_size = style.text_font_size
    if not style.bold_font_weight:
        style.bold_font_weight = style.text_font_weight
    if not style.bold_font_slant:
        style.bold_font_slant = style.text_font_slant
    # italic style
    if not style.italic_color:
        style.italic_color = style.text_color
    if not style.italic_font_family:
        style.italic_font_family = style.text_font_family
    if not style.italic_font_size:
        style.italic_font_size = style.text_font_size
    if not style.italic_font_weight:
        style.italic_font_weight = style.text_font_weight
    if not style.italic_font_slant:
        style.italic_font_slant = style.text_font_slant
    # warning style
    if not style.warning_color:
        style.warning_color = style.text_color
    if not style.warning_font_family:
        style.warning_font_family = style.text_font_family
    if not style.warning_font_size:
        style.warning_font_size = style.text_font_size
    if not style.warning_font_weight:
        style.warning_font_weight = style.text_font_weight
    if not style.warning_font_slant:
        style.warning_font_slant = style.text_font_slant
    # overstrike style
    if not style.overstrike_color:
        style.overstrike_color = style.text_color
    if not style.overstrike_font_family:
        style.overstrike_font_family = style.text_font_family
    if not style.overstrike_font_size:
        style.overstrike_font_size = style.text_font_size
    if not style.overstrike_font_weight:
        style.overstrike_font_weight = style.text_font_weight
    if not style.overstrike_font_slant:
        style.overstrike_font_slant = style.text_font_slant
    # link style
    if not style.link_color:
        style.link_color = style.text_color
    if not style.link_font_family:
        style.link_font_family = style.text_font_family
    if not style.link_font_size:
        style.link_font_size = style.text_font_size
    if not style.link_font_weight:
        style.link_font_weight = style.text_font_weight
    if not style.link_font_slant:
        style.link_font_slant = style.text_font_slant
    # inlink style
    if not style.inlink_color:
        style.inlink_color = style.link_color
    if not style.inlink_font_family:
        style.inlink_font_family = style.link_font_family
    if not style.inlink_font_size:
        style.inlink_font_size = style.link_font_size
    if not style.inlink_font_weight:
        style.inlink_font_weight = style.link_font_weight
    if not style.inlink_font_slant:
        style.inlink_font_slant = style.link_font_slant
    # codeblock title style
    if not style.codeblock_title_color:
        style.codeblock_title_color = style.text_color
    if not style.codeblock_title_font_family:
        style.codeblock_title_font_family = style.text_font_family
    if not style.codeblock_title_font_size:
        style.codeblock_title_font_size = style.text_font_size
    if not style.codeblock_title_font_weight:
        style.codeblock_title_font_weight = style.text_font_weight
    if not style.codeblock_title_font_slant:
        style.codeblock_title_font_slant = style.text_font_slant
    # codeblock style
    if not style.codeblock_color:
        style.codeblock_color = style.text_color
    if not style.codeblock_font_family:
        style.codeblock_font_family = style.text_font_family
    if not style.codeblock_font_size:
        style.codeblock_font_size = style.text_font_size
    if not style.codeblock_font_weight:
        style.codeblock_font_weight = style.text_font_weight
    if not style.codeblock_font_slant:
        style.codeblock_font_slant = style.text_font_slant
    return style


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
