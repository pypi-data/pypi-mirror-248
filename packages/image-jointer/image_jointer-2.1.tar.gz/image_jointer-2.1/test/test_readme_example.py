# Copyright (c) 2023 Nanahuse
# This software is released under the MIT License
# https://github.com/Nanahuse/ImageJointer/blob/main/LICENSE


def test_example0():
    from image_jointer import JointAlignment, ImageJointer
    from PIL import Image

    red = Image.new("RGBA", (50, 50), (255, 0, 0))
    green = Image.new("RGBA", (100, 100), (0, 255, 0))
    blue = Image.new("RGBA", (50, 50), (0, 0, 255))

    jointed = ImageJointer().joint(JointAlignment.RIGHT_CENTER, red, green, blue)
    joint_img = jointed.to_image()

    # -------------------------------------------
    joint_img.save("./doc/example0.png")


def test_example1():
    from image_jointer import JointAlignment, ImageJointer, Blank
    from PIL import Image

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blank = Blank(50, 100)
    green = Image.new("RGBA", (100, 100), (0, 255, 0))

    jointed = ImageJointer().joint(JointAlignment.RIGHT_CENTER, red, blank, green)
    joint_img = jointed.to_image()

    # -------------------------------------------
    joint_img.save("./doc/example1.png")


def test_example2():
    from image_jointer import JointAlignment, ImageJointer
    from PIL import Image

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (100, 200), (0, 0, 255))
    green = Image.new("RGBA", (100, 100), (0, 255, 0))

    jointed = ImageJointer(red).joint(JointAlignment.LEFT_BOTTOM, blue).joint(JointAlignment.DOWN_CENTER, green)
    joint_img = jointed.to_image()

    # -------------------------------------------
    joint_img.save("./doc/example2.png")
