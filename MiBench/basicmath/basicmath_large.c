#include "snipmath.h"
#include <math.h>
#include <marker.h>

/* The printf's may be removed to isolate just the math calculations */

int main(void)
{
        add_marker(START);
        double  a1 = 1.0, b1 = -10.5, c1 = 32.0, d1 = -30.0;
        double  x[3];
        double X;
        int     solutions;
        int i;
        unsigned long l = 0x3fed0169L;
        struct int_sqrt q;
        long n = 0;

        add_marker(1);
        /* solve soem cubic functions */
        printf("********* CUBIC FUNCTIONS ***********\n");
        /* should get 3 solutions: 2, 6 & 2.5   */
        SolveCubic(a1, b1, c1, d1, &solutions, x);  
        printf("Solutions:");
        for(i=0;i<solutions;i++)
        {
                add_marker(2);
                printf(" %f",x[i]);
        }
        printf("\n");

        a1 = 1.0; b1 = -4.5; c1 = 17.0; d1 = -30.0;
        /* should get 1 solution: 2.5           */
        SolveCubic(a1, b1, c1, d1, &solutions, x);  
        printf("Solutions:");
        for(i=0;i<solutions;i++)
        {
                add_marker(3);
                printf(" %f",x[i]);
        }
        printf("\n");

        a1 = 1.0; b1 = -3.5; c1 = 22.0; d1 = -31.0;
        SolveCubic(a1, b1, c1, d1, &solutions, x);
        printf("Solutions:");
        for(i=0;i<solutions;i++)
        {
                add_marker(4);
                printf(" %f",x[i]);
        }
        printf("\n");

        a1 = 1.0; b1 = -13.7; c1 = 1.0; d1 = -35.0;
        SolveCubic(a1, b1, c1, d1, &solutions, x);
        printf("Solutions:");
        for(i=0;i<solutions;i++)
        {
                add_marker(5);
                printf(" %f",x[i]);
        }
        printf("\n");

        a1 = 3.0; b1 = 12.34; c1 = 5.0; d1 = 12.0;
        SolveCubic(a1, b1, c1, d1, &solutions, x);
        printf("Solutions:");
        for(i=0;i<solutions;i++)
        {
                add_marker(6);
                printf(" %f",x[i]);
        }
        printf("\n");

        a1 = -8.0; b1 = -67.89; c1 = 6.0; d1 = -23.6;
        SolveCubic(a1, b1, c1, d1, &solutions, x);
        printf("Solutions:");
        for(i=0;i<solutions;i++)
        {
                add_marker(7);
                printf(" %f",x[i]);
        }
        printf("\n");

        a1 = 45.0; b1 = 8.67; c1 = 7.5; d1 = 34.0;
        SolveCubic(a1, b1, c1, d1, &solutions, x);
        printf("Solutions:");
        for(i=0;i<solutions;i++)
        {
                add_marker(8);
                printf(" %f",x[i]);
        }
        printf("\n");

        a1 = -12.0; b1 = -1.7; c1 = 5.3; d1 = 16.0;
        SolveCubic(a1, b1, c1, d1, &solutions, x);
        printf("Solutions:");
        for(i=0;i<solutions;i++)
        {
                add_marker(9);
                printf(" %f",x[i]);
        }
        printf("\n");

        /* Now solve some random equations */
        for(a1=1;a1<10;a1+=1) {
                add_marker(10);
                for(b1=10;b1>0;b1-=.25) {
                        add_marker(11);
                        for(c1=5;c1<15;c1+=0.61) {
                                add_marker(12);
                                for(d1=-1;d1>-5;d1-=.451) {
                                        add_marker(13);
                                        SolveCubic(a1, b1, c1, d1, &solutions, x);  
                                        printf("Solutions:");
                                        for(i=0;i<solutions;i++)
                                                printf(" %f",x[i]);
                                        printf("\n");
                                }
                        }
                }
        }


        printf("********* INTEGER SQR ROOTS ***********\n");
        /* perform some integer square roots */
        for (i = 0; i < 100000; i+=2)
        {
                add_marker(100);
                usqrt(i, &q);
                // remainder differs on some machines
                // printf("sqrt(%3d) = %2d, remainder = %2d\n",
                printf("sqrt(%3d) = %2d\n",
                                i, q.sqrt);
        }
        printf("\n");
        for (l = 0x3fed0169L; l < 0x3fed4169L; l++)
        {
                add_marker(101);
                usqrt(l, &q);
                //printf("\nsqrt(%lX) = %X, remainder = %X\n", l, q.sqrt, q.frac);
                printf("sqrt(%lX) = %X\n", l, q.sqrt);
        }


        printf("********* ANGLE CONVERSION ***********\n");
        /* convert some rads to degrees */
        /*   for (X = 0.0; X <= 360.0; X += 1.0) */
        for (X = 0.0; X <= 360.0; X += .001)
        {
                add_marker(102);
                printf("%3.0f degrees = %.12f radians\n", X, deg2rad(X));
        }
        puts("");
        /*   for (X = 0.0; X <= (2 * PI + 1e-6); X += (PI / 180)) */
        for (X = 0.0; X <= (2 * PI + 1e-6); X += (PI / 5760))
        {
                add_marker(103);
                printf("%.12f radians = %3.0f degrees\n", X, rad2deg(X));
        }

        add_marker(END);
        return 0;
}
