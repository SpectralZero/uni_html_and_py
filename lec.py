# # Calculate the Nim product of three numbers
# def cal_nim (n1,n2,n3):
#     minnum = min(n1,n2,n3)
#     return (n1*n2*n3)/minnum
# print(cal_nim(3,5,2))

# #using a for loop and without a for loop — to multiply all elements in a list by 2
# nums = [1, 2, 3, 4, 5]

# for i in range(len(nums)):
#     nums[i] = nums[i] * 2

# print(nums)

# # Without using a for loop
# nums = [1, 2, 3, 4, 5]
# new_nums = list(map(lambda x: x * 2, nums))
# print(new_nums)

# # list comprehension to create a new list with each element multiplied by 2
# nums = [1, 2, 3, 4, 5]
# nums = [x * 2 for x in nums]
# print(nums)

# # take user input for many numbers and calculate their sum
# def summation():
#     numbers = input("Enter numbers separated by spaces: ")
#     num_list = list(map(int, numbers.split()))# map 
#     total = sum(num_list)
#     print("The sum is:", total)

#summation()


# function that take user input to see if there are any vowels in a string using lists and print the vowel indexes in that string
# def has_vowels(s):
#     vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
#     vowel_indexes = []
#     for i, char in enumerate(s):
#         if char in vowels:
#             vowel_indexes.append(i+1)
#     return vowel_indexes
# user_input = input("Enter a string: ")
# vowel_indexes = has_vowels(user_input)
# if vowel_indexes:
#     print("The string contains vowels at the following indexes:", vowel_indexes)
# else:
#     print("The string does not contain vowels.", user_input)

# split function example comprehensive 
# def split_string(s):
#     return s.split()

# user_input = input("Enter a string: ")
# print("The split string is:", split_string(user_input))


