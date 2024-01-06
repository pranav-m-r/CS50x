// Encrypts messages using a substitution cipher
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

string encipher(string, string);

int main(int argc, string argv[])
{
    // Checks if exactly one key has been provided
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    // Gets the key
    string key = argv[1];
    int length = strlen(key);

    // Validates the key
    if (length != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    for (int i = 0; i < length; i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }

        for (int j = i + 1; j < length; j++)
        {
            if (key[i] == key[j])
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }

    // Gets plaintext
    string plaintext = get_string("plaintext: ");

    // Encipher
    string ciphertext = encipher(plaintext, key);

    // Print ciphertext
    printf("ciphertext: %s\n", ciphertext);
}

string encipher(string plaintext, string key)
{
    string ciphertext = plaintext;
    for (int i = 0, textlength = strlen(plaintext); i < textlength; i++)
    {
        if (isalpha(plaintext[i]))
        {
            if (isupper(plaintext[i]))
            {
                ciphertext[i] = toupper(key[plaintext[i] - 65]);
            }
            else
            {
                ciphertext[i] = tolower(key[plaintext[i] - 97]);
            }
        }
    }
    return ciphertext;
}
