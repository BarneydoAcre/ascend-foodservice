from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets, generics, filters

from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from sale.serializers import *
from sale.models import *
from default.models import *
import json


class SaleViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Sale.objects.filter(company_worker__person=self.request.user.id)
        return queryset
    serializer_class = SaleSerializer
    
    def create(self, request):
        for c in CompanyWorker.objects.filter(id=request.data['company_worker'][0],person=request.user.id):
            if c.company.id == int(request.data['company'][0]):
                sale_data = SaleSerializer(data=request.data)
                if sale_data.is_valid():
                    sale = Sale.objects.create(
                        company=sale_data.validated_data['company'],
                        company_worker=sale_data.validated_data['company_worker'],
                        value=sale_data.validated_data['value'],
                        delivery=sale_data.validated_data['delivery'],
                        total=sale_data.validated_data['total']
                    )
                    serialized_data = SaleSerializer(instance=sale)
                    return Response(serialized_data.data, status=status.HTTP_201_CREATED)    
        return Response({'detail': 'Dados inválidos.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def list(self, request):
        try:
            worker = get_object_or_404(CompanyWorker, company__slug=request.GET['company'],person=request.user.id)
        except MultiValueDictKeyError:
            worker = get_object_or_404(CompanyWorker, company__slug=0,person=request.user.id)
            
        sale = Sale.objects.filter(company=worker.company, canceled=False)
        data = []
        for sl in sale:
            sale_items = SaleItems.objects.prefetch_related('sale').filter(sale=sl.id)
            products = []
            for sli in sale_items:
                products.append({
                    'id': sli.product.id,
                    'name': sli.product.name,
                    'price': sli.product.price,
                    'quantity': sli.quantity
                })
            data.append({
                'sale': f'{sl.id}',
                'company': f'{sl.company}',
                'value': f'{sl.value}',
                'delivery': f'{sl.delivery}',
                'total': f'{sl.total}',
                'created': f'{sl.created}',
                'products': products
            })
        return Response(data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        sale = Sale.objects.filter(id=pk)
        body = json.loads(request.body)
        
        # value
        try:
            if body['value'] is not None:
                sale.update(value=body['value'])
        except:
            pass
        try:
            if request.data['value'] is not None:
                sale.update(value=request.data['value'])
        except:
            pass
        # total
        try:
            if body['total'] is not None:
                sale.update(total=body['total'])
        except:
            pass
        try:
            if request.data['total'] is not None:
                sale.update(total=request.data['total'])
        except:
            pass
        # canceled
        try:
            if body['canceled'] is not None:
                sale.update(canceled=body['canceled'])
        except:
            pass
        try:
            if request.data['canceled'] is not None:
                sale.update(canceled=request.data['canceled'])
        except:
            pass
        return Response(SaleSerializer(sale, many=True).data)
    
@csrf_exempt
def printPDF(request, id):
    import io
    sale = models.Sale.objects.get(id=id)
    sale_items = models.SaleItems.objects.filter(sale=id)
    company = default.models.Company.objects.get(id=sale.company.id)
    buffer = io.BytesIO()
    cnv = canvas.Canvas(buffer, pagesize=(mm2p(72),mm2p(100)))
    line = 95
    col = 1
    total = 0
    l = "_______________________________________"

    cnv.setFont("Helvetica", 8)
    cnv.drawString(mm2p(col+25),mm2p(line),company.company) ##AQUI ERA DELICIAS DA LIA
    line += -6
    delivery = sale.delivery
    date = str(sale.created).split(' ')[0].split('-')
    date = date[2]+'/'+date[1]+'/'+date[0]
    cnv.drawString(mm2p(col),mm2p(line),"Venda Nº: "+str(sale.id))
    cnv.drawString(mm2p(col+44),mm2p(line),str(date))
    line += -2
    cnv.drawString(mm2p(col-1),mm2p(line),l)
    line += -6
    cnv.drawString(mm2p(col-1),mm2p(line),"|produto|                                           |preço| |total|")
    line += -6
    sale_items = SaleItems.objects.prefetch_related('sale').filter(sale=sale.id)
    for sli in sale_items:
        total = total + sli.price*sli.quantity
        if sli.quantity == 0.5:
            cnv.drawString(mm2p(col),mm2p(line),'½ '+sli.product.name)
        else:
            cnv.drawString(mm2p(col),mm2p(line),str(int(sli.quantity))+' - '+sli.product.name)
        cnv.drawString(mm2p(col+44),mm2p(line),str(sli.price))
        cnv.drawString(mm2p(col+53),mm2p(line),str(sli.price*sli.quantity))
        line += -4
    cnv.drawString(mm2p(col-1),mm2p(line),l)
    line += -4
    cnv.drawString(mm2p(col-1),mm2p(line),"Entrega_____________________________"+str(round(delivery,3)))
    line += -1
    cnv.drawString(mm2p(col-1),mm2p(line),l)
    line += -4
    cnv.drawString(mm2p(col-1),mm2p(line),l)
    line += -4
    cnv.setFont("Helvetica", 10)
    cnv.drawString(mm2p(col-1),mm2p(line),"Total_______________________"+str(round(total+delivery,3)))
    cnv.setFont("Helvetica", 8)
    line += -1
    cnv.drawString(mm2p(col-1),mm2p(line),l)
    line += -20
    if len(company.pix_key) > 3:
        cnv.setFont("Helvetica", 12)
        cnv.drawString(mm2p(col+3),mm2p(7),"Chave PIX: CPF -"+sale.company.pix_key)
    cnv.setFont("Helvetica", 6)
    cnv.drawString(mm2p(col+25),mm2p(3),"Versão 0.00.002")
    cnv.drawString(mm2p(col+25),mm2p(1),l)

    cnv.showPage()
    cnv.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=str(sale.id)+".pdf")

def mm2p(milimetros):
    return milimetros / 0.352777



from django.shortcuts import render, HttpResponse
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError

from setup.settings import BASE_DIR
import register.models
import default.models

from default.views import verifyLogin
from reportlab.pdfgen import canvas
import uuid
 
from . import forms
from . import models
import json


@csrf_exempt
def addSale(request):
    if request.method == "POST":
        body = json.loads(request.body)
        form = forms.AddSaleForm(body)
        if form.is_valid():
            last_id = form.save()
            return HttpResponse(last_id.id, status=200, headers={'content-type': 'application/json'})
        return HttpResponse("Invalid form!", status=401, headers={'content-type': 'application/json'})
    return HttpResponse("Need be a POST", status=402, headers={'content-type': 'application/json'})

@csrf_exempt
def addSaleItems(request):
    if request.method == "POST":
        body = json.loads(request.body)
        for i in body["products"]:
            model = register.models.ProductItems.objects.filter(company=body["company"],product=i["id"])
            for m in model:
                register.models.Product.objects.filter(company=body["company"],id=m.product_item.id).update(stock=round(m.product_item.stock-float(i["quantity"]),2))
            data = {
                "company": body["company"],
                "company_worker": body["company_worker"],
                "sale": body["sale"],
                "product": i["id"],
                "quantity": i["quantity"],
                "price": i["price"],
            }
            form = forms.AddSaleItemsForm(data)
            if form.is_valid():
                form.save()
            else:
                return HttpResponse("Invalid form!", status=401, headers={'content-type': 'application/json'})
        return HttpResponse(status=200, headers={'content-type': 'application/json'})
    return HttpResponse("Need be a POST", status=402, headers={'content-type': 'application/json'})

@csrf_exempt
def deleteSale(request):
    if request.method == "POST":
        body = json.loads(request.body)
        if verifyLogin(body["token"]):
            model = models.Sale.objects.filter(company=body["company"],id=body["sale"]).update(canceled=True)
            return HttpResponse(status=200, headers={'content-type': 'application/json'})
        return HttpResponse("Invalid login", status=40, headers={'content-type': 'application/json'})
    return HttpResponse("Need be a POST", status=402, headers={'content-type': 'application/json'})

def getSale(request):
    if request.method == 'GET':
        get = request.GET
        if verifyLogin(get["token"]):
            data = []
            model = models.Sale.objects.filter(company=get["company"], canceled=False).order_by('-id')
            for m in model:
                data.append({
                    "id": m.id,
                    "value": m.value,
                    "delivery": m.delivery,
                    "date": str(m.created).split(' ')[0],
                })
            return HttpResponse(json.dumps(data), status=200, headers={'content-type': 'application/json'})
        return HttpResponse("Invalid Login", status=400, headers={'content-type': 'application/json'})
    return HttpResponse("Need be a POST", status=402, headers={'content-type': 'application/json'})

def getSaleItems(request):
    if request.method == 'GET':
        get = request.GET
        if verifyLogin(get["token"]):
            data = []
            model = models.SaleItems.objects.filter(company=get["company"]).order_by('-id')
            for m in model:
                data.append({
                    "id": m.id,
                    "sale": m.sale.id,
                    "product_id": m.product.id,
                    "product_name": m.product.name,
                    "price": m.price,
                    "quantity": m.quantity
                })
            return HttpResponse(json.dumps(data), status=200, headers={'content-type': 'application/json'})
        return HttpResponse("Invalid Login", status=400, headers={'content-type': 'application/json'})
    return HttpResponse("Need be a POST", status=402, headers={'content-type': 'application/json'})

