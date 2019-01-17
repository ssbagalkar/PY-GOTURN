#!/usr/local/bin/python3

import cv2
import argparse
import os
import sys

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap .add_argument("-i", "--input", required=True, help="Input directory of images folder")
ap.add_argument("-ext", "--extension", required=False, default='png', help="extension name. default is 'png'.")
ap.add_argument("-o", "--output", required=True, help="output video file directory")
ap.add_argument("-f", "--fps", required=False, default=10, help="frame rate")
ap.add_argument("-c", "--codec", type=str, default="MJPG",help="codec of output video")
args = vars(ap.parse_args())

# Arguments
dir_path = args['input']
ext = args['extension']
output_folder = args['output']
output_file = output_folder.split("/")[-1]+".avi"
print("[INFO]: Output folder is {}".format(output_folder))
print("[INFO]: Output file --> {}.avi".format(output_file))

# If ouput directory is not present, create it
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)
    print("Output directory is not present, creating it")
else:
    if len(os.listdir(output_folder))!=0:
        print("Output directory is present and contains video.Exiting..")
        sys.exit()

# Concatenate all images from dir to an array
images=[]
for f in os.listdir(dir_path):
    if f.endswith(ext):
        images.append(f)
print("{} number of frames in video {}".format(len(images), dir_path.split("/")[-1] ))

# Determine the width and height from first image
image_path = os.path.join(dir_path, images[0])
print("The image path is {}".format(image_path))
frame = cv2.imread(image_path)
if frame.shape is None:
    print("Image was not read properly. Exiting")
    sys.exit()

height, width, channels = frame.shape
print("[INFO]:Image stats..")
print("Image height : {}".format(height))
print("Image width : {}".format(width))
print("Image channels : {}".format(channels))

#Sets the frame rate to argument, or defaults to 10
frame_rate = int(args['fps'])
print("The conversion frame rate is set at {}".format(frame_rate))

# define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*args["codec"]) # Be sure to use lower case
out = cv2.VideoWriter(os.path.join(output_folder,output_file),fourcc, frame_rate, (width, height))
print("Output video will be stored at {}".format(os.path.join(output_folder,output_file)))


num_images_written=0
for image in images:

    image_path = os.path.join(dir_path, image)
    frame = cv2.imread(image_path)
    if frame.shape is not None:
        print("[INFO]:Frame {} sucessfully read".format(num_images_written))
        print("[INFO]: Shape--> {}".format(frame.shape))
    else:
        print("Frame {} unable to read".format(num_images_written))

    out.write(frame) # Write out frame to video
    num_images_written+=1

# Release
out.release()
print("[INFO]:Total number of images processed--> {}".format(num_images_written))
if len(os.listdir(output_folder)) > 0:
    print(os.listdir(output_folder))
else:
    print("video could not be written")
if num_images_written == len(images) and os.listdir(output_folder)[0] == output_file:
    print("Video sucessfully written for {}".format(dir_path.split("/")[-1]))
else:
    print("Unsucessful in writing the video")





