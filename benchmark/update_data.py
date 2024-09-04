import getpass
import typing as tp

import numpy as np
import struct
import hvac
import chython
import peewee
import json

from reactlake_utils.database_utils.connection_factories import PostgreSQLConnectionFactory
from reactlake_utils.database_utils.peewee_utils.basemodel import BaseModel
from reactlake_utils.database_utils.peewee_utils.pages_iterator import iterate_pages

from reactlake_utils.utils import iterator_utils as iu


SDF_PROPERTIES_BUFFER_SIZE = 10000


test_proxy = peewee.DatabaseProxy()


class TestBaseModel(BaseModel):
    class Meta:
        database = test_proxy


class Smiles(TestBaseModel):
    id = peewee.AutoField()
    smiles = peewee.TextField()


class Morgan(TestBaseModel):
    id = peewee.AutoField()
    morgan = peewee.BlobField()


prod_proxy = peewee.DatabaseProxy()


class ProdBaseModel(BaseModel):
    class Meta:
        database = prod_proxy


class Structure(ProdBaseModel):
    id = peewee.AutoField()
    smiles = peewee.TextField(null=True)
    pach = peewee.BlobField(null=True)
    compound = peewee.IntegerField(null=True)

    class Meta:
        db_table = 'structure'

def update_db_pass(creds: dict) -> None:
    username = input('Username: ')
    password = getpass.getpass(prompt='Password: ')
    client = hvac.Client(url=creds['VAULT_URL'], verify=True)

    client.auth.ldap.login(username=username, password=password)

    if not client.is_authenticated():
        raise ValueError('Incorrect username or password')

    secret = client.secrets.kv.v2.read_secret_version(
        path=creds['VAULT_CONFIG_PATH'], raise_on_deleted_version=True,
    )

    creds['PASSWORD'] = secret['data']['data']['credentials'][creds['HOST']][creds['USER']]


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


def mol_to_fingerprint(bmol: bytes):
    try:
        mol = chython.MoleculeContainer.unpack(bmol)
        morgan = mol.morgan_fingerprint(length=2048)
        bytes_morgan = np.packbits(morgan, bitorder='little').tobytes(order='C')
        popcount = morgan.sum()
        return struct.pack('<h256s', popcount, bytes_morgan)
    except Exception:
        return None


def create_chunks(chunk: tp.Tuple[Structure]) -> tp.Tuple[tp.List[dict], tp.List[dict]]:
    res1 = []
    res2 = []
    for _model in chunk:
        if _model.pach is None or _model.smiles is None:
            continue
        res1.append({'id': _model.id, 'smiles': _model.smiles})
        res2.append({'id': _model.id, 'morgan': mol_to_fingerprint(_model.pach)})
    return res1, res2


def iterate_data() -> tp.Iterator[tp.Tuple[tp.List[dict], tp.List[dict]]]:
    model = Structure()
    model._meta.schema = 'modelboard'
    
    for page in iterate_pages(Structure, fields=[Structure.id, Structure.smiles, Structure.pach], page_size=100000):
        yield from map(create_chunks, iu.chunk_collection(page, size=10000))


def read_creds(path: str) -> dict:
    with open(path, 'r') as f:
        return json.load(f)


def main():
    prod_creds = read_creds('secrets/prod.json')
    update_db_pass(prod_creds)

    test_creds = read_creds('secrets/test.json')

    init_db(prod_creds, prod_proxy)
    init_db(test_creds, test_proxy)
    Smiles.create_table(safe=True)
    Morgan.create_table(safe=True)

    for smiles_res, morgan_res in iterate_data():
        Smiles.bulk_insert(smiles_res)
        Morgan.bulk_insert(morgan_res)


if __name__ == '__main__':
    main()
