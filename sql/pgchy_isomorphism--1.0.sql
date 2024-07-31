-- pgchy_isomorphism--1.0.sql

CREATE FUNCTION chython_compiled_structure_has_match(query_bytes bytea, mol_bytes bytea)
RETURNS boolean
AS 'MODULE_PATHNAME', 'chython_compiled_structure_has_match'
LANGUAGE C STRICT;
