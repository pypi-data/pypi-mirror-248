import math
import pathlib
import random
import time

from roleft.Enumerable.RoleftDateTime import xDateTime

_strSrc = "2345678abcdefghjkmnprstuvwxyzABCDEFGHJKMNPRSTUVWXYZ"


def GenRandom(min=0,  max=10) -> int:
    return random.randrange(min, max)


def GetRandomStr(length=16) -> str:
    return ''.join(random.sample(_strSrc, length))


def HasValue(items: list) -> bool:
    return len(items) > 0


def CheckIfBetween(src: int, min: int, max: int) -> bool:
    return src > min and src < max


def ReadAllText(path: str) -> str:
    fo = open(path, "r")
    content = fo.read()
    fo.close()
    return content


def Save2File(content: str, path: str) -> None:
    file = open(path, 'w')
    file.write(content)
    file.close()


def SureDir(dirPath: str) -> None:
    path = pathlib.Path(dirPath)
    if not path.exists():
        path.mkdir(511, True)


def RandomBool() -> bool:
    return bool(GenRandom(0, 2))


def RandomDateTime() -> xDateTime:
    ticks = GenRandom(0, 17280000000)
    tm = time.localtime(ticks)
    return xDateTime(tm)


_step = 1024
_kvps = {
    "B": math.pow(_step, 1),
    "KB": math.pow(_step, 2),
    "MB": math.pow(_step, 3),
    "GB": math.pow(_step, 4),
    "TB": math.pow(_step, 5),
}


def GenSizeDesc(length: int) -> str:
    showNum = float(length)

    currKey = ''
    for key, value in _kvps.items():
        currKey = key
        if showNum < _step:
            break

        showNum = length / value

    return f"{round(showNum, 2)}{currKey}"
