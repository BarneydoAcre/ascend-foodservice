import datetime
from decimal import *
import json
# import ujson
import psycopg2
from itertools import chain
from setup.settings import DATABASES

def converter(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return str(obj)
    
    raise TypeError (f"{type(obj)} variable error")

def model_to_json_dumped(instance):
    data = []
    for i in instance:
        opts = i._meta
        dt = {}
        for q in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            dt[q.name] = q.value_from_object(i)
        data.append(dt)
    return json.dumps(data, default=converter)

def manual_query(sql):
    conn = psycopg2.connect(host=DATABASES['default']['HOST'], database=DATABASES['default']['NAME'], user=DATABASES['default']['USER'], password=DATABASES['default']['PASSWORD'])
    cur = conn.cursor()
    cur.execute(sql)
    cols = [c[0] for c in cur.description]
    fetch = cur.fetchall()
    data = []
    for fet in fetch:
        dt = {}
        for i, f in enumerate(fet):
            dt[cols[i]] = f
        data.append(dt)
    return json.dumps(data, default=converter)
    