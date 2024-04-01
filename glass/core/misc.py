# author: Bradley Augstein <b.augstein@ucl.ac.uk>
# license: MIT
'''module for miscellaneous functions'''

def isTriangle(num: int) -> bool:
    n = int((2*num)**0.5)
    if tri(n)!= num:
        return False
    return True
    
def tri(num: int) -> int:
    return num*(num+1)//2
