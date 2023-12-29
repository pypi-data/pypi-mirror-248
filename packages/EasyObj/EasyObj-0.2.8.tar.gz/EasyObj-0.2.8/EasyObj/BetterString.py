"""
isWellFormed
localeCompare
normalize
"""


from typing_extensions import SupportsIndex
from EasyObj.BetterList import BetterList
import re


class BetterString(str):

    @property
    def length(self):
        return len(self)

    def at(self, index=0):
        if index < 0:
            index += self.length
        return self[index]

    def charAt(self, index=0):
        if index >= self.length or index < 0:
            return ""
        return self[index]

    def charCodeAt(self, index=0):
        if index >= self.length or index < 0:
            return None
        return ord(self[index])

    def codePointAt(self, index=0):
        """
        Due to the fact that Python uses UTF-8 encoding, this method is the same as `BetterString.charCodeAt()`.
        """
        return self.charCodeAt(index)

    def concat(self, *args):
        return self + "".join(args)

    def endsWith(self, searchString, endPosition: str | None = None):
        if endPosition is None:
            endPosition = self.length

        if endPosition > self.length:
            endPosition = self.length

        return self[endPosition - len(searchString):endPosition] == searchString

    def fromCharCode(*charcodes: int):
        return BetterList(charcodes).map(lambda x: chr(x)).join("")

    def fromCodePoint(*charcodes: int):
        """
        Due to the fact that Python uses UTF-8 encoding, this method is the same as `BetterString.fromCharCode()`.
        """
        return BetterString.fromCharCode(*charcodes)

    def includes(self, searchString, position=0):
        return self.find(searchString, position) != -1

    def indexOf(self, searchString, position=0):
        return self.find(searchString, position)

    def lastIndexOf(self, searchString, position=0):
        return self.rfind(searchString, position)

    def match(self, regexp: str | re.Pattern):
        if isinstance(regexp, str):
            regexp = re.compile(regexp)

        return re.findall(regexp, self)

    def matchAll(self, regexp: str | re.Pattern):
        if isinstance(regexp, str):
            regexp = re.compile(regexp)

        res = BetterList(regexp.findall(self))
        if not isinstance(res[0], tuple):
            res = res.map(lambda x: BetterList([x,]))
        else:
            res = res.map(lambda x: BetterList(x))

        return res

    def padEnd(self, targetLength: int, padString: str = " "):
        return self + padString * (targetLength - self.length)

    def padStart(self, targetLength: int, padString: str = " "):
        return padString * (targetLength - self.length) + self

    def raw(string):
        return BetterString(repr(string)[1:-1])

    def repeat(self, count):
        if count < 0:
            raise ValueError("count cannot be negative")
        return self * count

    def replaceAll(self, pattern: str | re.Pattern, replacement):
        if isinstance(pattern, str):
            return super(BetterString, self).replace(pattern, replacement)
        elif isinstance(pattern, re.Pattern):
            return pattern.sub(replacement, self)

    def replace(self, pattern: str | re.Pattern, replacement):
        if isinstance(pattern, str):
            return super(BetterString, self).replace(pattern, replacement, 1)
        elif isinstance(pattern, re.Pattern):
            return pattern.sub(replacement, self, count=1)

    def search(self, regexp: str | re.Pattern):
        if isinstance(regexp, str):
            regexp = re.compile(regexp)

        return regexp.search(self).start()

    def slice(self, start, end=None):

        if start < 0:
            start += self.length

        if end is None:
            end = self.length

        if end < 0:
            end += self.length

        return BetterString(self[start:end])

    def split(self, seperator, limit=-1):
        if limit == -1:
            limit = self.length

        return BetterList(super(BetterString, self).split(seperator))[0:limit]

    def startswith(self, searchString, position=0):
        return self.find(searchString, position) == position

    def substring(self, indexStart, indexEnd=None):
        if indexEnd is None:
            indexEnd = self.length

        if indexStart < 0:
            indexStart = 0

        if indexEnd < 0:
            indexEnd = 0

        if indexStart > self.length:
            indexStart = self.length

        if indexEnd > self.length:
            indexEnd = self.length

        if indexStart > indexEnd:
            indexStart, indexEnd = indexEnd, indexStart

        return self[indexStart:indexEnd]

    def toLowerCase(self):
        return self.lower()

    def toUpperCase(self):
        return self.upper()

    def toString(self):
        return str(self)

    def trim(self):
        return self.strip()

    def trimEnd(self):
        return self.rstrip()

    def trimStart(self):
        return self.lstrip()

    def valueOf(self):
        return str(self)
