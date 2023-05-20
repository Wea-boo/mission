from django.db import models
from django.contrib.auth.models import AbstractUser, Group as DjangoGroup, GroupManager
from cpkmodel import CPkModel

# Create your models here.
def get_init_state_demand():
    init_state_demand, _ = StateDemand.objects.get_or_create(name="Init")
    return init_state_demand.id

def get_profile_missionaire():
    missionaire_profile, _ = Profile.objects.get_or_create(name="Missionaire")
    return missionaire_profile.id

class Direction(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class TypeDemand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class TypeMission(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    employee = models.OneToOneField('Employee', null=False, on_delete=models.CASCADE)
    main_profile = models.ForeignKey('Profile', null=False, on_delete=models.SET_DEFAULT,default=get_profile_missionaire)

    def __str__(self):
        return self.username

class Employee(models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    phone = models.CharField(max_length=10, null=True, blank=True)
    grade = models.CharField(max_length=50, null=False, blank=False)
    function = models.CharField(max_length=50, null=True, blank=True)
    direction = models.ForeignKey(Direction, null=False, on_delete=models.CASCADE)
    manager = models.ForeignKey('Employee', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class WorkFlow(models.Model):
    version = models.CharField(max_length=10, null=False, blank=False)
    demand_type = models.ForeignKey(TypeDemand, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.version} - {self.demand_type}"

class StateDemand(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    workflow = models.ForeignKey(WorkFlow, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Demand(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey(TypeDemand, null=False, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='created_demands')
    assignee = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='assigned_demands')
    state = models.ForeignKey(StateDemand, null=False, on_delete=models.CASCADE, default=get_init_state_demand)

    def __str__(self):
        return f"{self.type} : {self.creator.employee}"

class Agency(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.name

class MissionOrder(models.Model):
    mission_type = models.ForeignKey(TypeMission, null=False, on_delete=models.CASCADE)
    trip_purpose = models.TextField()
    use_personal_vehicle = models.BooleanField(null=False)
    departing = models.DateTimeField()
    returning = models.DateTimeField()
    mission_summary = models.TextField()
    demand = models.OneToOneField(Demand, null=False, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mission_type} : {self.demand.creator.employee}"

class Transition(models.Model):
    description = models.CharField(max_length=255, null=False, blank=False) # Changed name to description
    action = models.CharField(max_length=25, null=False, blank=False) # Added new field action
    start_state = models.ForeignKey(StateDemand, null=False, on_delete=models.CASCADE, related_name='start_point')
    end_state = models.ForeignKey(StateDemand, null=False, on_delete=models.CASCADE, related_name='end_point')
    workflow = models.ForeignKey(WorkFlow, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description}"

class Event(models.Model):
    demand = models.ForeignKey(Demand, null=False, on_delete=models.CASCADE)
    trigger_user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE)
    transition = models.ForeignKey(Transition, null=False, on_delete=models.CASCADE)
    time_event = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transition} par {self.trigger_user.employee} le {self.time_event}"

    class Meta:
        unique_together = ['demand', 'trigger_user', 'transition']

class ValidationInfo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    observation_text = models.TextField()
    attachment = models.FileField(upload_to='attachments/')

class MissionFee(models.Model):
    demand = models.OneToOneField(Demand, null=False, on_delete=models.CASCADE)
    mission_order = models.OneToOneField(MissionOrder, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"Frais pour {self.mission_order}"
    
class Profile(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Group(DjangoGroup):
    profile = models.OneToOneField(Profile, null=True, on_delete=models.SET_NULL, related_name='group')

    def __str__(self):
        return self.name