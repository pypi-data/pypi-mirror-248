from imgsegmentationmq import random
from imgsegmentationmq import np

def initialize_centroids_data(k,image):
    '''
    Function that initializes the centroids of our clusters.  
    
    Parameters
    ----------
    k: int
        Number of clusters  
    image: numpy.ndarray
        Numpy array representing the image for which to find some initial centroids.
    
    Returns
    -------
    centroids: numpy.ndarray
        Numpy array representing some initial centroids.
    '''
    # TypeErrors
    if(type(k) != int):
        raise TypeError('k must be an integer')
        
    if(type(image) != np.ndarray):
        raise TypeError('image must be a numpy.ndarray') 
        
    # ValueErrors
    
    if(len(image.shape) != 3):
        raise ValueError('The image must have 3 dimensions (length,width,color_scale)')
        
    dim_colscale = image.shape[2]
    if(k <= 0):
        raise ValueError('The number of clusters must be greater than 0')
        
    if(dim_colscale != 1 and dim_colscale != 3):
        raise ValueError('The dimension of the color scale must be one or three')
        
    
    centroids = np.zeros((1,k,dim_colscale))
    if(dim_colscale==1):
        # Grayscale, we initialize the clusters so that they are equally separated through the values of the image
        percentile_index = [i/(k+1) for i in range(1,k+1)]
        centroids = np.quantile(np.unique(image),percentile_index).reshape(1,k,dim_colscale)
    else:
        # RGB scale 
         for j in range(k):
                if j <= 3:
                    centroids[0,j,j%3] = random.randrange(75,175)  
                elif j == 4:
                    centroids[0,j,:] = np.array([random.randrange(75,175),random.randrange(75,175),0])
                elif j == 5:
                    centroids[0,j,:] = np.array([random.randrange(75,175),0,random.randrange(75,175)])
                elif j == 6:
                    centroids[0,j,:] = np.array([0,random.randrange(75,175),random.randrange(75,175)])
                else:
                    centroids[0,j,:] = np.array([random.randrange(0,250),random.randrange(0,250),random.randrange(0,250)])
    return centroids