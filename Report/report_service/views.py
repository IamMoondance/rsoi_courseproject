from django.shortcuts import render

from django.core.checks.messages import Info
from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.views import APIView
from http import HTTPStatus
from rest_framework.generics import get_object_or_404
import json
import datetime
import requests
import uuid
import jwt

from .models import CarStat, OfficeStat
#from .serializers import

AUTHLOCATION = "http://127.0.0.1:8000"

class BookingModelView(APIView):
    ## Статистика бронирования автомобилей по моделям
    def get(self, request):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse({"Message": "Токен авторизации отсутствует"}, status=401,
                                         content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION+'/api/v1/session/validate', headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse({"Message": "Токен авторизации не валиден"}, status=401,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response

        payload = jwt.decode(auth_header.split()[1], options={"verify_signature":False})

        if not payload['role']:
            http_response = HttpResponse(json.dumps({"Message": "Недостаточно прав"}), status=403,
                                         content_type="application/json")
            return http_response

        try:
            model = request.data["model"]
        except:
            http_response = HttpResponse(json.dumps({"Message": "Информация о модели не получена."}), status=400,
                                                    content_type="application/json")
            return http_response
        try:
            stat = CarStat.objects.get(model=model)
        except:
            http_response = HttpResponse(json.dumps({"Message": "Отсутствует статистика для данной модели."}), status=404,
                                                    content_type="application/json")
            return http_response

        http_response = HttpResponse(json.dumps({"Count": stat.count}), status=200,
                                                content_type="application/json")
        return http_response


    ## Увеличить статистику
    def post(self, request):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse({"Message": "Токен авторизации отсутствует"}, status=401,
                                         content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION+'/api/v1/session/validate', headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse({"Message": "Токен авторизации не валиден"}, status=401,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response

        payload = jwt.decode(auth_header.split()[1], options={"verify_signature":False})

        try:
            model = request.data["model"]
        except:
            http_response = HttpResponse(json.dumps({"Message": "Информация о модели не получена."}), status=400,
                                                    content_type="application/json")
            return http_response
        try:
            stat = CarStat.objects.get(model=model)
        except:
            http_response = HttpResponse(json.dumps({"Message": "Отсутствует статистика для данной модели."}), status=404,
                                                    content_type="application/json")
            return http_response

        stat.count = stat.count + 1

        http_response = HttpResponse(status=200, content_type="application/json")
        return http_response

    ## Инициализировать статистику
    def patch(self, request):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse({"Message": "Токен авторизации отсутствует"}, status=401,
                                         content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION+'/api/v1/session/validate', headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse({"Message": "Токен авторизации не валиден"}, status=401,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response

        payload = jwt.decode(auth_header.split()[1], options={"verify_signature":False})

        if not payload['role']:
            http_response = HttpResponse(json.dumps({"Message": "Недостаточно прав"}), status=403,
                                         content_type="application/json")
            return http_response

        try:
            model = request.data["model"]
        except:
            http_response = HttpResponse(json.dumps({"Message": "Информация о модели не получена."}), status=400,
                                                    content_type="application/json")
            return http_response

        if len(CarStat.objects.filter(model=model)) > 0:
            http_response = HttpResponse(json.dumps({"Message": "Статистика уже инициализирована."}), status=409,
                                                content_type="application/json")
            return http_response

        count_id = len(CarStat.objects.all())
        count_id += 1
        db_data = CarStat(id=count_id, model=model, count=0)
        db_data.save()

        http_response = HttpResponse(status=200,
                        content_type="application/json")
        return http_response

class BookingOfficesView(APIView):
    ## Статистика бронирования по офисам
    def get(self, request):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse({"Message": "Токен авторизации отсутствует"}, status=401,
                                         content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION+'/api/v1/session/validate', headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse({"Message": "Токен авторизации не валиден"}, status=401,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response

        payload = jwt.decode(auth_header.split()[1], options={"verify_signature":False})

        if not payload['role']:
            http_response = HttpResponse(json.dumps({"Message": "Недостаточно прав"}), status=403,
                                         content_type="application/json")
            return http_response

        try:
            location = request.data["location"]
        except:
            http_response = HttpResponse(json.dumps({"Message": "Информация о адресе не получена."}), status=400,
                                                    content_type="application/json")
            return http_response
        try:
            stat = OfficeStat.objects.get(location=location)
        except:
            http_response = HttpResponse(
                json.dumps({"Message": "Отсутствует статистика для данного офиса."}), status=404,
                           content_type="application/json")
            return http_response

        http_response = HttpResponse(json.dumps({"Count":stat.count}), status=200,
                                                content_type="application/json")
        return http_response

    ## Увеличить статистику
    def post(self,request):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse({"Message": "Токен авторизации отсутствует"}, status=401,
                                         content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION+'/api/v1/session/validate', headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse({"Message": "Токен авторизации не валиден"}, status=401,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response

        try:
            location = request.data["location"]
        except:
            http_response = HttpResponse(json.dumps({"Message": "Информация о адресе не получена."}), status=400,
                                                    content_type="application/json")
            return http_response
        try:
            stat = OfficeStat.objects.get(location=location)
        except:
            http_response = HttpResponse(
                json.dumps({"Message": "Отсутствует статистика для данного офиса."}), status=404,
                           content_type="application/json")
            return http_response
        stat.count = stat.count + 1

        http_response = HttpResponse(status=200,
                            content_type="application/json")
        return http_response

    ## Инициализировать статистику
    def patch(self, request):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse({"Message": "Токен авторизации отсутствует"}, status=401,
                                         content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION+'/api/v1/session/validate', headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse({"Message": "Токен авторизации не валиден"}, status=401,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response

        payload = jwt.decode(auth_header.split()[1], options={"verify_signature":False})

        if not payload['role']:
            http_response = HttpResponse(json.dumps({"Message": "Недостаточно прав"}), status=403,
                                         content_type="application/json")
            return http_response

        try:
            location = request.data["location"]
        except:
            http_response = HttpResponse(json.dumps({"Message": "Информация о адресе не получена."}), status=400,
                                                    content_type="application/json")
            return http_response

        if len(OfficeStat.objects.filter(location=location)) > 0:
            http_response = HttpResponse(json.dumps({"Message": "Статистика уже инициализирована."}, status=409,
                                                content_type="application/json"))
            return http_response

        count_id = len(OfficeStat.objects.all())
        count_id += 1
        db_data = OfficeStat(id=count_id, location=location, count=0)
        db_data.save()

        http_response = HttpResponse(status=200,
                            content_type="application/json")
        return http_response
