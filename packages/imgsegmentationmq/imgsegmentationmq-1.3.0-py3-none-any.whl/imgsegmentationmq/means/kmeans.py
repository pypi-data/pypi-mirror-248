from imgsegmentationmq import np
from imgsegmentationmq import initialize_centroids_data
def kmeans(k,image, max_it=100, init_centroids=None):
    '''
    Applies the k-means algorithm to an image.  
    
    Parameters
    ----------
    k: int
        Number of clusters
    image: numpy.ndarray
        Numpy array representing the image for which to find some initial centroids.
    max_it: int 
        Number of maximum iterations of the algorithm.
    init_centroids: numpy.ndarray
        Numpy array representing some initial centroids.
    
    Returns
    -------
    new_centroids: numpy.ndarray
        Numpy array representing the final centroids.
    pixel_classes: numpy.ndarray
        Numpy array representing the cluster to which each pixel of the original image belongs.
    '''
    # TypeErrors  
    if(type(k) != int):
        raise TypeError('k must be an integer')
    
    if(type(max_it) != int):
        raise TypeError('max_it must be an integer')
    
    if(type(image) != np.ndarray):
        raise TypeError('image must be a numpy.ndarray')   
        
    if(init_centroids is not None and type(init_centroids) != np.ndarray):
        raise TypeError('init_centroids must be a numpy.ndarray')   
    
    # ValueErrors    
    if(k <= 0):
        raise ValueError('The number of clusters must be greater than 0')
        
    if(max_it <= 0):
        raise ValueError('The number of maximum iterations must be greater than 0')
    
    if(len(image.shape) != 3):
        raise ValueError('The image must have 3 dimensions (length,width,color_scale)')
    
    if(init_centroids is not None and (len(init_centroids.shape) !=3 or init_centroids.shape[1] != k \
                                       or init_centroids.shape[2] != image.shape[2])):
        raise ValueError(('init_centroids must have 3 dimensions (length,k,color_scale) '
                          'with k being the number of clusters and '
                          'color_scale being the same as the color scale of the image'))
    
    # Get shape    
    img_length = image.shape[0]
    img_width = image.shape[1]
    img_colscale = image.shape[2]
    
    # Initialize centroids if needed 
    centroids = init_centroids
    if centroids is None:
        centroids = initialize_centroids_data(k,image)

    # Initialize classes
    pixel_classes = np.zeros((img_length,img_width,1))
    
    # Start algorithm
    new_centroids = np.zeros(centroids.shape)
    it = 0
    while it < max_it and not np.allclose(new_centroids,centroids):
        if it > 0:
            centroids = new_centroids
        new_centroids = np.zeros(centroids.shape)
        number_points = np.zeros(k)
        for i in range(img_length):
            for j in range(img_width):
                if(img_colscale == 1):
                    closestCentroid = np.argmin(abs((image[i,j,:].reshape(1,1,img_colscale) - centroids)))
                    pixel_classes[i,j,0] = closestCentroid
                    new_centroids[0,closestCentroid,:] = new_centroids[0,closestCentroid,:] + image[i,j,:]
                    number_points[closestCentroid] = number_points[closestCentroid] + 1
                else:
                    closestCentroid = int(np.argmin(np.linalg.norm(image[i,j,:].reshape(1,1,img_colscale) - centroids,axis=2),axis=1))
                    pixel_classes[i,j,0] = closestCentroid
                    new_centroids[0,closestCentroid,:] = new_centroids[0,closestCentroid,:] + image[i,j,:]
                    number_points[closestCentroid] = number_points[closestCentroid] + 1
        for i in range(k):
            if(number_points[i]>0):
                new_centroids[0,i,:] = new_centroids[0,i,:]/number_points[i]
        it = it +1
    return new_centroids,pixel_classes