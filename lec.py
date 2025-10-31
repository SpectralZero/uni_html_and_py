# Calculate the Nim product of three numbers
def cal_nim (n1,n2,n3):
    minnum = min(n1,n2,n3)
    return (n1*n2*n3)/minnum
print(cal_nim(3,5,2))

#using a for loop and without a for loop — to multiply all elements in a list by 2
nums = [1, 2, 3, 4, 5]

for i in range(len(nums)):
    nums[i] = nums[i] * 2

print(nums)

# Without using a for loop
nums = [1, 2, 3, 4, 5]
new_nums = list(map(lambda x: x * 2, nums))
print(new_nums)

# list comprehension to create a new list with each element multiplied by 2
nums = [1, 2, 3, 4, 5]
nums = [x * 2 for x in nums]
print(nums)

# take user input for many numbers and calculate their sum
def summation():
    numbers = input("Enter numbers separated by spaces: ")
    num_list = list(map(int, numbers.split()))# map 
    total = sum(num_list)
    print("The sum is:", total)

#summation()