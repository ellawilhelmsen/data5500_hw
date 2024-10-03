import numpy

# Big O notation: O(n)

def sum_numbers(nums):
    # add up all the numbers, and return the result
    val = 0
    for i in range(len(nums)):
        # add each number to the total
        val += nums[i]
    return val 

# create array
array = numpy.array([3,1,2,8,6,-2,9,5,3,2,-5])

# print sum of numbers in array
print(sum_numbers(array)) 
