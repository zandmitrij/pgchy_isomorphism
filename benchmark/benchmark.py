import random
import time
import json
import typing as tp
import dataclasses
import peewee
from reactlake_utils.database_utils.connection_factories import PostgreSQLConnectionFactory
import docker
from docker.models.containers import Container


test_proxy = peewee.DatabaseProxy()


def init_db(creds: dict, *proxies: peewee.DatabaseProxy) -> None:
    connection = PostgreSQLConnectionFactory.remote(
        database_name=creds['DATABASE'],
        user=creds['USER'],
        password=creds['PASSWORD'],
        host=creds['HOST'],
        port=5432,
    ).create_connection()

    for proxy in proxies:
        proxy.initialize(connection)


class Query:
    id: int
    treshold: float
    table_name: tp.Literal['morgan_lz4', 'morgan']
    function_name: tp.Literal['chython_fingerprint_has_match_not_compressed', 'chython_fingerprint_has_match']

    def sql_query(self) -> str:
        return f'''WITH mol_query AS (
            SELECT chython_mol_to_fingerprint(smiles)::bytea AS query_bytes
            FROM public.smiles
            WHERE id = {self.id}
        )
        SELECT id
        FROM public.{self.table_name}, mol_query
        WHERE {self.function_name}(mol_query.query_bytes, morgan, {self.treshold:0.2});'''


@dataclasses.dataclass
class CompressedTableQuery(Query):
    id: int
    treshold: float
    table_name: str = 'morgan_lz4'
    function_name: str = 'chython_fingerprint_has_match'
    filename: str = 'compressed_benchmark.txt'


@dataclasses.dataclass
class NotCompressedTableQuery(Query):
    id: int
    treshold: float
    table_name: str = 'morgan'
    function_name: str = 'chython_fingerprint_has_match_not_compressed'
    filename: str = 'not_compressed_benchmark.txt'


def create_query(id: int) -> tp.Union[CompressedTableQuery, NotCompressedTableQuery]:
    treshold = round(random.random(), 2) or 0.5

    if id % 2 == 0:
        return CompressedTableQuery(id, treshold)

    return NotCompressedTableQuery(id, treshold)


def run(creds: dict, id: int):
    init_db(creds, test_proxy)
    query = create_query(id)
    q = query.sql_query()
    start = time.time()
    test_proxy.execute_sql(q)
    end = time.time()
    with open(query.filename, 'a') as f:
        f.write(f'{end - start}\n')


def restart_db():
    client = docker.from_env()
    container: Container = client.containers.list()[0]
    container.restart(timeout=5)



def read_creds(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)


def main():
    test_creds = read_creds('secrets/test.json')

    for i in range(10, 30):
        print(f'running for id {i}')
        run(test_creds, i)
        print('resrtarting db')
        restart_db()
        time.sleep(10)
        print('ok')


if __name__ == "__main__":
    main()
