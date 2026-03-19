def calc():
    print("1.Add 2.Sub 3.Mul 4.Div 5.Mod")
    choice = input("Choice: ")
    a, b = float(input("Num1: ")), float(input("Num2: "))
    
    if choice == '1': print(a + b)
    elif choice == '2': print(a - b)
    elif choice == '3': print(a * b)
    elif choice == '4': print(a / b if b != 0 else "Error")
    elif choice == '5': print(a % b)

calc()