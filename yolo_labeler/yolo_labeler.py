#!/usr/bin/env python3
import os
import glob
import torch
import argparse
import numpy as np
import torch.nn as nn

from PIL import Image
from skimage import transform
from torchvision import transforms

from .utils import data_loader
from .utils.u2net import U2NET

from pymatting.alpha.estimate_alpha_cf import estimate_alpha_cf
from pymatting.foreground.estimate_foreground_ml import estimate_foreground_ml
from pymatting.util.util import stack_images
from scipy.ndimage.morphology import binary_erosion

def get_arg():
	"""getting arguments"""
	parser = argparse.ArgumentParser()
    
	_, all_arguments = parser.parse_known_args()
	script_args = all_arguments[0:]
    
	parser.add_argument("-ipath","--input_path", type=str, help="input path of image or image folder")
	parser.add_argument("-opath","--output_image_path", type=str, help="path to yolo output images")
	parser.add_argument("-tpath","--output_text_path", type=str, help="path to yolo output text files")
	parser.add_argument("-ylabel","--yolo_label", type=int, default=0, help="yolo string class number")
	parser.add_argument("-size","--size", type=bool, default=False, help="reverse resize flag (1 for no resizeing)")	
	parser.add_argument("-width","--width", type=int, default=416, help="when size != 1, image width for resize")
	parser.add_argument("-height","--height", type=int, default=416, help="when size != 1, image height for resize")
	parser.add_argument("-png_path","--png_path", type=str, help="path to output png images")
	parser.add_argument("-bg_img","--background_image", type=str, help="path to input background image")
	parser.add_argument("-bg_out","--background_out", type=str, help="path to output images with added background")
	parser.add_argument("-ae","--alpha_erode", type=int, help="possible to achieve better results by turning on alpha matting(default 10)")		
    
	parsed_script_args,_ = parser.parse_known_args(script_args)

	return parsed_script_args
	
