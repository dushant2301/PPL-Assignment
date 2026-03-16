# Taking input from the user and converting it to a tuple of integers
user_input = input("Enter a series of integers separated by space: ")
my_tuple = tuple(int(x) for x in user_input.split())

# a) Print total number of items
print(f"a) Total items: {len(my_tuple)}")

# b) Print the last item
print(f"b) Last item: {my_tuple[-1]}")

# c) Print elements in reverse order
print(f"c) Reversed order: {my_tuple[::-1]}")

# d) Check if 5 exists in the Tuple
print(f"d) Contains 5? {'Yes' if 5 in my_tuple else 'No'}")

# e) Remove first/last, sort remaining, and print
# We slice from index 1 to -1 (exclusive of the last item)
remaining_items = list(my_tuple[1:-1])
remaining_items.sort()
print(f"e) Remaining sorted items: {tuple(remaining_items)}")