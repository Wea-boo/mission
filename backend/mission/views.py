from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import authenticate, login
from rest_framework import permissions, serializers
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views import View

class CustomLoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        print(request.data)
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
            response = super().post(request, format=None)
            
            auth_token = response.data.get('token')
            response.set_cookie("auth_token", auth_token, httponly=True, max_age=None, samesite="Lax")
            response['Content-Type'] = 'application/json'
            return response
        else:
            raise serializers.ValidationError('Invalid username or password')
        


class CheckAuthView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({"is_authenticated": request.user.is_authenticated})
