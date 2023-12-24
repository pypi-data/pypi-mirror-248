import copy
import functools


class EmptyListItem:
    def __init__(self) -> None:
        pass


class BetterList(list):

    def at(self, index):
        return self[index]

    @property
    def length(self) -> int:
        return len(self)

    def map(self, func: callable):
        return BetterList(map(func, self))

    def filter(self, func: callable):
        return BetterList(filter(func, self))

    def forEach(self, func: callable, noIndex=False):
        """
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/forEach
        """
        if noIndex:
            for val in self:
                func(val)
        else:
            for index, val in enumerate(self):
                func(val, index)

    def deepClone(self):
        """
        https://lodash.com/docs/#cloneDeep
        """
        return copy.deepcopy(self)

    def reverse(self):
        self[:] = self[::-1]
        return BetterList(self)

    def toReversed(self):
        """
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toReversed
        """
        return BetterList(self[::-1])

    def concat(self, other):
        return BetterList(self + other)

    def reduce(self, func: callable, init=None):

        def reduce(func, iterable, init=None):
            iterator = iter(iterable)
            if init is None:
                try:
                    init = next(iterator)
                except StopIteration:
                    raise TypeError(
                        'reduce() of empty sequence with no initial value')
            accum_value = init
            for x in iterator:
                accum_value = func(accum_value, x)
            return accum_value

        if init is None:
            return reduce(func, self)
        else:
            return reduce(func, self, init)

    def reduceRight(self, func: callable, init=None):

        def reduce(func, iterable, init=None):
            iterator = iter(reversed(iterable))
            if init is None:
                try:
                    init = next(iterator)
                except StopIteration:
                    raise TypeError(
                        'reduce() of empty sequence with no initial value')
            accum_value = init
            for x in iterator:
                accum_value = func(accum_value, x)
            return accum_value

        if init is None:
            return reduce(func, self)
        else:
            return reduce(func, self, init)

    def find(self, func: callable):
        for val in self:
            if func(val):
                return val
        return None

    def findIndex(self, func: callable):
        for index, val in enumerate(self):
            if func(val):
                return index
        return -1

    def findLast(self, func: callable):
        for val in reversed(self):
            if func(val):
                return val
        return None

    def findLastIndex(self, func: callable):
        for index, val in reversed(list(enumerate(self))):
            if func(val):
                return index
        return -1

    def every(self, func):
        for val in self:
            if not func(val):
                return False
        return True

    def flat(self, depth=1):

        def flat(iterable, depth):
            for elem in iterable:
                if isinstance(elem, list) and depth > 0:
                    yield from flat(elem, depth - 1)
                else:
                    yield elem

        return BetterList(flat(self, depth))

    def fill(self, value: int, start: int = 0, end: int | None = None):
        if end is None:
            end = len(self)
        for i in range(start, end):
            self[i] = value

    def copyWithin(self, target: int, start: int | None = None, end: int | None = None):
        """
        Copies a sequence of elements within the list.
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/copyWithin
        """
        length = self.length
        _ = copy.deepcopy(self)
        if start is None:
            start = 0
        if end is None:
            end = self.length

        self[target:target + min(end, self.length) -
             start] = self[start:min(end, self.length)]

        if self.length > length:
            for i in range(length, self.length):
                del self[i]

        if self.length < length:
            for i in range(self.length, length):
                self.append(_[i])

        return self

    def entries(self):
        """
        Returns an iterable of key, value pairs for every entry in the list
        ```
        BetterList(['a', 'b', 'c']).entries() # [(0, 'a'), (1, 'b'), (2, 'c')]
        ```
        """
        return BetterList(enumerate(self))

    def flatMap(self, func: callable):
        """
        Returns a new list formed by applying a given callback function to each element of the list, and then flattening the result by one level.
        ```
        BetterList([1, 2, 3, 4]).flatMap(lambda x: [x, x * 2]) # [1, 2, 2, 4, 3, 6, 4, 8]
        ```
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/flatMap
        """
        return self.map(func).flat()

    def _from(iterable, func: callable = None):
        """
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from
        """
        if func == None:
            return BetterList(iterable)
        else:
            return BetterList(iterable).map(callable)

    def includes(self, searchelement, fromIndex: int = 0):
        """
        Returns a boolean indicating whether an element in the array equals the specified element, using the same algorithm as Array.prototype.includes().
        ```
        BetterList([1, 2, 3]).includes(2) # true
        ```
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/includes
        """
        return searchelement in self[fromIndex:]

    def indexOf(self, searchElement, fromIndex: int = 0):
        """
        Returns the first index at which a given element can be found in the array, or -1 if it is not present.
        ```
        BetterList([1, 2, 3]).indexOf(2) # 1
        ```
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/indexOf
        """
        if fromIndex < 0:
            fromIndex = fromIndex + self.length

        try:
            return self[fromIndex:].index(searchElement) + fromIndex
        except ValueError:
            return -1

    def isArray(arr):
        """
        Returns true if an object is an array, false if it is not.
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/isArray
        """
        if arr.__class__ == BetterList or arr.__class__ == list:
            return True
        else:
            return False

    def join(self, seperator: str = ","):
        """
        Joins all elements of an array into a string.
        ```
        BetterList(['a', 'b', 'c']).join() # 'a,b,c'
        ```
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/join
        """
        return str(seperator).join(self.map(str))

    def keys(self):
        """
        Returns a new Array Iterator object that contains the keys for each index in the array.
        ```
        BetterList(['a', 'b', 'c']).keys() # [0, 1, 2]
        ```
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/keys
        """
        return BetterList(range(self.length))

    def lastIndexOf(self, searchElement, fromIndex: int = None):
        """
        Returns the last index at which a given element can be found in the array, or -1 if it is not present. The array is searched backwards, starting at fromIndex.
        ```
        BetterList([1, 2, 3, 4, 5, 6, 7, 8, 9, 2]).lastIndexOf(2) # 9
        ```
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/lastIndexOf
        """

        if fromIndex is None:
            fromIndex = self.length - 1

        if fromIndex < 0:
            fromIndex = fromIndex + self.length

        if fromIndex >= self.length:
            fromIndex = self.length - 1

        try:
            for i in range(fromIndex, -1, -1):
                if self[i] == searchElement:
                    return i
        except:
            pass

        return -1

    def of(*arguments):
        """
        Creates a new Array instance from a variable number of arguments, regardless of number or type of the arguments.
        ```
        BetterList.of(1, 2, 3)
        ```
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/of
        """
        return BetterList(arguments)

    def pop(self):
        """
        Removes the last element from an array and returns that element.
        ```
        arr = [1, 2, 3]
        BetterList(arr).pop() # 3
        arr # [1, 2]
        ```
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/pop
        """

        if self.length == 0:
            return None

        last = self[-1]
        del self[-1]
        return last

    def push(self, *args):
        """
        Adds one or more elements to the end of an array and returns the new length of the array.
        ```
        arr = [1, 2, 3]
        BetterList(arr).push(4, 5) # 5
        arr
        ```
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/push
        """
        for arg in args:
            self.append(arg)
        return self.length

    def shift(self):
        """
        Removes the first element from an array and returns that removed element. This method changes the length of the array.
        ```
        arr = [1, 2, 3]
        BetterList(arr).shift() # 1
        arr # [2, 3]
        ```
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/shift
        """
        if self.length == 0:
            return None

        first = self[0]
        del self[0]
        return first

    def slice(self, start: int = 0, end: int | None = None):
        """
        Returns a shallow copy of a portion of an array into a new array object selected from begin to end (end not included). The original array will not be modified.
        ```
        BetterList([1, 2, 3, 4, 5]).slice(2, 4) # [3, 4]
        ```
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/slice
        """
        if start < 0:
            start += self.length

        if end is None:
            end = self.length

        if end < 0:
            end += self.length

        return BetterList(self[start:end])

    def some(self, func: callable):
        """
        Returns true if at least one element in this array satisfies the provided testing function.
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/some
        """
        for i in self:
            if func(i):
                return True
        return False

    def sort(self, compareFn: callable = None):
        """
        Sorts the elements of an array in place and returns the sorted array.
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
        """
        if compareFn is None:
            self[:] = BetterList(sorted(self))
        else:
            self[:] = BetterList(
                sorted(self, key=functools.cmp_to_key(compareFn)))
        return self

    def splice(self, start: int = None, deleteCount: int | None = None, *items):
        """
        Changes the contents of an array by removing or replacing existing elements and/or adding new elements in place.
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/splice
        """
        if start is None:
            return BetterList([])

        if start < 0:
            start += self.length

        if deleteCount is None:
            deleteCount = self.length - start

        if deleteCount < 0:
            deleteCount = 0

        if deleteCount > self.length - start:
            deleteCount = self.length - start

        if deleteCount == 0 and len(items) == 0:
            return BetterList([])

        deleted = BetterList(self[start:start + deleteCount])
        self[start:start + deleteCount] = items
        return deleted

    def toSorted(self, compareFn: callable = None):
        """
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSorted
        """
        if compareFn is None:
            return BetterList(sorted(self.deepClone()))
        else:
            return BetterList(
                sorted(self.deepClone(), key=functools.cmp_to_key(compareFn)))

    def toSpliced(self, *args):
        """
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSpliced
        """
        t = self.deepClone()
        t.splice(*args)
        return t

    def toString(self):
        """
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toString
        """
        return self.join()

    def unshift(self, *args):
        for arg in BetterList(args).reverse():
            self.insert(0, arg)
        return self.length

    def values(self):
        return iter(self)

    def _with(self, index: int, val):
        """
        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/with
        """
        t = self.deepClone()
        t[index] = val
        return t
