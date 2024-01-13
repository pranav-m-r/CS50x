#include "helpers.h"
#include <math.h>

// Define swap function
void swapPixels(RGBTRIPLE *a, RGBTRIPLE *b);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float average = 0.0;
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green, and blue
            average = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;
            // Update pixel values
            image[i][j].rgbtRed = round(average);
            image[i][j].rgbtGreen = round(average);
            image[i][j].rgbtBlue = round(average);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float sepiaRed = 0.0;
    float sepiaGreen = 0.0;
    float sepiaBlue = 0.0;
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia values
            sepiaRed = 0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue;
            sepiaGreen = 0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue;
            sepiaBlue = 0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue;
            // Update pixel with sepia values
            image[i][j].rgbtRed = (round(sepiaRed) <= 255) ? round(sepiaRed) : 255;
            image[i][j].rgbtGreen = (round(sepiaGreen) <= 255) ? round(sepiaGreen) : 255;
            image[i][j].rgbtBlue = (round(sepiaBlue) <= 255) ? round(sepiaBlue) : 255;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int temp = 0;
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Swap pixels
            swapPixels(&image[i][j], &image[i][width - j - 1]);
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    // Blur pixels
    float sumRed = 0.0;
    float sumGreen = 0.0;
    float sumBlue = 0.0;
    float count = 0.0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sumRed = image[i][j].rgbtRed;
            sumGreen = image[i][j].rgbtGreen;
            sumBlue = image[i][j].rgbtBlue;
            count = 1;
            if (i != 0)
            {
                if (j != 0)
                {
                    sumRed += image[i - 1][j - 1].rgbtRed;
                    sumGreen += image[i - 1][j - 1].rgbtGreen;
                    sumBlue += image[i - 1][j - 1].rgbtBlue;
                    count++;
                }
                if (j != width - 1)
                {
                    sumRed += image[i - 1][j + 1].rgbtRed;
                    sumGreen += image[i - 1][j + 1].rgbtGreen;
                    sumBlue += image[i - 1][j + 1].rgbtBlue;
                    count++;
                }
                sumRed += image[i - 1][j].rgbtRed;
                sumGreen += image[i - 1][j].rgbtGreen;
                sumBlue += image[i - 1][j].rgbtBlue;
                count++;
            }
            if (i != height - 1)
            {
                if (j != 0)
                {
                    sumRed += image[i + 1][j - 1].rgbtRed;
                    sumGreen += image[i + 1][j - 1].rgbtGreen;
                    sumBlue += image[i + 1][j - 1].rgbtBlue;
                    count++;
                }
                if (j != width - 1)
                {
                    sumRed += image[i + 1][j + 1].rgbtRed;
                    sumGreen += image[i + 1][j + 1].rgbtGreen;
                    sumBlue += image[i + 1][j + 1].rgbtBlue;
                    count++;
                }
                sumRed += image[i + 1][j].rgbtRed;
                sumGreen += image[i + 1][j].rgbtGreen;
                sumBlue += image[i + 1][j].rgbtBlue;
                count++;
            }
            if (j != 0)
            {
                sumRed += image[i][j - 1].rgbtRed;
                sumGreen += image[i][j - 1].rgbtGreen;
                sumBlue += image[i][j - 1].rgbtBlue;
                count++;
            }
            if (j != width - 1)
            {
                sumRed += image[i][j + 1].rgbtRed;
                sumGreen += image[i][j + 1].rgbtGreen;
                sumBlue += image[i][j + 1].rgbtBlue;
                count++;
            }
            copy[i][j].rgbtRed = round(sumRed / count);
            copy[i][j].rgbtGreen = round(sumGreen / count);
            copy[i][j].rgbtBlue = round(sumBlue / count);
        }
    }
    // Copy the edits back to original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }
    return;
}

// Swap pixels
void swapPixels(RGBTRIPLE *a, RGBTRIPLE *b)
{
    RGBTRIPLE temp = *a;
    *a = *b;
    *b = temp;
    return;
}
