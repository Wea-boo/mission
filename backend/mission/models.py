from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
from cpkmodel import CPkModel

# Create your models here.


class Direction(Enum):
    RETRAITES = 'Retraites'
    GESTION_CARRIERES = 'Gestion des Carrières'
    FINANCES = 'Finances'
    INFORMATIQUE_ORGANISATION = 'Informatique et Organisation'
    ADMINISTRATION_GENERALES = 'Administration Générales'

class TypeDemand(Enum):
    OM = 'Demande Ordre de mission'
    FM = 'Demande de Frais de mission'

class TypeMission(Enum):
    TECHNIC = 'Technique'
    INSPECT = 'Inspection'
    MANAGE = 'Management'
    AUDIT = 'Audit et Contrôle'

class CustomUser(AbstractUser):
    employee = models.OneToOneField('Employee', null=False, on_delete=models.CASCADE)

class Employee(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    phone = models.CharField(max_length=10, null=False, blank=True)
    grade = models.CharField(max_length=50, null=False, blank=False)
    function = models.CharField(max_length=50, null=False, blank=True)
    direction = models.CharField(
        max_length=255,
        choices=[(tag.value, tag.name) for tag in Direction])
    manager = models.ForeignKey('Employee', null=True, on_delete=models.SET_NULL)

# class Group(models.Model):
#     name = models.CharField(max_length=50, null=False, blank=False)

class WorkFlow(models.Model):
    version = models.CharField(max_length=10, null=False, blank=False)
    demand_type = models.CharField(
        max_length=255,
        choices=[(tag.value, tag.name) for tag in TypeDemand])

class StateDemand(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    workflow = models.ForeignKey(WorkFlow , null=False, on_delete=models.CASCADE)

class Demand(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(
        max_length=255,
        choices=[(tag.value, tag.name) for tag in TypeDemand])
    creator = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='created_demands')
    assignee = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='assigned_demands')
    state = models.ForeignKey(StateDemand, null=False, on_delete=models.CASCADE)

class Agency(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)

class MissionOrder(models.Model):
    mission_type = models.CharField(
        max_length=255,
        choices=[(tag.value, tag.name) for tag in TypeMission])
    use_personal_vehicle = models.BooleanField(null=False)
    departing = models.DateTimeField()
    returning = models.DateTimeField()
    observation_manager = models.CharField(max_length=255)
    observation_HR = models.CharField(max_length=255)
    demand = models.ForeignKey(Demand, null=False, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, null=False, on_delete=models.CASCADE)

class Transition(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    start_state = models.ForeignKey(StateDemand, null=True, on_delete=models.CASCADE, related_name='start_point')
    end_state = models.ForeignKey(StateDemand, null=False, on_delete=models.CASCADE, related_name='end_point')
    workflow = models.ForeignKey(WorkFlow, null=False, on_delete=models.CASCADE)

class Event(models.Model):
    demand = models.ForeignKey(Demand, null=False, on_delete=models.CASCADE)
    trigger_user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
    transit = models.ForeignKey(Transition, null=False, on_delete=models.CASCADE)
    time_event = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['demand','trigger_user','transit']

class MissionFee(models.Model):
    demand = models.ForeignKey(Demand, null=False, on_delete=models.CASCADE)
    mission_order = models.ForeignKey(MissionOrder, null=False, on_delete=models.CASCADE)
    