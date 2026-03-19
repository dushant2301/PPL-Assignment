def capitalize_input():
    print("Enter lines (press Enter on empty line to finish):")
    lines = []
    while True:
        s = input()
        if s: lines.append(s.upper())
        else: break
    for line in lines: print(line)

capitalize_input()