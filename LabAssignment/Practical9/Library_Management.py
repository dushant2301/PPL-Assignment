class Book:
    def __init__(self, title): self.title = title; self.is_lent = False

class Member:
    def __init__(self, name): self.name = name

class Library:
    def __init__(self): self.books = []
    
    def add(self, title): self.books.append(Book(title))
    
    def lend(self, title):
        for b in self.books:
            if b.title == title and not b.is_lent:
                b.is_lent = True; return "Lent!"
        return "Not available"

# Menu-driven logic
lib = Library()
while True:
    print("\n1.Add 2.Lend 3.Exit")
    ch = input("Choice: ")
    if ch == '1': lib.add(input("Title: "))
    elif ch == '2': print(lib.lend(input("Title: ")))
    else: break