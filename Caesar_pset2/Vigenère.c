#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// create of prototype of the function to convert keyword to interger
int shift(char c);

int main(int argc, string argv[])
{
    // check if one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    else
    {    
        // iterate and check if arguments provided are alphabetic
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (!isalpha(argv[1][i]))
            {
                printf("Usage: ./vigenere keyword\n");
                return 1;
            }
        }
    }
    // prompt user for plaintext
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    
    // define length of plaintext and argv[1]  to iterate
    int n = strlen(plaintext);
    int m = strlen(argv[1]) - 1;
    // iterate each character and convert each into an interger, then add the key
    for (int i = 0, j = 0; i < n; i++)
    {
        int p = plaintext[i];
        // add key only to alphabetic
        if (isalpha(p))
        {
            // count the key, if out of the number, recount from 0 again
            int key = shift(argv[1][j]);
            j++;
            if (j > m)
            {
                j = 0;
            }
            // if p is lower case letter
            if (p >= 97 && p <= 122)
            {
                // add the key to the letter provided in plaintext
                int a = (p + key);
                // if the result is out of the range of 122 in ACSII table
                if (a > 122)
                {
                    a = (p + key) % 26;
                    if (a <= 18)
                    {
                        int d = (26 * 4) + a;
                        printf("%c", d);
                    }
                    else if (a > 18 && a <= 25)
                    {
                        int d = (26 * 3) + a;
                        printf("%c", d);
                    }
                }
                else
                {
                    printf("%c", a);
                }
            }
            // if characters are upper case
            else if (p >= 65 && p <= 90)
            {
                // add the key to the letter provided in plaintext
                // and conver to lower case first
                int a = (p + key + 32);
                // if the result is out of the range of 122 in ACSII table
                if (a > 122)
                {
                    a = (p + key + 32) % 26;
                    if (a <= 18)
                    {
                        int d = (26 * 4) + a;
                        // convert back to upper case
                        printf("%c", d - 32);
                    }
                    else if (a > 18 && a <= 25)
                    {
                        int d = (26 * 3) + a;
                        // convert back to upper case
                        printf("%c", d - 32);
                    }
                }
                else
                {
                    printf("%c", a - 32);
                }
            }
        }
       
        // if characters are signs, not alphabetic
        else
        {
            printf("%c", p);
        }
    }
    printf("\n");
}

// define a function to convert keyword to interger
int shift(char c)
{
    // if lower case, then convert to interger
    if (islower(c))
    {
        // then convert to interger
        c = c - 97;
    }
    // if uppwer case, then convert to interger
    else
    {
        c = c - 65;
    }
    // return the interger
    return c;
}


































#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// prototype of a function to convert character to interger
int shift(char c);

int main(int argc, string argv[])
{
    // check if one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    else
    {    
        // iterate and check if arguments provided are alphabetic
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (!isalpha(argv[1][i]))
            {
                printf("Usage: ./vigenere keyword\n");
                return 1;
            }
        }
    }
    // prompt user for plaintext
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    // iterate each character and convert each into an interger, then add the key
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        // count keyword by j
        int j = strlen(argv[1]);
        // whether plaintext is longer than argv[1] or not, key will be i % j
        // and call the function to assign the converted keyword to key
        int key = shift(argv[1][i]);
        int p = plaintext[i];
        // if characters are lower case
        if (p >= 97 && p <= 122)
        {
            // add the key to the letter provided in plaintext
            int a = (p + key);
            // if the result is out of the range of 122 in ACSII table
            if (a > 122)
            {
                a = (p + key) % 26;
                if (a <= 18)
                {
                    int d = (26 * 4) + a;
                    printf("%c", d);
                }
                else if (a > 18 && a <= 25)
                {
                    int d = (26 * 3) + a;
                    printf("%c", d);
                }
            }
            else
            {
                printf("%c", a);
            }
        }
        // if characters are upper case
        else if (p >= 65 && p <= 90)
        {
            // add the key to the letter provided in plaintext and conver to lower case first
            int a = (p + key + 32);
            // if the result is out of the range of 122 in ACSII table
            if (a > 122)
            {
                a = (p + key + 32) % 26;
                if (a <= 18)
                {
                    int d = (26 * 4) + a;
                    // convert back to upper case
                    printf("%c", d - 32);
                }
                else if (a > 18 && a <= 25)
                {
                    int d = (26 * 3) + a;
                    // convert back to upper case
                    printf("%c", d - 32);
                }
            }
            else
            {
                printf("%c", a - 32);
            }
        }
        // if characters are signs, not alphabetic
        else
        {
            printf("%c", p);
        }
    }
    printf("\n");
}
// ceate a function for getting the shift value
int shift(char c)
{
    // convert keyword to all lower case characters
    if (c == tolower('A') || c == tolower('B') || c == tolower('C') || 
        c == tolower('D') || c == tolower('E') || c == tolower('F') || 
        c == tolower('G') || c == tolower('H') || c == tolower('I') || 
        c == tolower('J') || c == tolower('K') || c == tolower('L') || 
        c == tolower('M') || c == tolower('N') || c == tolower('O') || 
        c == tolower('P') || c == tolower('Q') || c == tolower('R') || 
        c == tolower('S') || c == tolower('T') || c == tolower('U') || 
        c == tolower('V') || c == tolower('W') || c == tolower('X') || 
        c == tolower('Y') || c == tolower('Z'))
    {
        // then convert to interger
        c = c - 97;
    }
    // return the interger
    return c;
}










































}
// ceate a function for getting the shift value
int shift(char c)
{
    // convert keyword to all lower case characters
    if (c == tolower('A') || c == tolower('B') || c == tolower('C') || 
        c == tolower('D') || c == tolower('E') || c == tolower('F') || 
        c == tolower('G') || c == tolower('H') || c == tolower('I') || 
        c == tolower('J') || c == tolower('K') || c == tolower('L') || 
        c == tolower('M') || c == tolower('N') || c == tolower('O') || 
        c == tolower('P') || c == tolower('Q') || c == tolower('R') || 
        c == tolower('S') || c == tolower('T') || c == tolower('U') || 
        c == tolower('V') || c == tolower('W') || c == tolower('X') || 
        c == tolower('Y') || c == tolower('Z'))
    {
        // then convert to interger
        c = c - 97;
    }
    // return the interger
    return c;
}



































