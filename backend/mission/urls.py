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
    path('demand/<int:pk>/envoyer/', CreatedToWaitingApproval.as_view(), name="submit-demand")
]