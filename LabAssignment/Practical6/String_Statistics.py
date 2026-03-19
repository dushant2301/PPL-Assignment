text = input("Enter a string: ")
vowels = "aeiouAEIOU"
v_count = c_count = s_count = l_count = 0

for char in text:
    if char.islower(): l_count += 1
    if char.isspace(): s_count += 1
    if char.isalpha():
        if char in vowels: v_count += 1
        else: c_count += 1

print(f"Vowels: {v_count}, Consonants: {c_count}, Spaces: {s_count}, Lowercase: {l_count}")