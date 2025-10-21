"""
hi my name is JImmie 
this is a Doc string 
"""

name = "Jamal Aldhamsha"
id = 3200606025
field = "Cyber Security"

print("my name is: ", name)
print("my id number :", id )
print("field :", field )

# --------2nd ex
print("\n-----2nd example -----\n")
dic = {name : "jamal",
       id : "3200606025",
       field : " Cyber Security"}

print(dic,"\n")

# --------user input 
print("\n-----user input ------\n")
user_input = int(input("Enter an integer "))
print("you entered : ", user_input)

if user_input > 0 :
    print("you have entered a positive number ")
    c= 0 
    while c <=user_input:
        print(name)
        c=c+1   
else:
    print("you have entered a negative number") 
    i=0
    for i in range(user_input,0):
        print("My name is ", name)  




