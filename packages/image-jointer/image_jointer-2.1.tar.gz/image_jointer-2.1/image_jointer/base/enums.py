# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from enum import Enum, auto


class JointAlignment(Enum):
    """
    How to joint new image to base image.

    XXX_YYY
    -> XXX: joint direction
       YYY: alignment line
    """

    UP_LEFT = auto()
    UP_CENTER = auto()
    UP_RIGHT = auto()

    DOWN_LEFT = auto()
    DOWN_CENTER = auto()
    DOWN_RIGHT = auto()

    LEFT_TOP = auto()
    LEFT_CENTER = auto()
    LEFT_BOTTOM = auto()

    RIGHT_TOP = auto()
    RIGHT_CENTER = auto()
    RIGHT_BOTTOM = auto()


class PositionAlignment(Enum):
    """
    Aliment position in a bounding.
    """

    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()

    CENTER_LEFT = auto()
    CENTER_CENTER = auto()
    CENTER_RIGHT = auto()

    BOTTOM_LEFT = auto()
    BOTTOM_CENTER = auto()
    BOTTOM_RIGHT = auto()
