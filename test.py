#!/usr/bin/env python3
import argparse
from yolo_labeler import yolo_labeler

def get_arg():
	"""getting arguments"""
	parser = argparse.ArgumentParser()
    
	_, all_arguments = parser.parse_known_args()
	script_args = all_arguments[0:]
    
	parser.add_argument("-ipath","--input_path", type=str)
	parser.add_argument("-opath","--output_image_path", type=str)
	parser.add_argument("-tpath","--output_text_path", type=str)
	parser.add_argument("-ylabel","--yolo_label", type=int, default=0)
	parser.add_argument("-size","--size", type=bool, default=False)	
	parser.add_argument("-width","--width", type=int, default=416)
	parser.add_argument("-height","--height", type=int, default=416)
	parser.add_argument("-png_path","--png_path", type=str)
	parser.add_argument("-bg_img","--background_image", type=str)
	parser.add_argument("-bg_out","--background_out", type=str)
	parser.add_argument("-ae","--alpha_erode", type=int)		
    
	parsed_script_args,_ = parser.parse_known_args(script_args)

	return parsed_script_args
	
def main():
	args = get_arg()
	yolo_labeler.run(args)

if __name__ == "__main__":
	main()
