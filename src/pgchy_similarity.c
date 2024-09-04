#include "postgres.h"
#include "fmgr.h"
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stddef.h>
#include <libpopcnt.h>

#include <includes/pgchy_similarity.h>


#ifdef PG_MODULE_MAGIC
PG_MODULE_MAGIC;
#endif


void and_vector_256(const uint8_t* fingerprint1, const uint8_t* fingerprint2, uint8_t *output) {
    size_t i;

    uint32_t* fp1 = (uint32_t*) fingerprint1;
    uint32_t* fp2 = (uint32_t*) fingerprint2;
    uint32_t* out = (uint32_t*) output;

    for (i = 0; i < SIM_VEC_SIZE_INT; i++) {
        out[i] = fp1[i] & fp2[i];
    }
}


int check_popcounts(Fingerprint* fingerprint1, Fingerprint* fingerprint2, float threshold) {
    uint16_t popcount1 = fingerprint1->popcount;
    uint16_t popcount2 = fingerprint2->popcount;
    if (popcount1 > popcount2) {
        return (popcount2 < (threshold * popcount1)) ? 0 : 1;
    }
    return (popcount1 < (threshold * popcount2)) ? 0 : 1;
}


int similarity_256(Fingerprint* fingerprint1, Fingerprint* fingerprint2, float threshold) {
    uint64_t intersection;
    uint64_t union_count;
    uint8_t fp_and[SIM_VEC_SIZE];

    if (check_popcounts(fingerprint1, fingerprint2, threshold) == 0) {
        return 0;
    }

    and_vector_256(fingerprint1->arr, fingerprint2->arr, fp_and);
    intersection = popcnt(fp_and, SIM_VEC_SIZE);
    union_count = fingerprint1->popcount + fingerprint2->popcount - intersection;

    return ((float)intersection / (float)union_count >= threshold) ? 1 : 0;
}


PGDLLEXPORT Datum is_tanimoto_similar(PG_FUNCTION_ARGS);

PG_FUNCTION_INFO_V1(is_tanimoto_similar);


Datum is_tanimoto_similar(PG_FUNCTION_ARGS) {
    Fingerprint* query_fingerprint;
    Fingerprint* mol_fingerprint;
    bool result;

    bytea* query_bytes = PG_GETARG_BYTEA_P(0);
    bytea* mol_bytes = PG_GETARG_BYTEA_P(1);
    float threshold = PG_GETARG_FLOAT4(2);

    query_fingerprint = (Fingerprint*) VARDATA(query_bytes);
    mol_fingerprint = (Fingerprint*) VARDATA(mol_bytes);

    result = similarity_256(query_fingerprint, mol_fingerprint, threshold) > 0;

    PG_RETURN_BOOL(result);
}
