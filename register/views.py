from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets, generics, filters

from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
 
from register.serializers import *
from register.models import *
from default.models import CompanyWorker
from . import forms
import json



class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ProductSerializer
    def get_queryset(self):
        try:
            data = json.loads(self.request.body)
            if len(data) == 0:
                raise
        except:
            data = self.request.data
            if len(data) == 0:
                pass
        try:
            company = self.request.GET['company']
        except:
            company = data['company']
        worker = get_object_or_404(CompanyWorker, company__slug=company, person=self.request.user.id)
        try:
            queryset = Product.objects.filter(company__slug=company, type=self.request.GET['type'])
        except MultiValueDictKeyError:
            try:
                queryset = Product.objects.filter(company__slug=company)
            except MultiValueDictKeyError:
                queryset = Product.objects.filter(company=0, type=0)
        return { 'queryset': queryset, 'worker': worker, 'data': data }
    
    def create(self, request):
        try:
            query = self.get_queryset()
        except:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        c = CompanyWorker.objects.get(company__slug=query['data']['company'], person=request.user.id)
        query['data']['company'] = c.company.id
        query['data']['company_worker'] = c.id
        product_data = ProductSerializer(data=query['data'])
        if query['data']['type'] == 2:
            if product_data.is_valid():
                product = Product.objects.create(
                    company=product_data.validated_data['company'],
                    company_worker=product_data.validated_data['company_worker'],
                    type=product_data.validated_data['type'],
                    name=product_data.validated_data['name'],
                    # brand=product_data.validated_data['total'],
                    # measure=product_data.validated_data['total'],
                    # stock=product_data.validated_data['total'],
                    # cost=product_data.validated_data['total'],
                    price=product_data.validated_data['price'],
                )
                query['data']['id'] = product.id
                products = []
                try:
                    for p in query['data']['products']:
                        print(p)
                        product_items = ProductItems.objects.create(
                            company=product_data.validated_data['company'],
                            company_worker=product_data.validated_data['company_worker'],
                            product=product,
                            product_item=Product.objects.get(id=int(p['id'])),
                            quantity=float(p['quantity'])
                        )
                        products.append({
                            "id": product_items.id,
                            "product": product_items.product.id,
                            "product_item": product_items.product_item.id,
                            "quantity": product_items.quantity
                        })
                    query['data']['products'] = products
                except:
                    Product.objects.filter(id=product.id).delete()
                    return Response({'detail': 'Dados inválidos.'}, status=status.HTTP_401_UNAUTHORIZED)
                return Response(query['data'], status=status.HTTP_201_CREATED)    
        elif query['data']['type'] == 1:
            if product_data.is_valid():
                product = Product.objects.create(
                    company=product_data.validated_data['company'],
                    company_worker=product_data.validated_data['company_worker'],
                    type=product_data.validated_data['type'],
                    name=product_data.validated_data['name'],
                    brand=product_data.validated_data['brand'],
                    measure=product_data.validated_data['measure'],
                    stock=product_data.validated_data['stock'],
                    cost=product_data.validated_data['cost'],
                    # price=product_data.validated_data['price'],
                )
            return Response(ProductSerializer(Product.objects.filter(id=product.id), many=True).data, status=status.HTTP_201_CREATED)
        try:
            Product.objects.filter(id=product.id).delete()
            return Response({'detail': 'Dados inválidos.'}, status=status.HTTP_401_UNAUTHORIZED)
        except: 
            return Response({'detail': 'Dados inválidos.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def list(self, request):
        """
        /?company=**&type=**
        """
        try:
            query = self.get_queryset()
        except:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        products = query['queryset']
        data = []
        for p in products:
            product = {
                'id': p.id,
                'name': p.name,
                'brand_id': p.brand.id if p.brand != None else None,
                'brand': p.brand.brand if p.brand != None else None,
                'measure_id': p.measure.id if p.measure != None else None,
                'measure': p.measure.measure if p.measure != None else None,
                'stock': p.stock,
                'cost': p.cost,
                'type': p.type,
                'price': p.price
            }
            product_items = []
            for pi in ProductItems.objects.filter(product=p.id).order_by('id'):
                product_items.append({
                    'id': pi.id,
                    'product': pi.product_item.id,
                    'name': pi.product_item.name,
                    'cost': pi.product_item.cost,
                    'quantity': pi.quantity
                })
            product['items'] = product_items
            data.append(product)  
        return Response(data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        """
        /?company=**
        
        {
            "company": "ascend-project",
            "name": "Teste Patch",
            "price": 16.0,
            "items": [
                {
                    "id": 23,
                    "product": 4,
                    "name": "Produto Tipo 1",
                    "quantity": 4.0
                }
            ]
        }
        """
        try:
            data = json.loads(request.body)
        except:
            data = request.data
            if len(data) == 0:
                pass
                
        query = self.get_queryset()
        if query['worker']:
            try:
                Product.objects.filter(id=kwargs['pk']).update(measure=query['data']['measure'])
            except:
                pass
            try:
                Product.objects.filter(id=kwargs['pk']).update(brand=query['data']['brand'])
            except:
                pass
            try:
                Product.objects.filter(id=kwargs['pk']).update(price=query['data']['price'])
            except:
                pass
            try:
                Product.objects.filter(id=kwargs['pk']).update(name=query['data']['name'])
            except:
                pass
            try:
                for i in query['data']['items']:
                    product_item = get_object_or_404(Product, id=i['product'])
                    if product_item.type == 1: 
                        prod = ProductItems.objects.create(
                            company=query['worker'].company,
                            company_worker=query['worker'],
                            product=get_object_or_404(Product, id=kwargs['pk']),
                            product_item=product_item,
                            quantity=i['quantity']    
                        )
            except:
                pass
                
            p = Product.objects.get(id=kwargs['pk'])
            product = {
                'id': p.id,
                'name': p.name,
                'brand_id': p.brand.id if p.brand != None else None,
                'brand': p.brand.brand if p.brand != None else None,
                'measure_id': p.measure.id if p.measure != None else None,
                'measure': p.measure.measure if p.measure != None else None,
                'stock': p.stock,
                'cost': p.cost,
                'type': p.type,
                'price': p.price
            }
            product_items = []
            for pi in ProductItems.objects.filter(product=p.id).order_by('id'):
                product_items.append({
                    'id': pi.id,
                    'product': pi.product_item.id,
                    'name': pi.product_item.name,
                    'quantity': pi.quantity,
                    'cost': pi.product_item.cost
                })
            product['items'] = product_items
            return Response(product, status=status.HTTP_201_CREATED)
        return Response({
            "modelo": "SIGA ESTE MODELO",
            "company": "empresa-slug",
            "brand": "brand-ID",
            "measure": "measure-ID",
            "price": "price-FLOAT",
            "name": "name-STRING",
            "items": [
                {
                    "id": 1,
                    "product": 1,
                    "quantity": 1.0
                }
            ]
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except:
            data = request.data
            if len(data) == 0:
                pass
        
        query = self.get_queryset()
        if query['worker']:
            if data['delete_type'] == 'p':  
                pi = ProductItems.objects.filter(company__slug=data['company'], product=kwargs['pk'])
                if len(pi) != 0:
                    pi.delete()
                Product.objects.filter(company__slug=data['company'], id=kwargs['pk']).delete()
                return Response({'detail': f'Produto {kwargs["pk"]} deletado com sucesso.'}, status=status.HTTP_200_OK)
            
            if data['delete_type'] == 'pi': 
                for i in data['items']: 
                    pi = get_object_or_404(ProductItems, company=query['worker'].company.id, pk=i['id'])
                    if pi:
                        pi.delete()
                        return Response({'detail': f'Item {i["id"]} do produto {kwargs["pk"]} deletado com sucesso.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Dados inválidos.'}, status=status.HTTP_401_UNAUTHORIZED)
    

class BrandViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        try:
            data = json.loads(self.request.body)
            if len(data) == 0:
                raise
        except:
            data = self.request.data
            if len(data) == 0:
                pass
        try:
            company = self.request.GET['company']
        except:
            company = data['company']
        worker = get_object_or_404(CompanyWorker, company__slug=company, person=self.request.user.id)
        try:
            queryset = ProductBrand.objects.filter(company__slug=company)
        except MultiValueDictKeyError:
            try:
                queryset = ProductBrand.objects.filter(company__slug=company)
            except MultiValueDictKeyError:
                queryset = ProductBrand.objects.filter(company=0, type=0)
        return { 'queryset': queryset, 'worker': worker, 'data': data }
    serializer_class = BrandSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            query = self.get_queryset()
        except:
            return Response({ "detail": "Dados Inválidos."}, status=status.HTTP_401_UNAUTHORIZED)
        query['data']['company'] = query['worker'].company.id
        query['data']['company_worker'] = query['worker'].id
        brand_serialized = BrandSerializer(data=query['data'])
        if brand_serialized.is_valid():
            brand = ProductBrand.objects.create(
                company = brand_serialized.validated_data['company'],
                company_worker = brand_serialized.validated_data['company_worker'],
                brand = brand_serialized.validated_data['brand'],
            )
            brand_serialized = BrandSerializer(data=brand)
            brand_serialized.is_valid()
        return Response(brand_serialized.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        try:
            query = self.get_queryset()
        except:
            return Response({ "detail": "Dados Inválidos."}, status=status.HTTP_401_UNAUTHORIZED)
        brand_serialized = BrandSerializer(query['queryset'], many=True)
        return Response(brand_serialized.data, status=status.HTTP_200_OK)
    

class MeasureViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        try:
            data = json.loads(self.request.body)
            if len(data) == 0:
                raise
        except:
            data = self.request.data
            if len(data) == 0:
                pass
        try:
            company = self.request.GET['company']
        except:
            company = data['company']
        worker = get_object_or_404(CompanyWorker, company__slug=company, person=self.request.user.id)
        try:
            queryset = ProductMeasure.objects.filter(company__slug=company)
        except MultiValueDictKeyError:
            try:
                queryset = ProductMeasure.objects.filter(company__slug=company)
            except MultiValueDictKeyError:
                queryset = ProductMeasure.objects.filter(company=0, type=0)
        return { 'queryset': queryset, 'worker': worker, 'data': data }
    serializer_class = MeasureSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            query = self.get_queryset()
        except:
            return Response({ "detail": "Dados Inválidos."}, status=status.HTTP_401_UNAUTHORIZED)
        query['data']['company'] = query['worker'].company.id
        query['data']['company_worker'] = query['worker'].id
        measure_serialized = MeasureSerializer(data=query['data'])
        if measure_serialized.is_valid():
            measure = ProductMeasure.objects.create(
                company = measure_serialized.validated_data['company'],
                company_worker = measure_serialized.validated_data['company_worker'],
                measure = measure_serialized.validated_data['measure'],
            )
            measure_serialized = MeasureSerializer(data=measure)
            measure_serialized.is_valid()
        return Response(measure_serialized.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        try:
            query = self.get_queryset()
        except:
            return Response({ "detail": "Dados Inválidos."}, status=status.HTTP_401_UNAUTHORIZED)
        measure_serialized = MeasureSerializer(query['queryset'], many=True)
        return Response(measure_serialized.data, status=status.HTTP_200_OK)

# @csrf_exempt
# def addProduct(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         body["company"] = int(body["company"])
#         body["company_worker"] = int(body["company_worker"])
        
#         if body["type"] == 1:
#             form = forms.AddProductForm(body)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponse(status=200, headers={'content-type': 'application/json'})
#             return HttpResponse("Access violation", status=401, headers={'content-type': 'application/json'})
#         elif body["type"] == 2:
#             form = forms.AddProductSaleForm(body)
#             if form.is_valid():
#                 last_id = form.save().id
#                 return HttpResponse(last_id, status=200, headers={'content-type': 'application/json'})
#             return HttpResponse("Access violation", status=401, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})

# @csrf_exempt
# def editProduct(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         if verifyLogin(body['token']):
#             prod = models.Product.objects.filter(company= body["company"], id=body["id"])
#             if prod[0].name != body["name"]:
#                 prod.update(name=body["name"])
#             elif prod[0].price != body["price"]:
#                 prod.update(price=body["price"])
#             elif prod[0].cost != body["cost"]:
#                 prod.update(cost=body["cost"])
#             elif prod[0].stock != body["stock"]:
#                 prod.update(stock=body["stock"])    
#             return HttpResponse(status=200, headers={'content-type': 'application/json'})
#         return HttpResponse("Access violation", status=401, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})

# @csrf_exempt
# def deleteProduct(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         if int(body["type"]) == 1:
#             model = models.Product.objects.filter(company=body["company"], id=body["id"])
#             productSale = models.ProductItems.objects.filter(company=body["company"], product_item=body["id"])
#             if len(productSale) > 0:
#                 return HttpResponse(status=201, headers={'content-type': 'application/json'})
#             else:
#                 model.delete()
#                 return HttpResponse(status=200, headers={'content-type': 'application/json'})
#         return HttpResponse("Access violation", status=401, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})

# @csrf_exempt
# def deleteProductSale(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         if int(body["type"]) == 2:
#             modelitem = models.ProductItems.objects.filter(company= body["company"], product= body["product"])
#             model = models.Product.objects.filter(company= body["company"], id= body["product"])
#             for m in modelitem:
#                 m.delete()
#             model.delete()
#             return HttpResponse(status=200, headers={'content-type': 'application/json'})
#         elif int(body["type"]) == 1:
#             models.ProductItems.objects.filter(company= body["company"], product= body["product"], product_item= body["product_item"]).delete() 
#             return HttpResponse(status=200, headers={'content-type': 'application/json'})
#         return HttpResponse("Access violation", status=401, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})

# def getProduct(request):
#     if request.method == "GET":
#         try:
#             get = dict(request.GET)
#         except MultiValueDictKeyError:
#             get = []
#             return HttpResponse("Invalid data!", status=401, headers={'content-type': 'application/json'})
#         if verifyLogin(get['token']):
#             model = models.Product.objects.filter(company=get['company'][0], type=get['type'][0])
#             data = []
#             for m in model:
#                 data.append({
#                     'id': str(m.id),
#                     'name': str(m.name),
#                     'brand_id': str(m.brand.id) if type(m.brand) != type(None) else '',
#                     'brand': str(m.brand),
#                     'measure_id': str(m.measure.id) if type(m.measure) != type(None) else '',
#                     'measure': str(m.measure),
#                     'stock': str(m.stock),
#                     'cost': str(round(m.cost,2)) if type(m.cost) != type(None) else '0',
#                     'price': str(m.price),
#                     'type': str(m.type)
#                 })
#             return HttpResponse(json.dumps(data), status=200, headers={'content-type': 'application/json'})
#         return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})

# def setProductCost(id, company):
#     model = models.ProductItems.objects.filter(company=company, product=id)
#     data = []
#     cost = 0
#     quantity = 0

#     for m in model:
#         cost += m.product_item.cost*m.quantity
#         quantity += m.quantity
#         data.append({
#             'id': str(m.id),
#             'cost': str(m.product_item.cost),
#         })
#     if quantity == 0:
#         return 0
#     else:    
#         models.Product.objects.filter(id=id).update(cost=cost)


# @csrf_exempt
# def addProductItems(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         for i in body["items"]:
#             form = forms.AddProductItemsForm({
#                 "company": body["company"],
#                 "company_worker": body["company_worker"],
#                 "product": body["product_sale"],
#                 "product_item": i["id"],
#                 "quantity": i["quantity"],
#             })
#             if form.is_valid():
#                 form.save()
#             setProductCost(body["product_sale"], body["company"])
#         return HttpResponse(status=200, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})

# @csrf_exempt
# def addProductItem(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         form = forms.AddProductItemsForm(body)
#         if form.is_valid():
#             models.Product.objects.filter(company=body["company"], id=body["product_sale"]).update()
#         return HttpResponse(status=200, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})

# def getProductItems(request):
#     if request.method == "GET":
#         try:
#             get = dict(request.GET)
#         except MultiValueDictKeyError:
#             get = []
#             return HttpResponse("Invalid data!", status=401, headers={'content-type': 'application/json'})
#         if verifyLogin(get['token'][0]):
#             model = models.ProductItems.objects.filter(company=get['company'][0], product=get['product'][0])
#             data = []
#             for m in model:
#                 data.append({
#                     'id': str(m.id),
#                     'prod': str(m.product.id),
#                     'prod_item': str(m.product_item.id),
#                     'name': str(m.product_item.name),
#                     'measure': str(m.product_item.measure),
#                     'quantity': str(m.quantity),
#                     'cost': str(round(m.product_item.cost,2)),
#                     'price': str(m.product_item.price),
#                 })
#             return HttpResponse(json.dumps(data), status=200, headers={'content-type': 'application/json'})
#         return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=403, headers={'content-type': 'application/json'})

# @csrf_exempt
# def addBrand(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         form = forms.AddBrandForm(body)
#         if form.is_valid():
#             form.save()
#             return HttpResponse(status=200, headers={'content-type': 'application/json'})
#         return HttpResponse("Access violation", status=401, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})

# def getBrand(request):
#     if request.method == "GET":
#         try:
#             get = dict(request.GET)
#         except MultiValueDictKeyError:
#             get = []
#             return HttpResponse("Invalid data!", status=401, headers={'content-type': 'application/json'})
#         if verifyLogin(get['token']):
#             data = []
#             for m in models.ProductBrand.objects.filter(company=get['company'][0]):
#                 data.append({
#                     'brand_id': m.id,
#                     'brand_name': m.brand,
#                 })
#             return HttpResponse(json.dumps(data), status=200, headers={'content-type': 'application/json'})
#         return HttpResponse(status=401, headers={'content-type': 'application/json'})

# @csrf_exempt
# def addMeasure(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         form = forms.AddMeasureForm(body)
#         if form.is_valid():
#             form.save()
#             return HttpResponse(status=200, headers={'content-type': 'application/json'})
#         return HttpResponse("Access violation", status=401, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})

# def getMeasure(request):
#     if request.method == "GET":
#         try:
#             get = dict(request.GET)
#         except MultiValueDictKeyError:
#             get = []
#             return HttpResponse("Invalid data!", status=401, headers={'content-type': 'application/json'})
#         if verifyLogin(get['token']):
#             data = []
#             for m in models.ProductMeasure.objects.filter(company=get['company'][0]):
#                 data.append({
#                     'measure_id': m.id,
#                     'measure_name': m.measure,
#                 })
#             return HttpResponse(json.dumps(data), status=200, headers={'content-type': 'application/json'})
#         return HttpResponse("Access violation", status=401, headers={'content-type': 'application/json'})

# @csrf_exempt
# def addProductStock(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         model = models.Product.objects.filter(company=body["company"],id=body["product"])
#         for m in model:
#             mod = m.cost*m.stock
#             front = float(body["quantity"])*float(body["cost"])
#             base = m.stock+float(body["quantity"])
#             if m.stock == 0 or base == 0:
#                 model.update(stock=base,cost=body["cost"])
#             else:
#                 model.update(stock=round(base,2),cost=(mod+front)/base) 
#         return HttpResponse(status=200, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})
    
# @csrf_exempt
# def addPartner(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         if verifyLogin(body["token"]):
#             form = forms.AddPartnerForm(body)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponse(status=200, headers={'content-type': 'application/json'})
#             return HttpResponse("Access violation", status=401, headers={'content-type': 'application/json'})
#         return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=403, headers={'content-type': 'application/json'})

# def getPartner(request):
#     if request.method == "GET":
#         try:
#             get = dict(request.GET)
#         except MultiValueDictKeyError:
#             return HttpResponse("Invalid data!", status=401, headers={'content-type': 'application/json'})
#         if verifyLogin(get['token'][0]):
#             data = []
#             for m in models.Partner.objects.filter(company=get['company'][0]):
#                 try:
#                     city = m.city.id
#                 except:
#                     city = ''
#                 data.append({
#                     'id': str(m.id),
#                     'person_f_j': m.person_f_j,
#                     'type_client': m.type_client,
#                     'type_provider': m.type_provider,
#                     'type_conveyor': m.type_conveyor,
#                     'name': m.name,
#                     'fantasy': m.fantasy,
#                     'cpf_cnpj': m.cpf if m.cpf != None else m.cnpj,
#                     'rg_ie': m.rg if m.rg != None else m.ie,
#                     'phone_number': m.phone_number,
#                     'email': m.email,
#                     'cep': m.cep,
#                     'street': m.street,
#                     'district': m.district,
#                     'city': city,
#                     'num': m.num,
#                 })
#             return HttpResponse(json.dumps(data, indent=3), status=200, headers={'content-type': 'application/json'})
#         return HttpResponse("Access violation", status=401, headers={'content-type': 'application/json'})

# @csrf_exempt
# def editPartner(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         if verifyLogin(body["token"]):
#             form = forms.AddPartnerForm(body)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponse(status=200, headers={'content-type': 'application/json'})
#             return HttpResponse("Access violation", status=401, headers={'content-type': 'application/json'})
#         return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=403, headers={'content-type': 'application/json'})

# @csrf_exempt
# def deletePartner(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         if verifyLogin(body["token"]):
#             form = forms.AddPartnerForm(body)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponse(status=200, headers={'content-type': 'application/json'})
#             return HttpResponse("Access violation", status=401, headers={'content-type': 'application/json'})
#         return HttpResponse("Access violation", status=402, headers={'content-type': 'application/json'})
#     return HttpResponse("Access violation", status=403, headers={'content-type': 'application/json'})

