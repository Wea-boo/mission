from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import *
import pytz

User = get_user_model()

class DemandTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeDemand
        fields = '__all__'

class MissionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeMission
        fields = '__all__'

class DirectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Direction
        fields = '__all__'

class ManagerSerializer(serializers.ModelSerializer):
    direction = DirectionSerializer()

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'phone', 'grade', 'function', 'direction')

class EmployeeSerializer(serializers.ModelSerializer):
    direction = DirectionSerializer()
    manager = ManagerSerializer()

    class Meta:
        model = Employee
        fields = ('first_name', 'last_name', 'phone', 'grade', 'function', 'direction', 'manager')

class CustomUserSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'employee')

class WorkFlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkFlow
        fields = '__all__'

class StateDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateDemand
        fields = '__all__'

class DemandReadSerializer(serializers.ModelSerializer):
    creator = CustomUserSerializer()
    assignee = CustomUserSerializer()
    state = StateDemandSerializer()
    type = DemandTypeSerializer()

    class Meta:
        model = Demand
        fields = '__all__'

class DemandWriteSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    assignee = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    state = serializers.PrimaryKeyRelatedField(queryset=StateDemand.objects.all())

    class Meta:
        model = Demand
        fields = '__all__'


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'

class MissionOrderWriteSerializer(serializers.ModelSerializer):
    demand = serializers.PrimaryKeyRelatedField(queryset=Demand.objects.all())
    agency = serializers.PrimaryKeyRelatedField(queryset=Agency.objects.all())
    observation_manager = serializers.CharField(required=False)
    observation_HR = serializers.CharField(required=False)

    def validate(self, data):
        if data['returning'] <= data['departing']:
            raise serializers.ValidationError("Returning time should be greater than departing time.")
        return data
    
    
    def validate_departing(self, value):
        if value <= datetime.now(pytz.utc):
            raise serializers.ValidationError("Departing time should be in the future.")
        return value
    
    class Meta:
        model = MissionOrder
        fields = '__all__'

class MissionOrderReadSerializer(serializers.ModelSerializer):
    demand = DemandReadSerializer()
    agency = AgencySerializer()
    mission_type = MissionTypeSerializer()

    class Meta:
        model = MissionOrder
        fields = '__all__'

class TransitionSerializer(serializers.ModelSerializer):
    start_state = StateDemandSerializer()
    end_state = StateDemandSerializer()

    class Meta:
        model = Transition
        fields = '__all__'

class EventReadSerializer(serializers.ModelSerializer):
    demand = DemandReadSerializer()
    trigger_user = CustomUserSerializer()
    transit = TransitionSerializer()

    class Meta:
        model = Event
        fields = '__all__'

class EventWriteSerializer(serializers.ModelSerializer):
    demand = serializers.PrimaryKeyRelatedField(queryset=Demand.objects.all())
    trigger_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    transition = serializers.PrimaryKeyRelatedField(queryset=Transition.objects.all())

    class Meta:
        model = Event
        fields = '__all__'

class MissionFeeSerializer(serializers.ModelSerializer):
    demand = DemandReadSerializer()
    mission_order = MissionOrderReadSerializer()

    class Meta:
        model = MissionFee
        fields = '__all__'

class TypeMissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeMission
        fields = '__all__'

