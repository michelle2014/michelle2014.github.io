import sys
from cs50 import get_string

# check if one command-line argument
if len(sys.argv) != 2:
    sys.exit("Usage: python caesar.py k")

# prompt user for plaintext
plaintext = get_string("plaintext: ")
print("ciphertext: ", end="")

# iterate each character and convert each into an interger, then add the key
for c in plaintext:
    k = int(sys.argv[1])
    p = ord(c)
    # if characters are lower case
    if (p >= 97 and p <= 122):
        a = (p + k)
        if (a > 122):
            a = (p + k) % 26
            if (a <= 18):
                d = (26 * 4) + a
                print(chr(d), end="")
            elif (a > 18 and a <= 25):
                d = (26 * 3) + a
                print(chr(d), end="")
        else:
            print(chr(a), end="")
    # if characters are upper case
    elif (p >= 65 and p <= 90):
        a = (p + k + 32)
        if (a > 122):
            a = (p + k + 32) % 26
            if (a <= 18):
                d = (26 * 4) + a
                print(chr(d - 32), end="")
            elif (a > 18 and a <= 25):
                d = (26 * 3) + a
                print(chr(d - 32), end="")
        else:
            print(chr(a - 32), end="")
    # if characters are signs, not alphabetic
    else:
        print(chr(p), end="")
print()