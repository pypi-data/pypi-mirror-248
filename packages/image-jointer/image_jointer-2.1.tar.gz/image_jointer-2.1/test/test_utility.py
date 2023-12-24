# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

import pytest
from pathlib import Path

from assert_image import assert_image

from image_jointer import PositionAlignment

IMAGE_FOLDER = Path("./test/image/")


@pytest.mark.parametrize(
    "alignment",
    (alignment for alignment in PositionAlignment),
)
def test_unify_image_size(alignment: PositionAlignment):
    from image_jointer import Blank, ImageJointer, JointAlignment, Utility
    from PIL import Image

    image_tuple = (
        Image.new("RGB", (30, 30), (255, 0, 0)),
        Image.new("RGB", (100, 50), (0, 255, 0)),
        Image.new("RGB", (50, 100), (0, 0, 255)),
        Blank(30, 30),
    )

    result_tuple = Utility.unify_image_size(alignment, *image_tuple)

    assert len(image_tuple) == len(result_tuple)

    jointed = ImageJointer()
    for result in result_tuple:
        assert result.width == 100
        assert result.height == 100
        jointed = jointed.joint(JointAlignment.RIGHT_CENTER, result)

    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "unify_image_size" / f"{alignment.name}_test.png")

    expected_image = Image.open(IMAGE_FOLDER / "unify_image_size" / f"{alignment.name}_expected.png")

    assert_image(joint_img, expected_image)
