# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from dataclasses import dataclass

from PIL import Image

from .figure import Figure
from .vector import Vector


@dataclass(frozen=True)
class _Part:
    source: Figure
    position: Vector = Vector()

    @property
    def width(self) -> int:
        return self.source.width

    @property
    def height(self) -> int:
        return self.source.height

    def paste(self, position: Vector):
        return _Part(self.source, self.position + position)

    def draw(self, output: Image.Image):
        self.source._draw(output, self.position)
