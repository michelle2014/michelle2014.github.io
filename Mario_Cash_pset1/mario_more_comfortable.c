#include <cs50.h>
#include <stdio.h>

int get_height_int(string prompt);

int main(void)
{
    // Prompt user for height
    int i = get_height_int("Height: ");
    
    // Print pyramid
    for (int j = 1; j <= i; j++)
    {
        
        for (int k = 1; k <= i - j; k++)
        {
            printf(" ");
        }
        
        for (int k = 1; k <= j; k++)
        {
            printf("#");
        }
        printf("  ");
        
        for (int k = 1; k <= j; k++)
        {
            printf("#");
        }
        
        printf("\n");
    }
}

// If height is less than 1 or greater than 8 or is not an interger, then prompt for height again
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
