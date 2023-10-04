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



 



    








        
        