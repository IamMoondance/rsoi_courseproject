from django.db import models
from django.shortcuts import render

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
from .models import Rental
from .serializers import RentalSerializer
import pytz

utc=pytz.UTC

##AUTHLOCATION = 'http://127.0.0.1:8000'
##STATLOCATION = 'http://127.0.0.1:8005'
##PAYMENTLOCATION = 'http://127.0.0.1:8003'
##OFFICELOCATION = 'http://127.0.0.1:8004'
##CARLOCATION = 'http://127.0.0.1:8001'

AUTHLOCATION = 'http://80.78.251.85:8000'
STATLOCATION = 'http://80.78.251.85:8005'
PAYMENTLOCATION = 'http://80.78.251.85:8003'
OFFICELOCATION = 'http://80.78.251.85:8004'
CARLOCATION = 'http://80.78.251.85:8001'

## POST /rental
class RentalView(APIView):
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

        payload = jwt.decode(auth_header.split()[1], options={"verify_signature": False})

        rentals = Rental.objects.filter(user_uid=payload["userUid"])

        data = []
        for i in rentals:
            tmp_data = {}
            tmp_data["payment_uid"] = str(i.payment_uid)
            tmp_data["rent_from"] = i.rent_from.date().isoformat()
            tmp_data["rent_until"] = i.rent_until.date().isoformat()
            tmp_data["status"] = i.status
            tmp_data["car_uid"] = str(i.car_uid)
            tmp_data["office_uid"] = str(i.ret_office_uid)
            tmp_data["id"] = str(i.id)
            data.append(tmp_data)
        http_response = HttpResponse(json.dumps(data), status=200, content_type="application/json")
        return http_response
    
    ## Забронировать машину
    def post(self, request):
        try:
            auth_header = request.headers["Authorization"]
        except KeyError:
            http_response = HttpResponse({"Message":
                            "Токен авторизации отсутствует"}, status=401,
                            content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION+'/api/v1/session/validate', headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse({"Message":
                                "Токен авторизации не валиден"}, status=401,
                                content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response

        body = request.data #{ car_uid, taken_from_office, return_to_office,booking_period, payment_data: { ... } }
        rent_uid = uuid.uuid1()
        try:
            car_uid = body['car_uid']
            user_uid = body['user_uid']
            payment_uid = body['payment_uid']
            rent_from = datetime.datetime.combine(datetime.date.fromisoformat(body['rent_from']), datetime.datetime.min.time())
            rent_until = datetime.datetime.combine(datetime.date.fromisoformat(body['rent_until']), datetime.datetime.min.time())

            this_car_rental = Rental.objects.filter(car_uid=car_uid, status='NEW')
            for r in this_car_rental:
                if (r.rent_from.replace(tzinfo=utc) <= rent_from.replace(tzinfo=utc) and rent_from.replace(tzinfo=utc) <= r.rent_until.replace(tzinfo=utc)) \
                or (r.rent_from.replace(tzinfo=utc) <= rent_until.replace(tzinfo=utc) and rent_until.replace(tzinfo=utc) <= r.rent_until.replace(tzinfo=utc)):
                    http_response = HttpResponse(json.dumps({"Message": "Автомобиль недоступен в данный период времени."}),
                                                 status=409,content_type='application/json')
                    return http_response

            status = 'NEW'
            rec_office_uid = body['rec_office_uid']
            ret_office_uid = body['ret_office_uid']
        except:
            http_response = HttpResponse(status=400, content_type='application/json')
            return http_response

        db_data = Rental(id=rent_uid,car_uid=car_uid,user_uid=user_uid,
                         payment_uid=payment_uid, rent_from=rent_from, rent_until=rent_until,
                         status=status,rec_office_uid=rec_office_uid, ret_office_uid=ret_office_uid)

        try:
            location_response = requests.get(OFFICELOCATION+'/api/v1/offices/'+rec_office_uid, headers={'Authorization': auth_header})
        except:
            http_response = HttpResponse(
                    content={"External server error. RentalOffice service is down."},
                    status=422)
            return http_response
        location = location_response.json()['location']

        try:
            car_response = requests.get(CARLOCATION+'/api/v1/cars/'+car_uid, headers={'Authorization': auth_header})
        except:
            http_response = HttpResponse(
                    content={"External server error. Car service is down."},
                    status=422)
            return http_response
        model = car_response.json()['car_model']
        try:
            requests.post(STATLOCATION+'/api/v1/reports/booking-by-models', data={"model": model},
                          headers={'Authorization': auth_header})
        except:
            http_response = HttpResponse(
                    content={"External server error. Report service is down."},
                    status=422)
            return http_response

        try:
            requests.post(STATLOCATION+'/api/v1/reports/booking-by-offices', data={"location": location},
                          headers={'Authorization': auth_header})
        except:
            pass

        db_data.save()
        
        http_response = HttpResponse(rent_uid ,status=201, content_type='application/json')
        return http_response

class EndRentalView(APIView):
    ## Отменить бронирование
    def delete(self, request, rentalUid):
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

        rental = get_object_or_404(Rental, id=rentalUid)
        rental.status = "CLOSED"
        rental.save()
        http_response = HttpResponse(status=200, content_type='application/json')
        return http_response

    ## Завершить бронирование
    def patch(self, request, rentalUid):
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

        rental = get_object_or_404(Rental, id=rentalUid)
        rental.status = "FINISHED"
        rental.save()
        http_response = HttpResponse(status=200, content_type='application/json')

        return http_response

class RentalInfoView(APIView):
    def get(self, request, carUid):
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

        rentals = Rental.objects.filter(carUid=carUid)

        dates = []
        for rental in rentals:
            dates.append({"from": rental.rent_from, "until": rental.rent_until})

        dates = json.dumps(dates)

        http_response = HttpResponse(dates, status=200, content_type="application/json")
        return http_response
