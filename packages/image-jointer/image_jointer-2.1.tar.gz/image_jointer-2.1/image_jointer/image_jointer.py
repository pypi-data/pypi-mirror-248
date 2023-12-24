# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from __future__ import annotations

from PIL import Image

from .base.blank import Blank
from .base.enums import JointAlignment
from .base.figure import Figure
from .base.adapter import ImageAdapter
from .base.part import _Part
from .base.vector import Vector


class ImageJointer(Figure):
    __parts: tuple[_Part, ...]

    def __init__(self, source: Image.Image | Figure | None = None) -> None:
        """
        Building up image by jointing images.
        Building image will be postponed until execute to_image.
        Method chainable.

        Args:
            source (Image.Image | Figure | None): source of building up. default to None

        Raises:
            ValueError: raise if source is invalid type
        """
        match source:
            case Image.Image():
                source = ImageAdapter(source)

        match source:
            case ImageJointer():
                self.__parts = source.__parts
                self.__width = source.width
                self.__height = source.height
            case None:
                self.__parts = tuple()
                self.__width = 0
                self.__height = 0
            case _:
                self.__parts = (_Part(source),)
                self.__width = source.width
                self.__height = source.height

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    def _paste(self, position: Vector):
        for part in self.__parts:
            yield part.paste(position)

    def _draw(self, output: Image.Image, position: Vector):
        for part in self.__parts:
            part.draw(output)

    def __calc_paste_pos(self, alignment: JointAlignment, paste_image: Figure) -> Vector:
        """
        Calculate paste position.
        origin is left top corner of self.
        width is x direction (to right). height is y direction (to down).
        paste position is always x>=0 and y>= 0. it means self width(height) is never smaller than paste_image.
        only consider jointing at right or down direction.
        """
        match alignment:
            case JointAlignment.RIGHT_TOP:
                return Vector(self.width, 0)
            case JointAlignment.RIGHT_CENTER:
                return Vector(self.width, (self.height - paste_image.height) // 2)
            case JointAlignment.RIGHT_BOTTOM:
                return Vector(self.width, self.height - paste_image.height)

            case JointAlignment.DOWN_LEFT:
                return Vector(0, self.height)
            case JointAlignment.DOWN_CENTER:
                return Vector((self.width - paste_image.width) // 2, self.height)
            case JointAlignment.DOWN_RIGHT:
                return Vector(self.width - paste_image.width, self.height)

            case _:
                raise ValueError("alignment is invalid")

    def __run_joint(self, image: Figure, paste_to: Vector):
        yield from self.__parts
        yield from image._paste(paste_to)

    def __joint_single(self, alignment: JointAlignment, image: Image.Image | Figure) -> ImageJointer:
        """
        Joint image.
        There are no side effect.

        Args:
            alignment (JointAlignment): how to align image

            image (Image.Image | Figure): image to joint

        Returns:
            ImageJointer: New instance of jointed image. Method chainable.
        """
        if not isinstance(image, (Image.Image, Figure)):
            raise ValueError("Image is invalid type")
        if not isinstance(alignment, JointAlignment):
            raise ValueError("alignment is invalid type")

        # apply adapter
        match image:
            case Image.Image():
                image = ImageAdapter(image)

        # only consider jointing at right or down direction.
        # if not, swap self and image for changing direction.
        match alignment:
            case JointAlignment.UP_LEFT:
                return ImageJointer(image).__joint_single(JointAlignment.DOWN_LEFT, self)
            case JointAlignment.UP_CENTER:
                return ImageJointer(image).__joint_single(JointAlignment.DOWN_CENTER, self)
            case JointAlignment.UP_RIGHT:
                return ImageJointer(image).__joint_single(JointAlignment.DOWN_RIGHT, self)

            case JointAlignment.LEFT_TOP:
                return ImageJointer(image).__joint_single(JointAlignment.RIGHT_TOP, self)
            case JointAlignment.LEFT_CENTER:
                return ImageJointer(image).__joint_single(JointAlignment.RIGHT_CENTER, self)
            case JointAlignment.LEFT_BOTTOM:
                return ImageJointer(image).__joint_single(JointAlignment.RIGHT_BOTTOM, self)

        # only consider jointing image to larger or equal size base_image.
        # if not, extend base_image size at first.
        match alignment:
            case JointAlignment.RIGHT_TOP | JointAlignment.RIGHT_CENTER | JointAlignment.RIGHT_BOTTOM:
                if self.height >= image.height:
                    base_image = self
                else:
                    base_image = ImageJointer(Blank(0, image.height)).__joint_single(alignment, self)
            case JointAlignment.DOWN_LEFT | JointAlignment.DOWN_CENTER | JointAlignment.DOWN_RIGHT:
                if self.width >= image.width:
                    base_image = self
                else:
                    base_image = ImageJointer(Blank(image.width, 0)).__joint_single(alignment, self)

        paste_to = base_image.__calc_paste_pos(alignment, image)

        # make output
        output = ImageJointer()
        output.__parts = tuple(base_image.__run_joint(image, paste_to))
        output.__width = max(base_image.width, image.width + paste_to.x)
        output.__height = max(base_image.height, image.height + paste_to.y)

        return output

    def joint(
        self,
        alignment: JointAlignment,
        *images: Image.Image | Figure,
    ) -> ImageJointer:
        """
        Joint new images to right side or bottom repeatedly.
        There are no side effect.

        Args:
            alignment (JointAlignment): how to align image

            *images (Image.Image | Figure): images to joint

        Returns:
            ImageJointer: New instance of jointed image. Method chainable.
        """
        jointed = self
        for element in images:
            jointed = jointed.__joint_single(alignment, element)
        return jointed

    def to_image(self):
        """
        Make Image.

        Returns:
            Image.Image: image
        """
        output = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        for part in self.__parts:
            part.draw(output)
        return output
