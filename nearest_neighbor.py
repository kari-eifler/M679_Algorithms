"""
Nearest neighbor using kd-trees

@author: Kari_Eifler
"""
import math
import numpy as np
from scipy import linalg
from scipy import spatial


def create_column_data(num_elements, dimension, 
                       lower_bound = -1.0, upper_bound = 1.0):    
    """
    The returned np.array has number of cols=num_elements and number of rows=dimension.
    Each column of the returned object is a data point containing values that 
    fall in the half-open interval [lower_bound, upper_bound).  The memory layout of
    the returned np.array is Fortran order (column major).
    
    """
    return np.random.uniform(low=lower_bound, high=upper_bound, size=(dimension,num_elements))

def nn_brute_force(test_point, data):
    """
    Computes the distance between test_point and every column in data.  The function
    assumes that the number of elements in test_point matches the length of each column
    in data.  The column with minimum distance is returned via a tuple containing the
    index of the column from data and the column itelf with shape modified to match 
    test_point.  Note that this function returns a view of the column from data and not
    a copy.
    """
    minindex = -1
    mindistance = 100000000
    
    if test_point is None or data is None:
        return (None,None)
    else:
        for i in range(np.shape(data)[1]):
            if distance(data[:,[i]],test_point) < mindistance:
                minindex = i
                mindistance = distance(data[:,[i]],test_point)
        return (minindex, data[:,minindex])


def nn_create_kd_tree(data):
    """
    data is a set of column-based points to be spatially sorted into a kd-tree.
    This function returns a scipy.spatial.KDTree object representing data or 
    None if data is None.
    
    """
    if data is None:
        return None
    else:
        dataT = data.transpose() #transpose the data so rows are points so we can use query
        return spatial.KDTree(dataT)


def nn_query_kd_tree(test_point, tree):
    """
    Given a test_point and a scipy.spatial.KDTree this function queries the
    kd-tree for the closest point to test_point.  The function returns a tuple
    containing the index of the closest point in the tree along with the 
    closest point itself reshaped to match the shape of test_point.  
    If either argument is None then (None, None) is returned.
    """
    if test_point is None or tree is None:
        return (None, None)
    else:
        dim = len(test_point)
        
        test_point_modified = np.reshape(test_point,(dim,))
        
        ans = tree.query(test_point_modified)
        return (ans[1],tree.data[ans[1]])



def create_projection_matrix(n, m): 
    """
    Returns an np.array with n rows and m columns whose values are ranomly sampled
    from a normal distribution (0.0, 1.0).  The memory layout for the returned
    np.array will be row-major.
    
    We would like you to modify create_projection_matrix so that it 
    returns a matrix whose random elements are scaled by 1 / sqrt(k), 
    where k is the size of the reduced dimension.
    """
    matrix = 1/math.sqrt(m) * np.random.uniform(low=0.0, high=1.0, size=(n,m))
    return matrix



def compute_distortion(X, T_X):
    """
    Computes and returns the distortion between the set of data points (columns in x)
    and their image (columns in T_x).  The distortion is computed as 
    max_i(||T_X_i|| / ||X_i||) * max_i(||X_i|| / ||T_X_i||), where T_X_i and X_i are the
    ith columns of T_X and X, respectively and max_i is the max over all i.  Also, ||a|| 
    here refers to the L2 norm.
    
    You need to compute the norms of the differences between all pairs of columns in X 
    in both the original space and the projected space.
    """
    
    maximum1 = 0 #max ||f(X_i) - f(X_j)|| / ||X_i - X_j||
    maximum2 = 0 #max ||X_i - X_j|| / ||f(X_i) - f(X_j)||
    for i in range(len(X)):
        for j in range(i+1,len(X)):
            Xdist = distance(X[:,i],X[:,j])
            T_Xdist = distance(T_X[:,i],T_X[:,j])
            if T_Xdist / Xdist > maximum1:
                maximum1 = T_Xdist / Xdist
            if Xdist / T_Xdist > maximum2:
                maximum2 = Xdist / T_Xdist
    ans = maximum1*maximum2
    return ans
                


def iterate_reduced_nn(X, y, reduced_dimension, num_trials=10):
    """
    This function performs a number of nearest neighbor trials, each of which 
    consists of the projection of the input data set X and test point y to a 
    lower dimension and the nearest neighbor of the test point is sought in 
    the data set (in the lower dimension).  The nearest neighbor computation 
    will be performed by first creating a scipy.spatial.KDTree with the 
    projected X and then querying it using the projected y.  The index of each
    identified nearest neighbor will be added to a list and only the unique
    indices returned (no duplicates).
    
    X - A column based data set from which the nearest neighbor to y is sought
    y - A test point with length equal to column length of X, which is to be used
        as a query point
    reduced_dimension - An integer representing the dimension of the reduced space
        in which the nearest neighbor computation will be performed.
    num_trials - The number of projection matrices to be tested.
    
    """
    
    data_dimension = np.shape(X)[0]
    list1 = []
    
    for trialnum in range(num_trials):
        A = create_projection_matrix(reduced_dimension, data_dimension)
        
        reduced_X = A@X
        reduced_y = A@y
        
        Tree = nn_create_kd_tree(reduced_X)
        (idx, nn) = nn_query_kd_tree(reduced_y, Tree)
        list1.append(idx)
    uniquelist = list(np.unique(np.array(list1)))
    return uniquelist


def nn_iterative(X, y, reduced_dimension, num_trials=10):
    """
    Perfrom a number of approximate nearest neighbor trials in a reduced space. 
    The results of those trials are used to select a subset of the data points in 
    X and repeat the nearest neighbor computation in the original dimension using
    only the selected data points.  The function returns a tuple containing the 
    index of the nearest neighbor in the original data set along with the nearest 
    neighbor itself reshaped to match the shape of test_point. 
    
    X - A column based data set from which the nearest neighbor to y is sought
    y - A test point with length equal to column length of X, which is to be used
        as a query point
    reduced_dimension - An integer representing the dimension of the reduced space
        in which the nearest neighbor computation will be performed.
    num_trials - The number of projection matrices to be tested.
    
    """
    list1 = iterate_reduced_nn(X, y, reduced_dimension, num_trials) #list of possible indices
    X_new = X[:,list1]
    
    tree = nn_create_kd_tree(X_new)
    
    (idx, nn) = nn_query_kd_tree(y, tree)
    
    ansvector = np.reshape(X[:,idx], np.shape(y))
    return (idx, ansvector)




