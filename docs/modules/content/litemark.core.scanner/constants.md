Back to [Modules overview](https://github.com/pyrustic/litemark/blob/master/docs/modules/README.md)
  
# Module documentation
>## litemark.core.scanner
No description
<br>
[constants (1)](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.scanner/constants.md) &nbsp;.&nbsp; [functions (3)](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.scanner/functions.md) &nbsp;.&nbsp; [classes (3)](https://github.com/pyrustic/litemark/blob/master/docs/modules/content/litemark.core.scanner/classes.md)


## Constants
```python
SPECIFICATION = [('CODEBLOCK', '`{3}([a-z-]*)\\n([\\s\\S]*?)\\n`{3}'), ('HEADING', '(?:^)(#{1,6}) ([^ \\n]+.*)'), ('BOLD', '\\*(([^\\s*])|((\\\\.|[^*])*[^\\s\\\\]))\\*'), ('ITALIC', '_(([^\\s_])|((\\\\.|[^_])*[^\\s\\\\]))_'), ('WARNING', '!(([^\\s!])|((\\\\.|[^!])*[^\\s\\\\]))!'), ('OVERSTRIKE', '~(([^\\s_])|((\\\\.|[^~])*[^\\s~]))~'), ('IMAGE', '!\\[([^\\]]*)\\]\\((.*?)\\s*("(?:.*[^"]|)")?\\s*\\)'), ('INLINK', '@\\[([^\\]]*)\\]\\((.*?)\\s*("(?:.*[^"]|)")?\\s*\\)'), ('LINK', '\\[([^\\]]*)\\]\\((.*?)\\s*("(?:.*[^"]|)")?\\s*\\)'), ('STRING', '\\S*\\s*')]

```

