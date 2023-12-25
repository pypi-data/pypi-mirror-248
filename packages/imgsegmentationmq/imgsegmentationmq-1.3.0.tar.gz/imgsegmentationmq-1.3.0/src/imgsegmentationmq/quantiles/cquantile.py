from imgsegmentationmq import np
from imgsegmentationmq import initialize_centroids_data
from imgsegmentationmq.quantiles import cquantile_centroid,cquantile_pxl_classes
def cquantile(k,image,m,k1,k2, max_it=100, init_centroids=None):
    '''
    Applies the c-quantile algorithm to the image.
    
    Parameters
    ----------
    k: int
        Number of clusters
    image: numpy.ndarray
        Numpy array representing the image for which to find some initial centroids.
    m: int or float
    k1: int or float
    k2: int or float
    max_it: int
        Maximum number of iterations for the algorithm
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
       
    if(type(k1) != int and type(k1) != float):
        raise TypeError('k1 must be an integer or a float')
        
    if(type(k2) != int and type(k2) != float):
        raise TypeError('k2 must be an integer or a float')
    
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
        
    if(k1 <= 0 or k2 <= 0):
        raise ValueError('k1 and k2 must be greater than 0')
        
    if(m <= 1):
        raise ValueError('m must be greater than 0')
    
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
    pixel_classes = cquantile_pxl_classes(image,centroids,k, m,k1,k2)

    # Start algorithm
    new_centroids = np.zeros(centroids.shape)
    it = 0
    while not np.allclose(new_centroids,centroids) and it<max_it:
        if it > 0:
            centroids = new_centroids
        new_centroids = cquantile_centroid(image, pixel_classes, k, m,k1,k2)
        pixel_classes = cquantile_pxl_classes(image,new_centroids,k, m,k1,k2)
        it = it +1

     # Selecting the cluster that maximizes the membership for each cluster
    px_class2 = np.zeros((img_length,img_width,1))
    for i in range(img_length):
        for j in range(img_width):
            px_class2[i,j,0] = int(np.argmax(pixel_classes[i,j,:]))
    return new_centroids,px_class2