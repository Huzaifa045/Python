## CORONASIMULATE  Simulate coronagraph and Gerchberg-Saxton algorithm
#
# A simulation of a coronagraph and the Gerchberg-Saxton algorithm, in the
# context of NASA's Roman Space Telescope, developed to help teach ENCMP
# 100 Computer Programming for Engineers at the University of Alberta. The
# program saves output figures to PNG files for subsequent processing.
#
# Copyright (c) 2022, University of Alberta
# Electrical and Computer Engineering
# All rights reserved.
#
# Student name: 
# Student CCID: 
# Others: 
#
# To avoid plagiarism, list the names of persons, Version 0 author(s)
# excluded, whose code, words, ideas, or data you used. To avoid
# cheating, list the names of persons, excluding the ENCMP 100 lab
# instructor and TAs, who gave you compositional assistance.
#
# After each name, including your own name, enter in parentheses an
# estimate of the person's contributions in percent. Without these
# numbers, adding to 100%, follow-up questions will be asked.
#
# For anonymous sources, enter pseudonyms in uppercase, e.g., SAURON,
# followed by percentages as above. Email a link to or a copy of the
# source to the lab instructor before the assignment is due.
#

import matplotlib.pyplot as plt
import numpy as np

def main():
    im = loadImage('300_26a_big-vlt-s.jpg')
    (im,Dphi,mask) = opticalSystem(im,300)
    images,errors = gerchbergSaxton(im,10,Dphi,mask)
    saveFrames(images,errors)

def loadImage(name): # For loading image and pre-processing
    """ 
    Load image and pre-process

    Parameters:
    name: Image file
       
    Return:
    numpy.ndarray: Pre-processed image
    """
    im = plt.imread(name)/255 #Load image

    if len(im.shape) > 2: #Converts to greyscale if required
        im = (im[:,:,0]+im[:,:,1]+im[:,:,2])/3

    #Pixel value restrriction to [0, 1]
    im[im < 0] = 0
    im[im > 1] = 1

    return im

def opticalSystem(im,diameter):
    """
    Implement occultation on the image, calculate the 2D discrete Fourier transform of the image, create random phase values for the inverse transformation, and execute the inverse transform with phase adjustment.

    Parameters:
    im: Input image.
    diameter: diameter of the region of the circle that is to be occulated

    Returns:
    numpy.ndarray: The new image
    numpy.ndarray: An arbitrary phase for the inverse transform
    numpy.ndarray: The mask that indicates the pixels that were occulated
    """
    im,mask = occultCircle(im,diameter) #Applying the occulation
    (IMa,IMp) = dft2(im) #Calculate the 2D discrete Fourier transfrom
    
    (IMa, IMp) = dft2(im) #calculating the 2D discrete Fourier transform of the image
    
    rng = np.random.default_rng(12345) #Generating a random phase for the inverse transform
    imR = rng.random(im.shape)
    (_,Dphi) = dft2(imR)

    im = idft2(IMa,IMp-Dphi) #Execute the inverse transform with the correction of phase

    return (im,Dphi,mask)

def occultCircle(im,diameter):
    """
    For occulating a circle space in a given image

    Parameters:
    im: Input image.
    diamter: The dimension of the circle space to be occulated.

    Returns:
    numpy.ndarray: The image that has the circle region occulated.
    numpy.ndarray: The mask that indicates the pixels occulated
    """
    h,w = im.shape

    centerH = h // 2
    centerW = w // 2

    circleRadius = diameter / 2 #The radius of the circle is half of its diamter

    y,x = np.ogrid[:h,:w] #Grid for the image

    (mask) = (x-centerW)**2 + (y-centerH)**2 <= circleRadius**2 #A mask that aquires the circles coordinates

    im[mask] = 0 #Making the circle pixels black by making them 0

    return im, mask


# (IMa,IMp) = dft2(im) returns the amplitude, IMa, and phase, IMp, of the
# 2D discrete Fourier transform of a grayscale image, im. The image, a 2D
# array, must have entries between 0 and 1. The phase is in radians.
def dft2(im):
    IM = np.fft.rfft2(im)
    IMa = np.abs(IM)
    IMp = np.angle(IM)
    return (IMa,IMp)

# im = idft2(IMa,IMp) returns a grayscale image, im, with entries between
# 0 and 1 that is the inverse 2D discrete Fourier transform (DFT) of a 2D
# DFT specified by its amplitude, IMa, and phase, IMp, in radians.
def idft2(IMa,IMp):
    IM = IMa*(np.cos(IMp)+1j*np.sin(IMp))
    im = np.fft.irfft2(IM)
    im[im < 0] = 0
    im[im > 1] = 1
    return im

def occultError(im, mask):
    """
    Calculating the occultation error in the image.

    Parameters:
    im : input image.
    mask : mask that indicates occulted pixels.

    Returns:
    float: occulating error.
    """
    error = np.sum(im[mask]**2)
    return error

def gerchbergSaxton(im,maxIters,Dphi,mask): # Perform the Gerchberg-Saxton algorithm
    """
    Perform the Gerchberg-Saxton algorithm. Take an input image, execute the algorithim for given iterations and return a list of images generated. Also returns a list of errors pertaining to each iteration
    
    Parameters:
    im: Input image
    maxIters: The maximum number of iterations.
    Dphi: A Random phase for inverse transform.
    mask: mask that indicates the pixels occulated

    Returns:
    list: A List of the generated images.
    list: A list of errors pertaining to each occulation
    """
    (IMa,IMp) = dft2(im) #magnitude & phase of the Fourier Transform
    images = [] #list to hold the generated images
    errors = [] #list to hold the errors that pertain to each iteration
    for k in range(maxIters+1):
        print("Iteration %d of %d" % (k,maxIters))
        if k == 0:
            im = idft2(IMa,IMp) #Fourier transform w/o phase correction
        elif k == maxIters:
            im = idft2(IMa,IMp+Dphi) #Fourier transform w/ phase correction
        else:
            alpha = k/maxIters
            im = idft2(IMa,(1 - alpha) * IMp + alpha * (IMp + Dphi))
        images.append(im) #add the generated image to the list defined
        error = occultError(im,mask) #calculate the occulation error
        errors.append(error) # add the calculated error to the list
    return images,errors

def saveFrames(images,errors): #Save the images that are generated in the format .png
    """
    Saving the frames as .png files (images). Also plot the errors

    Parameters:
    images: A List of the images that are to be saved.
    errors: A list containing the errors for each iteration

    """
    #Make empty image that has the same shape as the first image generated
    shape = (images[0].shape[0],images[0].shape[1],3)
    image = np.zeros(shape,images[0].dtype)

    maxIters = len(images)- 1 #max iterations
    maxErrors = max(errors) #max error
    
    for k in range(maxIters+ 1):
        # Plotting the errors pertaining to each interation
        plt.plot(errors[:k+1], color='red')
        plt.xlabel("Iteration")
        plt.ylabel("Sum Square Error")
        plt.xlim(0, maxIters)
        plt.ylim(0, maxErrors)

        #Change the RGB of the image to the current image
        image[:,:,0] = images[k] 
        image[:,:,1] = images[k]
        image[:,:,2] = images[k]
        
        #Displaying the image and the errors in the background
        plt.imshow(image,extent=(0,maxIters,0,maxErrors))
        plt.gca().set_aspect(maxIters/maxErrors)

        plt.title("Coronagraph Simulation") #graph title

        plt.savefig('coronagraph' + str(k) + '.png') #Saving as .png
        plt.show()

main()
