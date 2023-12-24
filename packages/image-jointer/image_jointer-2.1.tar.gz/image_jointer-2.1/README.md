# ImageJointer

Build up image by jointing images

## install 
```
pip install image_jointer
```

## how to use

```python
    from image_jointer import JointAlignment, ImageJointer
    from PIL import Image

    red = Image.new("RGBA", (50, 50), (255, 0, 0))
    green = Image.new("RGBA", (100, 100), (0, 255, 0))
    blue = Image.new("RGBA", (50, 50), (0, 0, 255))

    jointed = ImageJointer().joint(JointAlignment.RIGHT_CENTER, red, green, blue)
    joint_img = jointed.to_image()
```

![example0](./doc/example0.png)

```python
    from image_jointer import JointAlign, ImageJointer, Blank
    from PIL import Image    

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blank = Blank(50, 100)
    green = Image.new("RGBA", (100, 100), (0, 255, 0))

    jointed = (
        ImageJointer(red)
        .joint(blank, JointAlign.RIGHT_CENTER)
        .joint(green, JointAlign.RIGHT_CENTER)
    )
    joint_img = jointed.to_image()
```
![example1](./doc/example1.png)

```python
    from image_jointer import JointAlignment, ImageJointer
    from PIL import Image

    red = Image.new("RGBA", (100, 100), (255, 0, 0))
    blue = Image.new("RGBA", (100, 200), (0, 0, 255))
    green = Image.new("RGBA", (100, 100), (0, 255, 0))

    jointed = ImageJointer(red).joint(JointAlignment.LEFT_BOTTOM, blue).joint(JointAlignment.DOWN_CENTER, green)
    joint_img = jointed.to_image()
```
![example2](./doc/example2.png)
