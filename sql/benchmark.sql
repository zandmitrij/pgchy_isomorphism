
DO $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    iterations INTEGER := 1000;
    i INTEGER;
    result RECORD;
    smiles TEXT := 'C1CCCCC1';
BEGIN
    start_time := clock_timestamp();

    FOR i IN 1..iterations LOOP
        SELECT * INTO result
        FROM find_molecule_matches(smiles, 0.8, 'public', 'mol_table')
        LIMIT 1;
    END LOOP;

    end_time := clock_timestamp();

    RAISE NOTICE 'Total time: %', (end_time - start_time) / iterations;
END $$;
