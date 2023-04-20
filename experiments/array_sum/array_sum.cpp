#include <omp.h>
#include <cstdlib>
#include <chrono>
#include <iostream>

#define SIZE 1000000
#define ITERS 10

void compute_sum(int* a, int* b, int* c)
{
        #pragma omp parallel num_threads(16)
        {
                for(int i = 0; i < SIZE; i++)
                {
                        #pragma omp task
                        c[i] += a[i] + b[i];
                }
        }
}


int main()
{
        int *a, *b, *c;
        posix_memalign((void**) &a, 64, SIZE * sizeof(int));
        posix_memalign((void**) &b, 64, SIZE * sizeof(int));
        posix_memalign((void**) &c, 64, SIZE * sizeof(int));
        
        #pragma omp parallel for num_threads(16)
        for(int i = 0; i < SIZE; i++)
        {
                a[i] = i;
                b[i] = i;
                c[i] = i;
        }

        auto start = std::chrono::high_resolution_clock::now();
        for(int i = 0; i < ITERS; i++)
                compute_sum(a, b, c);

        auto stop = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(stop - start);
        std::cout << "Took " << duration.count() << "ms" << std::endl;
        
        free(a);
        free(b);
        free(c);
        return 0;
}