#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// prototype of a function to convert character to interger
int shift(char c);

int main(int argc, string argv[])
{
    // check if one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    else
    {    
        // iterate and check if arguments provided are alphabetic
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (!isalpha(argv[1][i]))
            {
                printf("Usage: ./vigenere keyword\n");
                return 1;
            }
        }
        // if arguments provided are alphabetic
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (isalpha(argv[1][i]))
            {
                // assign the return value of the function to an interger key
                int key = shift(argv[1][0]);
            }
        }
    }
    // prompt user for plaintext
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    // iterate each character and convert each into an interger, then add the key
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        int key = shift(argv[1][0]);
        int p = plaintext[i];
        printf("%c", p + key);
		// if characters are lower case
        if (p >= 97 && p <= 122)
        {
            int a = (p + key);
            if (a > 122)
            {
                a = (p + key) % 26;
                if (a <= 18)
                {
                    int c = (26 * 4) + a;
                    printf("%c", c);
                }
                else if (a > 18 && a <= 25)
                {
                    int c = (26 * 3) + a;
                    printf("%c", c);
                }
            }
            else
            {
                printf("%c", a);
            }
        }
        // if characters are upper case
        else if (p >= 65 && p <= 90)
        {
            int a = (p + key + 32);
            if (a > 122)
            {
                a = (p + key + 32) % 26;
                if (a <= 18)
                {
                    int c = (26 * 4) + a;
                    printf("%c", c - 32);
                }
                else if (a > 18 && a <= 25)
                {
                    int c = (26 * 3) + a;
                    printf("%c", c - 32);
                }
            }
            else
            {
                printf("%c", a - 32);
            }
        }
        // if characters are signs, not alphabetic
        else
        {
            printf("%c", p);
        }
    }
    printf("\n");
}
// ceate a function for getting the shift value
int shift(char c)
{
    // create an array of 26 letters
    int alpha[26] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 
                    'J', 'K', 'L', 'M', 'N',  'O', 'P', 'Q', 'R', 
                    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
                    };
    // iterate through each letter and convert to interger
    for (int i = 0; i < 26; i++)
    {
        // first lower the letter and then convert
        c = tolower(alpha[i]) -97;
    }
    return c;
}


if (m >= n)
        {
            int key = shift(argv[1][i]);
            int p = plaintext[i];
            // if characters are lower case
            if (p >= 97 && p <= 122)
            {
                int a = (p + key);
                if (a > 122)
                {
                    a = (p + key) % 26;
                    if (a <= 18)
                    {
                        int c = (26 * 4) + a;
                        printf("%c", c);
                    }
                    else if (a > 18 && a <= 25)
                    {
                        int c = (26 * 3) + a;
                        printf("%c", c);
                    }
                }
                else
                {
                    printf("%c", a);
                }
            }
            // if characters are upper case
            else if (p >= 65 && p <= 90)
            {
                int a = (p + key + 32);
                if (a > 122)
                {
                    a = (p + key + 32) % 26;
                    if (a <= 18)
                    {
                        int c = (26 * 4) + a;
                        printf("%c", c - 32);
                    }
                    else if (a > 18 && a <= 25)
                    {
                        int c = (26 * 3) + a;
                        printf("%c", c - 32);
                    }
                }
                else
                {
                    printf("%c", a - 32);
                }
            }
            // if characters are signs, not alphabetic
            else
            {
                printf("%c", p);
            }
        }

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// prototype of a function to convert character to interger
int shift(char c);

