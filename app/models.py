from django.db import models
from django.utils import timezone


class ParentModel(models.Model):
    week_number = models.IntegerField()
    year = models.IntegerField()
    plant_code=models.IntegerField()
    form_status=models.IntegerField()

   
class GeneralHse(models.Model):
    today_day_worked_file = models.FileField(upload_to='uploads/', null=True)
    total_man_days_worked = models.IntegerField()
    total_safe_man_hours = models.IntegerField()
    no_of_person_inducted_site = models.IntegerField()
    no_of_toolbox_attendees = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE,null=True)


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
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE,null=True)

   

    class Meta:
        verbose_name = "HSE Trainings" 
        verbose_name_plural = "HSE Trainings"

    
class HSEObservation(models.Model):
    hse_observation=models.FileField(upload_to='uploads/',null=True)
    daily_hse_observation=models.IntegerField()
    stop_work_notice=models.IntegerField()
    violation_memo_issued=models.IntegerField()
    complaint_from_customer=models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE,null=True)
     

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
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE,null=True)


    class Meta:
        verbose_name = "Management Visits" 
        verbose_name_plural = "Management Visits"
        

class Incidents(models.Model):
    no_of_incidents=models.IntegerField()
    no_of_occupation_illness=models.IntegerField()
    no_of_environment_illness=models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE,null=True)



    class Meta:
        verbose_name = "Incidents" 
        verbose_name_plural = "Incidents"








