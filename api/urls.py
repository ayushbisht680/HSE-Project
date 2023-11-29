from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('plant/',PlantAPI.as_view(),name='Plant'),
    path('general_hse/',GeneralHseAPI.as_view(),name='General HSE'),
    path('hse_trainingModel/', HseTrainingsAPI.as_view(), name='HSE Trainings'),
    path('hse_observation/', HseObservationAPI.as_view(), name="HSE Observations"),
    path('management_visit/', ManagementAPI.as_view(), name="Management Visits"),
    path('incidents/', IncidentsAPI.as_view(), name="incidents"),
    path('hse/', TemplateView.as_view(),name='HSE'),
    path('observations/', ObservationFormView.as_view(),name='Observations'),
    path('stopworks/', StopWorkFormView.as_view(),name='StopWorks'),
    path('violations/', ViolationMemoFormView.as_view(),name='Violations'),
    path('Incidents/', IncidentFormView.as_view(),name='Incidents'),
    path('my_observers_form/', ListObservers.as_view(),name='my_observers_form'),
    path('parent/', HSEView.as_view(),name='Parent'),
    path('child-models/', AllModelsListView.as_view(), name='child-model-list'),
    path('observation_form/', HSEObservationFormAPI.as_view(), name='observation_form'),
    path('stopWork_form/', StopWorkFormAPI.as_view(), name='stopWork_form'),
    path('violation_form/', ViolationMemoAPI.as_view(), name='violation_form'),
    path('incident_form/', IncidentFormAPI.as_view(), name='incident_form'),
    
    
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
