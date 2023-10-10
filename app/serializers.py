from rest_framework import serializers
from .serializers import *
from .models import *


class GeneralHSESerializer(serializers.ModelSerializer):

    class Meta:
        model=GeneralHse
        fields='__all__'
    
    
    
class HSETrainingsSerializer(serializers.ModelSerializer):
    class Meta:
        model=HSETrainingsModel
        fields='__all__'

    

class HSEObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=HSEObservation
        fields='__all__'

 
    
class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model=ManagementVisits
        fields='__all__'


class IncidentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Incidents
        fields='__all__'
    
    

class ParentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentModel
        fields = '__all__'
        

class FinalSubmitSerializer(serializers.ModelSerializer):
     class Meta:
        model = FinalSubmit
        fields = '__all__'

class HSEObservationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model=HSEObservationForm
        fields='__all__'

class StopWorkFormSerializer(serializers.ModelSerializer):
    class Meta:
        model=StopWorkForm
        fields='__all__'

class ViolationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model=ViolationMemoForm
        fields='__all__'

class IncidentFormSerializer(serializers.ModelSerializer):
    class Meta:
        model=IncidentForm
        fields='__all__'




 



    








        
        