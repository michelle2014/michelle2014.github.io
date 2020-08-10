#include <cs50.h>
#include <stdio.h>
#include <math.h>

float get_positive_float(string prompt);

int main(void)
{
    // Prompt user for float
    float dollars = get_positive_float("Change: ");
    
    // Convert dollars to cents
    int cents = round(dollars * 100);
    
    // Use the largest coin possible
    int q = 0;
    int d = 0;
    int n = 0;
    int p = 0;
    int count;
    
    // How many quarters can be used
    while (cents >= 25)
    {
        cents = cents - 25;
        q++;
    }
    
    // How many dimes can be used
    while (cents < 25 && cents >= 10)
    {
        cents = cents - 10;
        d++;
    }
    
    // How many nickels can be used
    while (cents < 10 && cents >= 5)
    {
        cents = cents - 5;
        n++;
    }
    
    // How many pennies can be used
    while (cents < 5 && cents >= 1)
    {
        cents = cents - 1;
        p++;
    }
    
    count = q + d + n + p;
    
    printf("%i\n", count);
}

// Prompt user for positive float
float get_positive_float(string prompt)
{
    float f;
    do
    {
        f = get_float("%s", prompt);
    }
    while (f <= 0);
    return f;
}