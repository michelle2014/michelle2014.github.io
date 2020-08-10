from cs50 import get_float, get_int

# Prompt user for float
while True:
    dollars = get_float("Change: ")
    if dollars > 0:
        break

# Convert dollars to cents
cents = round(dollars * 100)

# Use the largest coin possible
q = 0
d = 0
n = 0
p = 0
count = 0

# How many quarters can be used
while (cents >= 25):
    cents = cents - 25
    q += 1

# How many dimes can be used
while (cents < 25 and cents >= 10):
    cents = cents - 10
    d += 1

# How many nickels can be used
while (cents < 10 and cents >= 5):
    cents = cents - 5
    n += 1

# How many pennies can be used
while (cents < 5 and cents >= 1):
    cents = cents - 1
    p += 1

count = q + d + n + p

print(count)