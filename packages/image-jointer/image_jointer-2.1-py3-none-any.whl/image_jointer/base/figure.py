# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from __future__ import annotations

from abc import ABC, abstractproperty, abstractmethod
from typing import TYPE_CHECKING, Generator

from PIL import Image

from .vector import Vector

if TYPE_CHECKING:
    from .part import _Part


class Figure(ABC):
    @abstractproperty
    def width(self) -> int:
        ...

    @abstractproperty
    def height(self) -> int:
        ...

    @abstractmethod
    def _paste(self, position: Vector) -> Generator[_Part, None, None]:
        ...

    @abstractmethod
    def _draw(self, output: Image.Image, position: Vector):
        ...
