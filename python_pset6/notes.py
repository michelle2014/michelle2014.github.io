# find and execute the interpreter for you
#!/usr/bin/env python3

# Linux command line
chmod a+x <file>



# set example 1

# Words in dictionary
words = set()

def check(word):
    """Return true if word is in dictionary else false"""
    return word.lower() in words

def load(dictionary):
    """Load dictionary into memory, returning true if successful else false"""
    file = open(dictionary, "r")
    for line in file:
        words.add(line.rstrip("\n"))
    file.close()
    return True

def size():
    """Returns number of words in dictionary if loaded else 0 if not yet loaded"""
    return len(words)

def unload():
    """Unloads dictionary from memory, returning true if successful else false"""
    return True
	








# list examples

nums = [x for x in range(500)]

nums = list()

nums = [1, 2, 3, 4]
nums.append(5)

nums = [1, 2, 3, 4]
nums.insert(4, 5)

nums = [1, 2, 3, 4]
nums[len(nums):]=[5]






# list example 1

from cs50 import get_int

numbers = []

# Prompt for numbers (until EOF)
while True:

    # Prompt for number
    number = get_int("number: ")

    # Check for EOF
    if not number:
        break

    # Check whether number is already in list
    if number not in numbers:

        # Add number to list
        numbers.append(number)

# Print numbers
print()
for number in numbers:
    print(number)

# list example 2

from cs50 import get_string

# Space for students
students = []

# Prompt for students' names and dorms
for i in range(3):
    name = get_string("name: ")
    dorm = get_string("dorm: ")
    students.append({"name": name, "dorm": dorm})

# Print students' names and dorms
for student in students:
    print(f"{student['name']} is in {student['dorm']}.")









# dictionary (key-value pairs, similar to hash table) example 1

pizzas = {
	"cheese": 9, 
	"pepperoni": 10, 
	"vegetables": 11, 
	"buffalo chicken": 12
}

pizzas["cheese"] = 8

if pizzas["vegetables"] < 12: 
	# do something

pizzas["bacon"] = 14

for pie in pizzas: 
	# use pie in here as a stand-in for "i"

# you are not going to get the things in original order
for pie, price in pizzas.items(): 
	print(price)

for pie, price in pizzas.items(): 
	print("A whole {} pizza costs ${}".format(pie, price))

for pie, price in pizzas.items(): 
print("A whole" + pie + " pizza costs $" + str(price))











# tuple example 1
# a list of tuples
presidents = [
	("George Washington", 1789), 
	("John Adams", 1797),
	("Thomas Jefferson", 1801),
	("James Madison", 1809)
]

for prez, year in presidents: 
	print("In {1}, {0} took office".format(prez, year))







# objects (similiar to C structures) have properties and methods
object.method()

class Student():

	def __init__(self, name, id):
		self.name = name
		self.id = id
	
	def changeID(self, id):
		self.id = id

	def print(self):
		print("{} - {}".format(self.name, self.id))

jane = Student("Jane", 10)
jane.print()
jane.changeID(11)
jane.print()









# range example 1
# counting from 0, 2, 4, 6, all the way to 98
for x in range(0, 100, 2):
	print(x)