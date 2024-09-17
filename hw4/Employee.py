class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    # define a method to chage the salary by a percentage
    def change_salary(self, percent):
        self.salary += self.salary * percent
        return self.salary    
    
ella = Employee("Ella", 50000)

# increase ella's salary by 10%
ella.salary = ella.change_salary(.10)

print(f'{ella.name}\'s salary is now ${int(ella.salary)}.')
