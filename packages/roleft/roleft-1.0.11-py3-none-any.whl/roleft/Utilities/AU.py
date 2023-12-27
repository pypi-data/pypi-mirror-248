import hashlib
from enum import Enum, unique
from typing_extensions import TypedDict
from typing import NewType

InputCate = Enum('InputCate222', ('String', "File"))
AlgorithmCate = Enum('AlgorithmCate', ('Md5', "Sha1", "Sha256"))

_algoDic = {
    AlgorithmCate.Md5: hashlib.md5,
    AlgorithmCate.Sha1: hashlib.sha1,
    AlgorithmCate.Sha256: hashlib.sha256,
}


def _loadContent(cate: InputCate, input: str) -> bytes:
    if cate == InputCate.File:
        with open(input, "rb") as file:
            return file.read()
    elif cate == InputCate.String:
        return input.encode()
    else:
        raise f'未定义的输入类型 - {cate}'


def Calc(algoCate: AlgorithmCate, inputCate: InputCate, input: str) -> str:
    func = _algoDic[algoCate]
    return func(_loadContent(inputCate, input)).hexdigest()

def Md5Str(input: str) -> str:
    return Calc(AlgorithmCate.Md5, InputCate.String, input)


def Md5File(path: str) -> str:
    return Calc(AlgorithmCate.Md5, InputCate.File, path)


def Sha1Str(input: str) -> str:
    return Calc(AlgorithmCate.Sha1, InputCate.String, input)


def Sha1File(path: str) -> str:
    return Calc(AlgorithmCate.Sha1, InputCate.File, path)


def Sha256Str(input: str) -> str:
    return Calc(AlgorithmCate.Sha256, InputCate.String, input)


def Sha256File(path: str) -> str:
    return Calc(AlgorithmCate.Sha256, InputCate.File, path)

