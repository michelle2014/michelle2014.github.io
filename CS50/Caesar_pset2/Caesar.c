#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // check if one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else
    {    
        // iterate and check if arguments provided are digits
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (argv[1][i] != '0' && argv[1][i] != '1' && argv[1][i] != '2' && argv[1][i] != '3'
			&& argv[1][i] != '4' && argv[1][i] != '5' && argv[1][i] != '6' && argv[1][i] != '7'
			&& argv[1][i] != '8' && argv[1][i] != '9')
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        
        // convert string to number if arguments provided are digits
        for (int i = 0, n = strlen(argv[1]); i < n; i++)
        {
            if (argv[1][i] >= '0' && argv[1][i] <= '9')
            {
                int k = atoi(argv[1]);
            }
        }
    }
    
    // prompt user for plaintext
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    
    // iterate each character and convert each into an interger, then add the key
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        int k = atoi(argv[1]);
        int p = plaintext[i];
        // if characters are lower case
        if (p >= 97 && p <= 122)
        {
            int a = (p + k);
            if (a > 122)
            {
                a = (p + k) % 26;
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
            int a = (p + k + 32);
            if (a > 122)
            {
                a = (p + k + 32) % 26;
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


