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
    path('observation_form_/', MyFormView.as_view(),name='Observation'),
    path('stopwork_form_/', MyStopWork.as_view(),name='StopWork'),
    path('violation_memo_/', MyViolationMemo.as_view(),name='ViolationMemo'),
    path('incident_form_/', MyIncidentForm.as_view(),name='my_incident_form'),
    path('my_observers_form/', MyListObservers.as_view(),name='my_observers_form'),
    path('parent/', ParentAPI.as_view(),name='Parent'),
    path('child-models/', AllModelsListView.as_view(), name='child-model-list'),
    path('observation_form/', HSEObservationFormAPI.as_view(), name='observation_form'),
    path('stopWork_form/', StopWorkFormAPI.as_view(), name='stopWork_form'),
    path('violation_form/', ViolationMemoAPI.as_view(), name='violation_form'),
    path('incident_form/', IncidentFormAPI.as_view(), name='incident_form'),
    path('dataTable/', DataTable.as_view(), name='dataTable'),
    
    
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
