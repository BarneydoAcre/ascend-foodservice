from django.http import HttpResponse, JsonResponse
from setup.utils import model_to_json_dumped, manual_query
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

import json
from sale.models import *
from default.models import *


def sales_per_month(request, *args, **kwargs):
    instance = manual_query(f'''
     SELECT
        EXTRACT(DAY FROM T1.created) AS dia,
        EXTRACT(MONTH FROM T1.created) AS mes,
        EXTRACT(YEAR FROM T1.created) AS ano,
        SUM(T1."value"+T1."delivery") AS total_venda
        
    FROM "sale_sale" T1
        LEFT JOIN "default_company" ON (T1."company_id" = "default_company"."id") 
        
    WHERE
        T1."canceled" is not false AND
        T1."company_id" = {get_object_or_404(Company, slug=kwargs['company']).id}
        
    GROUP BY
	1, 2, 3
    
    ORDER BY
        ano ASC,
        mes ASC,
        dia ASC
    ''')
    return HttpResponse(instance)


