from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from base.models import *



CATEGORY_CHOICES = [
    ('Category', 'Category'),
    ('Legal Requirement', 'Legal Requirement'),
    ('Permit to Work', 'Permit to Work'),
    ('Electrical Work', 'Electrical Work'),
    ('Working at Height', 'Working at Height'),
    ('Lifting Operation', 'Lifting Operation'),
    ('Excavation', 'Excavation'),
    ('Hot Work', 'Hot Work'),
    ('Confined Space Work', 'Confined Space Work'),
    ('Manual Handling', 'Manual Handling'),
    ('Houskeeping', 'Houskeeping'),
    ('Chemical Handling', 'Chemical Handling'),
    ('SOP and Procedure Violation', 'SOP and Procedure Violation'),
    ('Medical Examination', 'Medical Examination'),
    ('PPE', 'PPE'),
    ('Vehicle Movment', 'Vehicle Movment'),
    ('Waste Management', 'Waste Management'),
    ('Welfare Facility', 'Welfare Facility'),
    ('General - Signage, Access, Walkway', 'General - Signage, Access, Walkway'),
    ('Emergency Preparedness', 'Emergency Preparedness'),
    ]


STATUS_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('NA', 'NA'),
    ]

INCIDENT_TYPE_CHOICES = [
        ('Near Miss', 'Near Miss'),
        ('LTI', 'LTI'),
        ('MTI', 'MTI'),
        ('Fatal', 'Fatal'),
        ('Property Damage', 'Property Damage'),
        ('Flash Over', 'Flash Over'),
        ('Arc Flash', 'Arc Flash'),
        ('Fire', 'Fire'),
    ]

CATEOGRIES=[
        ('Recordable','Recordable'),
        ('Non-Recordable','Non-Recordable')
    ]


class HSEUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hse_permission = models.BooleanField()
    
    class Meta:
        verbose_name = "HSE Users" 
        verbose_name_plural = "HSE Users"

    def __str__(self):
        return self.user.username

 
    
class HSESegment(models.Model):
    segment = models.CharField(max_length=20)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=True, blank=True)
    homescape = models.ForeignKey(HomeScape, on_delete=models.CASCADE, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True)

    
    class Meta:
        verbose_name = "HSESegment" 
        verbose_name_plural = "HSESegment"

    
    def __str__(self):
        return f"{self.segment}"


class HSE(models.Model):
    hse_segment=models.ForeignKey(HSESegment, on_delete=models.CASCADE, null=True, blank=True)    
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='created_hse_records',null=True,blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='updated_hse_records',null=True,blank=True)

    formSubmittedDate = models.DateField(default=None, null=True,blank=True)

    form_status=models.IntegerField()

    class Meta:
        verbose_name = "HSE" 
        verbose_name_plural = "HSE"
    
    def __str__(self):
        return f"HSE- ID: {self.id}, formSubmittedDate: {self.formSubmittedDate}"
    

class GeneralHse(models.Model):
    today_day_worked_file = models.FileField(upload_to='uploads/', null=True, blank=True)
    total_man_days_worked = models.PositiveIntegerField()
    total_safe_man_hours = models.FloatField()
    no_of_person_inducted_site = models.PositiveIntegerField()
    no_of_toolbox_attendees = models.PositiveIntegerField()
    toolbox_talk_manhours = models.FloatField()
    toolbox_talk_manhours_file = models.FileField(upload_to='uploads/', null=True, blank=True)
    promotional_activities = models.PositiveIntegerField()
    promotional_activities_file = models.FileField(upload_to='uploads/', null=True, blank=True)
    committe_meetings = models.PositiveIntegerField()
    submittedDate = models.DateField(default=None, null=True,blank=True)
    formSubmitted = models.BooleanField(default=False)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_general_hse_records', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_general_hse_records', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)

    hse = models.ForeignKey(HSE, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "General HSE"
        verbose_name_plural = "General HSE"

    def __str__(self):
        return f"General HSE - ID: {self.id}, Submitted Date: {self.submittedDate}"


class HSETrainingsModel(models.Model):
    hse_training_attendees = models.PositiveIntegerField()
    no_of_attendees_amplus = models.FileField(upload_to='uploads/', null=True)
    duration_of_trainee = models.FloatField()
    hse_training_contractor = models.PositiveIntegerField()
    no_of_attendees_contractor = models.FileField(upload_to='uploads/', null=True)
    duration_of_contractor = models.FloatField()
    amplus_hse_trainings = models.FloatField()
    contractor_hse_trainings = models.FloatField()
    submittedDate = models.DateField(default=None, null=True)
    formSubmitted = models.BooleanField(default=False)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_hse_training_records', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_hse_training_records', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)

    hse = models.ForeignKey(HSE, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "HSE Trainings" 
        verbose_name_plural = "HSE Trainings"
    
    def __str__(self):
        return f"HSE Training - ID: {self.id}, Submitted Date: {self.submittedDate}"

   
class HSEObservation(models.Model):
    hse_observation = models.FileField(upload_to='uploads/', null=True, blank=True)
    daily_hse_observation = models.PositiveIntegerField(null=True, blank=True)
    stop_work_notice = models.PositiveIntegerField(null=True, blank=True)
    violation_memo_issued = models.PositiveIntegerField(null=True, blank=True)
    complaint_from_customer = models.PositiveIntegerField(null=True, blank=True)
    submittedDate = models.DateField(default=None, null=True)
    formSubmitted = models.BooleanField(default=False)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_hse_observation_records', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_hse_observation_records', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)

    hse = models.ForeignKey(HSE, on_delete=models.CASCADE, null=True, blank=True)
     
    class Meta:
        verbose_name = "HSE Observation" 
        verbose_name_plural = "HSE Observation"
    
    def __str__(self):
        return f"HSE Observation - ID: {self.id}, Submitted Date: {self.submittedDate}"


