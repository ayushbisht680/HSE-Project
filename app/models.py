from django.db import models
from django.utils import timezone



class Plant(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Plant code')
    name = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200,  null=True, blank=True)
    country = models.CharField(max_length=200,null=True, blank=True)
    address = models.TextField(null=True, blank=True)

class HSE(models.Model):
    plant_code=models.ForeignKey(Plant, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    formSubmittedDate = models.DateField(default=None, null=True)

    form_status=models.IntegerField()

    class Meta:
        verbose_name = "HSE" 
        verbose_name_plural = "HSE"

   
class GeneralHse(models.Model):
    today_day_worked_file = models.FileField(upload_to='uploads/', null=True,blank=True)
    total_man_days_worked = models.IntegerField()
    total_safe_man_hours = models.IntegerField()
    no_of_person_inducted_site = models.IntegerField()
    no_of_toolbox_attendees = models.IntegerField()
    toolbox_talk_manhours=models.IntegerField()
    toolbox_talk_manhours_file=models.FileField(upload_to='uploads/', null=True,blank=True)
    promotional_activities=models.IntegerField()
    promotional_activities_file=models.FileField(upload_to='uploads/', null=True,blank=True)
    committe_meetings=models.IntegerField()
    submittedDate = models.DateField(default=None, null=True)
    formSubmitted = models.BooleanField(default=False)  

    hse = models.ForeignKey(HSE, on_delete=models.CASCADE,null=True)


    class Meta:
        verbose_name = "General HSE"
        verbose_name_plural = "General HSE"


class HSETrainingsModel(models.Model):
    hse_training_attendees=models.IntegerField()
    no_of_attendees_amplus=models.FileField(upload_to='uploads/',null=True)
    duration_of_trainee=models.IntegerField()
    hse_training_contractor=models.IntegerField()
    no_of_attendees_contractor=models.FileField(upload_to='uploads/',null=True)
    duration_of_contractor=models.IntegerField()
    amplus_hse_trainings=models.IntegerField()
    contractor_hse_trainings=models.IntegerField()
    submittedDate = models.DateField(default=None, null=True)
    formSubmitted = models.BooleanField(default=False)  

    hse = models.ForeignKey(HSE, on_delete=models.CASCADE,null=True)

   

    class Meta:
        verbose_name = "HSE Trainings" 
        verbose_name_plural = "HSE Trainings"

    
class HSEObservation(models.Model):
    hse_observation=models.FileField(upload_to='uploads/',null=True,blank=True)
    daily_hse_observation=models.IntegerField(null=True,blank=True)
    stop_work_notice=models.IntegerField(null=True,blank=True)
    violation_memo_issued=models.IntegerField(null=True,blank=True)
    complaint_from_customer=models.IntegerField(null=True,blank=True)
    submittedDate = models.DateField(default=None, null=True)
    formSubmitted = models.BooleanField(default=False)  

    hse = models.ForeignKey(HSE, on_delete=models.CASCADE,null=True,blank=True)
     

    class Meta:
        verbose_name = "HSE Observation" 
        verbose_name_plural = "HSE Observation"

class ManagementVisits(models.Model):
    no_of_management_visits=models.IntegerField()
    no_of_management_visits_file=models.FileField(upload_to='uploads/',null=True)
    total_findings=models.IntegerField()
    total_findings_file=models.FileField(upload_to='uploads/',null=True)
    no_of_compilance_done=models.IntegerField()
    no_of_compilance_done_file=models.FileField(upload_to='uploads/',null=True)
    observation_pending=models.IntegerField()
    submittedDate = models.DateField(default=None, null=True)
    formSubmitted = models.BooleanField(default=False)  

    hse = models.ForeignKey(HSE, on_delete=models.CASCADE,null=True)


    class Meta:
        verbose_name = "Management Visits" 
        verbose_name_plural = "Management Visits"
        

class Incidents(models.Model):
    no_of_incidents=models.IntegerField(null=True,blank=True)
    no_of_occupation_illness=models.IntegerField(null=True,blank=True)
    no_of_environment_illness=models.IntegerField(null=True,blank=True)
    submittedDate = models.DateField(default=None, null=True)
    formSubmitted = models.BooleanField(default=False)  

    hse = models.ForeignKey(HSE, on_delete=models.CASCADE,null=True,blank=True)



    class Meta:
        verbose_name = "Incidents" 
        verbose_name_plural = "Incidents"


class HSEObservationForm(models.Model):
    SrNo=models.IntegerField()
    Date=models.TextField(max_length=100)
    Time=models.TextField(max_length=100)
    Location=models.TextField(max_length=100)
    PlantSite=models.TextField(max_length=100)
    Observation=models.TextField(max_length=100)
    UnsafeCondition=models.TextField(max_length=100)
    Cateogry=models.TextField(max_length=100)
    CorrrectiveActionTAken=models.TextField(max_length=100)
    ResponsiblePerson=models.TextField(max_length=100)
    ClosureDate=models.TextField(max_length=100)
    Status=models.TextField(max_length=100)
    StopWork=models.TextField(max_length=100)
    OpenEvidence=models.FileField(upload_to='formUploads',null=True)
    ClosedEvidence=models.FileField(upload_to='formUploads',null=True)
    Remark=models.TextField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    hse_observation = models.ForeignKey(HSEObservation, on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = "Observation Form" 
        verbose_name_plural = "Observation Form"
    

class StopWorkForm(models.Model):
    SrNo=models.IntegerField()
    Date=models.TextField(max_length=100)
    Time=models.TextField(max_length=100)
    Location=models.TextField(max_length=100)
    PlantSite=models.TextField(max_length=100)
    DescriptionOfIssue=models.TextField(max_length=100)
    UnsafeAct=models.TextField(max_length=100)
    Cateogry=models.TextField(max_length=100)
    CorrrectiveActionTAken=models.TextField(max_length=100)
    RemainingHazard=models.TextField(max_length=100)
    ResponsiblePerson=models.TextField(max_length=100)
    ClosureDate=models.TextField(max_length=100)
    Status=models.TextField(max_length=100)
    OpenEvidence=models.FileField(upload_to='formUploads',null=True)
    ClosedEvidence=models.FileField(upload_to='formUploads',null=True)
    Remark=models.TextField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    hse_observation = models.ForeignKey(HSEObservation, on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = "Stop Work Form" 
        verbose_name_plural = "Stop Work Form"


class ViolationMemoForm(models.Model):
    SrNo=models.IntegerField()
    Date=models.TextField(max_length=100)
    ProjectName=models.TextField(max_length=100)
    ProjectCode=models.TextField(max_length=100)
    BusinessSegment=models.TextField(max_length=100)
    MemoNo=models.TextField(max_length=100)
    Description=models.TextField(max_length=100)
    ActionTaken=models.TextField(max_length=100)
    IssuedBy=models.TextField(max_length=100)
    IssuedTo=models.TextField(max_length=100)
    PenaltyImposed=models.TextField(max_length=100)
    Amount=models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    hse_observation = models.ForeignKey(HSEObservation, on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = "Violation Memo Form" 
        verbose_name_plural = "Violation Memo Form"


class IncidentForm(models.Model):
    SrNo=models.IntegerField()
    IncidentDate=models.TextField(max_length=100)
    IncidentTime=models.TextField(max_length=100)
    Location=models.TextField(max_length=100)
    ExactLocation=models.TextField(max_length=100)
    PlantSite=models.TextField(max_length=100)
    ProjectCode=models.TextField(max_length=100)
    DescriptionOfIncident=models.TextField(max_length=100)
    RootCause=models.TextField(max_length=100)
    TypeOfIncident=models.TextField(max_length=100)
    HiPotentialIncident=models.TextField(max_length=100)
    Cateogry=models.TextField(max_length=100)
    ImmediateActionTaken=models.TextField(max_length=100)
    CorrectiveAction=models.TextField(max_length=100)
    PreventionAction=models.TextField(max_length=100)
    ResponsiblePerson=models.TextField(max_length=100)
    InvestigationStatus=models.TextField(max_length=100)
    AttachReport=models.FileField(upload_to='formUploads',null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    incidents = models.ForeignKey(Incidents, on_delete=models.CASCADE,null=True)

    class Meta:
        verbose_name = "Incident Form" 
        verbose_name_plural = "Incident Form"





   
    











