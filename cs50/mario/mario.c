#include <cs50.h>
#include <stdio.h>
int main(void)
{
  int n, m, i;
  bool b;

    do
  {

    n = get_int("Height:");

if(n>0 && n < 9)
   b = false;
else
   b =true;

  }
    while (b);


m =n;
while(m>0)
{
    for(i= 1; i<m; i++)
    {
        printf(" ");
    }

   for(int k = n; k>=m; k--)
    {
        printf("#");
    }
 printf("\n");
 m--;
}
}