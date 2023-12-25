from imgsegmentationmq import np
from imgsegmentationmq import initialize_centroids_data
from imgsegmentationmq.means import cmeans_centroid,cmeans_pxl_classes
def cmeans(k,image,m,max_it=100,init_centroids=None):
    '''
    Applies the c-means algorithm to an image.  
    
    Parameters
    ----------
    k: int
        Number of clusters
    image: numpy.ndarray
        Numpy array representing the image for which to find some initial centroids.
    m: int or float
        Weighting exponent
    max_it: int 
        Number of maximum iterations of the algorithm.
    init_centroids: numpy.ndarray
        Numpy array representing some initial centroids.
    
    Returns
    -------
    new_centroids: numpy.ndarray
        Numpy array representing the final centroids.
    px_class: numpy.ndarray
        Numpy array representing the cluster to which each pixel of the original image belongs.

    '''
    # TypeErrors  
    if(type(k) != int):
        raise TypeError('k must be an integer')
    
    if(type(m) != int and type(m) != float):
        raise TypeError('m must be an integer or a float')
    
    if(type(max_it) != int):
        raise TypeError('max_it must be an integer')
    
    if(type(image) != np.ndarray):
        raise TypeError('image must be a numpy.ndarray')   
        
    if(init_centroids is not None and type(init_centroids) != np.ndarray):
        raise TypeError('init_centroids must be a numpy.ndarray') 
    
    # ValueErrors
    if(k <= 0):
        raise ValueError('The number of clusters must be greater than 0')
        
    if(m <= 1):
        raise ValueError('m must be greater than 1')
    
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
    
    # Initialize centroids if needed 
    centroids = init_centroids
    if centroids is None:
        centroids = initialize_centroids_data(k,image)

    # Initialize classes
    pixel_classes = cmeans_pxl_classes(image,centroids,k, m)

    # Start algorithm
    new_centroids = np.zeros(centroids.shape)
    it = 0
    while not np.allclose(new_centroids,centroids) and it<max_it:
        if it > 0:
            centroids = new_centroids
        new_centroids = cmeans_centroid(image, pixel_classes, k, m)
        pixel_classes = cmeans_pxl_classes(image,new_centroids,k, m)
        it = it +1
    
    # Selecting the cluster that maximizes the membership for each cluster
    px_class = np.zeros((img_length,img_width,1))
    for i in range(img_length):
        for j in range(img_width):
            px_class[i,j,0] = int(np.argmax(pixel_classes[i,j,:]))
    return new_centroids,px_class