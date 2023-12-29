<div align="center"><h1>EasyDict</h1></div>

<div align="center">

[English](https://github.com/Howardzhangdqs/EasyObj/blob/master/README.md) | [中文简体](https://github.com/Howardzhangdqs/EasyObj/blob/master/README_zh-CN.md)

</div>

`EasyObj` lets you manipulate objects as easily as in `JavaScript`.

## Installation

```bash
pip install easyobj
```

## Usage

### Better List

```python
from EasyObj import BetterList

betterlist = BetterList([1, 2, 3, 4, 5])
# betterlist: BetterList([1, 2, 3, 4, 5])

print(betterlist.length)
# 5

betterlist.append(6)
# betterlist: BetterList([1, 2, 3, 4, 5, 6])

print(betterlist.join(" "))
# '1 2 3 4 5 6'

print(betterlist.filter(lambda x: x >= 4))
# BetterList([4, 5, 6])

print(betterlist.concat(["a", "b", "c"]))
# BetterList([1, 2, 3, 4, 5, 6, 'a', 'b', 'c'])

print(betterlist.map(lambda x: x * 2))
# BetterList([2, 4, 6, 8, 10, 12])
```

And so on...

Most Methods are exactly the same as the Array object methods in JavaScript.

But since Python does not support using reserved words as method names, we have converted some method names:

| JavaScript | Python |
| :---: | :---: |
| `Array.prototype.with()` | `EasyObj.BetterList._with()` |
| `Array.from()` | `EasyObj.BetterList._from()` |

Please refer to the detailed documentation: [list.test.ipynb](https://github.com/Howardzhangdqs/EasyObj/blob/master/unittest/list.test.ipynb)


### Better Dict

Because it is difficult to implement many of the features of JavaScript's Object in Python, we only implemented a part of them.

Each `BetterDict` object will perform an operation similar to `EasyDict`, converting a normal dictionary into a nested `BetterDict` object.

```python
from EasyObj import BetterDict

betterdict = BetterDict({"very": "good"})
# betterdict: BetterDict({'very': 'good'})

betterdict.very
# 'good'
```

Due to Python syntax limitations, we cannot add new methods to the `BetterDict` class like in JavaScript, so we need to introduce another `DictUtils` class to implement some of the features in JavaScript

```python
from EasyObj import DictUtils

DictUtils.keys(betterdict)
# ['very']
```

`EasyObj` also implements the `Object.seal` and `Object.freeze` methods, which convert the `BetterDict` object into a `SealedBetterDict` and `FrozenBetterDict` object.

```python
sealedDict = DictUtils.seal(betterdict)
# sealedDict: SealedBetterDict({'very': 'good'})

sealedDict.very = "bad"
# sealedDict: SealedBetterDict({'very': 'bad'})

sealedDict.a = 1
# AttributeError: SealedDict object does not support assigning new attributes

frozenDict = DictUtils.freeze(betterdict)
# sealedDict: FrozenBetterDict({'very': 'good'})

sealedDict.very = "bad"
# AttributeError: SealedDict object does not support assigning new attributes

sealedDict.a = 1
# AttributeError: SealedDict object does not support assigning new attributes
```


Due to Python syntax limitations, we have converted some method names:

| JavaScript | Python |
| :---: | :---: |
| `Object` | `EasyObj.DictUtils` |
| `Object.prototype.isPrototypeOf()` | `EasyObj.DictUtils.isPrototypeOf()` |


Due to Python syntax limitations, the following methods cannot be implemented:

| Method name |
| :--: |
| `Object.defineProperty()` | 
| `Object.getOwnPropertyDescriptor()` |
| `Object.getOwnPropertyDescriptors()` |
| `Object.getPrototypeOf()` |
| `Object.isExtensible()` |
| `Object.preventExtensions()` |
| `Object.setPrototypeOf()` |
| `Object.prototype.hasOwnProperty()` |
| `Object.prototype.propertyIsEnumerable()` |
| `Object.prototype.toLocaleString()` |
| `Object.prototype.toString()` |
| `Object.prototype.valueOf()` |

Please refer to the detailed documentation: [dict.test.ipynb](https://github.com/Howardzhangdqs/EasyObj/blob/master/unittest/dict.test.ipynb)


### BetterString

Because many methods in JavaScript's String are not very useful (mainly difficult to implement), we have only implemented a portion of them.

Please refer to the detailed documentation: [string.test.ipynb](https://github.com/Howardzhangdqs/EasyObj/blob/master/unittest/string.test.ipynb)


## License

GPLv3