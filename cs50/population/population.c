#include <cs50.h>
#include <stdio.h>
int main(void)
{
    int n, m, years = 0;

    do
  {
      m = get_int("Start size:");
  }
    while (m < 9);

    do
  {
      n = get_int("End size:");
  }
    while (n < m);

  while(m < n)
  {

      m = m+m/3-m/4;
      years++;
  }



  printf("Years: %i\n", years);

}


