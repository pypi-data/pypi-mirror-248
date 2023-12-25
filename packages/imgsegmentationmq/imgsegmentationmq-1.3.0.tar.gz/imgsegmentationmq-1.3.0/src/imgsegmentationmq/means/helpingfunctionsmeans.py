from imgsegmentationmq import np
from imgsegmentationmq import math
def cmeans_centroid(image, pxl_classes, clusters, m):
    '''
    Calculate the centroids for the c-means algorithm.  
    
    Parameters
    ----------
    image: numpy.ndarray
        Numpy array representing the image for which to find some initial centroids.
    pxl_classes: numpy.ndarray
        Numpy array representing the membership of each pixel to the different clusters.
    clusters: int
        Number of clusters
    m: int or float
        Weighting exponent
    
    Returns
    -------
    centroids: numpy.ndarray
        Numpy array representing the new centroids.
    '''
    
    # TypeErrors  
    if(type(clusters) != int):
        raise TypeError('clusters must be an integer')
    
    if(type(m) != int and type(m) != float):
        raise TypeError('m must be an integer or a float')
    
    if(type(image) != np.ndarray):
        raise TypeError('image must be a numpy.ndarray')   
        
    if(type(pxl_classes) != np.ndarray):
        raise TypeError('pxl_classes must be a numpy.ndarray')  
    
    # ValueErrors   
    if(clusters <= 0):
        raise ValueError('The number of clusters must be greater than 0')
        
    if(m <= 1):
        raise ValueError('m must be greater than 1')
    
    if(len(image.shape) != 3):
        raise ValueError('The image must have 3 dimensions (length,width,color_scale)')
    
    if(len(pxl_classes.shape) != 3 or pxl_classes.shape[2] != clusters):
        raise ValueError('pxl_classes must have 3 dimensions (length,width,clusters)')
    
    img_length = image.shape[0]
    img_width = image.shape[1]
    img_colscale = image.shape[2]
    centroids = np.zeros((1,clusters,img_colscale))
    for k in range(clusters):
        coefs_sum = 0 
        for i in range(img_length):
            for j in range(img_width):
                coefs_sum = coefs_sum + pxl_classes[i,j,k]**m
                centroids[0,k,:] = centroids[0,k,:] + (pxl_classes[i,j,k]**m)*image[i,j,:]
        centroids[0,k,:] = centroids[0,k,:]/coefs_sum        
    return centroids
def cmeans_pxl_classes(image,centroids,clusters,m):
    '''
    Calculate the membership of each pixel to the different clusters.
    
    Parameters
    ----------
    image: numpy.ndarray
        Numpy array representing the image for which to find some initial centroids.
    centroids: numpy.ndarray
        Numpy array representing the centroids of the clusters.
    clusters: int
        Number of clusters
    m: int or float
        Weighting exponent
    
    Returns
    -------
    pxl_classes: numpy.ndarray
        Numpy array representing the membership of each pixel to the different clusters.
    '''
    
    # TypeErrors  
    if(type(clusters) != int):
        raise TypeError('clusters must be an integer')
    
    if(type(m) != int and type(m) != float):
        raise TypeError('m must be an integer or a float')
    
    if(type(image) != np.ndarray):
        raise TypeError('image must be a numpy.ndarray')   
        
    if(type(centroids) != np.ndarray):
        raise TypeError('centroids must be a numpy.ndarray') 
    
    # ValueErrors    
    if(clusters <= 0):
        raise ValueError('The number of clusters must be greater than 0')
        
    if(m <= 1):
        raise ValueError('m must be greater than 1')
    
    if(len(image.shape) != 3):
        raise ValueError('The image must have 3 dimensions (length,width,color_scale)')
    
    if(len(centroids.shape) != 3 or centroids.shape[1] != clusters or centroids.shape[2] != image.shape[2]):
        raise ValueError('centroids must have 3 dimensions (1,clusters,color_scale)')
    
    img_length = image.shape[0]
    img_width = image.shape[1]
    img_colscale = image.shape[2]
    
    pxl_classes = np.zeros((img_length,img_width,clusters))
    for i in range(img_length):
        for j in range(img_width):
            sum_val = 0 
            break_condition = False
            for k in range(clusters):
                if(img_colscale == 1):
                    if(not np.any(abs(image[i,j,:] - centroids[0,k,:]))):
                        # If the distance to one centroid is 0 then the class is 1 for that cluster and 0 for the rest
                        break_condition = True
                        k_val = k
                        break
                    else:
                        sum_val = sum_val + (1/abs(image[i,j,:] - centroids[0,k,:]))**(2/(m-1))
                else:
                    if(not np.any(np.linalg.norm(image[i,j,:] - centroids[0,k,:]))):
                        break_condition = True
                        k_val = k
                        break 
                    else:
                        sum_val = sum_val + (1/np.linalg.norm(image[i,j,:] - centroids[0,k,:]))**(2/(m-1))
            if(not break_condition):
                for k in range(clusters):
                    if(img_colscale == 1):
                        pxl_classes[i,j,k] = abs(image[i,j,:] - centroids[0,k,:])**(2/(m-1))*sum_val
                    else:
                        pxl_classes[i,j,k] = np.linalg.norm(image[i,j,:] - centroids[0,k,:])**(2/(m-1))*sum_val
            else:
                pxl_classes[i,j,:] = math.inf*np.ones(clusters)
                pxl_classes[i,j,k_val] = 1
    pxl_classes = 1/pxl_classes
    return pxl_classes