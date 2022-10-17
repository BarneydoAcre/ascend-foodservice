from django.shortcuts import render, HttpResponse
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError

from foodservice.settings import BASE_DIR
import register.models

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

@csrf_exempt
def printPDF(request, id):
    import io
    sale = models.Sale.objects.filter(id=id)
    sale_items = models.SaleItems.objects.filter(sale=id)
    buffer = io.BytesIO()
    cnv = canvas.Canvas(buffer, pagesize=(mm2p(72),mm2p(130)))
    line = 125
    col = 1
    total = 0
    l = "_______________________________________"

    cnv.setFont("Helvetica", 8)
    cnv.drawString(mm2p(col+25),mm2p(line),"DELICIAS DA LIA")
    line += -6
    for i in sale:
        delivery = i.delivery
        cnv.drawString(mm2p(col),mm2p(line),"Venda Nº: "+str(i.id))
        cnv.drawString(mm2p(col+44),mm2p(line),str(i.created).split(' ')[0])
        line += -2
    cnv.drawString(mm2p(col-1),mm2p(line),l)
    line += -6
    cnv.drawString(mm2p(col-1),mm2p(line),"|produto|                                           |preço| |total|")
    line += -6
    for i in sale_items:
        total = total + i.price*i.quantity
        if i.quantity == 0.5:
            cnv.drawString(mm2p(col),mm2p(line),'½ '+i.product.name)
        else:
            cnv.drawString(mm2p(col),mm2p(line),str(int(i.quantity))+' '+i.product.name)
        cnv.drawString(mm2p(col+44),mm2p(line),str(i.price))
        cnv.drawString(mm2p(col+53),mm2p(line),str(i.price*i.quantity))
        line += -4
    cnv.drawString(mm2p(col-1),mm2p(line),l)
    line += -5
    cnv.drawString(mm2p(col-1),mm2p(line),"Frete_______________________________"+str(round(delivery,3)))
    line += -1
    cnv.drawString(mm2p(col-1),mm2p(line),l)
    line += -10
    cnv.drawString(mm2p(col-1),mm2p(line),l)
    line += -5
    cnv.drawString(mm2p(col-1),mm2p(line),"Total_______________________________"+str(round(total+delivery,3)))
    line += -1
    cnv.drawString(mm2p(col-1),mm2p(line),l)
    line += -10
    cnv.drawString(mm2p(col+3),mm2p(7),"Chave PIX: CPF - 002.715.540-45")
    cnv.setFont("Helvetica", 6)
    cnv.drawString(mm2p(col+25),mm2p(3),"Versão 0.00.001")
    cnv.drawString(mm2p(col+25),mm2p(1),l)

    cnv.showPage()
    cnv.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=str(sale[0].id)+".pdf")

def mm2p(milimetros):
    return milimetros / 0.352777
