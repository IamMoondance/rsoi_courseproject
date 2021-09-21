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
import hashlib
import base64
import time

from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from django.core import serializers

from .models import User
from .serializers import UserSerializer

PUBLIC_KEY = b'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCOXHrINTbLzzfViJ41WoPmLgei
R9urG9sworHWcoApB8qvMa3qVSVqDGd48YeLigwLpzL0ondtPUOAG50vX2TLAfvW
NgA+GjbE1R5mBhrWiXSBJPh3R2p6aKuv4TBi+5h7fQ4lPu1r9RM1NT1oIJsSQlIx
uQLbXOg48TVPhdH/FQIDAQAB
-----END PUBLIC KEY-----'''

PRIVATE_KEY = b'''-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQCOXHrINTbLzzfViJ41WoPmLgeiR9urG9sworHWcoApB8qvMa3q
VSVqDGd48YeLigwLpzL0ondtPUOAG50vX2TLAfvWNgA+GjbE1R5mBhrWiXSBJPh3
R2p6aKuv4TBi+5h7fQ4lPu1r9RM1NT1oIJsSQlIxuQLbXOg48TVPhdH/FQIDAQAB
AoGAMNp3oCDyzvordPHPKQwI24LMR9pU/eEvVP9f+/GLHYl4+qoXvqS9lCjxkUWB
eFdFTvJvwBfI2AoAEgRn6ovX8HdevBRzzr2H5JzzOcsXzEqOZ0IVKCn2ouV/Ucym
JyYqDQQMtuG/MEIxBX4Bex4SodYehtAvm5GOraIGw5WRJMECQQDKHB51hG7npz2x
aGGCHVcWqq5n1bHeFR6bGzwrvrbUm+argS36Y5+gRfDi/giTeEWExnBEYt5YFKFK
WORMwZmpAkEAtFH2UjsSrrepgY2N+JnEuGXcehvkohoW+xfY8rT+LGQm1iEuvg+G
D4i5GPVCGP0CgR8nHnO8E/CsYiB+HVmVjQJAFTR2DaZjbHKjimWFNX2WkY4+1i4Z
h0938pYc7goIbK4euYfIJykkqlAsQeSdSbuor5GSXdpxsZQYiBBjg5ocYQJAeCbp
IA/2ue7thsLg59bmSwyspbzyUsVZrMROLiNF/iRZ8HK557EGXlF3LNc3zNjCE3HD
qjnqB8tlwhjuj/YCfQJAXG0+Y1cZjTDWdpYVZmVwMAQa9YRNM/nx7cW4fE/BgckT
yBMNuKn/a3tbtVEVZJKEuHh2/vxyOiCDgg5G+1abHA==
-----END RSA PRIVATE KEY-----'''



## Проверка JWT на валидность
def check_JWT(jwt_code):
    try:
        check_valid = jwt.decode(jwt_code, PUBLIC_KEY, algorithms=['RS256'])
        is_valid = True
    except:
        is_valid = False

    return is_valid

## Функция хэширования пароля
def hash_password(password):
    salt = '8^gj56o@jzx119)!^4@g=q78(&^=k^!8-s4vhwj-b1rb%$wfc9'
    return str(hashlib.sha256(salt.encode() + password.encode()).hexdigest())

## Обработка логина и пароля
def decode_log_pass(base64_text):
    decoded = base64.b64decode(base64_text).decode('utf-8')
    login = decoded.split(':')[0]
    password = decoded.split(':')[1]
    password = str(hash_password(password))

    return login, password

class SessionAuthView(APIView):
    ## Авторизация пользователя
    @permission_classes([AllowAny])
    def get(self, request):
        try:
            header = request.headers["Authorization"]
        except KeyError:
            response = HttpResponse(
                content={"Authorization header not found."},
                status=401)

            return response

        authorization_type = header.split()[0]
        if authorization_type != "Basic":
            if authorization_type != "Bearer":
                response = HttpResponse(
                    content={"Incorrect authorization type."},
                    status=401)
            else:
                data = header.split()[1]
                try:
                    jwt_data = jwt.decode(data, PUBLIC_KEY, algorithms=['RS256'])
                except:
                    response = HttpResponse(
                        content={"Incorrect token."},
                        status=401)

                    return response
                    
                jwt_data["exp"] = time.time() + 60 * 60
                jwt_token = jwt.encode(jwt_data, PRIVATE_KEY, algorithm='RS256')
                
                response = HttpResponse(
                    content=jwt_token,
                    status=200)
                
        else:
            data = header.split()[1]
            try:
                ##  Разделение логина и пароля
                login, password = decode_log_pass(data)
            except:
                return HttpResponse(
                    content={"Authorization header has been broken."},
                    status=401)
            ##  Сравнение с базой
            user = get_object_or_404(User, login=login, password=password)
            ##  Если совпало, генерируем рефреш-токен и джвт-токен (refresh_token, userUid, exp=время создания (Unix Time) + время жизни)
            refresh_token = str(uuid.uuid4())

            jwt_data = {}
            jwt_data["refresh_token"] = refresh_token
            jwt_data["userUid"] = str(user.user_uid)
            jwt_data["role"] = user.role
            jwt_data["exp"] = time.time() + 60 * 60
            jwt_token = jwt.encode(jwt_data, PRIVATE_KEY, algorithm='RS256')

            response = HttpResponse(
                    content=jwt_token,
                    status=200)
            
        return response        

    ## Регистрация пользователя
    @permission_classes([AllowAny])
    def post(self, request):
        body = request.data
        login = body["login"]

        ## Проверка существования пользователя с введённым логином
        is_in_db = User.objects.filter(login=login)
        
        if is_in_db:
            return HttpResponse(
                content={"There is such login in the database."},
                status=409)
        
        try:
            password = body["password"]
            surname = body["surname"]
            name = body["name"]
            patronymic = body["patronymic"]
        except:
            return HttpResponse(
                content={"Incorrect data."},
                status=400)
        role = False
        refresh_token = ''
        useruuid = uuid.uuid1()

        hashed_password = str(hash_password(password))        

        count_id = len(User.objects.all())
        count_id += 1

        db_data = User(id=count_id, user_uid=useruuid, login=login,
                       password=hashed_password, surname=surname,
                       name=name, patronymic=patronymic,
                       role=role, refresh_token=refresh_token)

        db_data.save()
        
        return HttpResponse(status=201)

class SessionValidateView(APIView):    
    ## Проверка валидности токена
    @permission_classes([AllowAny])
    def get(self, request):
        try:
            header = request.headers["Authorization"]
        except KeyError:
            response = HttpResponse(
                content={"Authorization header not found."},
                status=401)

            return response

        try:    
            authorization_type = header.split()[0]
        except:
            return HttpResponse(
                content={"No token."},
                status=401)
        if authorization_type != "Bearer":
            response = response = HttpResponse(
                content={"Incorrect authorization type."},
                status=401)
            return response

        try:
            jwt_code = header.split()[1]
        except:
            return HttpResponse(
                content={"Empty token."},
                status=401)

        res = check_JWT(jwt_code)
        if res == True:
            response = HttpResponse(
                content={"Authorized user."},
                status=200)
        else:
            response = HttpResponse(
                content={"Incorrect token."},
                status=401)

        return response

## Инициализация базы данных администратором
class InitDBView(APIView):
    def get(self, request):
        adm = User.objects.filter(login="admin")
        if len(adm) == 0:
            admin_data = User(user_uid=uuid.uuid1(), login='admin',
                        password='admin', surname='AdminSurname', name='AdminName',
                        patronymic='AdminPatronymic', role=True, refresh_token='')
            admin_data.save()
        return HttpResponse(status=204)
