## CORONAANIMATE  Animate coronagraph and Gerchberg-Saxton algorithm
#
# A simulation of a coronagraph and the Gerchberg-Saxton algorithm, in the
# context of NASA's Roman Space Telescope, developed to help teach ENCMP
# 100 Computer Programming for Engineers at the University of Alberta. The
# program loads images from PNG files and produces an AVI video file.
#
# Copyright (c) 2022, University of Alberta
# Electrical and Computer Engineering
# All rights reserved.
#
import cv2
lastNum = int(input("Last frame number? "))
(prefix,suffix) = ('coronagraph','.png')
image = cv2.imread(prefix+'0'+suffix)

if image is not None:
    fps = 10 # (frames per second)
    size = (image.shape[1],image.shape[0])
    code = cv2.VideoWriter_fourcc('M','J','P','G')
    video = cv2.VideoWriter(prefix+'.avi',code,fps,size)
    video.write(image)

    for k in range(1,lastNum+1):
        image = cv2.imread(prefix+str(k)+suffix)
        if image is not None:
            video.write(image)
        else:
            break # for

    video.release()
