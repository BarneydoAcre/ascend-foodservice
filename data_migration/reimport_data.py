import pandas as pd
import json
import psycopg2 as pg
from datetime import datetime


class data_import():
    def con(self):
        con = pg.connect(host='localhost', database='database',
        user='postgres', password='postgres')
        return con

    def prod_type1(self):
        j = open('D:\\Programas\\Projetos\\Ascend Project\\FoodService\\back\\data_migration\\exports\\procuct_type1_deliciasdalia.json', 'r')
        arq = json.loads(j.read())
        for a in arq:
            conn = self.con()
            cur = conn.cursor()
            cur.execute(f'''
            insert into register_product (
                id,
                company_id,
                company_worker_id,
                type,
                name,
                stock,
                cost,
                price,
                created,
                updated
            ) values (
                {a['id']},
                '2',
                '1',
                {a['type']},
                '{a['name']}',
                {a['stock']},
                {a['cost']},
                {a['price'] if a['price'] != 'None' else 'null'},
                '{datetime.now().date()}',
                '{datetime.now().date()}'
            ) ON CONFLICT (id) DO  
            update set
                type = {a['type']},
                name = '{a['name']}',
                stock = {a['stock']},
                cost = {a['cost']},
                price = {a['price'] if a['price'] != 'None' else 'null'}
                
            ''')
            conn.commit()
            conn.close()

    def prod_type2(self):
        j = open('D:\\Programas\\Projetos\\Ascend Project\\FoodService\\back\\data_migration\\exports\\procuct_type2_deliciasdalia.json', 'r', encoding="utf-8")
        arq = json.loads(j.read())
        for a in arq:
            conn = self.con()
            cur = conn.cursor()
            cur.execute(f'''
            insert into register_product (
                id,
                company_id,
                company_worker_id,
                type,
                name,
                stock,
                cost,
                price,
                created,
                updated
            ) values (
                {a['id']},
                '2',
                '1',
                {a['type']},
                '{a['name'] if a['name'] != 'None' else 'null'}',
                {a['stock'] if a['stock'] != 'None' else 'null'},
                {a['cost'] if a['cost'] != 'None' else 'null'},
                {a['price'] if a['price'] != 'None' else 'null'},
                '{datetime.now().date()}',
                '{datetime.now().date()}'
            ) ON CONFLICT (id) DO  
            update set
                type = {a['type']},
                name = '{a['name']}',
                stock = {a['stock'] if a['stock'] != 'None' else 'null'},
                cost = {a['cost'] if a['cost'] != 'None' else 'null'},
                price = {a['price'] if a['price'] != 'None' else 'null'}
                
            ''')
            conn.commit()
            conn.close()

    def sale(self):
        arq = open('D:\\Programas\\Projetos\\Ascend Project\\FoodService\\back\\data_migration\\exports\\sale_deliciasdalia.json', 'r', encoding='utf-8')
        arq = json.loads(arq.read())
        for a in arq:
            conn = self.con()
            cur = conn.cursor()
            cur.execute(f'''
            insert into sale_sale (
                id,
                company_id,
                company_worker_id,
                total,
                delivery,
                value,
                canceled,
                created,
                updated
            ) values (
                {a['id']},
                '2',
                '1',
                {a['value']+a['delivery']},
                {a['delivery'] if a['delivery'] != 'None' else 'null'},
                {a['value'] if a['value'] != 'None' else 'null'},
                false,
                '{a['date']}',
                '{datetime.now().date()}'
            ) ON CONFLICT (id) DO  
            update set
                total = {a['value']+a['delivery']},
                delivery = '{a['delivery']}',
                value = {a['value']},
                created = '{a['date']}',
                canceled = false       
            ''')
            conn.commit()
            conn.close()

    def saleItems(self):
        arq = open('D:\\Programas\\Projetos\\Ascend Project\\FoodService\\back\\data_migration\\exports\\saleitems_deliciasdalia.json', 'r', encoding='utf-8')
        arq = json.loads(arq.read())
        # print(arq)
        for a in arq:
            try:
                conn = self.con()
                cur = conn.cursor()
    #{'id': 149, 'sale': 22, 'product_id': 54, 'product_name': 'Pão Caseiro', 'price': 10.0, 'quantity': 1.0}
                cur.execute(f'''
                insert into sale_saleitems (
                    id,
                    company_id,
                    company_worker_id,
                    sale_id,
                    product_id,
                    price,
                    quantity,
                    created,
                    updated
                ) values (
                    {a['id']},
                    '2',
                    '1',
                    {a['sale']},
                    (select id from register_product where name = '{a['product_name']}'),
                    {a['price']},
                    '{a['quantity']}',
                    '{datetime.now().date()}',
                    '{datetime.now().date()}'
                ) ON CONFLICT (id) DO  
                update set
                    company_id = 2,
                    company_worker_id = 1,
                    sale_id = {a['sale']},
                    product_id = (select id from register_product where name = '{a['product_name']}'),
                    price = {a['price']},
                    quantity = '{a['quantity']}'   
                ''')
                conn.commit()
                conn.close()
            except:
                pass

# data_import().prod_type1()
# data_import().prod_type2()
# data_import().sale()
data_import().saleItems()
