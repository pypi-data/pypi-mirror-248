# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

from __future__ import annotations

from PIL import Image

from .base.blank import Blank
from .base.enums import JointAlignment, PositionAlignment
from .base.figure import Figure
from .image_jointer import ImageJointer


class Utility(object):
    def __init__(
        self,
    ):
        raise NotImplementedError("Cannot construct")

    @staticmethod
    def unify_image_size(align: PositionAlignment, *images: Image.Image | Figure):
        """
        All image will be unified to maximum width and heigh.
        Add transparent padding if image width (height) is smaller then maximum width (height).

        Args:
            align (PositionAlignment): how to add transparent padding
            *images (Image.Image | Figure): images to joint

        Returns:
            tuple[ImageJointer]: tuple of adjusted image
        """
        width = max(element.width for element in images)
        height = max(element.height for element in images)

        match align:
            case PositionAlignment.TOP_LEFT:
                height_align = JointAlignment.RIGHT_TOP
                width_align = JointAlignment.DOWN_LEFT
            case PositionAlignment.TOP_CENTER:
                height_align = JointAlignment.RIGHT_TOP
                width_align = JointAlignment.DOWN_CENTER
            case PositionAlignment.TOP_RIGHT:
                height_align = JointAlignment.RIGHT_TOP
                width_align = JointAlignment.DOWN_RIGHT
            case PositionAlignment.CENTER_LEFT:
                height_align = JointAlignment.RIGHT_CENTER
                width_align = JointAlignment.DOWN_LEFT
            case PositionAlignment.CENTER_CENTER:
                height_align = JointAlignment.RIGHT_CENTER
                width_align = JointAlignment.DOWN_CENTER
            case PositionAlignment.CENTER_RIGHT:
                height_align = JointAlignment.RIGHT_CENTER
                width_align = JointAlignment.DOWN_RIGHT
            case PositionAlignment.BOTTOM_LEFT:
                height_align = JointAlignment.RIGHT_BOTTOM
                width_align = JointAlignment.DOWN_LEFT
            case PositionAlignment.BOTTOM_CENTER:
                height_align = JointAlignment.RIGHT_BOTTOM
                width_align = JointAlignment.DOWN_CENTER
            case PositionAlignment.BOTTOM_RIGHT:
                height_align = JointAlignment.RIGHT_BOTTOM
                width_align = JointAlignment.DOWN_RIGHT

        return tuple(
            ImageJointer(Blank(0, height)).joint(height_align, element).joint(width_align, Blank(width, 0))
            for element in images
        )
