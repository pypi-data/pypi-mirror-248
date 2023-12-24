# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from dataclasses import dataclass
from typing import Generator

from PIL import Image

from .figure import Figure
from .part import _Part
from .vector import Vector


@dataclass(frozen=True)
class ImageAdapter(Figure):
    image: Image.Image

    @property
    def width(self) -> int:
        return self.image.width

    @property
    def height(self) -> int:
        return self.image.height

    def _paste(self, position: Vector) -> Generator[_Part, None, None]:
        yield _Part(self, position)

    def _draw(self, output: Image.Image, position: Vector):
        output.paste(self.image, (position.x, position.y))
