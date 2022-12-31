from django.http import HttpResponse, JsonResponse
from setup.utils import model_to_json_dumped, manual_query
from django.forms.models import model_to_dict
from sale.models import *
import json


def sales_per_month(request):
    instance = manual_query(f'''
    SELECT
        EXTRACT(MONTH FROM T1.created) AS mes,
        EXTRACT(YEAR FROM T1.created) AS ano,
        SUM(T1."value"+T1."delivery") AS total_venda
        
    FROM "sale_sale" T1
        INNER JOIN "default_company" ON (T1."company_id" = "default_company"."id") 
        
    WHERE
        T1."canceled" is not false AND
        T1."company_id" = 1
        
    GROUP BY
	1, 2
    ''')
    return HttpResponse(instance)


