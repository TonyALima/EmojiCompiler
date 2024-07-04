#include <stdio.h>

int main()
{
    float  r=5.1 , p=3.141592654 , v;
    float  c=r * r * r;

    v= (4.0 / 3.0) * p * c;

    printf("Volume da esfera de raio %f: %f\n",r,v);
    
    return  0;
}
