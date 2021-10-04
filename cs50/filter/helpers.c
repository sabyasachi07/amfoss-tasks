#include "helpers.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    for (int i =0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
            {

            float blue = image[i][j].rgbtBlue;
            float green = image[i][j].rgbtGreen;
            float red = image[i][j].rgbtRed;           
            int average = round((red + blue + green) / 3);            
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i]  [j].rgbtRed = average;

            }
        }
    }


// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    
for (int i = 0; i < height; i++)
{
    for (int j = 0; j < width; j++)
    {
        int red = image[i][j].rgbtRed;
        int blue = image[i][j].rgbtBlue;
        int green = image[i][j].rgbtGreen;

        int sepiaRed = round(0.393 * red + 0.769 * green + 0.189 * blue)  ;


        int sepiaGreen = round(0.349 * red + 0.686 * green + 0.168 * blue) ;


        int sepiaBlue = round(0.272 * red + 0.534 * green + 0.131 * blue) ;




        if (sepiaRed >= 256)
            {
                sepiaRed = 255;

            }

        if (sepiaGreen  >= 256)
            {
                sepiaGreen = 255;

            }


        if (sepiaBlue  >= 256)
            {
            sepiaBlue= 255;

            }
        image[i][j].rgbtRed = sepiaRed;
        image[i][j].rgbtBlue = sepiaBlue;
        image[i][j].rgbtGreen = sepiaGreen;
      }
   }
}
// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{

     for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }



}




// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

 RGBTRIPLE temp[height][width];
 int avg;
    for (int i =0; i < height; i++) {

        for(int j = 0; j < width; j++) {

            int sumRed = 0, sumBlue = 0, sumGreen = 0, counter = 0;


           for(int k = -1; k < 2; k++) {

               for(int l = -1; l < 2; l++) {

                   if(i+k<0 || i+k > height-1) {
                       continue;
                   }

                   if(j+l<0 || j+l > height-1) {
                       continue;
                   }

                  sumRed+=image[i+k][j+l].rgbtRed;
                  sumBlue+=image[i+k][j+l].rgbtBlue;
                  sumGreen+=image[i+k][j+l].rgbtGreen;
                  counter++;
                }
              

             }
              temp[i][j].rgbtRed = round(sumRed/counter);
              temp[i][j].rgbtGreen = round(sumGreen/counter);
              temp[i][j].rgbtBlue = round(sumBlue/counter);
       
         }
    }

        for (int i =0; i < height; i++) {

        for(int j = 0; j < width; j++) {
            
        image[i][j].rgbtRed = temp[i][j].rgbtRed;
        image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
        image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
        }
}