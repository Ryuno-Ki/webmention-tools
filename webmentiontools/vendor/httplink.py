"""
Parser for rfc8288 links.
This is a backport of https://pypi.org/project/httplink/ for Python2
"""

import re
from sys import version_info
from urllib import unquote

if version_info[0] == 2:
    from io import BytesIO as StringIO
else:  # Python3
    from io import StringIO

__all__ = [
    'parse_link_header',
]


def decode_extended_value(value):
    """
    Decode ext-value according to rfc8187
    """
    match = RE_EXT_VALUE.match(value)
    if not match:
        raise ValueError('Bad extended value: {!r}'.format(value))
    charset, language, encoded_value = match.groups()

    if charset.upper() != 'UTF-8':
        raise ValueError('Only UTF-8 is acceptable, got {!r}'.format(charset))

    return unquote(encoded_value, errors='strict'), language, charset


class Link:
    """
    One Link from a Link header
    """

    def __init__(self, target, attributes):
        self.target = target
        self.attributes = attributes

        # Populate _attributes. Need to keep a temporary second dict (extended)
        # with values whose key ends in '*'. Those need to override the values
        # with normal keys.
        self._attributes = {}
        extended = {}
        for key, value in self.attributes:
            if key[-1] != '*':
                self._attributes[key.lower()] = value
            else:
                extended[key[:-1].lower()] = decode_extended_value(value)[0]

        self._attributes.update(extended)

        # Populate rel.
        try:
            self.rel = {rel.lower() for rel in self['rel'].split()}
        except KeyError:
            self.rel = set()

    def __getitem__(self, key):
        return self._attributes[key.lower()]

    def __contains__(self, key):
        return key.lower() in self._attributes

    def __len__(self):
        return len(self.attributes)

    def __repr__(self):
        return (
            '<Link ' +
            repr(self.target) +
            ' ' +
            str(sorted(self.rel)) +
            ' ' +
            ' '.join('{!r}={!r}'.format(key, val) for key, val in sorted(self._attributes.items()) if key != 'rel') +  # noqa: E501
            '>'
        )


class ParsedLinks:
    """
    Container for links parsed from a Links HTTP header.
    """
    def __init__(self, links):
        self.links = links
        self._relations = {
            rel: link
            for link in links
            for rel in link.rel
        }

    def __getitem__(self, key):
        return self._relations[key.lower()]

    def __contains__(self, key):
        return key.lower() in self._relations

    def __len__(self):
        return len(self.links)

    def __repr__(self):
        return (
            '<ParsedLinks: ' +
            ', '.join('{}: {}'.format(rel, link) for rel, link in sorted(self._relations.items())) +  # noqa: E501
            '>'
        )


def parse_link_header(link):
    """
    Parse rfc8288 Link into a list of Link objects.

    Raises ValueError if the link cannot be parsed.
    """
    result = []

    # on first run, don't require a comma delimiter
    matcher = RE_LINK_VALUE
    while link:
        # match leading <URI-Reference> and remove the matched string from
        # `link`

        uri_match = matcher.match(link)
        if not uri_match:
            break
        link = link[uri_match.end():]

        # on subsequent runs, DO require a comma delimiter
        matcher = RE_LINK_VALUE_COMMA

        uri = uri_match.group(1)

        attributes = []
        while True:
            # match leading ;link-param and remove the matched string from
            # `link`
            param_match = RE_LINK_PARAM.match(link)
            if not param_match:
                break
            link = link[param_match.end():]

            # value is either a token or quoted
            key, value_t, value_q = param_match.groups()
            if value_t:
                value = value_t
            else:
                value = unescape(value_q.encode("utf8"))
            attributes.append((key, value))

        result.append(Link(uri, attributes))

    # Check for illegal leftovers
    if not RE_TRAILING_COMMA.match(link):
        raise ValueError('Bad link: {!r}'.format(link))

    return ParsedLinks(result)


# rfc8288 link_value (with optional leading ",")
RE_LINK_VALUE = re.compile(r'''
    ^
    [\s,]*                             # Skip empty elements (rfc7230#7).
    <
    ([^>]*)                            # URI-Reference; contains no ">" according to grammar.  # noqa: E501
    >
''', re.X)

# rfc8288 link_value (with mandatory leading ",")
RE_LINK_VALUE_COMMA = re.compile(r'''
    ^
    \s*,[\s,]*                         # Skip empty elements; require at least one delimiter (rfc7230#7).  # noqa: E501
    <
    ([^>]*)                            # URI-Reference; contains no ">" according to grammar.  # noqa: E501
    >
''', re.X)

# rfc8288 link-param (including ";" from link_value)
RE_LINK_PARAM = re.compile(r'''
    ^
    \s*                                # OWS
    ;                                  # ";"
    \s*                                # OWS
    ([-0-9A-Za-z!#$%&'*+-.^_`|~]+)     # token
    \s*                                # BWS
    =                                  # "="
    \s*                                # BWS
    (?:
        ([-0-9A-Za-z!#$%&'*+.^_`|~]+)  # token
        |
        "(                             # quoted-string
            (?:
                [\t !#-[\]-~]          # qdtext
                |
                \\[\t -~\x80-\xff]     # quoted-pair
            )*
        )"
    )
''', re.X)

# rfc8187 ext_value
RE_EXT_VALUE = re.compile(r'''
    ^
    ([-0-9A-Za-z!#$%&+^_`{}~]+)        # charset
    '
    ([-0-9A-Za-z]+)                    # language
    '
    ((?:                               # value-chars
        %[0-9a-fA-F]{2}                # pct-encoded
        |
        [-0-9A-Za-z!#$&+.^_`|~]        # attr-char
    )*)
    $
''', re.X)

# trailing empty elements (rfc7230#7)
RE_TRAILING_COMMA = re.compile(r'''
    ^
    [\s,]*
    $
''', re.X)


def unescape(escaped_string):
    """
    Remove backslash escaping from quoted-pair as per rfc7230#3.2.6
    e.g. r"foo\\b\ar" => r"foo\bar"
    """

    result = StringIO()

    seen_backslash = False
    for char in escaped_string:
        if seen_backslash:
            result.write(char)
            seen_backslash = False
        elif char == '\\':
            seen_backslash = True
        else:
            result.write(char)
    if seen_backslash:
        raise ValueError('Trailing backslash')

    result.seek(0)
    return result.read()
