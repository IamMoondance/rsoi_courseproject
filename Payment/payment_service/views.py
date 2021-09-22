from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.views import APIView
from http import HTTPStatus
from rest_framework.generics import get_object_or_404
import json
import datetime
import requests
import uuid

from .models import Payment
from .serializers import PaymentSerializer

##AUTHLOCATION = 'http://127.0.0.1:8000'

AUTHLOCATION = 'http://80.78.251.85:8000'

class PaymentInfoView(APIView):
    def get(self, request, paymentUid):
        try:
            auth_header = request.headers["Authorization"]
        except KeyError:
            http_response = HttpResponse({"Message":
                            "Токен авторизации отсутствует"}, status=401,
                            content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION + '/api/v1/session/validate',
                                         headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse({"Message": "Токен авторизации не валиден"}, status=401,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response

        payment = Payment.objects.get(rent_uid=paymentUid)

        data = {
            "price":payment.price
        }

        http_response = HttpResponse(json.dumps(data), status=200,
                                     content_type="application/json")
        return http_response

class PaymentView(APIView):
    # Добавить сущность оплаты бронирования
    def post(self, request):
        try:
            auth_header = request.headers["Authorization"]
        except KeyError:
            http_response = HttpResponse({"Message":
                            "Токен авторизации отсутствует"}, status=401,
                            content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION + '/api/v1/session/validate',
                                         headers={'Authorization': auth_header})
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
            body = request.data
            price = body["price"]
            rent_uid = uuid.uuid1()
            status = "NEW"

            count_id = len(Payment.objects.all())
            count_id += 1
            
            db_data = Payment(id=count_id, price=price, rent_uid=rent_uid, status=status)
            db_data.save()

            return HttpResponse(rent_uid, status=201)
        except:
            return HttpResponse(
                content={"Некорректные данные для создания оплаты"},
                status=400)

## Откат данных в транзакции
class RollbackPaymentView(APIView):
    ## Отмена бронирования   
    def delete(self, request, rent_uid):
        try:
            auth_header = request.headers["Authorization"]
        except KeyError:
            http_response = HttpResponse({"Message":
                            "Токен авторизации отсутствует"}, status=401,
                            content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION + '/api/v1/session/validate',
                                         headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse({"Message": "Токен авторизации не валиден"}, status=401,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response

        payment = get_object_or_404(Payment, id=payment_uid)
        payment.delete()
        http_response = HttpResponse(status=204)
        return http_response

class HealthCheckView(APIView):
    # Health
    def get(self, request):
        return HttpResponse(status=200)
