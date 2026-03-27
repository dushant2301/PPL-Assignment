import pandas as pd

data = {
    'Title': ['The Hobbit', 'Deep Work', 'Python Crash Course', 'Atomic Habits'],
    'Author': ['J.R.R. Tolkien', 'Cal Newport', 'Eric Matthes', 'James Clear'],
    'Price': [15.99, 14.50, 25.00, 14.50],
    'Publishing_House': ['Allen & Unwin', 'Grand Central', 'No Starch Press', 'Penguin'],
    'Publication_Year': [1937, 2016, 2019, 2018]
}

df = pd.DataFrame(data)
df.to_csv('books.csv', index=False)
print("File 'books.csv' has been created! You can run your main script now.")
try:
    df = pd.read_csv('books.csv')

    # a) Print the complete report in tabular form
    print("--- Complete Book Report ---")
    print(df.to_string(index=False))
    print("\n")

    # b) Print list of books by a given author
    author_name = input("Enter Author name to search: ")
    author_books = df[df['Author'].str.contains(author_name, case=False)]
    print(f"Books by {author_name}:\n", author_books[['Title', 'Price']])

    # c) Print list of books by a given publishing house
    pub_house = input("\nEnter Publishing House to search: ")
    pub_books = df[df['Publishing_House'].str.contains(pub_house, case=False)]
    print(f"Books from {pub_house}:\n", pub_books[['Title', 'Author']])

    # d) Print Titles of cheapest & costliest books
    cheapest = df.loc[df['Price'].idxmin(), 'Title']
    costliest = df.loc[df['Price'].idxmax(), 'Title']
    print(f"\nCheapest Book: {cheapest}")
    print(f"Costliest Book: {costliest}")

    # e) Sort by Year of Publication
    sorted_df = df.sort_values(by='Publication_Year')
    print("\n--- Books Sorted by Publication Year ---")
    print(sorted_df[['Title', 'Publication_Year']])

except FileNotFoundError:
    print("Error: 'books.csv' not found. Please create the file first.")