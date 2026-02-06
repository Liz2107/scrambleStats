import cube

def lossTotalColors(c):
    """    
    :param c: cube

    only valid for 

    get center size and number permissible per side
    initialize a running count, and go through each side 
    on each side, for each color, add |theoretical # permissible - actual #| to count
    """    
    center_size = (c.n - 1) ** 2
    per_side_theory = center_size // 6


def lossConnectedBits(c):
    """   
    :param c: cube

    for each side, for each color, count the number of blocks where there is an adjacent color (non-diagonal)
    keep a running tally, return result
    """


