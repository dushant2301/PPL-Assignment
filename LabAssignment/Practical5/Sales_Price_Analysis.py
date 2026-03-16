# Example data: Inputting prices
price_input = input("Enter prices of sold items separated by space: ")
prices = tuple(float(x) for x in price_input.split())

# a) Print total number of items sold
print(f"a) Total items sold: {len(prices)}")

# b) Print price of cheapest item
print(f"b) Cheapest item: {min(prices)}")

# c) Print price of costliest item
costliest = max(prices)
print(f"c) Costliest item: {costliest}")

# d) Print price list in ascending order
print(f"d) Prices in ascending order: {sorted(prices)}")

# e) Print the number of costliest items sold
# This counts how many times the maximum price appears
count_costliest = prices.count(costliest)
print(f"e) Number of costliest items sold: {count_costliest}")