from operator import index
import psycopg2 as pg
import pandas as pd

class data_export():
    def con(self):
        con = pg.connect(host='localhost', database='helpdesk',
        user='postgres', password='postgres')
        return con

    def company(self):
        conn = self.con()
        cur = conn.cursor()
        sql = '''
        select
            id,
            slug,
            company,
            cnpj,
            created,
            updated,
            owner_id
        from default_company
        '''
        cur.execute(sql)

        data = []
        for c in cur.fetchall():
            data.append({
                'id': c[0],
                'slug': c[1],
                'company': c[2],
                'cnpj': c[3],
                'created': str(c[4])[0:26],
                'updated': str(c[5])[0:26],
                'owner_id': c[6],
            })
        table = pd.DataFrame(data).to_excel("exports/company.xlsx", index=False)
        conn.close()
        
    def companyposition(self):
        conn = self.con()
        cur = conn.cursor()
        sql = '''
        select
            id,
            position,
            created,
            updated,
            company_id
        from default_companyposition
        '''
        cur.execute(sql)

        data = []
        for c in cur.fetchall():
            data.append({
                'id': c[0],
                'position': c[1],
                'created': str(c[2])[0:26],
                'updated': str(c[3])[0:26],
                'company_id': c[4],
            })
        table = pd.DataFrame(data).to_excel("exports/companyposition.xlsx", index=False)
        conn.close()
    
    def user(self):
        conn = self.con()
        cur = conn.cursor()
        sql = '''
        select
            id,
            password,
            last_login,
            is_superuser,
            username,
            first_name,
            last_name,
            email,
            is_staff,
            is_active,
            date_joined
        from auth_user 
        '''
        cur.execute(sql)

        data = []
        for c in cur.fetchall():
            data.append({
                'id': c[0],
                'password': c[1],
                'last_login': str(c[2]),
                'is_superuser': c[3],
                'username': c[4],
                'first_name': c[5],
                'last_name': c[6],
                'email': c[7],
                'is_staff': c[8],
                'is_active': c[9],
                'date_joined': str(c[10]),
            })
        table = pd.DataFrame(data).to_excel("exports/user.xlsx", index=False)
        conn.close()

    def companyworker(self):
        conn = self.con()
        cur = conn.cursor()
        sql = '''
        select
            id,
            cpf,
            rg,
            phone_number,
            created,
            updated,
            company_id,
            person_id,
            position_id
        from default_companyworker
        '''
        cur.execute(sql)

        data = []
        for c in cur.fetchall():
            data.append({
                'id': c[0],
                'cpf': c[1],
                'rg': c[2],
                'phone_number': c[3],
                'created': str(c[4])[0:26],
                'updated': str(c[5])[0:26],
                'company_id': c[6],
                'person_id': c[7],
                'position_id': c[8],
            })
        table = pd.DataFrame(data).to_excel("exports/companyworker.xlsx", index=False)
        conn.close()
        
    def bugreport(self):
        conn = self.con()
        cur = conn.cursor()
        sql = '''
        select
            id,
            bug,
            created,
            updated,
            company_id,
            company_worker_id
        from default_bugreport 
        '''
        cur.execute(sql)

        data = []
        for c in cur.fetchall():
            data.append({
                'id': c[0],
                'bug': c[1],
                'created': str(c[2])[0:26],
                'updated': str(c[3])[0:26],
                'company_id': c[4],
                'company_worker_id': c[5],
            })
        table = pd.DataFrame(data).to_excel("exports/bugreport.xlsx", index=False)
        conn.close()

    def newregister(self):
        conn = self.con()
        cur = conn.cursor()
        sql = '''
        select
            id,
            email,
            first_name,
            last_name,
            phone_number,
            created,
            updated
        from default_newregister
        '''
        cur.execute(sql)

        data = []
        for c in cur.fetchall():
            data.append({
                'id': c[0],
                'email': c[1],
                'first_name': c[2],
                'last_name': c[3],  
                'phone_number': c[4],
                'created': str(c[5])[0:26],
                'updated': str(c[6])[0:26],
            })
        table = pd.DataFrame(data).to_excel("exports/newregister.xlsx", index=False)
        conn.close()

    def productbrand(self):
        conn = self.con()
        cur = conn.cursor()
        sql = '''
        select
            id,
            brand,
            created,
            updated,
            company_id,
            company_worker_id
        from foodservice_productbrand
        '''
        cur.execute(sql)

        data = []
        for c in cur.fetchall():
            data.append({
                'id': c[0],
                'brand': c[1],
                'created': str(c[2])[0:26],
                'updated': str(c[3])[0:26],
                'company_id': c[4],
                'company_worker_id': c[5],
            })
        table = pd.DataFrame(data).to_excel("exports/productbrand.xlsx", index=False)
        conn.close()

    def productmeasure(self):
        conn = self.con()
        cur = conn.cursor()
        sql = '''
        select
            id,
            measure,
            created,
            updated,
            company_id,
            company_worker_id
        from foodservice_productmeasure
        '''
        cur.execute(sql)

        data = []
        for c in cur.fetchall():
            data.append({
                'id': c[0],
                'measure': c[1],
                'created': str(c[2])[0:26],
                'updated': str(c[3])[0:26],
                'company_id': c[4],
                'company_worker_id': c[5],
            })
        table = pd.DataFrame(data).to_excel("exports/productmeasure.xlsx", index=False) 
        conn.close()

    # def productgroup(self):
    #     conn = self.con()
    #     cur = conn.cursor()
    #     sql = '''
    #     select
    #         *
    #     from foodservice_groups f
    #     '''
    #     cur.execute(sql)

    #     data = []
    #     for c in cur.fetchall():
    #         data.append({
    #             'id': c[0],
    #             'name': c[1],
    #             'created': str(c[2]),
    #             'updated': str(c[3]),

    #         })
    #     table = pd.DataFrame(data).to_excel("exports/groups.xlsx", index=False)
    #     conn.close()

    def product(self):
        conn = self.con()
        cur = conn.cursor()
        sql = '''
        select
            id,
            name,
            stock,
            cost,
            created,
            updated,
            brand_id,
            company_id,
            company_worker_id,
            measure_id,
            price,
            type
        from foodservice_product
        '''
        cur.execute(sql)

        data = []
        for c in cur.fetchall():
            data.append({
                'id': c[0],
                'name': c[1],
                'stock': c[2],
                'cost': c[3],
                'created': str(c[4])[0:26],
                'updated': str(c[5])[0:26],
                'brand_id': c[6],
                'company_id': c[7],
                'company_worker_id': c[8],
                'measure_id': c[9],
                'price': c[10],
                'type': c[11],
            })
        table = pd.DataFrame(data).to_excel("exports/product.xlsx", index=False)
        conn.close()

    def productitems(self):
        conn = self.con()
        cur = conn.cursor()
        sql = '''
        select
            id,
            created,
            updated,
            company_id,
            company_worker_id,
            product_id,
            product_item_id,
            quantity
        from foodservice_productitems
        '''
        cur.execute(sql)

        data = []
        for c in cur.fetchall():
            data.append({
                'id': c[0],
                'created': str(c[1])[0:26],
                'updated': str(c[2])[0:26],
                'company_id': c[3],
                'company_worker_id': c[4],
                'product_id': c[5],
                'product_item_id': c[6],
                'quantity': c[7],

            })
        table = pd.DataFrame(data).to_excel("exports/productitems.xlsx", index=False)
        conn.close()

    def sale(self):
        conn = self.con()
        cur = conn.cursor()
        sql = '''
        select
            id,
            created,
            updated,
            company_id,
            company_worker_id,
            delivery,
            value,
            total
        from foodservice_sale
        '''
        cur.execute(sql)

        data = []
        for c in cur.fetchall():
            data.append({
                'id': c[0],
                'created': str(c[1])[0:26],
                'updated': str(c[2])[0:26],
                'company_id': c[3],
                'company_worker_id': c[4],
                'delivery': c[5],
                'value': c[6],
                'total': c[7],

            })
        table = pd.DataFrame(data).to_excel("exports/sale.xlsx", index=False)
        conn.close()

    def saleitems(self):
        conn = self.con()
        cur = conn.cursor()
        sql = '''
        select
            id,
            created,
            updated,
            company_id,
            company_worker_id,
            product_id,
            price,
            quantity,
            sale_id
        from foodservice_saleitems
        '''
        cur.execute(sql)

        data = []
        for c in cur.fetchall():
            data.append({
                'id': c[0],
                'created': str(c[1])[0:26],
                'updated': str(c[2])[0:26],
                'company_id': c[3],
                'company_worker_id': c[4],
                'product_id': c[5],
                'price': c[6],
                'quantity': c[7],
                'sale_id': c[8],

            })
        table = pd.DataFrame(data).to_excel("exports/saleitems.xlsx", index=False)
        conn.close()

if __name__ == "__main__":
    data_export().company()
    data_export().companyposition()
    data_export().user()
    data_export().companyworker()
    data_export().bugreport()
    data_export().newregister()
    data_export().productbrand()
    # data_export().groups()
    data_export().productmeasure()
    data_export().product()
    data_export().productitems()
    data_export().sale()
    data_export().saleitems()
