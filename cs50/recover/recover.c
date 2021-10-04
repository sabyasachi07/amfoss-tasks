#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>



int main(int argc, char *argv[])
{
     if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
int size = 512;
int file_size = 0, open = 0;
char jpeg[8];
FILE *output = NULL;
int jpeg_num = 0;

uint8_t buffer[size], BYTE;

while(fread(&buffer, 512, 1, input)==1)
{

if(buffer[0]== 0xff && buffer[1]==0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0 ) {
  if(open == 1)
   {
     fclose(output);
     open = 0;
   }

sprintf(jpeg, "%03i.jpg", jpeg_num++);
output = fopen(jpeg, "w");
open = 1;
}

if(open != 0) {
fwrite(&buffer, 512, 1, output);
}
}


if(open)
fclose(output);
fclose(input);
}