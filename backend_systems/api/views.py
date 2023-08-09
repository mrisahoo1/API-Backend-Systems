from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import User, KeyValueData
from .serializers import UserSerializer, KeyValueDataSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta
from django.utils.crypto import get_random_string

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']

        if User.objects.filter(username=username).exists():
            return Response({
                "status": "error",
                "code": "USERNAME_EXISTS",
                "message": "The provided username is already taken. Please choose a different username."
            }, status=status.HTTP_409_CONFLICT)

        if User.objects.filter(email=email).exists():
            return Response({
                "status": "error",
                "code": "EMAIL_EXISTS",
                "message": "The provided email is already registered. Please use a different email address."
            }, status=status.HTTP_409_CONFLICT)

        password = serializer.validated_data['password']
        if len(password) < 8:
            return Response({
                "status": "error",
                "code": "INVALID_PASSWORD",
                "message": "The provided password does not meet the requirements."
            }, status=status.HTTP_400_BAD_REQUEST)

        age = serializer.validated_data['age']
        if age <= 0:
            return Response({
                "status": "error",
                "code": "INVALID_AGE",
                "message": "Invalid age value. Age must be a positive integer."
            }, status=status.HTTP_400_BAD_REQUEST)

        gender = serializer.validated_data['gender']
        if not gender:
            return Response({
                "status": "error",
                "code": "GENDER_REQUIRED",
                "message": "Gender field is required. Please specify the gender."
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            full_name=serializer.validated_data['full_name'],
            age=age,
            gender=gender
        )

        return Response({
            "status": "success",
            "message": "User successfully registered!",
            "data": {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "age": user.age,
                "gender": user.gender
            }
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "status": "error",
            "code": "INVALID_REQUEST",
            "message": "Invalid request. Please provide all required fields: username, email, password, full_name."
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def generate_token(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            "status": "error",
            "code": "MISSING_FIELDS",
            "message": "Missing fields. Please provide both username and password."
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({
            "status": "error",
            "code": "INVALID_CREDENTIALS",
            "message": "Invalid credentials. The provided username or password is incorrect."
        }, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, user.password):
        return Response({
            "status": "error",
            "code": "INVALID_CREDENTIALS",
            "message": "Invalid credentials. The provided username or password is incorrect."
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Generate access token and set its expiration time
    access_token = get_random_string(32)
    expires_in = timezone.now() + timedelta(seconds=3600)  # Token expires in 1 hour

    # Store access token in the database for validation
    user.access_token = access_token
    user.access_token_expires = expires_in
    user.save()

    return Response({
        "status": "success",
        "message": "Access token generated successfully.",
        "data": {
            "access_token": access_token,
            "expires_in": 3600
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def store_data(request):
    access_token = request.headers.get('Authorization', '').replace('Bearer ', '')

    try:
        user = User.objects.get(access_token=access_token)
    except User.DoesNotExist:
        return Response({
            "status": "error",
            "code": "INVALID_TOKEN",
            "message": "Invalid access token provided."
        }, status=status.HTTP_401_UNAUTHORIZED)

    serializer = KeyValueDataSerializer(data=request.data)
    if serializer.is_valid():
        key = serializer.validated_data['key']
        value = serializer.validated_data['value']

        if KeyValueData.objects.filter(key=key).exists():
            return Response({
                "status": "error",
                "code": "KEY_EXISTS",
                "message": "The provided key already exists in the database. To update an existing key, use the update API."
            }, status=status.HTTP_409_CONFLICT)

        data = KeyValueData.objects.create(key=key, value=value)
        user.data.add(data)
        user.save()

        return Response({
            "status": "success",
            "message": "Data stored successfully."
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "error",
            "code": "INVALID_REQUEST",
            "message": "Invalid request. Please provide a valid key and value."
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def retrieve_data(request, key):
    access_token = request.headers.get('Authorization', '').replace('Bearer ', '')

    try:
        user = User.objects.get(access_token=access_token)
    except User.DoesNotExist:
        return Response({
            "status": "error",
            "code": "INVALID_TOKEN",
            "message": "Invalid access token provided."
        }, status=status.HTTP_401_UNAUTHORIZED)

    try:
        data = user.data.get(key=key)
        serializer = KeyValueDataSerializer(data)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    except KeyValueData.DoesNotExist:
        return Response({
            "status": "error",
            "code": "KEY_NOT_FOUND",
            "message": "The provided key does not exist in the database."
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_data(request, key):
    access_token = request.headers.get('Authorization', '').replace('Bearer ', '')

    try:
        user = User.objects.get(access_token=access_token)
    except User.DoesNotExist:
        return Response({
            "status": "error",
            "code": "INVALID_TOKEN",
            "message": "Invalid access token provided."
        }, status=status.HTTP_401_UNAUTHORIZED)

    try:
        data = user.data.get(key=key)
        serializer = KeyValueDataSerializer(data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Data updated successfully."
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "code": "INVALID_REQUEST",
                "message": "Invalid request. Please provide a valid value."
            }, status=status.HTTP_400_BAD_REQUEST)
    except KeyValueData.DoesNotExist:
        return Response({
            "status": "error",
            "code": "KEY_NOT_FOUND",
            "message": "The provided key does not exist in the database."
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_data(request, key):
    access_token = request.headers.get('Authorization', '').replace('Bearer ', '')

    try:
        user = User.objects.get(access_token=access_token)
    except User.DoesNotExist:
        return Response({
            "status": "error",
            "code": "INVALID_TOKEN",
            "message": "Invalid access token provided."
        }, status=status.HTTP_401_UNAUTHORIZED)

    try:
        data = user.data.get(key=key)
        data.delete()
        return Response({
            "status": "success",
            "message": "Data deleted successfully."
        }, status=status.HTTP_200_OK)
    except KeyValueData.DoesNotExist:
        return Response({
            "status": "error",
            "code": "KEY_NOT_FOUND",
            "message": "The provided key does not exist in the database."
        }, status=status.HTTP_404_NOT_FOUND)
