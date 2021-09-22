from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.views import APIView
from http import HTTPStatus
from rest_framework.generics import get_object_or_404
import json
import datetime
import requests
import uuid
from datetime import date
import jwt
import hashlib
import base64
import time

from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from django.core import serializers

##AUTHLOCATION = "http://127.0.0.1:8000"
##CARLOCATION = "http://127.0.0.1:8001"
##RENTALLOCATION = "http://127.0.0.1:8002"
##OFFICESLOCATION = "http://127.0.0.1:8004"
##PAYMENTLOCATION = "http://127.0.0.1:8003"

AUTHLOCATION = "http://80.78.251.85:8000"
CARLOCATION = "http://80.78.251.85:8001"
RENTALLOCATION = "http://80.78.251.85:8002"
OFFICESLOCATION = "http://80.78.251.85:8004"
PAYMENTLOCATION = "http://80.78.251.85:8003"

# Вывод домашней страницы
class IndexView(APIView):
    def get(self, request):
        pass

# Список офисов
class OfficeListView(APIView):
    def get(self, request):
        try:
            user_response = requests.get(OFFICESLOCATION+'/api/v1/offices',
                                         headers={'Authorization': request.headers['Authorization']})
        except:
            http_response = HttpResponse(status=401, content_type='application/json')
            return http_response
        try:
            http_response = HttpResponse(user_response.text, status=user_response.status_code,
                                         content_type='application/json')
        except:
            http_response = HttpResponse(
                    content={"External server error. RentalOffice service is down."},
                    status=422)
        return http_response

# Информация об офисе
class OfficeInfoView(APIView):
    def get(self, request, officeUid):
        try:
            user_response = requests.get(OFFICESLOCATION + '/api/v1/offices/'+str(officeUid),
                                         headers={'Authorization': request.headers['Authorization']})
        except:
            http_response = HttpResponse(status=401, content_type='application/json')
            return http_response
        try:
            http_response = HttpResponse(user_response.text, status=user_response.status_code,
                                         content_type='application/json')
        except:
            http_response = HttpResponse(
                    content={"External server error. RentalOffice service is down."},
                    status=422)
        return http_response

# Список автомобилей
class CarListView(APIView):
    def get(self, request):
        try:
            user_response = requests.get(CARLOCATION + '/api/v1/cars',
                                         headers={'Authorization': request.headers['Authorization']})
        except:
            http_response = HttpResponse(status=401, content_type='application/json')
            return http_response
        try:
            http_response = HttpResponse(user_response.text, status=user_response.status_code,
                                         content_type='application/json')
        except:
            http_response = HttpResponse(
                    content={"External server error. Car service is down."},
                    status=422)
        return http_response

# Список автомобилей офиса
class OfficeCarInfoView(APIView):
    def get(self, request, officeUid):
        try:
            user_response = requests.get(OFFICESLOCATION + '/api/v1/offices/'+str(officeUid)+'/cars',
                                         headers={'Authorization': request.headers['Authorization']})
        except:
            http_response = HttpResponse(status=401, content_type='application/json')
            return http_response
        try:
            http_response = HttpResponse(user_response.text, status=user_response.status_code,
                                         content_type='application/json')
        except:
            http_response = HttpResponse(
                    content={"External server error. RentalOffice service is down."},
                    status=422)
        return http_response

# Бронирование автомобиля
class RentalView(APIView):
    # Просмотр бронирований
    def get(self, request):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse({"Message": "Токен авторизации отсутствует"}, status=401,
                                         content_type="application/json")
            return http_response

        try:
            rent_response = requests.get(RENTALLOCATION+'/api/v1/rental',
                                         headers={'Authorization': request.headers['Authorization']})
            if rent_response.status_code != 200:
                http_response = HttpResponse(rent_response.text, status=rent_response.status_code,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. Rental service is down."},
                    status=422)
            return http_response
        
        rent_json = rent_response.json()
        data_array = []
        for i in rent_json:
            tmp_data = {}
            tmp_data["rental_uid"] = i["id"]
            tmp_data["car_uid"] = i["car_uid"]
            tmp_data["office_uid"] = i["office_uid"]
            tmp_data["payment_uid"] = i["payment_uid"]

            try:
                car_response = requests.get(CARLOCATION + '/api/v1/cars/' + i["car_uid"],
                                            headers={'Authorization': request.headers['Authorization']})
##                if car_response.status_code != 200:
##                    http_response = HttpResponse(car_response.text, status=car_response.status_code,
##                                                 content_type="application/json")
##                    return http_response
                car_json = car_response.json()
                tmp_data['car'] = car_json["brand"]+" "+car_json["car_model"]
            except:
                pass

            try:
                office_response = requests.get(OFFICESLOCATION+'/api/v1/offices/'+i["office_uid"],
                                              headers={'Authorization': request.headers['Authorization']})
