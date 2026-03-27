try:
    with open('data.txt', 'r') as f:
        data = f.read()
        print(f"Total number of characters: {len(data)}")
except FileNotFoundError:
    print("Error: 'data.txt' not found.")