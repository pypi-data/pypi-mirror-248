from imgsegmentationmq import np
from imgsegmentationmq import math
def generalizedManhattan(x,y,k1,k2):
    '''
    
    Calculates the generalized Manhattan distance between x and y given k1 and k2.  
    
    Parameters
    ----------
    x: numpy.ndarray
    y: numpy.ndarray
    k1: int or float
    k2: int or float

    Returns
    -------
    distance: numpy.ndarray
        Numpy array representing the distance from x the different points (centroids) in y.
    
    '''
    # TypeErrors  
    if(type(k1) != int and type(k1) != float):
        raise TypeError('k1 must be an integer or a float')
        
    if(type(k2) != int and type(k2) != float):
        raise TypeError('k2 must be an integer or a float')
    
    if(type(x) != np.ndarray):
        raise TypeError('x must be a numpy.ndarray')   
        
    if(type(y) != np.ndarray):
        raise TypeError('y must be a numpy.ndarray')   
    
    # ValueErrors   
    x_shape = x.shape
    y_shape = y.shape
    
    if(k1 <= 0 or k2 <= 0):
        raise ValueError('k1 and k2 must be greater than 0')
        
    if(x_shape[0] != y_shape[0] or x_shape[2] != y_shape[2] or x_shape[0] != 1 or x_shape[1] != 1):
        raise ValueError('x and y must have shapes (1,1,n) and (1,k,n) respectively, where k and n are both positive integers')
    
    img_colscale = x_shape[2]
    distance = np.zeros(y_shape[1])
    for cluster_index in range(y_shape[1]):
        for i in range(img_colscale):
            if(y[0,cluster_index,i] < x[0,0,i]):
                distance[cluster_index] += k1*(x[0,0,i] - y[0,cluster_index,i])
            else:
                distance[cluster_index] += k2*(y[0,cluster_index,i] - x[0,0,i])
    return distance

def cquantile_centroid(image, pxl_classes, clusters, m, k1, k2):
    '''
    Function to calculate the centroids in the c-quantile algorithm.
    
    Parameters
    ----------
    image: numpy.ndarray
        Numpy array representing the image for which to find some initial centroids.
    pxl_classes: numpy.ndarray
        Numpy array representing the cluster to which each pixel of the original image belongs.
    clusters: int
        Number of clusters
    m: int or float
        Weighting exponent
    k1: int or float
    k2: int or float
    
    Returns
    -------
    centroids: numpy.ndarray
        Numpy array representing the new centroids.
    
    '''
    # TypeErrors  
    if(type(clusters) != int):
        raise TypeError('k must be an integer')
       
    if(type(k1) != int and type(k1) != float):
        raise TypeError('k1 must be an integer or a float')
        
    if(type(k2) != int and type(k2) != float):
        raise TypeError('k2 must be an integer or a float')
    
    if(type(m) != int and type(m) != float):
        raise TypeError('m must be an integer or a float')
    
    if(type(image) != np.ndarray):
        raise TypeError('image must be a numpy.ndarray')   
        
    if(type(pxl_classes) != np.ndarray):
        raise TypeError('pxl_classes must be a numpy.ndarray') 
    
    # ValueErrors   
    if(clusters <= 0):
        raise ValueError('The number of clusters must be greater than 0')
        
    if(k1 <= 0 or k2 <= 0):
        raise ValueError('k1 and k2 must be greater than 0')
        
    if(m <= 1):
        raise ValueError('m must be greater than 1')
    
    if(len(image.shape) != 3):
        raise ValueError('The image must have 3 dimensions (length,width,color_scale)')
    
    if(len(pxl_classes.shape) != 3 or pxl_classes.shape[2] != clusters):
        raise ValueError('pxl_classes must have 3 dimensions (length,width,clusters)')
        
    img_length = image.shape[0]
    img_width = image.shape[1]
    img_colscale = image.shape[2]
    
    # Get the index of the proper quantile
    order_quantile = k1/(k1+k2)
    idx = int(round(order_quantile*(img_length*img_width)))
    
    centroids = np.zeros((1,clusters,img_colscale))
    
    new_dim = img_length*img_width
    result = np.zeros((new_dim,img_colscale))

    # Reshaping image       
    reshaped_image = image.reshape((new_dim,img_colscale))

    # Reshaping pixel classes
    reshaped_pxlc = pxl_classes.reshape((new_dim,clusters))
    
    for k in range(clusters):        
        for i in range(new_dim):
            result[i,:] = (reshaped_pxlc[i,k]**m)*reshaped_image[i,:]
        
        # Index of the pixels of the image from which to take the color value
        idx_quantile = np.argpartition(result,idx,axis=0)[idx]
        centroids[0,k,:] = np.array([reshaped_image[idx_quantile[j]][j] for j in range(img_colscale)])

    return centroids

def cquantile_pxl_classes(image,centroids,clusters,m,k1,k2):
    '''
    Function to calculate the class for each pixel in the c-quantile algorithm.
    
    Parameters
    ----------
    image: numpy.ndarray
        Numpy array representing the image for which to find some initial centroids.
    centroids: numpy.ndarray
        Numpy array representing the centroids.
    clusters: int
        Number of clusters
    m: int or float
        Weighting exponent
    k1: int or float
    k2: int or float
    
    Returns
    -------
    pxl_classes: numpy.ndarray
        Numpy array representing the membership of each pixel to the different clusters.
    
    '''
    # TypeErrors  
    if(type(clusters) != int):
        raise TypeError('clusters must be an integer')
       
    if(type(k1) != int and type(k1) != float):
        raise TypeError('k1 must be an integer or a float')
        
    if(type(k2) != int and type(k2) != float):
        raise TypeError('k2 must be an integer or a float')
    
    if(type(m) != int and type(m) != float):
        raise TypeError('m must be an integer or a float')
    
    if(type(image) != np.ndarray):
        raise TypeError('image must be a numpy.ndarray')   
        
    if(type(centroids) != np.ndarray):
        raise TypeError('centroids must be a numpy.ndarray') 
        
    # ValueErrors    
    if(clusters <= 0):
        raise ValueError('The number of clusters must be greater than 0')
        
    if(k1 <= 0 or k2 <= 0):
        raise ValueError('k1 and k2 must be greater than 1')
    
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
            break_condition =  False
            for k in range(clusters):
                if(not np.any(generalizedManhattan(image[i,j,:].reshape(1,1,img_colscale),
                                               centroids[0,k,:].reshape(1,1,img_colscale),
                                               k1,k2))):
                    break_condition = True
                    k_val = k
                    break 
                else:
                    sum_val = sum_val + (1/generalizedManhattan(image[i,j,:].reshape(1,1,img_colscale),
                                                           centroids[0,k,:].reshape(1,1,img_colscale),
                                                           k1,k2))**(2/(m-1))
            if(not break_condition):
                for k in range(clusters):
                    pxl_classes[i,j,k] = (generalizedManhattan(image[i,j,:].reshape(1,1,img_colscale),
                                                               centroids[0,k,:].reshape(1,1,img_colscale),
                                                               k1,k2))**(2/(m-1))*sum_val
            else:
                pxl_classes[i,j,:] = math.inf*np.ones(clusters)
                pxl_classes[i,j,k_val] = 1
    pxl_classes = 1/pxl_classes
    return pxl_classes