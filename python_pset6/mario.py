# import a library for getting interger
from cs50 import get_int

# prompt user for height
while True:
    h = get_int("Height: ")
    # if height is less than 1 or higher than 8, prompt user for height again
    if h >= 1 and h <= 8:
        break

# define an interger to print one more # each line each time
j = 1
j <= h

# define an interger to print one less space each line each time
k = h - 1
k >= 0

# define the line loop for printing
for i in range(h):
    # print space without new line then print #
    print(" " * k, end="")
    k -= 1
    # print # one more each line
    print("#" * j)
    j += 1