from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('general_hse/',GeneralHSEAPI.as_view(),name='General HSE'),
    path('hse_trainingModel/', HSETrainingsAPI.as_view(), name='HSE Trainings'),
    path('hse_observation/', HSEObservationAPI.as_view(), name="HSE Observations"),
    path('management_visit/', ManagementAPI.as_view(), name="Management Visits"),
    path('incidents/', IncidentsAPI.as_view(), name="Incidents"),
    path('my_html/', MyTemplateView.as_view(),name='MyHTML'),
    path('my_form/', MyFormView.as_view(),name='MyForm'),
    path('my_stopwork/', MyStopWork.as_view(),name='StopWork'),
    path('violation_memo/', MyViolationMemo.as_view(),name='ViolationMemo'),
    path('my_incident_form/', MyIncidentForm.as_view(),name='my_incident_form'),
    path('parent/', ParentAPI.as_view(),name='Parent'),
    path('child-models/', AllModelsListView.as_view(), name='child-model-list'),
    path('update_status/', UpdateFormStatus.as_view(), name='update_status'),
    path('observation_form/', HSEObservationFormAPI.as_view(), name='observation_form'),
    path('stopWork_form/', StopWorkFormAPI.as_view(), name='stopWork_form'),
    path('violation_form/', ViolationMemoAPI.as_view(), name='violation_form'),
    path('incident_form/', IncidentFormAPI.as_view(), name='incident_form'),
    
    
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
