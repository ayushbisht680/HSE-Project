from rest_framework import serializers
from .serializers import *
from .models import *

class PlantSerializer(serializers.ModelSerializer):

    class Meta:
        model=Plant
        # fields='__all__'
        fields = ['id']  # Add other fields as needed

class HomeScapeSerializer(serializers.ModelSerializer):

    class Meta:
        model=HomeScape
        # fields='__all__'
        fields = ['cluster']  

class WarehouseSerializer(serializers.ModelSerializer):

    class Meta:
        model=Warehouse
        # fields='__all__'
        fields = ['code'] 

class HSESegmentSerializer(serializers.ModelSerializer):
     
     class Meta:
        model=HSESegment
        fields='__all__'




class GeneralHSESerializer(serializers.ModelSerializer):

    class Meta:
        model=GeneralHse
        fields='__all__'

    
    
    
class HSETrainingsSerializer(serializers.ModelSerializer):
    class Meta:
        model=HSETraining
        fields='__all__'

    

class HSEObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=HSEObservation
        fields='__all__'

 
    
class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model=ManagementVisit
        fields='__all__'


class IncidentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Incidents
        fields='__all__'
    
    

class HSESerializer(serializers.ModelSerializer):
    class Meta:
        model = HSE
        fields = '__all__'
        



class SubObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubObservation
        fields='__all__'


class StopWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model=StopWork
        fields='__all__'


class ViolationMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model=ViolationMemo
        fields='__all__'
        

class SubIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubIncident
        fields='__all__'






 



    








        
        