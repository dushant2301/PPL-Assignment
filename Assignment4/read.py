try:
    with open('names.txt', 'r') as f:
        content = f.read()
        print("Contents of names.txt:")
        print(content)
except FileNotFoundError:
    print("Error: 'names.txt' not found. Run Program 1 first.")