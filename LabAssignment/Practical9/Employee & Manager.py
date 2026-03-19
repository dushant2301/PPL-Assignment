class Employee:
    def get_info(self):
        self.name = input("Name: ")
        self.age = input("Age: ")
        self.salary = input("Salary: ")

class Manager(Employee):
    def display(self):
        print(f"Mgr: {self.name} | Age: {self.age} | Salary: {self.salary}")

managers = []
for _ in range(10):
    m = Manager()
    m.get_info()
    managers.append(m)

for m in managers: m.display()