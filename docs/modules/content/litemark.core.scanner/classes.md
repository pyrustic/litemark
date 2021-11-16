Back to [Modules overview](https://github.com/pyrustic/litemark/blob/master/docs/modules/README.md)
  
# Module documentation
>## litemark.core.scanner
No description
<br>
[constants (1)](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.scanner/constants.md) &nbsp;.&nbsp; [functions (3)](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.scanner/functions.md) &nbsp;.&nbsp; [classes (3)](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.scanner/classes.md)


## Classes
```python
class Element(object):
    """
    
    """


    BOLD = "BOLD"
    
    CODEBLOCK = "CODEBLOCK"
    
    HEADING = "HEADING"
    
    IMAGE = "IMAGE"
    
    INLINK = "INLINK"
    
    ITALIC = "ITALIC"
    
    LINK = "LINK"
    
    OVERSTRIKE = "OVERSTRIKE"
    
    STRING = "STRING"
    
    WARNING = "WARNING"
    
```

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
class Regex(object):
    """
    
    """


    BOLD = "\*(([^\s*])|((\\.|[^*])*[^\s\\]))\*"
    
    CODEBLOCK = "`{3}([a-z-]*)\n([\s\S]*?)\n`{3}"
    
    HEADING = "(?:^)(#{1,6}) ([^ \n]+.*)"
    
    IMAGE = "!\[([^\]]*)\]\((.*?)\s*("(?:.*[^"]|)")?\s*\)"
    
    INLINK = "@\[([^\]]*)\]\((.*?)\s*("(?:.*[^"]|)")?\s*\)"
    
    ITALIC = "_(([^\s_])|((\\.|[^_])*[^\s\\]))_"
    
    LINK = "\[([^\]]*)\]\((.*?)\s*("(?:.*[^"]|)")?\s*\)"
    
    OVERSTRIKE = "~(([^\s_])|((\\.|[^~])*[^\s~]))~"
    
    STRING = "\S*\s*"
    
    WARNING = "!(([^\s!])|((\\.|[^!])*[^\s\\]))!"
    
```

