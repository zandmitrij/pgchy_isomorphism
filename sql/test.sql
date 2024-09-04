
CREATE TABLE public.mol_table (
    mol_bytes bytea
);


select smiles_to_lz4_compressed_fingerprint('C1CCCCC1')::bytea;


INSERT INTO public.mol_table (mol_bytes) VALUES 
(smiles_to_lz4_compressed_fingerprint('C1CCCCC1')::bytea),
(smiles_to_lz4_compressed_fingerprint('C1CCCCC1С')::bytea),
(smiles_to_lz4_compressed_fingerprint('C1=CC=CC=C1')::bytea),
(smiles_to_lz4_compressed_fingerprint('C1=CC=CC=C1CCCCN')::bytea),
(smiles_to_lz4_compressed_fingerprint('C1=CC=CC=C1CC(CCCC)CC')::bytea);


SELECT * FROM find_molecule_matches('C1CCCCC1', 0.2, 'public', 'mol_table');


-- 3 tables lz4_fp not_lz4_fp smiles
-- 