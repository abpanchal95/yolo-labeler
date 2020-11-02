# Automatic YOLO Labeler

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://img.shields.io/badge/License-MIT-blue.svg)

#### Note: Tool works for single object per image only. Please use images with single object for accurate results. You can verify labels by checking png images. If the background is correctly removed from image then it is labelled correctly.

YOLO Labeler is a tool to remove images background and label object in YOLO format.

### Examples
<p style="display: flex;align-items: center;justify-content: center;">
  <img src="https://raw.githubusercontent.com/abpanchal95/yolo-labeler/master/examples/1.jpg" width="400" />
  <img src="https://raw.githubusercontent.com/abpanchal95/yolo-labeler/master/examples/1_.png" width="400" />
  <div class="textcontent">
    <div class="text"><b> YOLO String: 0 0.513942 0.407692 0.272115 0.746795 </b></div>
  </div>
</p>

<p style="display: flex;align-items: center;justify-content: center;"> 
  <img src="https://raw.githubusercontent.com/abpanchal95/yolo-labeler/master/examples/2.jpg" width="400" />
  <img src="https://raw.githubusercontent.com/abpanchal95/yolo-labeler/master/examples/2_.png" width="400" />
  <div class="textcontent">
    <div class="text"><b> YOLO String: 0 0.287500 0.580769 0.575000 0.837821 </b></div>
  </div>  
</p>

<p style="display: flex;align-items: center;justify-content: center;">  
  <img src="https://raw.githubusercontent.com/abpanchal95/yolo-labeler/master/examples/3.jpg" width="400" />
  <img src="https://raw.githubusercontent.com/abpanchal95/yolo-labeler/master/examples/3_.png" width="400" />
  <div class="textcontent">
    <div class="text"><b> YOLO String: 1 0.546627 0.473380 0.899471 0.834987 </b></div>
  </div>
</p>

<p style="display: flex;align-items: center;justify-content: center;">  
  <img src="https://raw.githubusercontent.com/abpanchal95/yolo-labeler/master/examples/4.jpg" width="400" />
  <img src="https://raw.githubusercontent.com/abpanchal95/yolo-labeler/master/examples/4_.png" width="400" />
  <div class="textcontent">
    <div class="text"><b> YOLO String: 2 0.312660 0.499840 0.625321 0.999679 </b></div>
  </div>
</p>

<p style="display: flex;align-items: center;justify-content: center;">  
  <img src="https://raw.githubusercontent.com/abpanchal95/yolo-labeler/master/examples/5.jpg" width="400" />
  <img src="https://raw.githubusercontent.com/abpanchal95/yolo-labeler/master/examples/5_.png" width="400" />
  <div class="textcontent">
    <div class="text"><b> YOLO String: 2 0.484135 0.499840 0.363141 0.999679 </b></div>
  </div>
</p>

### Installation

```bash
pip3 install yolo-labeler
```

### Usage as a library

In `test.py`

```python
from yolo_labeler import yolo_labeler

yolo_labeler.run(args)
```

run command
```bash
python3 test.py --input_path /path/to/input/image or image_folder --output_image_path /path/to/output/images --output_text_path /path/to/output/text --yolo_label class_num
```

### Advance usage

To not resize images provide --resize flag to 1
```bash
python3 test.py --input_path /path/to/input/image or image_folder --output_image_path /path/to/output/images --output_text_path /path/to/output/text --yolo_label class_num --size 1
```

To save output png images provide --png_path
```bash
python3 test.py --input_path /path/to/input/image or image_folder --output_image_path /path/to/output/images --output_text_path /path/to/output/text --yolo_label class_num --size 1 --png_path /path/to/output/png
```

To resize images of custom width x height provide --width and --height. Default is 416x416
```bash
python3 test.py --input_path /path/to/input/image or image_folder --output_image_path /path/to/output/images --output_text_path /path/to/output/text --yolo_label class_num --png_path /path/to/output/png --width 416 --height 416
```

To change background behind object provide --background_image
```bash
python3 test.py --input_path /path/to/input/image or image_folder --output_image_path /path/to/output/images --output_text_path /path/to/output/text --yolo_label class_num --png_path /path/to/output/png --width 1000 --height 1000 --background_image /path/to/background/image
```

To save changed background images provide --background_out
```bash
python3 test.py --input_path /path/to/input/image or image_folder --output_image_path /path/to/output/images --output_text_path /path/to/output/text --yolo_label class_num --png_path /path/to/output/png --width 416 --height 416 --background_image /path/to/background/image --background_out /path/to/output/changed/background/images
```

### References

- https://github.com/NathanUA/U-2-Net

### License

Copyright (c) 2020-present [Abhi Panchal](https://github.com/abpanchal95)

Licensed under [MIT License](./LICENSE)
