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

from .models import RentalOffice, OfficeCar
from .serializers import RentalOfficeSerializer, OfficeCarSerializer

AUTHLOCATION = "http://127.0.0.1:8000"
CARLOCATION = "http://127.0.0.1:8001"
STATLOCATION = "http://127.0.0.1:8005"

class OfficeInfoView(APIView):
    def get(self, request, officeUid):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse({"Message": "Токен авторизации отсутствует"}, status=401,
                                         content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION + '/api/v1/session/validate', headers={'Authorization': auth_header})
            if auth_response.status_code != 200:
                http_response = HttpResponse({"Message": "Токен авторизации не валиден"}, status=401,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. User service is down."},
                    status=422)
            return http_response
        office = RentalOffice.objects.get(officeUid=officeUid)

        http_response = HttpResponse(json.dumps({'location': office.location}), status=200,
                                     content_type="application/json")
        return http_response

## GET /offices
class OfficeView(APIView):
    ## Получение списка всех офисов 
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

        offices = RentalOffice.objects.all()
        response = []
        for office in offices:
            tmp_response = {
                "officeUid": str(office.officeUid),
                "location": office.location
            }
            response.append(tmp_response)
        json_response = json.dumps(response)
        http_response = HttpResponse(json_response, status=200, content_type='application/json')
        return http_response

    ## Добавить новый офис
    def post(self, request):
        try:
            auth_header = request.headers["Authorization"]
        except:
            http_response = HttpResponse({"Message": "Токен авторизации отсутствует"}, status=401,
                                         content_type="application/json")
            return http_response

        try:
            auth_response = requests.get(AUTHLOCATION+'/api/v1/session/validate',
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
            payload = jwt.decode(auth_header.split()[1], options={"verify_signature":False})
        except:
            return HttpResponse(
                content={"Отсутствует хэдер"},
                status=401)
        if not payload['role']:
            http_response = HttpResponse({"Message": "Недостаточно прав"}, status=403,
                                         content_type="application/json")
            return http_response

        location = request.data["location"]
        officeUid = uuid.uuid1()
        count_id = len(RentalOffice.objects.all())
        count_id += 1

        db_data = RentalOffice(id=count_id, location=location, officeUid=officeUid)
        try:
            if len(RentalOffice.objects.filter(location=location)) == 0:
                stat_response = requests.patch(STATLOCATION+'/api/v1/reports/booking-by-offices', data={"location": location},
                              headers={'Authorization': auth_header})
                if stat_response.status_code != 200:
                        return HttpResponse(
                        content={"External server error. Report service is down."},
                        status=422)
        except:
            pass
        
        db_data.save()
        http_response = HttpResponse(officeUid, status=201, content_type = "application/json")
        return http_response
    
## GET /offices/{officeUid}/cars
class CarsInOfficeView(APIView):
    ## Информация обо всех машинах офиса  
    def get(self, request, officeUid):
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

        office = get_object_or_404(RentalOffice, officeUid=officeUid) # Проверка сущетсвования офиса с указаным Uid
        office_cars = OfficeCar.objects.filter(officeUid=officeUid)
        print(len(office_cars))
        cars_info = []
        for car in office_cars:
            try:
                car_response = requests.get(CARLOCATION+"/api/v1/cars/"+str(car.carUid), headers={"Authorization": auth_header})
                info = json.loads(car_response.content)
                
                cars_info.append(info)
            except:
                http_response = HttpResponse(
                        content={"External server error. Car service is down."},
                        status=422)
                return http_response
        
        http_response = HttpResponse(json.dumps(cars_info), status=200, content_type="application/json")

        return http_response

## GET /offices/cars/{carUid}
class CarInAllOfficesView(APIView):
    ## Информация о машине и её доступности во всех офисах  
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

        try:
            car_response = requests.get(CARLOCATION+'/api/v1/cars/'+str(carUid), headers={"Authorization": auth_header})
            if car_response.status_code != 200:
                http_response = HttpResponse(car_response.json(), status=car_response.status_code,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. Car service is down."},
                    status=422)
            return http_response
        car_info = json.loads(car_response.content)

        locations = []
        office_cars = OfficeCar.objects.filter(carUid=carUid)
        for office_car in office_cars:
            office = RentalOffice.objects.get(officeUid=office_car.officeUid)
            locations.append(office.location)

        result = {"CarInfo":car_info, "Locations":locations}
        
        http_response = HttpResponse(json.dumps(result), status=200, content_type="application/json")
        return http_response

## GET /offices/{officeUid}/cars/{carUid}
class OfficeCarInfoView(APIView):
    ## Информация о машине и её доступности в конкретном офисе 
    def get(self, request, officeUid, carUid):
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

        office_car = get_object_or_404(OfficeCar, officeUid=officeUid, carUid=carUid)

        try:
            car_response = requests.get(CARLOCATION+"/api/v1/cars/" + str(carUid), headers={"Authorization": auth_header})
        except:
            http_response = HttpResponse(
                    content={"External server error. Car service is down."},
                    status=422)
            return http_response
        carInfo = json.loads(car_response.content)

        try:
            RentalOffice.objects.get(officeUid=officeUid)
            availability = True
        except:
            availability = False

        carInfo["availability"] = availability
        
        http_response = HttpResponse(json.dumps(carInfo), status=200, content_type="application/json")
        return http_response


## POST /offices/{officeUid}/car/{carUid}
## DELETE /offices/{officeUid}/car/{carUid}
class ChangeOfficeStateView(APIView):
    ## Добавление нового автомобиля в офис
    def post(self, request, officeUid, carUid):
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
            payload = jwt.decode(auth_header.split()[1], options={"verify_signature":False})
        except:
            return HttpResponse(
                content={"Отсутствует хэдер"},
                status=401)
        if not payload['role']:
            http_response = HttpResponse({"Message": "Недостаточно прав"}, status=403,
                                         content_type="application/json")
            return http_response

        office = get_object_or_404(RentalOffice, officeUid=officeUid)

        try:
            car_response = requests.get(CARLOCATION+'/api/v1/cars/'+str(carUid), headers={'Authorization': auth_header})
            if car_response.status_code != 200:
                http_response = HttpResponse(car_response.json(), status=car_response.status_code,
                                             content_type="application/json")
                return http_response
        except:
            http_response = HttpResponse(
                    content={"External server error. Car service is down."},
                    status=422)
            return http_response

        officecar = OfficeCar.objects.filter(officeUid=officeUid, carUid=carUid)
        if (len(officecar) > 0):
            http_response = HttpResponse(json.dumps({"Message":"Машина уже была добавлена ранее."}), status=409,
                                         content_type="application/json")
            return http_response

        id = uuid.uuid1()
        db_data = OfficeCar(id=id, officeUid=officeUid, carUid=carUid)

        db_data.save()

        http_response = HttpResponse(status=200, content_type="application/json")
        return http_response
    
    ## Удаление автомобиля из офиса  
    def delete(self, request, officeUid, carUid):
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

        if not payload['role']:
            http_response = HttpResponse(json.dumps({"Message": "Недостаточно прав"}), status=403,
                                         content_type="application/json")
            return http_response

        office_car = get_object_or_404(OfficeCar, officeUid=officeUid, carUid=carUid)
        
        office_car.delete()

        http_response = HttpResponse(status=200, content_type='application/json')
        return http_response

## GET /offices/healthcheck
## Проверка состояния сервиса
class HealthCheckView(APIView):
    def get(self, request):
        return HttpResponse(status=200)
