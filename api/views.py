from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics, status

from api.models import CustomUser
from api.serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail


# Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Register
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        subject = 'Your Account has been created in OpenCV Pvt.Ltd'
        message = f'Hi {user.username},\n\nYour account has been successfully created.\n\nUsername: {user.username}\nPassword: {serializer.validated_data["password"]}\n\nThank you for registering.\n\nThanks&Regard\n\nOpenCV Pvt.Ltd'
        from_email = 'thepratyushranjan6060@gmail.com'  # Update this with your email
        to_email = [user.email]
        send_mail(subject, message, from_email, to_email, fail_silently=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# api/profile  and api/profile/update
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    serializer = UserProfileSerializer(user, many=False)
    serializer = serializer.data
    return Response(serializer)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
