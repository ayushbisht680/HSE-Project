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
    path('parent/', ParentAPI.as_view(),name='Parent'),
    path('child-models/', AllModelsListView.as_view(), name='child-model-list'),
    
    
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
