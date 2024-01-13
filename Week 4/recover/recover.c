#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover card.raw\n");
        return 1;
    }

    // Read the memory card
    FILE *memory = fopen(argv[1], "r");
    if (memory == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Define temporary variables
    uint8_t *buffer = malloc(512);
    FILE *file;
    int found = 0;
    char name[8] = "000.jpg";

    // Loop until all the data in the memory card is covered
    while (fread(buffer, 1, 512, memory) != 0)
    {
        // Close the last file and write to a new file if a JPEG header is found
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0))
        {
            if (found != 0)
            {
                fclose(file);
            }
            sprintf(name, "%03i.jpg", found);
            file = fopen(name, "w");
            found++;
        }
        if (found != 0)
        {
            fwrite(buffer, 1, 512, file);
        }
    }

    // Free allocated memory
    free(buffer);

    // Close files
    fclose(file);
    fclose(memory);
}
