import cv2 as cv
from glob import glob

# Read all frames from ./frames directory
frames = [cv.imread(path) for path in sorted(glob('frames/frame*.png'), key=lambda path: int(path[12:].split('.')[0]))]
*size, _ = frames[0].shape

# Creating video from frames
video = cv.VideoWriter('yea.avi', cv.VideoWriter_fourcc(*'MJPG'), 60, (size[1], size[0]))
for frame in frames: video.write(frame)
video.release()