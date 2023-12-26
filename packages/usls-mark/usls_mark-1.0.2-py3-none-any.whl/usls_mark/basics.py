from enum import Enum, auto


class Task(Enum):
    RECT = 0
    POINT = auto()
    POLYGON = auto()


class Mode(Enum):
    READ = 0
    MARK = auto()
    DOODLE = auto()
