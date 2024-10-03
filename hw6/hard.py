import numpy

def max_diff(numbers):
    # sort the array from small to large
    numbers = numpy.sort(numbers)

    # return the first element subtracted from the last element
    return numbers[-1] - numbers[0]
    
# create array
array = numpy.array([3,1,-2,8,6,2,9,5,-3,2,5])

# print the difference between the largest and smallest number in the array
print(max_diff(array))