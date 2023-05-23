from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import authenticate, login
from rest_framework import permissions, serializers
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets
from django.db.models import Count, Avg, Value, CharField, F
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear, Concat
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, FileResponse, Http404
from django.views import View
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from django.conf import settings
from .models import *
from .serializers import *
from .permissions import *
from django.db.models import Q, Prefetch
from django.db import transaction
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.shortcuts import get_object_or_404
import os
from django.utils import timezone
import datetime

# ALLOWED_ACTIONS = {
#     "Manager": {
#         "WaitingApproval": ["Approve", "Deny"],
#     },
#     "HR": {
#         "Approved": ["GenerateOrder"],
#     },
    
# }
class CustomLoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        print(request.data)
        user = authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            login(request, user)
            response = super().post(request, format=None)
            auth_token = response.data.get('token')
            response.set_cookie("auth_token", auth_token, httponly=False, max_age=7200, samesite="Lax")
            response['Content-Type'] = 'application/json'
            return response
        else:
            raise serializers.ValidationError('Invalid username or password')
        

class CheckAuthView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        return JsonResponse({"is_authenticated": True})

class TypeMissionList(generics.ListCreateAPIView):
    queryset = TypeMission.objects.all()
    serializer_class = TypeMissionSerializer

class AgencyList(generics.ListCreateAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer

def get_transition(start_state_name, end_state_name, wf):
    start_state = StateDemand.objects.get(name=start_state_name, workflow=wf)
    end_state = StateDemand.objects.get(name=end_state_name, workflow=wf)
    return Transition.objects.get(start_state=start_state, end_state=end_state, workflow=wf)

class CreateOwnDemandView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        # Get the user who submitted the form
        user = request.user

        # Create a new Demand instance with the initial state
        initial_state = StateDemand.objects.get(name="Init")
        demand_data = {
            "type": request.data["type_demand"],
            "creator": user.id,
            "assignee": user.id,
            "state": initial_state.id
        }
        demand_serializer = DemandWriteSerializer(data=demand_data)
        if demand_serializer.is_valid():
            demand = demand_serializer.save()
        else:
            return Response(demand_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create a new MissionOrder instance with the provided data
        mission_order_data = {
            "mission_type": request.data["type_mission"],
            "use_personal_vehicle": request.data["use_personel_v"],
            "trip_purpose": request.data["mission_reason"],
            "agency": request.data["destination"],
            "departing": request.data["departure"],
            "returning": request.data["return"],
            "mission_summary": request.data["mission_summary"],
            "demand": demand.id
        }
        mission_order_serializer = MissionOrderWriteSerializer(data=mission_order_data)
        if mission_order_serializer.is_valid():
            mission_order = mission_order_serializer.save()
        else:
            return Response(mission_order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Event instance with the created Demand and the appropriate Transition
        latest_workflow = WorkFlow.objects.latest('id')
        transition = get_transition("Init", "Crée", latest_workflow)
        event_data = {
            "demand": demand.id,
            "trigger_user": user.id,
            "transition": transition.id
        }
        event_serializer = EventWriteSerializer(data=event_data)
        if event_serializer.is_valid():
            event = event_serializer.save()
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update the state of the created Demand to "Crée"
        created_state = StateDemand.objects.get(name="Crée")
        demand.state = created_state
        demand.save()

        return Response({"message": "Demand, MissionOrder, and Event instances created successfully.", "id": demand.id}, status=status.HTTP_201_CREATED)

class CreateOthersDemandView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSecretary]

    @transaction.atomic
    def post(self, request):
        # Get the user who submitted the form
        user = request.user

        creator_id = request.data.get("creator")
        if not creator_id:
            return Response({"error": "creator_id field is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Demand instance with the initial state
        initial_state = StateDemand.objects.get(name="Init")
        demand_data = {
            "type": request.data["type_demand"],
            "creator": creator_id,
            "assignee": user.id,
            "state": initial_state.id
        }
        demand_serializer = DemandWriteSerializer(data=demand_data)
        if demand_serializer.is_valid():
            demand = demand_serializer.save()
        else:
            return Response(demand_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        mission_order_data = {
            "mission_type": request.data["type_mission"],
            "use_personal_vehicle": request.data["use_personel_v"],
            "trip_purpose": request.data["mission_reason"],
            "agency": request.data["destination"],
            "departing": request.data["departure"],
            "returning": request.data["return"],
            "mission_summary": request.data["mission_summary"],
            "demand": demand.id
        }
        mission_order_serializer = MissionOrderWriteSerializer(data=mission_order_data)
        if mission_order_serializer.is_valid():
            mission_order = mission_order_serializer.save()
        else:
            return Response(mission_order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Event instance with the created Demand and the appropriate Transition
        latest_workflow = WorkFlow.objects.latest('id')
        transition = get_transition("Init", "Crée", latest_workflow)
        event_data = {
            "demand": demand.id,
            "trigger_user": user.id,
            "transition": transition.id
        }
        event_serializer = EventWriteSerializer(data=event_data)
        if event_serializer.is_valid():
            event = event_serializer.save()
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update the state of the created Demand to "Crée"
        created_state = StateDemand.objects.get(name="Crée")
        demand.state = created_state
        demand.save()

        return Response({"message": "Demand, MissionOrder, and Event instances created successfully.", "id": demand.id}, status=status.HTTP_201_CREATED)

class DemandDetailsView(generics.RetrieveAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    queryset = Demand.objects.all()
    serializer_class = DemandReadSerializer

    def retrieve(self, request, *args, **kwargs):
        demand_instance = self.get_object()
        print(demand_instance)
        mission_order_instance = MissionOrder.objects.get(demand=demand_instance)
        mission_order_serializer = MissionOrderReadSerializer(mission_order_instance)
        return Response(
            mission_order_serializer.data
        )

class DemandTransitionsAPIView(generics.GenericAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    serializer_class = TransitionSerializer

    def get_queryset(self):
        demand_id = self.kwargs['pk']
        demand = Demand.objects.get(id=demand_id)
        
        if demand.assignee != self.request.user:
            # If the user is not the assignee, return an empty queryset
            return Transition.objects.none()
        
        return Transition.objects.filter(start_state=demand.state)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class CreatedToWaitingApproval(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)
        pk = self.kwargs['pk']
        demand = Demand.objects.get(id=pk)
        
        # Check the IsAssigned permission
        if not IsAssigned().has_object_permission(request, self, demand):
            self.permission_denied(
                request, message="You are not the assignee of this demand."
            )

    @transaction.atomic
    def post(self, request, pk):
        user = request.user
        demand = Demand.objects.get(id=pk)

        if demand.state.name != "Crée":
            return Response({"message": "Invalid transition. Demand is not in the 'Created' state."}, status=status.HTTP_400_BAD_REQUEST)
        
        manager_user = CustomUser.objects.get(employee=demand.assignee.employee.manager)
        manager_group = Group.objects.get(profile__name='Responsable Hierarchique')
        new_assignee = None
        if manager_user.main_profile.name == 'Responsable Hierarchique' or manager_user.groups.filter(id=manager_group.id).exists():
            new_assignee = manager_user
        else:
            # If the manager does not have the manager profile or group, find a user from the same direction with the manager profile or group.
            same_direction_manager_users = CustomUser.objects.filter(
                Q(employee__direction=demand.assignee.employee.direction), 
                Q(main_profile__name='Responsable Hierarchique') | Q(groups__id=manager_group.id)
            )
            if same_direction_manager_users.exists():
                new_assignee = same_direction_manager_users.first()

        # Check if a new assignee was found.
        if new_assignee is None:
            return Response({"message": "No suitable user found to assign the demand."}, status=status.HTTP_400_BAD_REQUEST)
        
        observation_text = request.data.get('observation_text')
        attachment = request.FILES.get('attachment')

        validation_info_serializer = ValidationInfoWriteSerializer(data={"observation_text": observation_text, "attachment": attachment})
        if not validation_info_serializer.is_valid():
            return Response(validation_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        latest_workflow = demand.state.workflow
        transition = get_transition("Crée", "Attente Approbation", latest_workflow)
        event_data = {
            "demand": demand.id,
            "trigger_user": user.id,
            "transition": transition.id
        }
        event_serializer = EventWriteSerializer(data=event_data)
        if event_serializer.is_valid():
            event = event_serializer.save()
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Update the state of the Demand to "Attente Validation"

        validation_info = validation_info_serializer.save(event=event)

        awaiting_validation_state = StateDemand.objects.get(name="Attente Approbation")
        demand.state = awaiting_validation_state
        demand.assignee = new_assignee
        demand.save()

        return Response({"message": "Transitioned to 'Awaiting Validation' state successfully."}, status=status.HTTP_200_OK)

class WaitingApprovalToApproved(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsManager]

    def check_permissions(self, request):
        super().check_permissions(request)
        pk = self.kwargs['pk']
        demand = Demand.objects.get(id=pk)
        
        # Check the IsAssigned permission
        if not IsAssigned().has_object_permission(request, self, demand):
            self.permission_denied(
                request, message="You are not the assignee of this demand."
            )

    def post(self, request, pk):
        user = request.user
        demand = Demand.objects.get(id=pk)

        if demand.state.name != "Attente Approbation":
            return Response({"message": "Invalid transition. Demand is not in the 'Waiting Approval' state."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve validation info from request
        observation_text = request.data.get('observation_text')
        attachment = request.FILES.get('attachment')

        validation_info_serializer = ValidationInfoWriteSerializer(data={"observation_text": observation_text, "attachment": attachment})
        if not validation_info_serializer.is_valid():
            return Response(validation_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get HR Agent user/group
        hr_agent_group = Group.objects.get(profile__name='Agent RH')
        hr_agent_user = CustomUser.objects.filter(
            Q(main_profile__name='Agent RH') | 
            Q(groups__id=hr_agent_group.id)
        ).first()

        # Check if an HR Agent user was found.
        if hr_agent_user is None:
            return Response({"message": "No suitable HR Agent user found to assign the demand."}, status=status.HTTP_400_BAD_REQUEST)

        # Record the transition event
        latest_workflow = demand.state.workflow
        transition = get_transition("Attente Approbation", "Approuvé", latest_workflow)
        event_data = {
            "demand": demand.id,
            "trigger_user": user.id,
            "transition": transition.id
        }
        event_serializer = EventWriteSerializer(data=event_data)
        if event_serializer.is_valid():
            event = event_serializer.save()
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validation_info = validation_info_serializer.save(event=event)

        approved_state = StateDemand.objects.get(name="Approuvé")
        demand.state = approved_state
        demand.assignee = hr_agent_user
        demand.save()
        
        return Response({"message": "Transitioned to 'Approved' state successfully."}, status=status.HTTP_200_OK)
    
class WaitingApprovalToDenied(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsManager]

    def check_permissions(self, request):
        super().check_permissions(request)
        pk = self.kwargs['pk']
        demand = Demand.objects.get(id=pk)
        
        # Check the IsAssigned permission
        if not IsAssigned().has_object_permission(request, self, demand):
            self.permission_denied(
                request, message="You are not the assignee of this demand."
            )

    def post(self, request, pk):
        user = request.user
        demand = Demand.objects.get(id=pk)

        if demand.state.name != "Attente Approbation":
            return Response({"message": "Invalid transition. Demand is not in the 'Waiting Approval' state."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve validation info from request
        observation_text = request.data.get('observation_text')
        attachment = request.FILES.get('attachment')

        validation_info_serializer = ValidationInfoWriteSerializer(data={"observation_text": observation_text, "attachment": attachment})
        if not validation_info_serializer.is_valid():
            return Response(validation_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Get HR Agent user/group
        demand_creator = demand.creator

        # Check if an HR Agent user was found.

        # Update the observation_manager field in MissionOrder associated with the demand
        mission_order = demand.missionorder
        mission_order.observation_manager = validation_info['obs_manager']
        mission_order.save()

        # Record the transition event
        latest_workflow = demand.state.workflow
        transition = get_transition("Attente Approbation", "Annulé", latest_workflow)
        event_data = {
            "demand": demand.id,
            "trigger_user": user.id,
            "transition": transition.id
        }
        event_serializer = EventWriteSerializer(data=event_data)
        if event_serializer.is_valid():
            event = event_serializer.save()
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validation_info = validation_info_serializer.save(event=event)

        approved_state = StateDemand.objects.get(name="Approuvé")
        demand.state = approved_state
        demand.assignee = demand_creator
        demand.save()
        
        return Response({"message": "Transitioned to 'Approved' state successfully."}, status=status.HTTP_200_OK)

class WaitingValidationToValidated(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsHRManager]

    def check_permissions(self, request):
        super().check_permissions(request)
        pk = self.kwargs['pk']
        demand = Demand.objects.get(id=pk)
        
        # Check the IsAssigned permission
        if not IsAssigned().has_object_permission(request, self, demand):
            self.permission_denied(
                request, message="You are not the assignee of this demand."
            )

    def post(self, request, pk):
        user = request.user
        demand = Demand.objects.get(id=pk)

        if demand.state.name != "Attente Validation":
            return Response({"message": "Invalid transition. Demand is not in the 'Waiting Validation' state."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve validation info from request
        observation_text = request.data.get('observation_text')
        attachment = request.FILES.get('attachment')

        validation_info_serializer = ValidationInfoWriteSerializer(data={"observation_text": observation_text, "attachment": attachment})
        if not validation_info_serializer.is_valid():
            return Response(validation_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the employee who created the demand
        creator = demand.creator

        # Update the observation_hr field in MissionOrder associated with the demand
        mission_order = demand.missionorder
        mission_order.observation_HR = validation_info['obs_hr']
        mission_order.save()

        # Record the transition event
        latest_workflow = demand.state.workflow
        transition = get_transition("Attente Validation", "Validé", latest_workflow)
        event_data = {
            "demand": demand.id,
            "trigger_user": user.id,
            "transition": transition.id
        }
        event_serializer = EventWriteSerializer(data=event_data)
        if event_serializer.is_valid():
            event = event_serializer.save()
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validation_info = validation_info_serializer.save(event=event)

        validated_state = StateDemand.objects.get(name="Validé")
        demand.state = validated_state
        demand.assignee = creator
        demand.save()
        
        return Response({"message": "Transitioned to 'Validated' state successfully."}, status=status.HTTP_200_OK)

class CreatedToCancelled(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)
        pk = self.kwargs['pk']
        demand = Demand.objects.get(id=pk)

        # Check the IsAssigned permission
        if not IsAssigned().has_object_permission(request, self, demand):
            self.permission_denied(
                request, message="You are not the assignee of this demand."
            )

    def post(self, request, pk):
        user = request.user
        demand = Demand.objects.get(id=pk)

        if demand.state.name != "Crée":
            return Response({"message": "Invalid transition. Demand is not in the 'Created' state."}, status=status.HTTP_400_BAD_REQUEST)


        observation_text = request.data.get('observation_text')
        attachment = request.FILES.get('attachment')

        validation_info_serializer = ValidationInfoWriteSerializer(data={"observation_text": observation_text, "attachment": attachment})
        if not validation_info_serializer.is_valid():
            return Response(validation_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Record the transition event
        latest_workflow = demand.state.workflow
        transition = get_transition("Crée", "Annulé", latest_workflow)
        event_data = {
            "demand": demand.id,
            "trigger_user": user.id,
            "transition": transition.id
        }
        event_serializer = EventWriteSerializer(data=event_data)
        if event_serializer.is_valid():
            event = event_serializer.save()
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validation_info = validation_info_serializer.save(event=event)

        # Change the state of the Demand to "Cancelled"
        cancelled_state = StateDemand.objects.get(name="Annulé")
        demand.state = cancelled_state
        demand.assignee = demand.creator
        demand.save()

        return Response({"message": "Transitioned to 'Cancelled' state successfully."}, status=status.HTTP_200_OK)

class WaitingValidationToDenied(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsHRManager]

    def check_permissions(self, request):
        super().check_permissions(request)
        pk = self.kwargs['pk']
        demand = Demand.objects.get(id=pk)
        
        # Check the IsAssigned permission
        if not IsAssigned().has_object_permission(request, self, demand):
            self.permission_denied(
                request, message="You are not the assignee of this demand."
            )

    def post(self, request, pk):
        user = request.user
        demand = Demand.objects.get(id=pk)

        if demand.state.name != "Attente Validation":
            return Response({"message": "Invalid transition. Demand is not in the 'Waiting Validation' state."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve validation info from request
        observation_text = request.data.get('observation_text')
        attachment = request.FILES.get('attachment')

        validation_info_serializer = ValidationInfoWriteSerializer(data={"observation_text": observation_text, "attachment": attachment})
        if not validation_info_serializer.is_valid():
            return Response(validation_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the employee who created the demand
        creator = demand.creator

        # Update the observation_hr field in MissionOrder associated with the demand
        mission_order = demand.missionorder
        mission_order.observation_HR = validation_info['obs_hr']
        mission_order.save()

        # Record the transition event
        latest_workflow = demand.state.workflow
        transition = get_transition("Attente Validation", "Annulé", latest_workflow)
        event_data = {
            "demand": demand.id,
            "trigger_user": user.id,
            "transition": transition.id
        }
        event_serializer = EventWriteSerializer(data=event_data)
        if event_serializer.is_valid():
            event = event_serializer.save()
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validation_info = validation_info_serializer.save(event=event)

        denied_state = StateDemand.objects.get(name="Annulé")
        demand.state = denied_state
        demand.assignee = creator
        demand.save()
        
        return Response({"message": "Transitioned to 'Denied' state successfully."}, status=status.HTTP_200_OK)

class ApprovedToWaitingValidation(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsHRAgent]

    def check_permissions(self, request):
        super().check_permissions(request)
        pk = self.kwargs['pk']
        demand = Demand.objects.get(id=pk)
        
        # Check the IsAssigned permission
        if not IsAssigned().has_object_permission(request, self, demand):
            self.permission_denied(
                request, message="You are not the assignee of this demand."
            )
    @transaction.atomic
    def post(self, request, pk):
        user = request.user
        demand = Demand.objects.get(id=pk)

        if demand.state.name != "Approuvé":
            return Response({"message": "Invalid transition. Demand is not in the 'Approved' state."}, status=status.HTTP_400_BAD_REQUEST)

        observation_text = request.data.get('observation_text')
        attachment = request.FILES.get('attachment')

        validation_info_serializer = ValidationInfoWriteSerializer(data={"observation_text": observation_text, "attachment": attachment})
        if not validation_info_serializer.is_valid():
            return Response(validation_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get HR Manager user/group
        hr_manager_group = Group.objects.get(profile__name='Responsable RH')
        hr_manager_user = CustomUser.objects.filter(
            Q(main_profile__name='Responsable RH') | 
            Q(groups__id=hr_manager_group.id)
        ).first()

        # Check if an HR Manager user was found.
        if hr_manager_user is None:
            return Response({"message": "No suitable HR Manager user found to assign the demand."}, status=status.HTTP_400_BAD_REQUEST)

        # Record the transition event
        latest_workflow = demand.state.workflow
        transition = get_transition("Approuvé", "Attente Validation", latest_workflow)
        event_data = {
            "demand": demand.id,
            "trigger_user": user.id,
            "transition": transition.id
        }
        event_serializer = EventWriteSerializer(data=event_data)
        if event_serializer.is_valid():
            event = event_serializer.save()
        else:
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validation_info = validation_info_serializer.save(event=event)

        waiting_validation_state = StateDemand.objects.get(name="Attente Validation")
        demand.state = waiting_validation_state
        demand.assignee = hr_manager_user
        demand.save()
        
        return Response({"message": "Transitioned to 'Waiting Validation' state successfully."}, status=status.HTTP_200_OK)



class UsersInSameDirection(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user_direction = request.user.employee.direction
        users_in_same_direction = User.objects.filter(employee__direction=current_user_direction)
        serializer = CustomUserSerializer(users_in_same_direction, many=True)
        return Response(serializer.data)

class UserProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        is_secretary = user.main_profile.name == 'Secrétaire' or user.groups.filter(name='Secrétaire').exists()
        is_manager = user.main_profile.name == 'Responsable Hierarchique' or user.groups.filter(name='Responsable Hierarchique').exists()
        is_hragent = user.main_profile.name == 'Agent RH' or user.groups.filter(name='Agent RH').exists()
        is_admin = user.main_profile.name == 'Administrateur' or user.groups.filter(name='Administrateur').exists()
        is_hrmanager = user.main_profile.name == 'Responsable RH' or user.groups.filter(name='Responsable RH').exists()
        # add other roles as necessary

        return Response({
            "is_secretary": is_secretary,
            "is_manager": is_manager,
            "is_hragent": is_hragent,
            "is_admin": is_admin,
            "is_hrmanager": is_hrmanager
            # add other roles as necessary
        }, status=status.HTTP_200_OK)

class CustomPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 1000

class DemandList(generics.GenericAPIView):
    serializer_class = DemandListSerializer
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Demand.objects.all().order_by('-created_at')
        # Filtering
        creator = self.request.query_params.get('creator', None)
        assignee = self.request.query_params.get('assignee', None)
        state = self.request.query_params.get('state', None)
        _type = self.request.query_params.get('type', None)
        
        if creator is not None:
            queryset = queryset.filter(creator__username=creator)
        if assignee is not None:
            queryset = queryset.filter(assignee__username=assignee)
        if state is not None:
            state_list = state.split(',')
            queryset = queryset.filter(state__name__in=state_list)
        if _type is not None:
            queryset = queryset.filter(type__name=_type)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def dashboard_filters(request):
    user = request.user
    filters = []
    list_assignee = []

    mes_demandes_states = StateDemand.objects.filter(name__in=['Crée', 'Validée', 'Annulé'])
    mes_demandes_count = Demand.objects.filter(creator=user, state__in=mes_demandes_states).count()
    filters.append({
        'name': 'Mes Demandes',
        'state': StateDemandSerializer(mes_demandes_states, many=True).data,
        'creator': user.username,
        'assignee': None,
        'count': mes_demandes_count,
    })

    # Demandes en attentes filter
    demandes_attentes_states = StateDemand.objects.filter(name__in=['Attente Approbation', 'Approuvé', 'Attente Validation'])
    demandes_attentes_count = Demand.objects.filter(creator=user, state__in=demandes_attentes_states).count()
    filters.append({
        'name': 'Demandes en attentes',
        'state': StateDemandSerializer(demandes_attentes_states, many=True).data,
        'creator': user.username,
        'assignee': None,
        'count': demandes_attentes_count,
    })

    def add_state_to_assignee(state_name, filter_name):
        state = StateDemand.objects.filter(name=state_name).first()
        if state and not any(item['state'] == state for item in list_assignee):
            list_assignee.append({
                'filter_name': filter_name,
                'state': state,
            })

    if user.main_profile.name == 'Responsable Hierarchique' or user.groups.filter(name='Responsable Hierarchique').exists():
        add_state_to_assignee('Attente Approbation', "Demandes en attente d'approbation")

    if user.main_profile.name == 'Agent RH' or user.groups.filter(name='Agent RH').exists():
        add_state_to_assignee('Approuvé', "Demandes approuvées")

    if user.main_profile.name == 'Secrétaire' or user.groups.filter(name='Secrétaire').exists():
        add_state_to_assignee('Crée', "Demandes crées")

    if user.main_profile.name == 'Responsable RH' or user.groups.filter(name='Responsable RH').exists():
        add_state_to_assignee('Attente Validation', "Demandes en attente de validation")
    
    if user.main_profile.name == 'Administrateur' or user.groups.filter(name='Administrateur').exists():
        add_state_to_assignee('Crée', "Demandes crées")
        add_state_to_assignee('Attente Approbation', "Demandes en attente d'approbation")
        add_state_to_assignee('Approuvé', "Demandes approuvées")
        add_state_to_assignee('Attente Validation', "Demandes en attente de validation")

    for item in list_assignee:
        assignee_filter_count = Demand.objects.filter(assignee=user, state=item['state']).count()
        filters.append({
            'name': item["filter_name"],
            'state': StateDemandSerializer(item['state']).data,
            'creator': None,
            'assignee': user.username,
            'count': assignee_filter_count,
        })

    return Response(filters)

class DemandEventsView(generics.GenericAPIView):
    serializer_class = SimplifiedEventSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        demand = get_object_or_404(Demand, pk=pk)
        events = Event.objects.filter(demand=demand).prefetch_related(Prefetch('validationinfo_set', queryset=ValidationInfo.objects.all(), to_attr='validation_info'))
        for event in events:
            event.validation_info = event.validation_info[0] if event.validation_info else None
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)


class EventValidationInfoView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = ValidationInfoReadSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'event_id'
    lookup_url_kwarg = 'event_id'
    
    def get_object(self):
        event = super().get_object()
        validation_info = get_object_or_404(ValidationInfo, event=event)
        return validation_info

def download(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    raise Http404

def total_demands(request, time_frame):
    if time_frame == 'all':
        total = Demand.objects.count()
    elif time_frame == 'year':
        total = Demand.objects.filter(created_at__year=timezone.now().year).count()
    elif time_frame == 'month':
        total = Demand.objects.filter(created_at__month=timezone.now().month, created_at__year=timezone.now().year).count()
    elif time_frame == 'week':
        total = Demand.objects.filter(created_at__date__gte=timezone.now() - datetime.timedelta(days=7)).count()
    else:
        return JsonResponse({'error': 'Invalid time frame'}, status=400)
    
    return JsonResponse({'total': total})

def avg_demands(request, time_frame):
    if time_frame == 'day':
        avg = Demand.objects.annotate(date=TruncDay('created_at')).values('date').annotate(avg=Avg('id')).aggregate(Avg('avg'))
    elif time_frame == 'week':
        avg = Demand.objects.annotate(week=TruncWeek('created_at')).values('week').annotate(avg=Avg('id')).aggregate(Avg('avg'))
    elif time_frame == 'month':
        avg = Demand.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(avg=Avg('id')).aggregate(Avg('avg'))
    else:
        return JsonResponse({'error': 'Invalid time frame'}, status=400)
    
    return JsonResponse({'average': avg})


from django.db.models import Value as V
from django.db.models.functions import Concat

class EmployeeDemandStatsView(APIView):
    """
    Returns a list of employees with the highest number of created demands.
    """
    def get(self, request):
        N = int(request.query_params.get('N', 10))  # default to 10 if N is not provided
        M = int(request.query_params.get('M', 20))  # default to 20 if M is not provided

        # Get the counts
        employee_counts = (
            Demand.objects.values('creator__employee_id')
            .annotate(created_demands=Count('creator'))
            .order_by('-created_demands')
        )

        # Fetch only the top N
        top_counts = employee_counts[:N]

        # Get the names
        employee_names = Employee.objects.filter(customuser__in=top_counts.values('creator')).annotate(
            full_name=Concat('first_name', V(' '), 'last_name')
        ).values('id', 'full_name')

        # Create a dictionary for easier lookup
        name_dict = {item['id']: item['full_name'] for item in employee_names}

        # Merge the results
        result = []
        for count in top_counts:
            result.append({
                'full_name': name_dict.get(count['creator__employee_id'], 'Unknown'),
                'created_demands': count['created_demands'],
            })

        # Handle the remaining employees
        remaining_counts = employee_counts[N:M]

        remaining_names = Employee.objects.filter(customuser__in=remaining_counts.values('creator')).annotate(
            full_name=Concat('first_name', V(' '), 'last_name')
        ).values('id', 'full_name')

        remaining_name_dict = {item['id']: item['full_name'] for item in remaining_names}

        for count in remaining_counts:
            result.append({
                'full_name': remaining_name_dict.get(count['creator__employee_id'], 'Unknown'),
                'created_demands': count['created_demands'],
            })
        return Response(result)
    
class MissionTypeStatsView(APIView):
    """
    Returns a list of mission types and their respective count.
    """
    def get(self, request):
        mission_types = (
            MissionOrder.objects.values('mission_type__name')
            .annotate(mission_count=Count('mission_type'))
            .order_by('-mission_count')
        )
        return Response(mission_types)