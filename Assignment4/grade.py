try:
    with open('grades.txt', 'r') as f_in, open('passed.txt', 'w') as f_out:
        for line in f_in:
            parts = line.strip().split()
            if len(parts) >= 2:
                name = parts[0]
                grade = parts[1]
                if grade in ['A', 'B']:
                    f_out.write(name + "\n")
    print("Successfully created 'passed.txt' with eligible students.")
except FileNotFoundError:
    print("Error: 'grades.txt' not found.")