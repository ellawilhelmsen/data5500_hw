from easy import *
# imports the easy.py file, and the functions and test object from that file

# function to find if a value is in the tree
def search_value(root, value):
    # if the value is not in the tree
    if root is None:
        return False
    # if the value is in the tree
    if root.key == value:
        return True
    # use of recursion to keep searhing the tree
    if value < root.key:
        return search_value(root.left, value)
    else:
        return search_value(root.right, value)
    
print(search_value(test, 1)) 
print(search_value(test, 10))