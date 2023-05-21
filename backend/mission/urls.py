from django.urls import path
from .views import CustomLoginView
from knox.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='knox_login'),
    path('logout/', LogoutView.as_view(), name='knox_logout'),
    path('check_auth/', CheckAuthView.as_view(), name='check_auth'),
    path("mission-types/", TypeMissionList.as_view(), name="mission-types"),
    path("agencies/", AgencyList.as_view(), name="agency-list"),
    path("create-demand/", CreateOwnDemandView.as_view(), name="create_demand"),
    path('demand/<int:pk>/', DemandDetailsView.as_view(), name='demand_details'),
    path('demand/<int:pk>/transitions/', DemandTransitionsAPIView.as_view(), name='demand-transitions'),
    path('demand/<int:pk>/envoyer/', CreatedToWaitingApproval.as_view(), name="submit-demand"),
    path('demand/<int:pk>/approuver/', WaitingApprovalToApproved().as_view(), name="approve-demand"),
    path('demand/<int:pk>/annuler/', CreatedToCancelled.as_view(), name='cancel-demand'),
    path('demand/<int:pk>/refuser/', WaitingApprovalToDenied.as_view(), name='deny-demand'),
    path('demand/<int:pk>/etablir-ordre/', ApprovedToWaitingValidation.as_view(), name='establish-order'),
    path('demand/<int:pk>/valider/', WaitingValidationToValidated.as_view(), name='validate-order'),
    path('demand/<int:pk>/rejeter/', WaitingApprovalToDenied.as_view(), name='deny-order'),
    path('users-in-direction/', UsersInSameDirection.as_view(), name='users-in-same-direction'),
    path('user-profile/', UserProfile.as_view(), name='user-profile'),
    path('create-others-demand/', CreateOthersDemandView.as_view(), name="create_demand_pc"),
    path('demands/', DemandList.as_view(), name='demand-list'),
    path('dashboard-filters/', dashboard_filters, name='dashboard_filters'),
    path('demand/<int:pk>/events/', DemandEventsView.as_view(), name='demand-events'),
    path('events/<int:event_id>/validationinfo/', EventValidationInfoView.as_view(), name='event-validationinfo'),
    path('total_demands_<str:time_frame>/', total_demands),
    path('avg_demands_<str:time_frame>/', avg_demands),
]