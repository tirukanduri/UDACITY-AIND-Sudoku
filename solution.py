assignments = []

rows='ABCDEFGHI'
cols='123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]
    pass

# Get the required boxes setup
boxes=cross(rows,cols)

row_units=[cross(r,cols) for r in rows]

column_units=[cross(rows,c) for c in cols]

square_units=[cross(rs,cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# create diagonal units
diagonal_units_main=[rows[i]+cols[i] for i in range(0,9)]
diagonal_units_cross=[rows[i]+cols[8-i] for i in range(0,9)]
diagonals=[]
diagonals.append(diagonal_units_main)
diagonals.append(diagonal_units_cross)
unitlist= diagonals + row_units + column_units + square_units



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def replace_for_twins(values,peer_list,equal_boxes_list):
    """For every box in the peer list, remove the elements that correspond to the twins 
    For example, if the twins are 2,4 remove these values from all the other boxes
    """

    n = list(values[equal_boxes_list[0]])
    for x in peer_list:
        if len(values[x])==1:
            continue
        if x in equal_boxes_list:
            continue
        poss = values[x]
        for a in n:
            poss = poss.replace(a,'')
        if not values[x]==poss:
            assign_value(values, x, poss)

    return values

import itertools
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    for peer_list in unitlist:
        peer_values = dict((k,values[k]) for k in peer_list)
        for a in peer_list:
            t = [x for x in peer_list if x != a and values[x] == values[a] ]
            if(len(t))<1:
                 continue

            if len(values[a])==(len(t)+1):
                t.append(a)
                values=replace_for_twins(values,peer_list,t)
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    data = list(grid)
    for n, i in enumerate(data):
        if i == '.':
            data[n] = '123456789'
    return dict(zip(boxes, data))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def replace (values, boxes,box):
    for x in boxes:

        if len(values[x])==1:
            continue
        if x==box:
            continue
        values[x]=values[x].replace(values[box],'')
    return values

from heapq import merge

def eliminate(values):
    for locus_box in values.keys():
        if not len(values[locus_box])==1:
            continue
        peer_list= [x for x in unitlist if locus_box in x]
        for peers in peer_list:
            for current in peers:
                if current==locus_box:
                    continue
                values[current] = values[current].replace(values[locus_box],'')

    return values


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def check_for_error(values,boxset,box):
    for x in boxset:
        if(x==box):
            continue
        if(values[x]==values[box]):
            return False;
    return True;

def check_sudoku(values):

    for peer_list in unitlist:
        for locus_box in peer_list:
            if len(values[locus_box])>1:
                continue
            if not check_for_error(values, peer_list, locus_box):
                return False

    return True


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False

    # values = naked_twins(values)

    #if not check_sudoku(values):
     #   return False

    if all((len(values[s])) == 1 for s in values.keys()):
        if check_sudoku(values):
            return values

    length, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for possible_value in values[s]:
        new_values = values.copy()
        new_values[s] = possible_value
        a = search(new_values)
        if a:
            return a

def solve(grid):

    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    grid = grid_values(grid)
    grid = reduce_puzzle(grid)

    grid = search(grid)
    return grid

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
