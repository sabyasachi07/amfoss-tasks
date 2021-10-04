#include <cs50.h>
#include <stdio.h>
#include <math.h>
int main(void)
{
long int m, k;
long int count = 0,n, a, sum1 = 0, sum2 = 0, i =0, r, r2, r3 , num, rev = 0, remainder;;


    do
  {
      m = get_long("Number:");
  }
    while (m < 1);
k = m;
n = m;
num = m;

while(k!=0)
{
   a = k %10;
   count++;
   k/=10;
}


while(n!=0)
{


i++;
  if(i%2==0) {
     r=n%10;
                                                                            //4003600000000014
     if(2*r > 9) {
     r2 =(2*r) %10;
     r3=(2*r)/10;

     sum1 = sum1 + r3 +r2;
     }
     else {
        sum1+=2*r;
     }



    }
  else {
    r=n%10;
    sum2+=r;

}
 n/=10;
}





while (num!= 0) {
        remainder = num % 10;
        rev = rev * 10 + remainder;
        num /= 10;
}

int startingdigits = m / (long) (pow (10, count- 2));


if( sum1>0 && sum2> 0)
{
if(((sum1+sum2)%10==0 && (rev %10 == 4)) && ((count==16) || (count==13)))
    printf("VISA\n");
else if(((sum1+sum2)%10==0 && (startingdigits >= 51 && startingdigits <= 55)) && (count==16) )
     printf("MASTERCARD\n");

else if( ((sum1+sum2)%10== 0 && (rev % 100 == 73)) && ((count==16) || (count==15)) )
     printf("AMEX\n");
else
    printf("INVALID\n");

}






}