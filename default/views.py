from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets, generics, filters

from default.serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from default.models import Company, CompanyWorker

    
# class LoginViewSet(viewsets.ModelViewSet):
#     def get_queryset(self):
#         queryset = Token.objects.select_related('user').filter(user=self.request.user.id)
#         return queryset
#     serializer_class = TokenSerializer
    
#     authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]
    
    
class CompanyWorkerViewSet(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        company = CompanyWorker.objects.select_related('company').filter(person=request.user.id)
        serializer = CompanyWorkerSerializer(company, many=True)
        return Response(serializer.data)
      


#### OLD API ####################################################
from django.shortcuts import render, HttpResponse               #
from django.utils.datastructures import MultiValueDictKeyError  #
from django.views.decorators.csrf import csrf_exempt            #
from django.contrib.auth.models import User                     #
from django.contrib.auth import authenticate, login             #
from . import forms                                             #
from . import models                                            #
import json                                                     #
import requests as r                                            #
#################################################################

# @csrf_exempt
def login(request):
    # body = json.loads(request.body)
    # email = body['email']
    # password = body['password']
    # user = User.objects.get(email=email)
    log = login(authenticate(username='admin', password='admin'))
    print(log)
    return HttpResponse(json.dumps({ 'e': 'w' }), status=200, headers={'content-type': 'application/json'})
    # return HttpResponse(json.dumps({ 'e': 'w' }), status=200, headers={'content-type': 'application/json'})
    # return HttpResponse(status=201)

def verifyLogin(token):
    req = r.post('http://127.0.0.1:8080/auth/jwt/verify/', {
        'token': token,
    })
    return HttpResponse(status=req.status_code)

@csrf_exempt
def register(request):
    if request.method == "POST":
        body = json.loads(request.body)
        form = forms.NewRegisterForm(body)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200, headers={'content-type': 'application/json'})
        return HttpResponse("Invalid form!", status=401, headers={'content-type': 'application/json'})
    return HttpResponse("Need be a POST", status=401, headers={'content-type': 'application/json'})
    
def getCompany(request):
    try:
        get = request.GET
    except MultiValueDictKeyError:
        return HttpResponse("Cannot find your email!", status=401, headers={'content-type': 'application/json'})
    token = get["token"]
    email = get["email"]
    if verifyLogin(token):
        user = models.User.objects.get(email=email)
        companyworker = models.CompanyWorker.objects.filter(person=user).order_by('company')
        comp = []
        for w in companyworker:
            comp.append({
                'company_id': str(w.company.id),
                'company': str(w.company.company),
                'worker_id': str(w.id),
                'slug': str(w.company.slug),
                'email': str(w.person.email),
                'first_name': str(w.person.first_name), 
            })
        return HttpResponse(json.dumps(comp), status=200, headers={'content-type': 'application/json'})
    return HttpResponse("Cannot find your key!", status=401, headers={'content-type': 'application/json'})
   
def getCities(request):
    if request.method == "GET":
        try:
            get = dict(request.GET)
        except MultiValueDictKeyError:
            get = []
            return HttpResponse("Invalid data!", status=401, headers={'content-type': 'application/json'})
        if verifyLogin(get['token'][0]):
            model = models.City.objects.all()
            cities = []
            for m in model:
                cities.append({
                    'id': str(m.id),
                    'name': str(m.name),
                })
            return HttpResponse(json.dumps(cities), status=200, headers={'content-type': 'application/json'})
        return HttpResponse("Access violation!", status=401, headers={'content-type': 'application/json'})
    return HttpResponse("Access violation!", status=402, headers={'content-type': 'application/json'})

@csrf_exempt
def addBugReport(request):
    if request.method == "POST":
        body = json.loads(request.body)
        form = forms.AddBugReportForm(body)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200, headers={'content-type': 'application/json'})
        return HttpResponse("Invalid form!", status=401, headers={'content-type': 'application/json'})
    return HttpResponse("Need be a POST", status=401, headers={'content-type': 'application/json'})