from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.generics import CreateAPIView
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from adnet.models import User
from admin.models import Advisor
from django.contrib.auth.signals import user_logged_in
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from adnet.serializers import UserSerializer, BookingSerializer
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from django.conf import settings
from django.db.models import F


class CreateUser(CreateAPIView):
    # Allow any user (authenticated or not) to access this url
    # permission_classes = (AllowAny,)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email = data["email"],
             password=data["password"])
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, settings.SECRET_KEY)
            account = {}
            account['token'] = str(token)[2:-1]
            account['id'] = user.id
            user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
            return JsonResponse(data = account, safe = False,
             status=status.HTTP_200_OK)
        else:
            return JsonResponse(data = serializer.errors, safe = False,
            status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
# @permission_classes([AllowAny, ])
def login(request):
    try:
        email = request.data['email']
        password = request.data['password']
        user = User.objects.get(email=email, password=password)
        try:
            account = {}
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, settings.SECRET_KEY)
            account['token'] = str(token)[2:-1]
            account['id'] = user.id
            user_logged_in.send(sender=user.__class__,
                                            request=request, user=user)
            return JsonResponse(data = account, safe = False,
                 status=status.HTTP_200_OK)

        except Exception as e:
            raise e
    except User.DoesNotExist:
        return JsonResponse(data = 'AUTHENTICATION ERROR', safe = False,
        status = status.HTTP_401_UNAUTHORIZED)
    except KeyError as e:
        return JsonResponse(data = 'key %s is missing'%e, safe = False,
        status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ad(request, user_id):
    try:
        User.objects.get(id = user_id)
        return JsonResponse(data = list(Advisor.objects.values()), safe = False,
        status = status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse(data = 'Wrong User ID', safe = False,
        status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book(request, user_id, advisor_id):
    try:
        user = User.objects.get(id = user_id)
        advisor = Advisor.objects.get(id = advisor_id)
        data = {}
        data['user'] = user.id
        data['advisor'] = advisor.id
        data['time'] = JSONParser().parse(request)["time"]
        serializer = BookingSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data = {},safe = False,
            status = status.HTTP_200_OK)
        else : return JsonResponse(data = serializer.errors, safe = False,
        status = status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return JsonResponse(data = 'Wrong User ID', safe = False,
        status = status.HTTP_400_BAD_REQUEST)
    except Advisor.DoesNotExist:
        return JsonResponse(data = 'Wrong Advisor ID', safe = False,
        status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book(request, user_id):
    try:
        uid = User.objects.get(id = user_id).id
        f1 =  Advisor.objects.filter(appointment__user__id = uid).all().values(
        advisor_name = F('name'), advisor_profile_pic = F('profile_pic_url'),
         advisor_id = F('id'), booking_id = F('appointment__id'),
         booking_time = F('appointment__time'))
        return JsonResponse(data = list(f1), safe = False,
        status = status.HTTP_200_OK)
    except User.DoesNotExist:
        return JsonResponse(data = 'Wrong User ID', safe = False,
        status = status.HTTP_400_BAD_REQUEST)
