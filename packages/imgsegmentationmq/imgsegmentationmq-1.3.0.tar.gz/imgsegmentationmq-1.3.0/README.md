# Description
Repository for the image segmentation package.

# Installing the package

To install the package in Unix/macOS, execute the following command:

python3 -m pip install imgsegmentationmq


To install the package in Windows, execute the following command:

py -m pip install imgsegmentationmq

# Importing and uding the package

To import the package to your python script run the following line:

import imgsegmentationmq

To import all the algorithms to your script run the following line:

from imgsegmentationmq import *

Once you have run the previous line, you can start using the algorithms by using the respective calls:  

    For the k-means algorithm:

        imgsegmentationmq.means.kmeans(k,image, max_it, init_centroids)

    For the c-means algorithm:

        imgsegmentationmq.means.kmeans(k,image,m,max_it,init_centroids)

    For the k-quantile algorithm:

        imgsegmentationmq.means.kmeans(k,image,k1,k2,max_it,init_centroids)

    For the c-quantile algorithm:
    
        imgsegmentationmq.means.kmeans(k,image,m,k1,k2, max_it, init_centroids)

Please make sure you have the arguments in the appropiate form. Specifically note that to use these algorithms
the image to which you will apply it needs to be a numpy array with shape (image length, image width, image colorscale),
this means that for a 60x40 image in gray colorscale, the shape should be (60,40,1) while for the a 60x40 image with RGB
colorscale, the shape of the numpy array should be (60,40,3).