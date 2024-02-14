from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from api.models import CustomUser
from api.serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.mail import send_mail
# OpenAI
from model.model import model
from model.model_1 import generate_response
from ingest.ingest import document_loader, create_embeddings
from django.core.files import File


# Upload File
class CustomFile(File):
    def __init__(self, file, *args, **kwargs):
        super().__init__(file, *args, **kwargs)
        self.filename = file.name

    def save(self, path):
        content = self.read()
        with open(path, 'wb') as destination_file:
            destination_file.write(content)


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


# OpenAI View
class QueryHandlerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        global db
        value = request.query_params.get("value")
        docs = db.similarity_search(value)
        result = chain.run(input_documents=docs, question=value)
        return Response(result, status=status.HTTP_200_OK)


class QueryResponseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        resp = request.query_params.get("resp")
        response = generate_response(resp)
        return Response(response, status=status.HTTP_200_OK)


# Upload File
class FileUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        print("hello", request.data)
        uploaded_file = request.FILES['file']
        uploaded_file = CustomFile(uploaded_file)
        print(uploaded_file)
        loader = document_loader(uploaded_file)
        chunks, embeddings = create_embeddings(loader)
        global db, chain
        db, chain = model(chunks, embeddings)
        return Response({'filename': uploaded_file.name}, status=status.HTTP_200_OK)
