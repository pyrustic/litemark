import re
from collections import namedtuple


class Element:
    CODEBLOCK = "CODEBLOCK"
    HEADING = "HEADING"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    WARNING = "WARNING"
    OVERSTRIKE = "OVERSTRIKE"
    IMAGE = "IMAGE"
    INTRALINK = "INTRALINK"
    LINK = "LINK"


class Regex:
    CODEBLOCK = r"`{3}([a-z-]*)\n([\s\S]*?)\n`{3}"  # language, code)
    HEADING = r"(?:^)(#{1,6}) ([^ \n]+.*)"  # hashtags, title)
    BOLD = r"\*(([^\s*])|((\\.|[^*])*[^\s*]))\*"  # string
    ITALIC = r"_(([^\s_])|((\\.|[^_])*[^\s_]))_"  # string
    WARNING = r"!(([^\s!])|((\\.|[^!])*[^\s!]))!"  # string
    OVERSTRIKE = r"~(([^\s_])|((\\.|[^~])*[^\s~]))~"  # string
    IMAGE = r"""!\[([^\]]*)\]\((.*?)\s*("(?:.*[^"]|)")?\s*\)"""  # title, location, description
    INTRALINK = r"""%\[([^\]]*)\]\((.*?)\s*("(?:.*[^"]|)")?\s*\)"""  # title, location, description
    LINK = r"""\[([^\]]*)\]\((.*?)\s*("(?:.*[^"]|)")?\s*\)"""  # title, location, description


SPECIFICATION = [
        (Element.CODEBLOCK, Regex.CODEBLOCK),
        (Element.HEADING, Regex.HEADING),
        (Element.BOLD, Regex.BOLD),
        (Element.ITALIC, Regex.ITALIC),
        (Element.WARNING, Regex.WARNING),
        (Element.OVERSTRIKE, Regex.OVERSTRIKE),
        (Element.IMAGE, Regex.IMAGE),
        (Element.INTRALINK, Regex.INTRALINK),
        (Element.LINK, Regex.LINK),
        ("STRING", r"\S*\s*")]


def scan(text):
    compiled = get_compiled_regex()
    Token = namedtuple("Token", ["name", "data"])
    for match in compiled.finditer(text):
        name = match.lastgroup
        cache = []
        for item in match.groups():
            if item is not None:
                cache.append(item)
        if name == Element.CODEBLOCK:
            data = cache[1], cache[2]
        elif name == Element.HEADING:
            data = len(cache[1]), cache[2].strip()
        elif name == Element.BOLD:
            data = cache[1].replace("\\*", "*")
        elif name == Element.ITALIC:
            data = cache[1].replace("\\_", "_")
        elif name == Element.WARNING:
            data = cache[1].replace("\\!", "!")
        elif name == Element.OVERSTRIKE:
            data = cache[1].replace("\\~", "~")
        elif name in (Element.IMAGE, Element.INTRALINK, Element.LINK):
            title, location = cache[1], cache[2]
            title = title.strip("\"'")
            try:
                description = cache[3]
            except IndexError as e:
                description = ""
            else:
                description = description.strip("\"")
            data = title, location, description
        elif name == "STRING":
            data = cache[0].replace("\\_", "_").replace("\\*", "*")
        else:
            raise Error("Unknown element {} !".format(name))
        yield Token(name, data)


def get_compiled_regex():
    pattern = '|'.join("(?P<{}>{})".format(name, regex)
                       for name, regex in SPECIFICATION)
    return re.compile(pattern, re.MULTILINE)


class Error(Exception):
    pass


if __name__ == "__main__":
    import pkgutil
    text = pkgutil.get_data("tkmark", "demo.md")
    text = text.decode("utf-8")
    scan(text)
    cache = []
    for token in scan(text):
        print(token)