##                if office_response.status_code != 200:
##                    http_response = HttpResponse(office_response.text, status=office_response.status_code,
##                                                 content_type="application/json")
##                    return http_response
                tmp_data['office'] = office_response.json()["location"]
            except:
                pass

            try:
                payment_response = requests.get(PAYMENTLOCATION+'/api/v1/payment/'+i["payment_uid"],
                                               headers={'Authorization': request.headers['Authorization']})

##                if payment_response.status_code != 200:
##                    http_response = HttpResponse(payment_response.text, status=payment_response.status_code,
##                                                 content_type="application/json")
##                    return http_response
                tmp_data['price'] = payment_response.json()["price"]
            except:
                pass
                
            tmp_data['rent_from'] = i["rent_from"]
            tmp_data['rent_until'] = i["rent_until"]
            tmp_data['status'] = i['status']
            data_array.append(tmp_data)

        http_response = HttpResponse(json.dumps(data_array), status=200,
                                     content_type="application/json")
        return http_response

    # Регистрация запроса бронирования
    def post(self, request):
        body = request.data
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse({"Message": "Токен авторизации отсутствует"}, status=401,
                                         content_type="application/json")
            return http_response

        date_from = date.fromisoformat(body["rent_from"])
        date_until = date.fromisoformat(body["rent_until"])
        diff = (date_until-date_from).days

        try:
            car_response = requests.get(CARLOCATION+'/api/v1/cars/'+body["carUid"],
                                        headers={'Authorization': request.headers['Authorization']})
            if car_response.status_code!=200:
                http_response = HttpResponse(car_response.text, status=car_response.status_code,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. Car service is down."},
                    status=422)
            return http_response

        car_price = car_response.json()["price_per_hour"]

        price = int(float(car_price)*24*diff)
        try:
            payment_response = requests.post(PAYMENTLOCATION + '/api/v1/payment', data={"price":price},
                                         headers={'Authorization': request.headers['Authorization']})
            if payment_response.status_code != 201:
                http_response = HttpResponse(payment_response.text, status=payment_response.status_code,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. Payment service is down."},
                    status=422)
            return http_response

        payment_uid = payment_response.text
        # получить UserUid
        try:
            payload = jwt.decode(auth_header.split()[1], options={"verify_signature": False})
        except:
            return HttpResponse(
                content={"Отсутствует хэдер"},
                status=401)
        
        data = {
            "car_uid": body["carUid"],
            "user_uid": payload["userUid"],
            "payment_uid": payment_uid,
            "rent_from": body["rent_from"],
            "rent_until": body["rent_until"],
            "rec_office_uid": body["officeUid"],
            "ret_office_uid": body["officeUid"]
        }

        try:
            rental_response = requests.post(RENTALLOCATION + '/api/v1/rental', data=data,
                          headers={'Authorization': request.headers['Authorization']})

            http_response = HttpResponse(rental_response.text, status=rental_response.status_code,
                         content_type="application/json")
            return http_response
        except:
            cancel_payment = requests.delete(PAYMENTLOCATION + '/api/v1/rollback/' +
                                             str(payment_uid),
                                             headers={'Authorization': request.headers['Authorization']})
            http_response = HttpResponse(
                    content={"External server error. Rental service is down."},
                    status=422)
            return http_response

class RentalChangeView(APIView):
    def patch(self, request, rentalUid):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse({"Message": "Токен авторизации отсутствует"}, status=401,
                                         content_type="application/json")
            return http_response

        try:
            rental_response = requests.patch(RENTALLOCATION+"/api/v1/rental/"+str(rentalUid),
                                             headers={'Authorization': request.headers['Authorization']})

            http_response = HttpResponse(rental_response.text, status=rental_response.status_code,
                                         content_type="application/json")
            return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. Rental service is down."},
                    status=422)
            return http_response

    def delete(self, request, rentalUid):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse({"Message": "Токен авторизации отсутствует"}, status=401,
                                         content_type="application/json")
            return http_response

        try:
            rental_response = requests.delete(RENTALLOCATION + "/api/v1/rental/" + str(rentalUid),
                                             headers={'Authorization': request.headers['Authorization']})

            http_response = HttpResponse(rental_response.text, status=rental_response.status_code,
                                         content_type="application/json")
            return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. Rental service is down."},
                    status=422)
            return http_response

# Вход
class SignInView(APIView):
    # Вход
    def get(self, request):
        try:
            user_response = requests.get(AUTHLOCATION+'/api/v1/session/authorize',
                                         headers={'Authorization': request.headers['Authorization']})
        except:
            http_response = HttpResponse(status=400, content_type='application/json')
        try:
            http_response = HttpResponse(user_response.text, status=user_response.status_code,
                                         content_type='application/json')
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
        return http_response

# Регистрация
class SignUpView(APIView):
    # Запрос регистрации
    def post(self, request):
        try:
            user_response = requests.post(AUTHLOCATION + '/api/v1/session/authorize', data=request.data)
            http_response = HttpResponse(user_response.text, status=user_response.status_code,
                                         content_type='application/json')
            return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response
