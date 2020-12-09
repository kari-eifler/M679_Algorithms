"""
Semi-definite program to compute the Euclidean distortion for 
a variety of graphs

@author: Kari_Eifler
"""
import numpy as np
import cvxpy as cp


def optimize_sdp(n, dist_func, dist_arg=None, verbose=False):
    """
    n - The number of vertices in your graph
    dist_func - A distance function to be called as 
            dist_func(i,j,dist_arg) for i,j in range(n)
    dist_arg - An additional paramter to be passed to dist_func
    verbose - Flag to be passed to solve indicating whether or not
            it should display its progress during the solve.
    Returns - (optimization status, D, G, delta)
    """
    
    dist_matrix_sq = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            dist_matrix_sq[i,j] = dist_func(i,j,dist_arg)**2
    
    # create variables
    delta = cp.Variable((n,n)) #symmetric matrix
    G = cp.Variable((n-1,n-1),PSD=True)
    D2 = cp.Variable() #this is the variable for D^2
    
    #define the constraints
    constraints = [G >> 0,
                   D2 >= 0,
                   dist_matrix_sq <= delta
                  ]
    for i in range(1,n):
        for j in range(1,n):
            constraints += [
                D2*dist_matrix_sq[i,j] >= delta[i,j],
                G[i-1,j-1] == 1/2*(delta[0,i]+delta[0,j]-delta[i,j])
            ]
    
    
    objective = cp.Minimize(D2) #later we take the square root
    
    prob = cp.Problem(objective,constraints)
    prob.solve()
    
    status = prob.status
    D = D2.value
    D = np.sqrt(D)
    G = G.value
    delta = delta.value
    
    return [status, D, G, delta]



