import copy
from typing import Callable, TypeVar

from roleft.Entities.RoleftKeyValue import KeyValue




T = TypeVar('T')
TOut = TypeVar('TOut')

def Add(lst: list[T], item: T):
    lst.append(item)
    
def AddRange(lst: list[T], others: list[T]):
    lst += others
    return lst

def RemoveAt(lst: list[T], index: int):
    del lst[index] # 【闻祖东 2023-07-26 102651】其实 self.__items.pop(index) 也可以
    
def Remove(lst: list[T], item: T):
    lst.remove(item)
    
def Exists(lst: list[T], predicate: Callable[[T], bool]) -> bool:
    for x in lst:
        if (predicate(x)):
            return True
        
    return False

def Count(lst: list[T]):
    return len(lst)
    
def Clear(lst: list[T]):
    lst = []
    
def FindAll(lst: list[T], predicate: Callable[[T], bool]):
    newList: list[T] = []
    for x in lst:
        if (predicate(x)):
            newList.append(x)
        
    return newList

def First(lst: list[T], predicate: Callable[[T], bool]):
    newItems = FindAll(lst, predicate)
    return newItems[0] if len(newItems) > 0 else None
    
def FirstIndex(lst: list[T], predicate: Callable[[T], bool]):
    index = 0
    for x in lst:
        if (predicate(x)):
            return index
        index += 1
    
    return -1

def ToList(lst: list[T]):
    return Select(lst, lambda x: x)
    
def ForEach(lst: list[T], predicate: Callable[[T], None]):
    for x in lst:
        predicate(x)

def Select(lst: list[T], predicate: Callable[[T], TOut]):
    newList = []
    for x in lst:
        temp = predicate(x)
        newList.append(temp)
    
    return newList

def OrderBy(lst: list[T], predicate: Callable[[T], str]):
    kts = Select(lst, lambda x: KeyValue(predicate(x), x))
    keys = Select(kts, lambda x: x.key).ToList()
    keys.sort()

    newList = list()
    newItems = copy.deepcopy(lst)
    for key in keys:
        index = FirstIndex(lst, lambda x: key == predicate(x))
        newList.append(newItems[index])
        RemoveAt(lst, index)
    
    return newList

def InsertAt(lst: list[T], item: T, index: int):
    lst.insert(index, item)

def RemoveAll(lst: list[T], predicate: Callable[[T], bool]):
    indexes = list[int]()
    index = 0
    for item in lst:
        if (predicate(item)):
            indexes.append(index)
        index += 1
    
    indexes.reverse()
    for idx in indexes:
        RemoveAt(lst, idx)

# def Print(self):
#     print(self.__items)