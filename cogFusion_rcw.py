#
# Code written for cogFusion project at NeurohackWeek/Seattle
# Robert C. Welsh
# Salt Lake City
# 2016
#

# Three functions
#
#   1) contrastDotProductAvg
#
#        calculate the avergage contrast image from each list and then calculate
#        the dot product.
#
#   2) contrastAvgDotProduct
#
#        calculate the dot product of all combinations and return a list
#
#   3) readImageList
#
#        return a list of nibabel image objects.
#
#

# Packages needed:
#
#   scipy.ndimage
#   nibabel
#   numpy
#

# just in case we want to smooth the image.

import scipy.ndimage as ndimage

# need for reading in the image

import nibabel as nib

# and need for manipulating the image

import numpy as np

# Function to calculate the similarity of two sets of contrasts
# by calculating the inner product of the average.

def contrastDotProductAvg(imageList1,imageList2,maskingImage,smooth1=[0,0,0],smooth2=[0,0,0]):
    ''' 
        This command will take two nibabel lists of images and average the images,
        then mask them with the nibabel maskingimage. If smoothing is specified the
        data will be smoothed. The inner product of the images will then be calculated.
        
        Parameters
        -----------
        imageList1    -  is a list of nibabel objects
        imageList2    -  is a list of nibabel objects
        maskingImage  -  is a list [singular] of nibabel objects.
        smooth1       -  is a 3 list of gaussian smoothing parameters (x,y,z)
        smooth2       -  is a 3 list of guassian smoothing parameters (x,y,z)

        Returns
        -----------

        ourDotProduct -  is the dot product between the averages of the contrast images
                         

        '''
    
    # Initalize our arrays - by geting the first image
    
    data1 = 0*imageList1[0].get_data()
    data2 = data1

    # read in our first stack

    for image1 in imageList1:
        data1 = data1 + image1.get_data()

    # read in our second stack

    for image2 in imageList2:
        data2 = data2 + image2.get_data()

    # now get the masking image.

    maskData = maskingImage[0].get_data()

    # just in case some of these are weirdly 4D, which 
    # in the test case of using a hdr/img it came with 
    # a singular 4th dimension, so squeezing them!

    data1 = np.squeeze(data1)/len(imageList1)
    data2 = np.squeeze(data2)/len(imageList2)

    # optional smoothing.

    data1 = ndimage.gaussian_filter(data1,smooth1)
    data2 = ndimage.gaussian_filter(data2,smooth2)

    maskData = np.squeeze(maskData)

    dataM1 = np.sqrt(sum(sum(sum(data1*data1*maskData))))
    dataM2 = np.sqrt(sum(sum(sum(data2*data2*maskData))))

    #print(dataM1)
    #print(dataM2)

    ourDotProduct = sum(sum(sum(data1*data2*maskData)))

    #print(ourDotProduct)

    ourDotProduct = ourDotProduct/dataM1
    ourDotProduct = ourDotProduct/dataM2

    return ourDotProduct


# Function to calculate the similarity of two sets of contrasts
# by calculating the pair-wise and then taking the average 
# and also returning the variance.

def contrastAvgDotProduct(imageList1,imageList2,maskingImage,smooth1=[0,0,0],smooth2=[0,0,0]):
    ''' 
        This command will take two nibabel lists of images and average the images,
        then mask them with the nibabel maskingimage. If smoothing is specified the
        data will be smoothed. The inner product of the images will then be calculated.
         
        Parameters
        -----------
        imageList1    -  is a list of nibabel objects
        imageList2    -  is a list of nibabel objects
        maskingImage  -  is a list [singular] of nibabel objects.
        smooth1       -  is a 3 list of gaussian smoothing parameters (x,y,z)
        smooth2       -  is a 3 list of guassian smoothing parameters (x,y,z)

        Returns
        -----------

        ourDotProduct -  is all of the pair-wise dot-products, this will allow for taking
                         the average and calculating the variance.
        '''
    
    ourDotProduct = []

    # now get the masking image.

    maskData = maskingImage[0].get_data()
    
    
    for image1 in imageList1:
        for image2 in imageList2:
            data1 = image1.get_data()
            data2 = image2.get_data()
            
            # just in case some of these are weirdly 4D, which 
            # in the test case of using a hdr/img it came with 
            # a singular 4th dimension, so squeezing them!
            
            data1 = np.squeeze(data1)/len(imageList1)
            data2 = np.squeeze(data2)/len(imageList2)
            
            # optional smoothing.
            
            data1 = ndimage.gaussian_filter(data1,smooth1)
            data2 = ndimage.gaussian_filter(data2,smooth2)
            
            maskData = np.squeeze(maskData)
            
            dataM1 = np.sqrt(sum(sum(sum(data1*data1*maskData))))
            dataM2 = np.sqrt(sum(sum(sum(data2*data2*maskData))))
            
            #print(dataM1)
            #print(dataM2)
            
            ourDotProduct.append(sum(sum(sum(data1*data2*maskData)))/dataM1/dataM2)
            
    return ourDotProduct


# Function to take the list of strings (file names) and 
# return a list of nibabel file objects.

def readImageList(nameList):
    ''' 
       Take list of file names and return the nibabel obejcts as a list.

       Parameters
       -----------
       nameList   -  is a list of file names.

    
       Returns
       -----------
       imageList  -  is a list of nibabel image objects from nib.load
    
       '''

    imageList = []
    for theName in nameList:
        imageList.append(nib.load(theName))
        
    return imageList

