# BetterDict is the same as [EasyDict](https://github.com/makinacorpus/easydict/)
"""
The following methods are not implemented:
Object.defineProperty()
Object.getOwnPropertyDescriptor()
Object.getOwnPropertyDescriptors()
Object.getPrototypeOf()
Object.prototype.hasOwnProperty()
Object.isExtensible()
Object.preventExtensions()
Object.prototype.propertyIsEnumerable()
Object.setPrototypeOf()
Object.prototype.toLocaleString()
Object.prototype.toString()
Object.prototype.valueOf()
"""


from typing import Dict, List, Any
from EasyObj.BetterList import BetterList
from EasyObj.Symbol import Symbol


class BetterDict(dict):

    def __init__(self, d=None, **kwargs):

        if d is None:
            d = {}
        else:
            d = dict(d)

        if kwargs:
            d.update(**kwargs)

        for k, v in d.items():
            setattr(self, k, v)

        # Class attributes
        for k in self.__class__.__dict__.keys():
            if not (k.startswith('__') and k.endswith('__')) and not k in ('update', 'pop'):
                setattr(self, k, getattr(self, k))

    def __setattr__(self, name, value):

        if isinstance(value, (list, tuple)):
            value = [self.__class__(x)
                     if isinstance(x, dict) else x for x in value]
        elif isinstance(value, dict) and not isinstance(value, BetterDict):
            value = BetterDict(value)

        super(BetterDict, self).__setattr__(name, value)
        super(BetterDict, self).__setitem__(name, value)

    __setitem__ = __setattr__

    def update(self, e=None, **f):
        d = e or dict()
        d.update(f)
        for k in d:
            setattr(self, k, d[k])

    def pop(self, k, d=None):

        delattr(self, k)
        return super(BetterDict, self).pop(k, d)


class FrozenBetterDict(BetterDict):

    __frozen = False

    def __init__(self, d=None, **kwargs):

        super(FrozenBetterDict, self).__init__(d, **kwargs)

        self.__frozen = True

    def __setattr__(self, name, value):

        if self.__frozen == True:
            raise AttributeError(
                "FrozenDict object does not support attribute assignment")

        super(FrozenBetterDict, self).__setattr__(name, value)

    __setitem__ = __setattr__

    def __delattr__(self, key):
        raise AttributeError(
            "FrozenDict object does not support attribute deletion")


class SealedBetterDict(BetterDict):

    __sealed = False

    def __init__(self, d=None, **kwargs):

        super(SealedBetterDict, self).__init__(d, **kwargs)

        self.__sealed = True

    def __setattr__(self, name, value):

        if self.__sealed == True and DictUtils.hasOwn(self, name) == False:
            raise AttributeError(
                "SealedDict object does not support attribute assignment")

        super(SealedBetterDict, self).__setattr__(name, value)

    __setitem__ = __setattr__

    def __delattr__(self, key):
        raise AttributeError(
            "SealedDict object does not support attribute deletion")


DictLike = Dict | BetterDict | FrozenBetterDict | SealedBetterDict


