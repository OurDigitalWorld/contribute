
from collections import namedtuple
from django.db import connections


def sql_call(qry, db):
    """ execute given SELECT or INSERT (with return) query against db """
    with connections[db].cursor() as cur:
        cur.execute(qry)
        col_names = [desc[0] for desc in cur.description]
        sql_rtn = cur.fetchall()
    cur.close()
    result = []
    for row in sql_rtn:
        result.append(create_record(row, col_names))
    return result


def create_record(obj, fields):
    """ given obj from db returns named tuple with fields mapped to values """
    Record = namedtuple("Record", fields)
    mappings = dict(zip(fields, obj))
    return Record(**mappings)


def sql_update(qry):
    """ execute given UPDATE or DELETE OR INSERT (without return) query against db """
    with connections['vita'].cursor() as cur:
        cur.execute(qry)
        connections['vita'].commit()
