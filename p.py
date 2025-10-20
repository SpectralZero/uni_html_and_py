# for i in range (12,260,10):
#     print(i)
# c = 12 
# while c < 260 :
#      print (c)
#      c = c+10


# c = 45 
# while c>=3:
#         print (c*2)
#         c = c-5

# for num in range (45,2,-5):
#     print (num*2)

# -------------------------
# check if even or odd example 1
# print("--- example for even and odd num ---")
# li = lambda lst : [(x, "even" if x % 2 == 0 else "odd") for x in lst]
# print(li([1,2,3,5,56,7,8]))

# print("\n--- example for even numbers ---")
# # check if even example 2
# my_list = [1,2,3,4,5,6,7,8,9,10]
# even_list = list(filter(lambda x : (x for x in my_list) if x % 2 ==0 else False ,my_list))
# print(even_list)

# print("\n--- example for odd numbers ---")
# # check if odd example 3
# my_list = [1,2,3,4,5,6,7,8,9,10]
# odd_list = list(filter(lambda x : (x for x in my_list) if x % 2 !=0 else False ,my_list))
# print(odd_list)

# print("\n--- example 1 for primes ---")
# # example 1 check prime
# is_prime = lambda x: x > 1 and not [i for i in range(2, x) if x % i == 0]
# print(is_prime(7))  # True
# print(is_prime(25)) # False

# print("\n--- example 2 for primes ---")
# # example 2 check if prime
# is_prime = lambda x: all(x % i != 0 for i in range(2, x)) if x > 1 else False # all() checks if all elements in a list or tuple are True
# prime_numbers = lambda lst: [x for x in lst if is_prime(x)]
# print(prime_numbers(range(2, 25)))

# print("\n--- example 3 for primes ---")
# # example 3 for primes
# prime_list = list(range(2,30))
# prime_num = list(filter(lambda x :all(x % i != 0 for i in range(2,x)) if x > 1 else False ,prime_list))
# print(prime_num)



