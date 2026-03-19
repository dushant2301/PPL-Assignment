with open("source.txt", "r") as f1, open("dest.txt", "w") as f2:
    f2.write(f1.read().upper())