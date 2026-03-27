names = ["Alice", "Bob", "Charlie"]
with open('names.txt', 'w') as f:
    for name in names:
        f.write(name + "\n")
print("File 'names.txt' created successfully.")