# Create a class called Pet with attributes name and age. Implement a method within the class to calculate the age of the pet in equivalent human years. Additionally, create a class variable called species to store the species of the pet. Implement a method within the class that takes the species of the pet as input and returns the average lifespan for that species.
class Pet:
    # define the class variable
    species = "unknown"
    # define the constructor
    def __init__(self, name, age):
        self.name = name
        self.age = age
    # define a method to calculate the age of the pet in equivalent human years
    def human_years(self):
        return self.age * 7
    # define a method to return the average lifespan for the species of the pet
    def lifespan(self):
        species = self.species
        if species == "dog":
            return 13
        elif species == "cat":
            return 15
        elif species == "bird":
            return 7
        
# Instantiate three objects of the Pet class with different names, ages, and species.
toby = Pet("Toby", 9)
toby.species = "dog"

cali = Pet("Cali", 4)
cali.species = "cat"

skye = Pet("Skye", 1)
skye.species = "bird"

print()
# Calculate and print the age of each pet in human years.
print(f'Toby is {toby.human_years()} years old in human years.')
print(f'Cali is {cali.human_years()} years old in human years.')
print(f'Skye is {skye.human_years()} years old in human years.')

print()
# Use the average lifespan function to retrieve and print the average lifespan for each pet's species.   
print(f'The average lifespan for Toby\'s species is {toby.lifespan()} years.')
print(f'The average lifespan for Cali\'s species is {cali.lifespan()} years.')
print(f'The average lifespan for Skye\'s species is {skye.lifespan()} years.') 