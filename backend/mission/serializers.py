from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import *
import pytz
import magic

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
        fields = ('id','username', 'email', 'employee')

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

class ValidationInfoWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationInfo
        fields = ['observation_text', 'attachment']

    def validate_attachment(self, value):
        allowed_mime_types = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        mime_type = magic.from_buffer(value.read(), mime=True)  # You will need to install python-magic for this
        if mime_type not in allowed_mime_types:
            raise serializers.ValidationError('Invalid file type. Allowed file types are: pdf, doc, docx.')

        return value

class DemandListSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField('get_creator_name')
    assignee = serializers.SerializerMethodField('get_assignee_name')
    state = serializers.CharField(source='state.name')
    type = serializers.CharField(source='type.name')

    class Meta:
        model = Demand
        fields = ['id','created_at', 'type', 'last_modified', 'creator', 'assignee', 'state']
    
    def get_creator_name(self, obj):
        return f"{obj.creator.employee.first_name} {obj.creator.employee.last_name}"

    def get_assignee_name(self, obj):
        return f"{obj.assignee.employee.first_name} {obj.assignee.employee.last_name}"

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
    mission_summary = serializers.CharField(required=True)

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
    transition = TransitionSerializer()

    class Meta:
        model = Event
        fields = '__all__'

class ValidationInfoReadSerializer(serializers.ModelSerializer):
    event = EventReadSerializer()

    class Meta:
        model = ValidationInfo
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

class SimplifiedTransitionSerializer(serializers.ModelSerializer):
    start_state = serializers.CharField(source='start_state.name')
    end_state = serializers.CharField(source='end_state.name')

    class Meta:
        model = Transition
        fields = ['id', 'start_state', 'end_state', 'description', 'action']

class SimplifiedValidationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationInfo
        fields = ['observation_text', 'attachment']


class SimplifiedEventSerializer(serializers.ModelSerializer):
    trigger_user = serializers.SerializerMethodField('get_trigger_user_full_name')
    transition = SimplifiedTransitionSerializer()
    validation_info = SimplifiedValidationInfoSerializer()

    class Meta:
        model = Event
        fields = ['id', 'trigger_user', 'transition', 'time_event', 'validation_info']

    def get_trigger_user_full_name(self, obj):
        return f"{obj.trigger_user.employee.first_name} {obj.trigger_user.employee.last_name}"