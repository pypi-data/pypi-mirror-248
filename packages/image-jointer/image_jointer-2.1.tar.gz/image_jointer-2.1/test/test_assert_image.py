# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE

import pytest
from PIL import Image

from assert_image import assert_image


@pytest.mark.parametrize(
    "test_image, is_same",
    (
        (Image.new("RGBA", (100, 100), (255, 0, 0)), True),
        (Image.new("RGBA", (100, 100), (255, 10, 0)), False),
        (Image.new("RGBA", (100, 101), (255, 0, 0)), False),
    ),
)
def test_assert_image(test_image: Image.Image, is_same: bool):
    expected = Image.new("RGBA", (100, 100), (255, 0, 0))

    assert_image(test_image, expected, is_same)
