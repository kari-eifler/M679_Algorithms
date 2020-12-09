"""
Basic sorting algorithms

@author: Kari_Eifler
"""

def quicksort_lomuto(elements, low_idx=None, high_idx=None):
    """
    This function sorts the elements list in place using the 
    Lomuto partitioning scheme.  Only the values in the range
    [low_idx, high_idx] are sorted by a call to this function.
    
    elements - A list of values to be sorted
    low_idx  - The starting index of the elements list to be 
               sorted.  Values appearing before this index are
               not touched. Default is 0.
    high_idx - The ending value of the elements list to be 
               sorted.  Values appearing after this index are
               not touched.  Default is len(elements)-1.
    """
    
    if low_idx is None:
        low_idx = 0
    if high_idx is None:
        high_idx = len(elements)-1
    
    pivot_value = elements[high_idx]
    
    swap_idx = low_idx
    for i in range(low_idx,high_idx):
        if elements[i] < pivot_value:
            elements[i], elements[swap_idx] = elements[swap_idx], elements[i]
            swap_idx += 1 #increment the swap index
            continue
    # Swap the pivot with the element in current swap location
    elements[high_idx], elements[swap_idx] = elements[swap_idx], elements[high_idx]
    
    #here do it recursively
    if swap_idx-1 > low_idx and swap_idx+1 < high_idx: #sort first AND second half
        elements = quicksort_lomuto(elements,low_idx,swap_idx-1)
        elements = quicksort_lomuto(elements, swap_idx+1, high_idx)
    elif swap_idx-1 > low_idx and swap_idx+1 >= high_idx: #sort first half only
        elements = quicksort_lomuto(elements,low_idx,swap_idx-1)
    elif swap_idx-1 <= low_idx and swap_idx+1 < high_idx: #sort second half only
        elements = quicksort_lomuto(elements, swap_idx+1, high_idx)
    
    return elements



def partition_hoare(elements, low_idx = None, high_idx = None):
    if low_idx is None:
        low_idx = 0
    if high_idx is None:
        high_idx = len(elements)-1
    
    left_idx = low_idx-1
    right_idx = high_idx+1
    pivot_value = elements[low_idx] #first element is pivot
    
    while left_idx != right_idx:
        right_idx -= 1
        while elements[right_idx] > pivot_value:
            right_idx -= 1
        left_idx += 1
        while elements[left_idx] < pivot_value:
            left_idx += 1
        if left_idx >= right_idx:
            return right_idx
        elements[left_idx], elements[right_idx] = elements[right_idx], elements[left_idx]


def quicksort_hoare(elements, low_idx=None, high_idx=None):
    """
    This function sorts the elements list in place using the 
    Lomuto partitioning scheme.  Only the values in the range
    [low_idx, high_idx] are sorted by a call to this function.
    
    elements - A list of values to be sorted
    low_idx  - The starting index of the elements list to be 
               sorted.  Values appearing before this index are
               not touched. Default is 0.
    high_idx - The ending value of the elements list to be 
               sorted.  Values appearing after this index are
               not touched.  Default is len(elements)-1.
    """
    if low_idx is None:
        low_idx = 0
    if high_idx is None:
        high_idx = len(elements)-1
    
    if low_idx < high_idx:
        MIDDLE = partition_hoare(elements,low_idx,high_idx)
    
        if MIDDLE > low_idx and MIDDLE+1 < high_idx: # if you need to do left and right
            elements = quicksort_hoare(elements,low_idx,MIDDLE)
            elements = quicksort_hoare(elements, MIDDLE+1, high_idx)
        elif MIDDLE > low_idx and MIDDLE+1 >= high_idx: # if you need to do only left
            elements = quicksort_hoare(elements,low_idx,MIDDLE)
        elif MIDDLE <= low_idx and MIDDLE+1 < high_idx: # if you need to do only right
            elements = quicksort_hoare(elements, MIDDLE+1, high_idx)
    
    return elements




