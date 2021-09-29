import tkinter as tk


# TODO: migrate Tooltip to megawidget
class Tooltip:
    def __init__(self, master, text):
        self._master = master
        self._text = text
        self._planned = False
        self._busy = False
        self._cancelled = False
        self._cache = []

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        self._text = val

    def show(self):
        if self._busy or self._planned:
            return
        self._planned = True
        pointer_x = self._master.winfo_pointerx()
        pointer_y = self._master.winfo_pointery()
        command = (lambda self=self, pointer_x=pointer_x,
                          pointer_y=pointer_y:
                    self._show(pointer_x, pointer_y))
        self._cache.append(self._master.after(700, command))

    def cancel(self):
        if self._busy:
            return
        if self._planned:
            self._cancelled = True

    def _show(self, pointer_x, pointer_y):
        if self._cancelled:
            self._reset_variables()
            return
        #self._reset_variables()
        self._busy = True
        #self._planned = True
        window = tk.Toplevel(self._master)
        command = (lambda self=self, window=window:
                   self._on_destroy(window))
        window.after(1000, command)
        window.overrideredirect(1)
        label = tk.Label(window, text=self._text,
                         bg="white", fg="#404040",
                         font=("Liberation Mono", 11))
        label.pack()
        window.withdraw()
        window.update_idletasks()
        width = window.winfo_reqwidth()
        height = window.winfo_reqheight()
        x = pointer_x
        y = pointer_y + 17
        x = abs(x)
        y = abs(y)
        if window.winfo_screenwidth() - x < width:
            x = window.winfo_screenwidth() - width
        if window.winfo_screenheight() - y < height:
            y = pointer_y - window.winfo_reqheight()
        # align
        window.geometry("+{}+{}".format(x, y))
        window.deiconify()

    def _on_destroy(self, window):
        window.withdraw()
        window.destroy()
        self._reset_variables()

    def _reset_variables(self):
        for x in self._cache:
            self._master.after_cancel(x)
            self._cache = []
        self._busy = False
        self._cancelled = False
        self._planned = False


def center_window(window):
    """ Center the window """
    window.withdraw()
    window.update_idletasks()
    window.geometry("+0+0")
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    if (window.winfo_screenwidth() - x) < width:
        x = window.winfo_screenwidth() - width
    if (window.winfo_screenheight() - y) < height:
        y = window.winfo_screenheight() - height
    window.geometry("+{}+{}".format(x, y))
    window.deiconify()