def download(url, fname, path):
    if os.path.exists(path):
        return

    resp = requests.get(url, stream=True)
    total = int(resp.headers.get("content-length", 0))
    with open(path, "wb") as file, tqdm(
        desc=fname, total=total, unit="iB", unit_scale=True, unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
            
def load_model(model_name: str = "u2net"):
	os.makedirs(os.path.expanduser(os.path.join("~", ".u2net")), exist_ok=True)
	if model_name == "u2net":
		net = U2NET(3, 1)
		path = os.path.expanduser(os.path.join("~", ".u2net", model_name))
		download(
			"https://www.dropbox.com/s/qetmux2r5hks944/u2net?dl=1",
			"u2net.pth",
			path,
		)
	try:
		if torch.cuda.is_available():
			net.load_state_dict(torch.load(path))
			net.to(torch.device("cuda"))
		else:
			net.load_state_dict(torch.load(path, map_location="cpu",))
	except FileNotFoundError:
		raise FileNotFoundError(
			errno.ENOENT, os.strerror(errno.ENOENT), model_name + ".pth"
		)

	net.eval()

	return net
	
def norm_pred(d):
    ma = torch.max(d)
    mi = torch.min(d)
    dn = (d - mi) / (ma - mi)

    return dn

def preprocess(image):
    label_3 = np.zeros(image.shape)
    label = np.zeros(label_3.shape[0:2])

    if 3 == len(label_3.shape):
        label = label_3[:, :, 0]
    elif 2 == len(label_3.shape):
        label = label_3

    if 3 == len(image.shape) and 2 == len(label.shape):
        label = label[:, :, np.newaxis]
    elif 2 == len(image.shape) and 2 == len(label.shape):
        image = image[:, :, np.newaxis]
        label = label[:, :, np.newaxis]

    transform = transforms.Compose(
        [data_loader.RescaleT(320), data_loader.ToTensorLab(flag=0)]
    )
    sample = transform({"imidx": np.array([0]), "image": image, "label": label})

    return sample
    
def predict(net, item):

    sample = preprocess(item)

    with torch.no_grad():

        if torch.cuda.is_available():
            inputs_test = torch.cuda.FloatTensor(
                sample["image"].unsqueeze(0).cuda().float()
            )
        else:
            inputs_test = torch.FloatTensor(sample["image"].unsqueeze(0).float())

        d1, d2, d3, d4, d5, d6, d7 = net(inputs_test)

        pred = d1[:, 0, :, :]
        predict = norm_pred(pred)

        predict = predict.squeeze()
        predict_np = predict.cpu().detach().numpy()
        img = Image.fromarray(predict_np * 255).convert("RGB")

        del d1, d2, d3, d4, d5, d6, d7, pred, predict, predict_np, inputs_test, sample

        return img
        
def alpha_matting_cutout(img, mask, foreground_threshold=240, background_threshold=10, erode_structure_size=10):
    base_size = (1000, 1000)
    size = img.size

    img.thumbnail(base_size, Image.LANCZOS)
    mask = mask.resize(img.size, Image.LANCZOS)

    img = np.asarray(img)
    mask = np.asarray(mask)

    # guess likely foreground/background
    is_foreground = mask > foreground_threshold
    is_background = mask < background_threshold

    # erode foreground/background
    structure = None
    if erode_structure_size > 0:
        structure = np.ones((erode_structure_size, erode_structure_size), dtype=np.int)

    is_foreground = binary_erosion(is_foreground, structure=structure)
    is_background = binary_erosion(is_background, structure=structure, border_value=1)

    # build trimap
    # 0   = background
    # 128 = unknown
    # 255 = foreground
    trimap = np.full(mask.shape, dtype=np.uint8, fill_value=128)
    trimap[is_foreground] = 255
    trimap[is_background] = 0

    # build the cutout image
    img_normalized = img / 255.0
    trimap_normalized = trimap / 255.0

    alpha = estimate_alpha_cf(img_normalized, trimap_normalized)
    foreground = estimate_foreground_ml(img_normalized, alpha)
    cutout = stack_images(foreground, alpha)

    cutout = np.clip(cutout * 255, 0, 255).astype(np.uint8)
    cutout = Image.fromarray(cutout)
    cutout = cutout.resize(size, Image.LANCZOS)

    return cutout
        
def get_top(img):
	width, height = img.size
	for y in range(height):
		for x in range(width):
			r, g, b, a = img.getpixel((x, y))
			if a == 0:
				pass
			else:
				top = y
				return top
	
def get_bottom(img):
	width, height = img.size
	for y in reversed(range(height)):
		for x in range(width):
			r, g, b, a = img.getpixel((x, y))
			if a == 0:
				pass
			else:
				bottom = y
				return bottom
				
def get_left(img):
	width, height = img.size	
	for x in range(width):
		for y in range(height):
			r, g, b, a = img.getpixel((x, y))
			if a == 0:
				pass
			else:
				left = x
				return left

def get_right(img):
	width, height = img.size	
	for x in reversed(range(width)):
		for y in range(height):
			r, g, b, a = img.getpixel((x, y))
			if a == 0:
				pass
			else:
				right = x
				return right

def main(args, model, image_path):	
	print(f"Processing {image_path}")
	img = Image.open(image_path).convert('RGB')

	if not args.size:
		img = img.resize((args.width, args.height), resample=Image.LANCZOS)
	mask = predict(model, np.array(img)).convert("L")

	if args.alpha_erode:
		cutout = alpha_matting_cutout(img, mask, erode_structure_size=args.alpha_erode)
	else:
		empty = Image.new("RGBA", (img.size), 0)
		cutout = Image.composite(img, empty, mask.resize(img.size, Image.LANCZOS))
	
	width, height = cutout.size
	
	#YOLOv5
	top = get_top(cutout)
	bottom = get_bottom(cutout)
	left = get_left(cutout)
	right = get_right(cutout)
	center = (((left+right)/2)/width, ((top+bottom)/2)/height)
	width = right/width - left/width
	height = bottom/height - top/height
	
	yolo_string = f"{args.yolo_label} {center[0]:.6f} {center[1]:.6f} {width:.6f} {height:.6f}"
	#print(yolo_string)
	
	#add background
	if args.background_image and args.background_out:
		back_img = Image.open(args.background_image)
		back_img = back_img.resize(cutout.size, resample=Image.LANCZOS)
		back_img.paste(cutout, (0, 0), cutout)
		if not os.path.isdir(args.background_out):
			os.makedirs(args.background_out)
		back_img.save(os.path.join(args.background_out, f'{os.path.basename(image_path)}'.split('.')[0] + '_.png'), 'PNG')

	#saving output
	if args.output_text_path:
		if not os.path.isdir(args.output_text_path):
			os.makedirs(args.output_text_path)
		with open(os.path.join(args.output_text_path, f'{os.path.basename(image_path)}'.split('.')[0] + '_.txt'), 'w') as f:
			f.write(yolo_string)
	if args.output_image_path:
		if not os.path.isdir(args.output_image_path):
			os.makedirs(args.output_image_path)
		img.save(os.path.join(args.output_image_path, f'{os.path.basename(image_path)}'.split('.')[0] + '_.jpg'), 'JPEG')
	if args.png_path:
		if not os.path.isdir(args.png_path):
			os.makedirs(args.png_path)
		cutout.save(os.path.join(args.png_path, f'{os.path.basename(image_path)}'.split('.')[0] + '_.png'), 'PNG')
		
	return yolo_string
		
def run(args):
    model = load_model()
	
    if os.path.isdir(args.input_path):  
        types = (os.path.join(args.input_path,'*.jpg'), os.path.join(args.input_path,'*.jpeg'), os.path.join(args.input_path,'*.png'))
        files_grabbed = []
        for files in types:
            files_grabbed.extend(glob.iglob(files))  
    elif os.path.isfile(args.input_path):  
        files_grabbed = [args.input_path]
    else:  
        raise ValueError("File PATH is NOT Valid")        

    for image_path in files_grabbed:
        yolo_string = main(args, model, image_path)
