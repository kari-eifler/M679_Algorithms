#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tower of Hanoi

@author: Kari_Eifler
"""

def hanoi(initial_state, solution, num_towers, num_discs, start_tower_idx, target_tower_idx):
    """
    This function solves the Tower of Hanoi problem for 3 towers
    and 'num_discs' discs.  This function creates a list whose 
    elements are the state of the towers after each move.  For example, 
    the following list would be generated for 3 discs (spacing added only
    for readability):
    [ [[2, 1, 0], [],     []         ], 
      [[2, 1],    [],     [0]        ], 
      [[2],       [1],    [0]        ], 
      [[2],       [1, 0], []         ], 
      [[],        [1, 0], [2]        ], 
      [[0],       [1],    [2]        ], 
      [[0],       [],     [2, 1]     ], 
      [[],        [],     [2, 1, 0]] ]
      
    initial_state    - The list of towers containing the discs in their 
                       initial state.
    solution         - The list that shall contain the list of states 
                       moving from the initial_state to the final state
                       upon completion of this function.
    num_towers       - The number of towers in each state.  You may assume
                       this is always 3.
    num_discs        - The number of discs.
    start_tower_idx  - The index of the tower containing all of the discs
                       in the initial state.
    target_tower_idx - The index of the tower that shall contain all of 
                       the discs in the final state.
    """
    # Use the list `solution` to store the steps of your algorithm as
    # described above.
    
    #initialize solution if necessary
    if solution == []:
        solution = [copy.deepcopy(initial_state)]
    
    #find extra tower we can use to move discs around
    extra_tower_idx = 0
    while extra_tower_idx == start_tower_idx or extra_tower_idx == target_tower_idx:
        extra_tower_idx += 1
    
    if num_discs == 1:
        #move the one disc - top disc - from start_tower_idx to target_tower_idx
        disc_moved = initial_state[start_tower_idx][-1]
        del initial_state[start_tower_idx][-1]
        initial_state[target_tower_idx].append(copy.deepcopy(disc_moved))
        
        #update solution
        solution.append(copy.deepcopy(initial_state))
        
    elif num_discs > 1:
        #move the num_discs from start_tower_idx to target_tower_idx by recurssion
        
        #move smaller stack above disc of interest to extra_tower_idx
        hanoi(initial_state, solution, num_towers, num_discs-1, start_tower_idx, extra_tower_idx)
        
        #move disc of interest to target_tower_idx
        disc_moved = initial_state[start_tower_idx][-1]
        del initial_state[start_tower_idx][-1]
        initial_state[target_tower_idx].append(copy.deepcopy(disc_moved))
        
        #update solution
        solution.append(copy.deepcopy(initial_state))
        
        #move smaller stack back ontop of disc of interest
        hanoi(initial_state, solution, num_towers, num_discs-1, extra_tower_idx, target_tower_idx)
        
    return solution
