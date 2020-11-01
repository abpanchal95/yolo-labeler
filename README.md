# Automatic YOLO Labeler

[![Downloads](https://pepy.tech/badge/yolo-labeler)](https://pepy.tech/project/yolo-labeler)
[![Downloads](https://pepy.tech/badge/yolo-labeler/month)](https://pepy.tech/project/yolo-labeler/month)
[![Downloads](https://pepy.tech/badge/yolo-labeler/week)](https://pepy.tech/project/yolo-labeler/week)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://img.shields.io/badge/License-MIT-blue.svg)

#### Note: This tool is using U-2-Net model for background removal. So it is preferred to use single point focused images as input.

YOLO Labeler is a tool to remove images background and label object in YOLO format.

<p style="display: flex;align-items: center;justify-content: center;">
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/1.jpg" width="250" />
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/1_.png" width="250" />
  <source src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/1_.png" width="250" type="text"/>
  <div class="textcontent">
    <div class="text"> 0 0.513942 0.407692 0.272115 0.746795 </div>
  </div>
</p>

<p style="display: flex;align-items: center;justify-content: center;"> 
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/2.jpg" width="250" />
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/2_.png" width="250" />
</p>

<p style="display: flex;align-items: center;justify-content: center;">  
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/3.jpg" width="250" />
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/3_.png" width="250" />
</p>

<p style="display: flex;align-items: center;justify-content: center;">  
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/4.jpg" width="250" />
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/4_.png" width="250" />
</p>

<p style="display: flex;align-items: center;justify-content: center;">  
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/5.jpg" width="250" />
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/5_.png" width="250" />
</p>

### Installation

```bash
    pip install yolo-labeler
```

### Usage as a cli

Remove the background from a remote image
```bash
    curl -s http://input.png | rembg > output.png
```

Remove the background from a local file
```bash
    rembg -o path/to/output.png path/to/input.png
```

Remove the background from all images in a folder
```bash
    rembg -p path/to/inputs
```

### Usage as a library

In `app.py`

```python
    import sys
    from rembg.bg import remove

    sys.stdout.buffer.write(remove(sys.stdin.buffer.read()))
```

Then run
```
    cat input.png | python app.py > out.png
```

### Advance usage

Sometimes it is possible to achieve better results by turning on alpha matting. Example:
```bash
    curl -s http://input.png | rembg -a -ae 15 > output.png
```

<table>
    <thead>
        <tr>
            <td>Original</td>
            <td>Without alpha matting</td>
            <td>With alpha matting (-a -ae 15)</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><img src="https://raw.githubusercontent.com/danielgatis/rembg/master/examples/food-1.jpg"/></td>
            <td><img src="https://raw.githubusercontent.com/danielgatis/rembg/master/examples/food-1.out.jpg"/></td>
            <td><img src="https://raw.githubusercontent.com/danielgatis/rembg/master/examples/food-1.out.alpha.jpg"/></td>
        </tr>
    </tbody>
</table>

### References

- https://github.com/NathanUA/U-2-Net

### License

Copyright (c) 2020-present [Daniel Gatis](https://github.com/danielgatis)

Licensed under [MIT License](./LICENSE.txt)
