total = 0
try:
    with open('numbers.txt', 'r') as f:
        for line in f:
            total += float(line.strip())
    print(f"The sum of numbers is: {total}")
except FileNotFoundError:
    print("Error: 'numbers.txt' not found.")
except ValueError:
    print("Error: File contains non-numeric data.")