// Recreates the pyramid of blocks from Super Mario Brothers
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Gets the height from the user
    int height;
    do
    {
        height = get_int("Height : ");
    }
    while (height < 1 || height > 8);

    // Creates the pyramid
    for (int i = 1; i <= height; i++)
    {
        for (int j = 0; j < (height - i); j++)
        {
            printf(" ");
        }
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        printf("  ");
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
