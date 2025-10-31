""" 
functions  
Simple Math Calculator using functions
by : Jamal
ID : 3200606025

""" 

def add_num(num1, num2): 

    sum =num1 + num2 

    print("Summation : ", sum) 

 

def subtraction(num1, num2): 

    sub = num1 - num2 

    print("Subtrtaction : ",sub) 

 

def multiplication(num1, num2): 

    multiply= num1 * num2 

    print("Multiplication :", multiply) 

 

def division(num1, num2): 

    if num2 ==0 : 

        print("Can not divid by zero ") 

        return 

    div = num1/num2 

    print("division : ", div) 

 

def user_input(): 

    print("\n--- Simple Math Calculator by Jimmie ---") 

    print("Choose an operation by number:") 

    print("1) Addition") 

    print("2) Subtraction") 

    print("3) Multiplication") 

    print("4) Division ") 

     

    try: 

        choice = int(input("Enter choice (1, 2, 3, or 4): ")) 

    except ValueError: 

        print("Invalid input. Please enter a number for your choice (1, 2,3, or 4).") 

        return  

   

    if choice in (1, 2, 3, 4): 

        try: 

            

            num1 = float(input("Enter number 1: ")) 

            num2 = float(input("Enter number 2: ")) 

        except ValueError: 

            print("Invalid input. Please enter valid numbers.") 

            return  

               

        if choice == 1: 

            add_num(num1, num2) 

        elif choice == 2: 

            subtraction(num1, num2) 

        elif choice == 3: 

            multiplication(num1, num2) 

        elif choice == 4: 

            division(num1, num2)     

    else: 

        print("Invalid choice. Please select 1, 2, or 3.") 

 

user_input() 

 

 

 