class ManagementVisits(models.Model):
    no_of_management_visits = models.PositiveIntegerField()
    no_of_management_visits_file = models.FileField(upload_to='uploads/', null=True)
    total_findings = models.PositiveIntegerField()
    total_findings_file = models.FileField(upload_to='uploads/', null=True)
    no_of_compilance_done = models.PositiveIntegerField()
    no_of_compilance_done_file = models.FileField(upload_to='uploads/', null=True)
    observation_pending = models.PositiveIntegerField()
    submittedDate = models.DateField(default=None, null=True)
    formSubmitted = models.BooleanField(default=False)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_management_visits_records', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_management_visits_records', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)

    hse = models.ForeignKey(HSE, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Management Visits" 
        verbose_name_plural = "Management Visits"

    def __str__(self):
        return f"Management Visits - ID: {self.id}, Submitted Date: {self.submittedDate}"


class Incidents(models.Model):
    no_of_incidents = models.PositiveIntegerField(null=True, blank=True)
    no_of_occupation_illness = models.PositiveIntegerField(null=True, blank=True)
    no_of_environment_illness = models.PositiveIntegerField(null=True, blank=True)
    submittedDate = models.DateField(default=None, null=True)
    formSubmitted = models.BooleanField(default=False)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_incidents_records', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_incidents_records', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)

    hse = models.ForeignKey(HSE, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Incidents" 
        verbose_name_plural = "Incidents"

    def __str__(self):
        return f"Incidents - ID: {self.id}, Submitted Date: {self.submittedDate}"


class HSEObservationForm(models.Model):
  

    datetime_observation = models.DateTimeField(blank=True,null=True)
    location = models.CharField(max_length=300)
    plant_site = models.CharField(max_length=300)
    observation = models.TextField()
    unsafe_condition = models.CharField(max_length=300)
    category = models.CharField(max_length=100,choices=CATEGORY_CHOICES,default='Category')
    corrective_action_taken = models.TextField()
    responsible_person = models.CharField(max_length=300)
    form_closure_date=models.DateField(blank=True,null=True)
    status = models.CharField(max_length=3,choices=STATUS_CHOICES,default='Yes')
    stop_work = models.CharField(max_length=300)
    open_evidence = models.FileField(upload_to='form_uploads', null=True)
    closed_evidence = models.FileField(upload_to='form_uploads', null=True)
    remark = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_observation_form_records', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_observation_form_records', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)
    hse_observation = models.ForeignKey(HSEObservation, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Observation Form"
        verbose_name_plural = "Observation Forms"

    def __str__(self):
        return f"Observation Form - ID: {self.id}"


class StopWorkForm(models.Model):
    
    datetime_observation = models.DateTimeField(blank=True,null=True)
    location = models.CharField(max_length=300)
    plant_site = models.CharField(max_length=300)
    description_of_issue = models.TextField()
    unsafe_act = models.CharField(max_length=300)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Category')
    corrective_action_taken = models.TextField()
    remaining_hazard = models.CharField(max_length=300)
    responsible_person = models.CharField(max_length=300)
    form_closure_date=models.DateField(blank=True,null=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES, default='Status')
    open_evidence = models.CharField(max_length=300, null=True)
    closed_evidence = models.CharField(max_length=300, null=True)
    remark = models.CharField(max_length=300)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_stopwork_form_records', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_stopwork_form_records', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)

    hse_observation = models.ForeignKey(HSEObservation, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Stop Work Form"
        verbose_name_plural = "Stop Work Forms"

    def __str__(self):
        return f"Stop Work Form - ID: {self.id}"


class ViolationMemoForm(models.Model):
    
    date_field = models.DateField(blank=True, null=True)
    project_name = models.CharField(max_length=300)
    project_code = models.CharField(max_length=300)
    business_segment = models.CharField(max_length=300)
    memo_no = models.CharField(max_length=10)
    description = models.TextField()
    action_taken = models.TextField()
    issued_by = models.CharField(max_length=300)
    issued_to = models.CharField(max_length=300)
    penalty_imposed = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Penalty_imposed')
    amount = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_violationMemo_form_records', null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_violationMemo_form_records', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)

    hse_observation = models.ForeignKey(HSEObservation, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Violation Memo Form"
        verbose_name_plural = "Violation Memo Forms"

    def __str__(self):
        return f"Violation Memo Form - ID: {self.id}"


class IncidentForm(models.Model):

    datetime_observation = models.DateTimeField(blank=True,null=True)
    location = models.TextField(max_length=100)
    exact_location = models.TextField(max_length=100)
    plant_site = models.TextField(max_length=100)
    project_code = models.TextField(max_length=100)
    description_of_incident = models.TextField()
    root_cause = models.TextField()
    type_of_incident = models.CharField(max_length=20, choices=INCIDENT_TYPE_CHOICES, default='Incident_type')
    high_potential_incident=models.CharField(max_length=50,choices=STATUS_CHOICES, default='high_potential_incident')
    category=models.CharField(max_length=50,choices=CATEOGRIES, default='Incident_choices')
    immediate_action_taken =models.TextField()
    corrective_action = models.TextField()
    prevention_action = models.TextField()
    responsible_person = models.TextField(max_length=100)
    investigation_status = models.TextField(max_length=100)
    attach_report = models.FileField(upload_to='form_uploads', null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='created_incident_form_records',null=True,blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='updated_incident_form_records',null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=True)

    incidents = models.ForeignKey(Incidents, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Incident Form"
        verbose_name_plural = "Incident Forms"

    def __str__(self):
        return f"Incident Form - ID: {self.id}"






   
    











