// benchmark.c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <includes/similarity_impl.h>



void initialize_random_vector(uint8_t* arr, size_t size) {
    int64_t i;
    int middle = RAND_MAX / 2;

    for (i = 0; i < size; i++) {
        arr[i] = (rand() < middle) ? 0 : 1;
    }   
}


void run_benchmark() {
    int64_t target_comparisons = 1000;
    int64_t i;
    clock_t start_time, end_time;
    double threshold = 0.5;

    double elapsed_time;

    uint8_t** fp_array_1 = (uint8_t**)malloc(target_comparisons * sizeof(uint8_t*));
    uint8_t** fp_array_2 = (uint8_t**)malloc(target_comparisons * sizeof(uint8_t*));

    for (i = 0; i < target_comparisons; i++) {
        fp_array_1[i] = malloc(sizeof(uint8_t) * SIM_VEC_SIZE);
        fp_array_2[i] = malloc(sizeof(uint8_t) * SIM_VEC_SIZE);
        initialize_random_vector(fp_array_1[i], SIM_VEC_SIZE);
        initialize_random_vector(fp_array_2[i], SIM_VEC_SIZE);
    }

    start_time = clock();

    for (i = 0; i < target_comparisons; i++) {
        similarity_256(fp_array_1[i], fp_array_2[i], threshold);
    }

    end_time = clock();
    elapsed_time = ((double) (end_time - start_time)) / CLOCKS_PER_SEC;

    for (i = 0; i < target_comparisons; i++) {
        free(fp_array_1[i]);
        free(fp_array_2[i]);
    }

    free(fp_array_1);
    free(fp_array_2);

    FILE *f = fopen("benchmark_results.txt", "w");
    if (f == NULL) {
        perror("Can't open file");
        exit(EXIT_FAILURE);
    }
    fprintf(f, "Time: %f seconds\n", elapsed_time);
    fprintf(f, "Operations per second: %f\n", target_comparisons / elapsed_time);
    fclose(f);
}

int main() {
    srand(0);   // Initialization, should only be called once.

    run_benchmark();
    return 0;
}
