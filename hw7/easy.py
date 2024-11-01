class Node:

	# Constructor to create a new node
	def __init__(self, key):
		self.key = key
		self.left = None
		self.right = None

# Write a Python function to insert a value into a binary search tree. The function should take the root of the tree and the value to be inserted as parameters.

def insert_value(root, value):
    if root is None:
        return Node(value)
    if value < root.key:
        root.left = insert_value(root.left, value)
    else:
        root.right = insert_value(root.right, value)
    return root

test = Node(5)

insert_value(test, 3)
insert_value(test, 7)
insert_value(test, 1)
insert_value(test, 4)
insert_value(test, 6)
insert_value(test, 8)

print(test.key)