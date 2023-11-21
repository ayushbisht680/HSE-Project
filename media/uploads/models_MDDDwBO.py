from django.db import models
from base.models import ErpEmployee

class ProjectViewOnlyEmployee(models.Model):
    view_only_employee = models.OneToOneField(ErpEmployee, on_delete=models.CASCADE)

    def __str__(self):
        return self.view_only_employee.__str__()

class Project(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    project_manager = models.ForeignKey(ErpEmployee, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='projects')
    site_construction_manager = models.ForeignKey(ErpEmployee, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_completed = models.BooleanField()

    def __str__(self):
        return self.id + ' | ' + self.name

class LandSite(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(ErpEmployee, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='land_site_created_by')
    updated_by = models.ForeignKey(ErpEmployee, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.id + ' | ' + self.project.name + ' | ' + self.name

    class Meta:
        unique_together = ('name', 'project')

class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name    

class Subtask(models.Model): 
    name = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.task.name + ' | ' + self.name

    class Meta:
        unique_together = ('name', 'task')

class SubtaskBasicInfo(models.Model):
    uom =  models.CharField(max_length=50)
    bom = models.IntegerField()
    base_line_completion_date = models.DateField()
    subtask = models.ForeignKey(Subtask, on_delete=models.CASCADE)
    land_site = models.ForeignKey(LandSite, on_delete=models.CASCADE, related_name='subtask_basic_infos')
    created_by = models.ForeignKey(ErpEmployee, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='subtask_basic_info_created_by')
    updated_by = models.ForeignKey(ErpEmployee, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'land site = ' + str(self.land_site.id) + ' | ' + self.subtask.__str__()

    class Meta:
        unique_together = ('subtask', 'land_site')

class SubtaskDailyProgress(models.Model): 
    STATUS = (
        ('ONG', 'Ongoing'),
        ('CPL', 'Complete'),
    )   
    dpr_date = models.DateField()
    today_progress = models.IntegerField(default=0)  
    status = models.CharField(max_length=3, choices=STATUS, default='ONG')
    construction_remarks = models.TextField(null=True, blank=True)
    man_power = models.TextField(null=True, blank=True)
    machinery = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    subtask_basic_info = models.ForeignKey(SubtaskBasicInfo, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(ErpEmployee, on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.subtask_basic_info.id) + ' | ' + self.dpr_date.strftime('%d/%m/%Y')  

    class Meta:
        unique_together = ('dpr_date', 'subtask_basic_info')