int main(int argc, string argv[])
{
    // check if one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    else
    {    
        // iterate and check if arguments provided are alphabetic
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (!isalpha(argv[1][i]))
            {
                printf("Usage: ./vigenere keyword\n");
                return 1;
            }
        }
        // if arguments provided are alphabetic
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (isalpha(argv[1][i]))
            {
                // assign the return value of the function to an interger key
                int key = shift(argv[1][0]);
            }
        }
    }
    // prompt user for plaintext
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    // iterate each character and convert each into an interger, then add the key
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        int key = shift(argv[1][0]);
        int p = plaintext[i];
        printf("%c", p + key);
    }
    printf("\n");
}
// ceate a function for getting the shift value
int shift(char c)
{
    // first lower the letter and then convert
    c = 'A' - 65;
    c = 'a' - 97;
    c = 'B' - 65;
    c = 'b' - 97;
    c = 'C' - 65;
    c = 'c' - 97;
    c = 'D' - 65;
    c = 'd' - 97;
    return c;
}

 c = tolower('C') - 97;
    c = tolower('D') - 97;
    c = tolower('E') - 97;
    c = tolower('F') - 97;
    c = tolower('G') - 97;
    c = tolower('H') - 97;
    c = tolower('I') - 97;
    c = tolower('J') - 97;
    c = tolower('K') - 97;
    c = tolower('L') - 97;
    c = tolower('M') - 97;
    c = tolower('N') - 97;
    c = tolower('O') - 97;
    c = tolower('P') - 97;
    c = tolower('Q') - 97;
    c = tolower('R') - 97;
    c = tolower('S') - 97;
    c = tolower('T') - 97;
    c = tolower('U') - 97;
    c = tolower('V') - 97;
    c = tolower('W') - 97;
    c = tolower('X') - 97;
    c = tolower('Y') - 97;
    c = tolower('Z') - 97;
	
	
	c = 'a' - 97;
    c = 'A' - 65;
    c = 'b' - 97;
    c = 'B' - 65;
    c = 'c' - 97;
    c = 'C' - 65;
    c = 'd' - 97;
    c = 'D' - 65;
    c = 'e' - 97;
    c = 'E' - 65;
    c = 'f' - 97;
    c = 'F' - 65;
    c = 'g' - 97;
    c = 'G' - 65;
    c = 'h' - 97;
    c = 'H' - 65;
    c = 'i' - 97;
    c = 'I' - 65;
    c = 'j' - 97;
    c = 'J' - 65;
    c = 'k' - 97;
    c = 'K' - 65;
    c = 'l' - 97;
    c = 'L' - 65;
    c = 'm' - 97;
    c = 'M' - 65;
    c = 'n' - 97;
    c = 'N' - 65;
    c = 'o' - 97;
    c = 'O' - 65;
    c = 'p' - 97;
    c = 'P' - 65;
    c = 'q' - 97;
    c = 'Q' - 65;
    c = 'r' - 97;
    c = 'R' - 65;
    c = 's' - 97;
    c = 'S' - 65;
    c = 't' - 97;
    c = 'T' - 65;
    c = 'u' - 97;
    c = 'U' - 65;
    c = 'v' - 97;
    c = 'V' - 65;
    c = 'w' - 97;
    c = 'W' - 65;
    c = 'x' - 97;
    c = 'X' - 65;
    c = 'y' - 97;
    c = 'Y' - 65;
    c = 'z' - 97;
    c = 'Z' - 65;
	
	
	
	
	if (c == tolower('A') || c == tolower('B') || c == tolower('C') || 
        c == tolower('D') || c == tolower('E') || c == tolower('F') || 
        c == tolower('G') || c == tolower('H') || c == tolower('I') || 
        c == tolower('J') || c == tolower('K') || c == tolower('L') || 
        c == tolower('M') || c == tolower('N') || c == tolower('O') || 
        c == tolower('P') || c == tolower('Q') || c == tolower('R') || 
        c == tolower('S') || c == tolower('T') || c == tolower('U') || 
        c == tolower('V') || c == tolower('W') || c == tolower('X') || 
        c == tolower('Y') || c == tolower('Z'))
		
		
		// convert keyword to all lower case characters
    if (c == 'A' || c == 'B' || c == 'C' || 
        c == 'D' || c == 'E' || c == 'F' || 
        c == 'G' || c == 'H' || c == 'I' || 
        c == 'J' || c == 'K' || c == 'L' || 
        c == 'M' || c == 'N' || c == 'O' || 
        c == 'P' || c == 'Q' || c == 'R' || 
        c == 'S' || c == 'T' || c == 'U' || 
        c == 'V' || c == 'W' || c == 'X' || 
        c == 'Y' || c == 'Z')
    {
        // then convert to interger
        c = c - 97;
    }
    else if (c == 'a' || c == 'b' || c == 'c' || 
        c == 'd' || c == 'e' || c == 'f' || 
        c == 'g' || c == 'h' || c == 'i' || 
        c == 'j' || c == 'k' || c == 'l' || 
        c == 'm' || c == 'n' || c == 'o' || 
        c == 'p' || c == 'q' || c == 'r' || 
        c == 's' || c == 't' || c == 'u' || 
        c == 'v' || c == 'w' || c == 'x' || 
        c == 'y' || c == 'z')
    {
        // then convert to interger
        c = c - 65;
    }