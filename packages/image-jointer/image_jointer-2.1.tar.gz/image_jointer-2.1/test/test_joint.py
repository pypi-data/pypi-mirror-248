# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

import pytest
from pathlib import Path

from assert_image import assert_image

from image_jointer import JointAlignment


IMAGE_FOLDER = Path("./test/image/")


def test_vector():
    from image_jointer import Vector

    assert Vector(5, 5) + Vector(6, 6) == Vector(11, 11)


@pytest.mark.parametrize(
    "alignment",
    (alignment for alignment in JointAlignment),
)
def test_joint_alignment(alignment: JointAlignment):
    from image_jointer import ImageJointer
    from PIL import Image

    test_name = alignment.name

    red = Image.new("RGBA", (50, 50), (255, 0, 0))
    green = Image.new("RGBA", (100, 100), (0, 255, 0))
    blue = Image.new("RGBA", (50, 50), (0, 0, 255))

    jointed = ImageJointer(red).joint(alignment, green).joint(alignment, blue)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "joint" / f"{test_name}_test.png")

    expected_image = Image.open(IMAGE_FOLDER / "joint" / f"{test_name}_expected.png")

    assert_image(joint_img, expected_image)


def test_joint_nest():
    from image_jointer import JointAlignment, ImageJointer
    from PIL import Image

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    green = Image.new("RGBA", (100, 100), (0, 255, 0))
    blue = Image.new("RGBA", (100, 100), (0, 0, 255))

    nest0 = (
        ImageJointer(red)
        .joint(JointAlignment.RIGHT_CENTER, green)
        .joint(JointAlignment.DOWN_LEFT, ImageJointer(blue).joint(JointAlignment.RIGHT_CENTER, blue))
    )
    nest0_image = nest0.to_image()
    nest0_image.save(IMAGE_FOLDER / "nest" / "Nest_test.png")

    nest1 = (
        ImageJointer()
        .joint(JointAlignment.RIGHT_CENTER, ImageJointer(red).joint(JointAlignment.DOWN_CENTER, blue))
        .joint(JointAlignment.RIGHT_CENTER, ImageJointer(green).joint(JointAlignment.DOWN_CENTER, blue))
    )
    nest1_image = nest1.to_image()

    expected_image = Image.open(IMAGE_FOLDER / "nest" / "Nest_expected.png")

    assert_image(nest0_image, nest1_image)
    assert_image(nest0_image, expected_image)


def test_joint_multiple_input():
    from image_jointer import JointAlignment, ImageJointer
    from PIL import Image

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    green = Image.new("RGBA", (100, 100), (0, 255, 0))
    blue = Image.new("RGBA", (100, 100), (0, 0, 255))

    multiple = ImageJointer().joint(JointAlignment.RIGHT_CENTER, red, green, blue)
    multiple_image = multiple.to_image()
    multiple_image.save(IMAGE_FOLDER / "multiple" / "MultipleInput_test.png")

    expected_image = Image.open(IMAGE_FOLDER / "multiple" / "MultipleInput_expected.png")

    assert_image(multiple_image, expected_image)


def test_blank():
    from image_jointer import JointAlignment, ImageJointer, Blank
    from PIL import Image

    red = Image.new("RGB", (100, 100), (255, 0, 0))
    blank = Blank(50, 100)
    green = Image.new("RGB", (100, 100), (0, 255, 0))

    jointed = ImageJointer().joint(JointAlignment.RIGHT_CENTER, red, blank, green)
    joint_img = jointed.to_image()
    joint_img.save(IMAGE_FOLDER / "blank" / "Blank.png")

    expected_image = Image.open(IMAGE_FOLDER / "blank" / "Blank.png")

    assert_image(joint_img, expected_image)
