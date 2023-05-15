from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import authenticate, login
from rest_framework import permissions, serializers
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views import View
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from django.conf import settings
from .models import *
from .serializers import *
from rest_framework import status
from .permissions import *
from django.db.models import Q
from django.db import transaction

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
    
        latest_workflow = WorkFlow.objects.latest('id')
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
        validation_info = request.data
        

        # Check if required fields are present in validation info
        if 'obs_manager' not in validation_info:
            return Response({"message": "Required fields missing in validation info."}, status=status.HTTP_400_BAD_REQUEST)

        # Get HR Agent user/group
        hr_agent_group = Group.objects.get(profile__name='Agent RH')
        hr_agent_user = CustomUser.objects.filter(
            Q(main_profile__name='Agent RH') | 
            Q(groups__id=hr_agent_group.id)
        ).first()

        # Check if an HR Agent user was found.
        if hr_agent_user is None:
            return Response({"message": "No suitable HR Agent user found to assign the demand."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the observation_manager field in MissionOrder associated with the demand
        mission_order = demand.missionorder
        mission_order.observation_manager = validation_info['obs_manager']
        mission_order.save()

        # Record the transition event
        latest_workflow = WorkFlow.objects.latest('id')
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
        
        approved_state = StateDemand.objects.get(name="Approuvé")
        demand.state = approved_state
        demand.assignee = hr_agent_user
        demand.save()
        
        return Response({"message": "Transitioned to 'Approved' state successfully."}, status=status.HTTP_200_OK)

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

        # Record the transition event
        latest_workflow = WorkFlow.objects.latest('id')
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

        # Change the state of the Demand to "Cancelled"
        cancelled_state = StateDemand.objects.get(name="Annulé")
        demand.state = cancelled_state

        # Set the assignee to the creator of the demand
        demand.assignee = demand.creator
        demand.save()

        return Response({"message": "Transitioned to 'Cancelled' state successfully."}, status=status.HTTP_200_OK)
    
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