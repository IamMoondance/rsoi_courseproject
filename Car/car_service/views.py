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

from .models import Car
from .serializers import CarSerializer

##AUTHLOCATION = "http://127.0.0.1:8000"
##STATLOCATION = "http://127.0.0.1:8005"

AUTHLOCATION = "http://80.78.251.85:8000"
STATLOCATION = "http://80.78.251.85:8005"

# GET /cars
# POST /cars
class CarsView(APIView):
    # Получение списка всех машин
    def get(self, request):
        try:
            auth_header = request.headers["Authorization"]
        except KeyError:
            http_response = HttpResponse(json.dumps({"Message":
                            "Токен авторизации отсутствует"}), status=401,
                            content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION+'/api/v1/session/validate',
                                         headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse(json.dumps({"Message":
                                "Токен авторизации не валиден"}), status=401,
                                content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response

        cars = Car.objects.all()
        response = []
        json_response = list({})
        for car in cars:
            tmp_response = {
                "carUid": str(car.carUid),
                "brand": car.brand,
                "car_model": car.car_model,
                "power": str(car.power),
                "car_type": car.car_type,
                "price_per_hour": str(car.price_per_hour)
                }
            response.append(tmp_response)
        json_response.append(json.dumps(response))
        http_response = HttpResponse(json_response, status=200, content_type='application/json')
        return http_response

    # Добавление нового автомобиля
    def post(self, request):
        try:
            auth_header = request.headers["Authorization"]
        except KeyError:
            http_response = HttpResponse(json.dumps({"Message":
                            "Токен авторизации отсутствует"}), status=401,
                            content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION+'/api/v1/session/validate', headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse(json.dumps({"Message": "Токен авторизации не валиден"}), status=401,
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

        body = request.data
        count_id = len(Car.objects.all())
        count_id += 1
        car_proto = {
            'id': count_id,
            'carUid': uuid.uuid1(),
            'brand': body["brand"],
            'car_model': body["car_model"],
            'power': body["power"],
            'car_type': body["car_type"],
            'price_per_hour': body["price_per_hour"]
        }

        model = body["car_model"]
        cars = Car.objects.filter(car_model=model)
        if len(cars) == 0:
            try:
                stat_response = requests.patch(STATLOCATION+'/api/v1/reports/booking-by-models', data={"model": body["car_model"]},
                            headers={'Authorization': auth_header})
            except:
                pass
    
        serializer = CarSerializer(data=car_proto)
        if serializer.is_valid(raise_exception=True):
            car_saved = serializer.save()

        http_response = HttpResponse(car_proto.get("carUid"), status=201)
        return http_response

# DELETE /cars/{carUid}
class CarView(APIView):
    def get(self, request, carUid):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse(json.dumps({"Message": "Токен авторизации отсутствует"}), status=401,
                                         content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION+'/api/v1/session/validate', headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse(json.dumps({"Message": "Токен авторизации не валиден"}), status=401,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response

        car = get_object_or_404(Car, carUid=carUid)

        tmp_response = {
            "carUid": str(car.carUid),
            "brand": car.brand,
            "car_model": car.car_model,
            "power": str(car.power),
            "car_type": car.car_type,
            "price_per_hour": str(car.price_per_hour)
            }
        json_response = json.dumps(tmp_response)
        http_response = HttpResponse(json_response, status=200, content_type='application/json')
        return http_response

    # Удаление информации об автомобиле
    def delete(self, request, carUid):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse(json.dumps({"Message":
                            "Токен авторизации отсутствует"}), status=401,
                            content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION+'/api/v1/session/validate', headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse(json.dumps({"Message": "Токен авторизации не валиден"}), status=401,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response

        payload = jwt.decode(auth_header.split()[1], options={"verify_signature": False})

        if not payload['role']:
            http_response = HttpResponse(json.dumps({"Message": "Недостаточно прав"}), status=403,
                                         content_type="application/json")
            return http_response

        car = get_object_or_404(Car, carUid=carUid)
        car.delete()
        
        http_response = HttpResponse(status=200, content_type='application/json')
        return http_response


# GET /cars/healthcheck
# Проверка состояния сервиса
class HealthCheckView(APIView):
    def get(self, request):
        return HttpResponse(status=200)
