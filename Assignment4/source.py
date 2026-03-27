try:
    with open('source.txt', 'r') as src:
        content = src.read()
    
    with open('destination.txt', 'w') as dest:
        dest.write(content)
    print("File copied successfully.")
except FileNotFoundError:
    print("Error: 'source.txt' not found.")