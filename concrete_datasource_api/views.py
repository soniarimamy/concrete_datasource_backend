from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, ApplicationSerializer, ConfirmApplicationSerializer
from .models import JobApplication


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'email': user.email}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['email'], password=serializer.validated_data['password'])
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'email': user.email})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CreateApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        app = serializer.save(user=request.user)
        return Response({'id': app.id, 'first_name': app.first_name, 'last_name': app.last_name, 'confirmed': app.confirmed}, status=status.HTTP_201_CREATED)



class ConfirmApplicationView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            app = JobApplication.objects.get(pk=pk, user=request.user)
        except JobApplication.DoesNotExist:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConfirmApplicationSerializer(app, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
