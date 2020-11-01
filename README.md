# Automatic YOLO Labeler

[![Downloads](https://pepy.tech/badge/yolo-labeler)](https://pepy.tech/project/yolo-labeler)
[![Downloads](https://pepy.tech/badge/yolo-labeler/month)](https://pepy.tech/project/yolo-labeler/month)
[![Downloads](https://pepy.tech/badge/yolo-labeler/week)](https://pepy.tech/project/yolo-labeler/week)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://img.shields.io/badge/License-MIT-blue.svg)

#### Note: This tool is using U-2-Net model for background removal. So it is preferred to use single point focused images as input.

YOLO Labeler is a tool to remove images background and label object in YOLO format.

<p style="display: flex;align-items: center;justify-content: center; border-style: groove;">
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/1.jpg" width="400" />
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/1_.png" width="400" />
  <div class="textcontent">
    <div class="text"><b> YOLO String: 0 0.513942 0.407692 0.272115 0.746795 </b></div>
  </div>
</p>

<p style="display: flex;align-items: center;justify-content: center;"> 
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/2.jpg" width="400" />
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/2_.png" width="400" />
  <div class="textcontent">
    <div class="text"><b> YOLO String: 0 0.287500 0.580769 0.575000 0.837821 </b></div>
  </div>  
</p>

<p style="display: flex;align-items: center;justify-content: center;">  
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/3.jpg" width="400" />
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/3_.png" width="400" />
  <div class="textcontent">
    <div class="text"><b> YOLO String: 1 0.546627 0.473380 0.899471 0.834987 </b></div>
  </div>
</p>

<p style="display: flex;align-items: center;justify-content: center;">  
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/4.jpg" width="400" />
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/4_.png" width="400" />
  <div class="textcontent">
    <div class="text"><b> YOLO String: 2 0.312660 0.499840 0.625321 0.999679 </b></div>
  </div>
</p>

<p style="display: flex;align-items: center;justify-content: center;">  
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/5.jpg" width="400" />
  <img src="https://github.com/abpanchal95/yolo-labeler/blob/master/examples/5_.png" width="400" />
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
import yolo_labeler

yolo_labeler.run(args)
```

run command
```bash
python3 test.py --input_path /path/to/image or image_folder --output_text_path /output/text/path
```

### Advance usage

Sometimes it is possible to achieve better results by turning on alpha matting. Example:
```bash
python3 test.py --input_path /path/to/image or image_folder --output_text_path /output/text/path
```


### References

- https://github.com/NathanUA/U-2-Net

### License

Copyright (c) 2020-present [Abhi Panchal](https://github.com/abpanchal95)

Licensed under [MIT License](./LICENSE.txt)
