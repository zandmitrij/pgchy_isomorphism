#include "postgres.h"
#include "fmgr.h"
#include "utils/array.h"
#include <stdint.h>
#include <lz4.h>

#ifdef PG_MODULE_MAGIC
PG_MODULE_MAGIC;
#endif

typedef struct {
    uint64_t field1;
    uint32_t field2;
    uint64_t field3;
} MyStruct;


PG_FUNCTION_INFO_V1(chython_compiled_structure_has_match);


static bool get_mapping(const MyStruct *query, const MyStruct *mol) {
    return false;
}


Datum chython_compiled_structure_has_match(PG_FUNCTION_ARGS) {

    MyStruct *query_struct;
    MyStruct *mol_struct;

    bytea *query_bytes = PG_GETARG_BYTEA_P(0);
    bytea *mol_bytes = PG_GETARG_BYTEA_P(1);

    uint8_t *query_data = (uint8_t *) VARDATA(query_bytes);
    size_t query_len = VARSIZE(query_bytes) - VARHDRSZ;

    uint8_t *mol_data = (uint8_t *) VARDATA(mol_bytes);
    size_t mol_len = VARSIZE(mol_bytes) - VARHDRSZ;

    size_t max_decompressed_size = 1024 * 1024;
    uint8_t *decompressed_query = (uint8_t *) palloc(max_decompressed_size);
    uint8_t *decompressed_mol = (uint8_t *) palloc(max_decompressed_size);

    int decompressed_query_size = LZ4_decompress_safe((const char *)query_data, (char *)decompressed_query, query_len, max_decompressed_size);
    int decompressed_mol_size = LZ4_decompress_safe((const char *)mol_data, (char *)decompressed_mol, mol_len, max_decompressed_size);

    if (decompressed_query_size < 0 || decompressed_mol_size < 0) {
        pfree(decompressed_query);
        pfree(decompressed_mol);
        ereport(ERROR, (errmsg("Decompression failed")));
    }

    query_struct = (MyStruct *) decompressed_query;
    mol_struct = (MyStruct *) decompressed_mol;

    bool result;
    result = get_mapping(query_struct, mol_struct);

    pfree(decompressed_query);
    pfree(decompressed_mol);

    PG_RETURN_BOOL(result);
}