class DictUtils:

    def assign(a: DictLike, *b):
        for c in b:
            for d in c:
                a[d] = c[d]
        return a

    def create(proto: DictLike, propertiesobject: DictLike):
        proto = BetterDict(proto)
        proto.update(propertiesobject)
        return proto

    def defineProperties(obj: DictLike, props):
        """
        Parameters
        - obj: The object on which to define or modify properties.
        - props: An object whose own enumerable string keyed properties define the properties to be defined or modified.

        Return value
            An object that has had its properties defined or modified.

        ```python
        OriginDict = BetterDict({"foo": 1})
        DictUtils.defineProperties(OriginDict, {"baz": 2})

        OriginDict # BetterDict({'foo': 1, 'baz': 2})
        """
        for prop in props:
            setattr(obj, prop, props[prop])
        return obj

    def entries(obj: DictLike):
        """
        Parameters
        - obj: An object.

        Return value
            An array of the given object's own enumerable string-keyed property key-value pairs. Each key-value pair is an array with two elements: the first element is the property key (which is always a string), and the second element is the property value.
        """

        return BetterList(obj.items())

    def freeze(obj: DictLike) -> FrozenBetterDict:
        """
        Parameters
            obj: The object to freeze.

        Return value
            The object that was passed to the function.
        """

        return FrozenBetterDict(obj)

    def keys(obj: DictLike):
        """
        Parameters
        - obj: An object.

        Return value
            An array of strings representing the given object's own enumerable string-keyed property keys.

        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/keys
        """
        return BetterList(obj.keys())

    def values(obj: DictLike):
        """
        Parameters
        - obj: An object.

        Return value
            An array containing the given object's own enumerable property values.

        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/values
        """
        return BetterList(obj.values())

    def fromEntries(iterable: List[List[Any]]):
        """
        Parameters
        - iterable: An iterable such as Array or Map or other objects implementing the iterable protocol.

        Return value
            A new object whose properties are given by the entries in the iterable.

        ```python
        DictUtils.fromEntries([
            ["foo", "bar"],
            ["baz", 42]
        ])
        # BetterDict({'foo': 'bar', 'baz': 42})
        ```

        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/fromEntries
        """

        return BetterDict(iterable)

    def getOwnPropertyNames(obj):
        """
        Due to the limitations of Python syntax, this method is exactly the same as `DictUtils.keys()`.

        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertyNames
        """

        return BetterList(obj.keys())

    def getOwnPropertySymbols(obj: BetterDict):
        """
        Parameters
        - obj: The object whose enumerable own property symbols are to be returned.

        Return value
            An array of symbolic property names.

        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertySymbols
        """

        return DictUtils.values(obj).filter(lambda x: isinstance(x, Symbol))

    def groupBy(items, callbackFn: callable):
        """
        Parameters
        - items: An iterable object.
        - callbackFn: A function that accepts up to three arguments. The groupBy method calls the callbackFn function one time for each element in the iterable.

        Return value
            A new object with the following properties:

            - A property for each unique return value of the callback function. Each property's value is an array of elements responsible for generating the return value.

        ```python
        inventory = [
            { "name": "asparagus", "type": "vegetables", "quantity": 5 },
            { "name": "bananas", "type": "fruit", "quantity": 0 },
            { "name": "goat", "type": "meat", "quantity": 23 },
            { "name": "cherries", "type": "fruit", "quantity": 5 },
            { "name": "fish", "type": "meat", "quantity": 22 },
        ]
        DictUtils.groupBy(inventory, lambda x: x["type"])
        '''
        {
            'vegetables': [
                { 'name': 'asparagus', 'type': 'vegetables', 'quantity': 5 }
            ],
            'fruit': [
                { 'name': 'bananas', 'type': 'fruit', 'quantity': 0 },
                { 'name': 'cherries', 'type': 'fruit', 'quantity': 5 }
            ],
            'meat': [
                { 'name': 'goat', 'type': 'meat', 'quantity': 23 },
                { 'name': 'fish', 'type': 'meat', 'quantity': 22 }
            ]
        }
        '''
        ```

        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/Reduce
        """

        result = BetterDict()
        for item in items:
            key = callbackFn(item)
            if key not in result:
                result[key] = []
            result[key].append(item)
        return result

    def hasOwn(obj, prop):
        """
        Parameters
        - obj: The object to test.
        - prop: The name of the property to test.

        Return value
            A Boolean indicating whether or not the object has the specified property as own property.

        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/hasOwn
        """

        return prop in obj.__dir__()

    def _is(obj1, obj2):
        """
        Parameters
        - obj1: The first object to compare.
        - obj2: The second object to compare.

        Return value
            A Boolean indicating whether or not the two arguments are the same object.

        ***Warning***: There might be some differences between this method and `Object.is()` in JavaScript. Please test it before you use it.

        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is
        """

        return obj1 is obj2

    def isFrozen(obj):
        """
        Parameters
        - obj: The object which should be checked.

        Return value
            A Boolean indicating whether or not the given object is frozen.

        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isFrozen
        """

        return isinstance(obj, FrozenBetterDict)

    def isPrototypeOf(obj1, obj2):
        """
        Parameters
        - obj1: The object whose prototype chain will be searched.
        - obj2: The object to be tested against each link in the prototype chain of obj1.

        Return value
            A Boolean indicating whether the calling object lies in the prototype chain of the specified object.

        ```python
        class Foo: pass
        class Bar(Foo): pass
        class Baz(Bar): pass
        DictUtils.isPrototypeOf(Foo, Baz) # True
        ```

        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isPrototypeOf
        """

        return issubclass(obj1, obj2)

    def seal(obj):
        """
        Parameters
        - obj: The object to seal.

        Return value
            The object that was passed to the function.

        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/seal
        """

        return SealedBetterDict(BetterDict(obj))

    def isSealed(obj):
        """
        Parameters
        - obj: The object which should be checked.

        Return value
            A Boolean indicating whether or not the given object is sealed.

        https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isSealed
        """

        return isinstance(obj, SealedBetterDict)
