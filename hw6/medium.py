import numpy

# Big O notation: O(n log n)
# I found this by looking up the big O notation for the numpy.sort() function

def second_largest(numbers):
    # sort the array from large to small
    numbers = numpy.sort(numbers)[::-1]
    # return the second element
    return numbers[1]

# create array
array = numpy.array([3,1,-2,8,6,2,-9,5,3,2,5])

# print second largest number in array
print(second_largest(array))