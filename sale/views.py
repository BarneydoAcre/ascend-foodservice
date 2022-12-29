from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets, generics, filters

from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse

from sale.serializers import *
from sale.models import *
from register.models import *
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
        try:
            data = json.loads(request.body)
        except:
            data = request.data
            if len(data) == 0:
                pass

        for c in CompanyWorker.objects.filter(company__slug=request.GET['company'],person=request.user.id):
            data['company'] = c.company.id
            data['company_worker'] = c.id
            sale_data = SaleSerializer(data=data)
            if sale_data.is_valid():
                sale = Sale.objects.create(
                    company=sale_data.validated_data['company'],
                    company_worker=sale_data.validated_data['company_worker'],
                    value=sale_data.validated_data['value'],
                    delivery=sale_data.validated_data['delivery'],
                    # total=sale_data.validated_data['total']
                )
                products = []
                for p in data['products']:
                    sale_items = SaleItems.objects.create(
                        company=sale_data.validated_data['company'],
                        company_worker=sale_data.validated_data['company_worker'],
                        sale=sale,
                        product=Product.objects.get(id=int(p['id'])),
                        price=float(p['price']),
                        quantity=float(p['quantity'])
                    )
                    products.append({
                        "id": sale_items.product.id,
                        "name": sale_items.product.name,
                        "price": sale_items.price,
                        "quantity": sale_items.quantity
                    })
                data['sale'] = sale.id
                data['products'] = products
                return Response(data, status=status.HTTP_201_CREATED)    
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
                'value': sl.value,
                'delivery': sl.delivery,
                # 'total': f'{sl.total}',
                'created': f'{sl.created}',
                'products': products
            })
            print(data)
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
        # try:
        #     if body['total'] is not None:
        #         sale.update(total=body['total'])
        # except:
        #     pass
        # try:
        #     if request.data['total'] is not None:
        #         sale.update(total=request.data['total'])
        # except:
        #     pass
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
    from reportlab.pdfgen import canvas
    import io
    sale = Sale.objects.get(id=id)
    sale_items = SaleItems.objects.filter(sale=id)
    company = Company.objects.get(id=sale.company.id)
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
            cnv.drawString(mm2p(col),mm2p(line),str(float(sli.quantity))+' - '+sli.product.name)
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
