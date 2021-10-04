// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    int16_t buffer, buffer2;
     
     
    
    
    


   uint8_t header[HEADER_SIZE];

   fread(header, sizeof(header), 1, input);

   fwrite(header,sizeof(header),1, output);


   while(fread(&buffer, sizeof(buffer), 1, input))
   {
       
          buffer2 = buffer * factor;

       fwrite(&buffer2, sizeof(buffer), 1, output);
   }


    // Close files
    fclose(input);
    fclose(output);
}
