#include <cs50.h>
#include <stdio.h>

int get_height_int(string prompt);

int main(void)
{
    // Prompt user for height
    int i = get_height_int("Height: ");
    
    for (int j = 1; j <= i; j++)
    {
        // Print left-align space
        for (int k = 1; k <= i - j; k++)
        {
            printf(" ");
        }
        // Print right-align hashes
        for (int k = 1; k <= j; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}

// If height is less than 1 or higher than 8 or not a interger, then prompt height again
int get_height_int(string prompt)
{
    int n;
    do
    {
        n = get_int("%s", prompt);
    }
    while (n < 1 || n > 8);
    return n;
}