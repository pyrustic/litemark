Back to [Modules overview](https://github.com/pyrustic/litemark/blob/master/docs/modules/README.md)
  
# Module documentation
>## litemark.core.viewer
No description
<br>
[constants (1)](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/constants.md) &nbsp;.&nbsp; [functions (26)](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/functions.md) &nbsp;.&nbsp; [classes (5)](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.viewer/classes.md)


## Classes
```python
class Error(Exception):
    """
    Common base class for all non-exit exceptions.
    """

    # inherited from Exception
    def __init__(self, /, *args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """


    args = <attribute 'args' of 'BaseException' objects>
    
```

```python
class Info(object):
    """
    
    """

    def __init__(self, viewer, widget, element, location):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

```

```python
class TokenError(litemark.core.viewer.Error):
    """
    Common base class for all non-exit exceptions.
    """

    # inherited from Exception
    def __init__(self, /, *args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """


    args = <attribute 'args' of 'BaseException' objects>
    
```

```python
class Viewer(object):
    """
    
    """

    def __init__(self, widget=None, root=None, style=<litemark.core.style.Style object at 0x7f60ff60a400>, on_browse=None):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """

    @property
    def readonly(self):
        """
        
        """

    @readonly.setter
    def readonly(self, val):
        """
        
        """

    @property
    def root(self):
        """
        
        """

    @property
    def style(self):
        """
        
        """

    @property
    def tokens(self):
        """
        
        """

    @property
    def widget(self):
        """
        
        """

    def anchor(self, name):
        """
        name = heading
        """

    def clear(self):
        """
        
        """

    def open(self, path):
        """
        
        """

    def render(self, data):
        """
        data = string or tokens
        """

    def _setup(self):
        """
        
        """

```

```python
class WidgetError(litemark.core.viewer.Error):
    """
    Common base class for all non-exit exceptions.
    """

    # inherited from Exception
    def __init__(self, /, *args, **kwargs):
        """
        Initialize self.  See help(type(self)) for accurate signature.
        """


    args = <attribute 'args' of 'BaseException' objects>
    
```

