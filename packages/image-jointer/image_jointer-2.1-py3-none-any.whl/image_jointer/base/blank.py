# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from PIL import Image

from .figure import Figure
from .vector import Vector


class Blank(Figure):
    def __init__(self, width: int, height: int) -> None:
        if not isinstance(width, int):
            pass
        if not isinstance(height, int):
            pass

        self.__width = width
        self.__height = height

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    def _paste(self, position: Vector):
        yield from []

    def _draw(self, output: Image.Image, position: Vector):
        pass
