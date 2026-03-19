src = input("Source file: ")
dst = input("Destination file: ")

with open(src, "r") as f:
    lines = [line for line in f if not line.strip().startswith("#")]

with open(dst, "w") as f:
    f.writelines(lines)

print("Source:\n", open(src).read(), "\nDestination:\n", open(dst).read())