count = 0
try:
    with open('words.txt', 'r') as f:
        text = f.read().lower()
        words = text.split()
        count = words.count('the')
    print(f"The word 'the' appears {count} times.")
except FileNotFoundError:
    print("Error: 'words.txt' not found.")