from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(HSE)
admin.site.register(HSESegment)
admin.site.register(GeneralHse)
admin.site.register(HSETraining)
admin.site.register(HSEObservation)
admin.site.register(SubObservation)
admin.site.register(StopWork)
admin.site.register(ManagementVisit)
admin.site.register(ViolationMemo)
admin.site.register(Incidents)
admin.site.register(SubIncident)
admin.site.register(HSEUser)


# @admin.register(GeneralHse)
# class YourModelAdmin(admin.ModelAdmin):
#     list_display = ('created_at', 'no_of_toolbox_attendees','no_of_person_inducted_site','total_safe_man_hours','total_man_days_worked')

# @admin.register(HSETraining)
# class YourModelAdmin(admin.ModelAdmin):
#     list_display = ('created_at', 'duration_of_contractor','hse_training_contractor','hse_training_attendees','duration_of_trainee')

# @admin.register(HSEObservation)
# class YourModelAdmin(admin.ModelAdmin):
#     list_display = ('created_at', 'complaint_from_customer','violation_memo_issued','stop_work_notice','daily_hse_observation','hse_observation')

# @admin.register(Incidents)
# class YourModelAdmin(admin.ModelAdmin):
#     list_display = ('created_at', 'no_of_environment_illness','no_of_occupation_illness','no_of_incidents')

# @admin.register(ManagementVisits)
# class YourModelAdmin(admin.ModelAdmin):
#     list_display = ('created_at', 'observation_pending','no_of_compilance_done','total_findings','no_of_compilance_done_file','total_findings_file','no_of_management_visits_file')
