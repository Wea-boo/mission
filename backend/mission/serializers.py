from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Employee, CustomUser

User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'phone', 'grade', 'function', 'direction', 'manager')

class CustomUserSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'employee')

