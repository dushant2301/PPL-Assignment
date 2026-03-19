balance = 0.0

def bank():
    global balance
    while True:
        print("\n1.Balance 2.Deposit 3.Withdraw 4.Exit")
        c = input("Choice: ")
        if c == '1': print(f"Balance: {balance}")
        elif c == '2': balance += float(input("Amount: "))
        elif c == '3': 
            amt = float(input("Amount: "))
            if amt <= balance: balance -= amt
            else: print("Insufficient funds")
        else: break

bank()