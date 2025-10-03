from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import PasswordResetOTP, SignupOTP
from .utils import send_otp_email
import random

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            context={'request': request},
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            code = str(random.randint(100000, 999999))
            SignupOTP.objects.update_or_create(user=user, defaults={'code': code, 'is_verified': False})
            send_otp_email(user.email, code, purpose="Signup")
            return Response({"message": "Account created. OTP sent to email.", "user_id": user.id})
        return Response(serializer.errors, status=400)
    

class VerifySignupOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            user = User.objects.get(email=email)
            otp = SignupOTP.objects.get(user=user, code=code, is_verified=False)
            if otp.is_expired():
                return Response({'error': 'OTP expired.'}, status=400)
            otp.is_verified = True
            otp.save()
            user.is_active = True
            user.save()
            user.backend = 'users.emailorusernames.EmailOrUsernameBackend'
            login(request, user)  # Log user in
            return Response({'message': 'Signup verified and user logged in.'})
        except (User.DoesNotExist, SignupOTP.DoesNotExist):
            return Response({'error': 'Invalid email or OTP'}, status=400)




# Send OTP
class RequestPasswordReset(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            code = str(random.randint(100000, 999999))
            PasswordResetOTP.objects.filter(user=user).delete()
            PasswordResetOTP.objects.create(user=user, code=code)
            send_otp_email(email, code)
            return Response({'message': 'OTP sent to your email.'})
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=404)

# Verify OTP
class VerifyOTP(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            user = User.objects.get(email=email)
            otp = PasswordResetOTP.objects.get(user=user, code=code, is_verified=False)
            if otp.is_expired():
                return Response({'error': 'OTP expired.'}, status=400)
            otp.is_verified = True
            otp.save()
            return Response({'message': 'OTP verified.'})
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return Response({'error': 'Invalid code or email.'}, status=400)

# Reset password
class ResetPassword(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        try:
            user = User.objects.get(email=email)
            otp = PasswordResetOTP.objects.filter(user=user, is_verified=True).latest('created_at')
            if otp.is_expired():
                return Response({'error': 'OTP expired.'}, status=400)
            user.set_password(new_password)
            user.save()
            otp.delete()
            return Response({'message': 'Password reset successful.'})
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return Response({'error': 'Verification required.'}, status=400)


