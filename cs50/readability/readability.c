#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
int main(void)
{



    string name = get_string("Text:");
    float sentence = 0, words = 1,symbols = 0,letters = 0,index;
    float L, S;



       for (int i = 0; i < strlen(name); i++)  
    {
         if(name[i] == ' ' && name[i+1]!=' ')
         words++;
          if(name[i]!='\0' && (name[i+1] == '!'|| name[i+1] == '.' || name[i+1] == '?'))
         sentence++;
         if(isalpha(name[i]))
           letters++;

    }

    L = letters/ words * 100;
    S = sentence/ words * 100;



   index = 0.0588 * L - 0.296 * S - 15.8;
   if(index>0 && index < 16)
   printf("Grade %.f\n", index);
   else  if( index > 16)
   printf("Grade 16+\n");
   else
   printf("Before Grade 1\n");
}