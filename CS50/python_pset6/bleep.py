from cs50 import get_string
from sys import argv
import sys


def main():

    # define a set to contain banned words
    words = set()

    # check command-line argument
    if len(sys.argv) != 2:
        sys.exit("Usage: python bleep.py dictionary")

    # open banned text file to read
    file = open(sys.argv[1], "r")

    # scan each line in file and add line to words
    for line in file:
        words.add(line.rstrip("\n"))

    # after adding, close file
    file.close()

    # Prompt user for a message
    message = get_string("What message would you like to censor?")

    # split message into separate words
    messageSplit = message.split()

    # iterate each word in message and lower case
    for i in range(len(messageSplit)):
        messageSplit[i].lower()

        # compare each word in banned text with each split message
        if (messageSplit[i].lower() in words):

            # if split message in words, print * for length of it of times
            print("*" * len(messageSplit[i]), end=" ")

            # if not in words, print original word
        else:
            print(messageSplit[i], end=" ")
    print()


if __name__ == "__main__":
    main()