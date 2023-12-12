from rest_framework.views import APIView 
from rest_framework.response import Response 
from .models import *
from .serializers import * 
from rest_framework import status
from django.template.response import TemplateResponse  
from django.http import HttpResponse
from rest_framework import generics
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from datetime import datetime, timedelta
from .models import CATEGORY_CHOICES,STATUS_CHOICES,INCIDENT_TYPE_CHOICES,CATEOGRIES

SEGMENTS=[
    ('hawkai','RT(Construction)/RT(O&M)/GM(Construction)/GM(O&M)/OA(Construction)/OA(O&M)'),
    ('homescape','HomeScape'),
    ('warehouse','Warehouse')
]



class TemplateView(APIView):
    def get(self, request):
        context = {
        'segment_choices': SEGMENTS

        }
        return TemplateResponse(request, "index.html",context)
    
class SubObservationView(APIView):
    def get(self, request):

        context = {
        'category_choices': CATEGORY_CHOICES,
        'status_choices': STATUS_CHOICES,
        'plant_site':PLANT_SITE,
        'unsafe_act':UNSAFE_ACT

        }
        return TemplateResponse(request, "observation.html",context)
    
class StopWorkView(APIView):
    def get(self, request):

        context = {
        'category_choices': CATEGORY_CHOICES,
        'status_choices': STATUS_CHOICES,
        'plant_site':PLANT_SITE,
        'unsafe_act':UNSAFE_ACT

        }

        return TemplateResponse(request, "stopwork.html",context)

class ViolationMemoView(APIView):
    def get(self, request):

        context = {
        'penalty_choices': STATUS_CHOICES,

        }

        return TemplateResponse(request, "violationForm.html",context)

class IncidentView(APIView):
    def get(self, request):
        

        context = {
        'incident_choices': INCIDENT_TYPE_CHOICES,
        'cateogries':CATEOGRIES,
        'potential_incident':STATUS_CHOICES,
        'plant_site':PLANT_SITE


        }
        return TemplateResponse(request, "incidentForm.html",context)

class ListObservers(APIView):
     def get(self, request):
        return TemplateResponse(request, "mockDrill.html")


class PlantAPI(APIView):

    def get(self, request): 
        obj = Plant.objects.all()
        serializer = PlantSerializer(obj, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)  
    
          
class HomeScapeAPI(APIView):
      def get(self, request): 
        obj = HomeScape.objects.all()
        serializer = HomeScapeSerializer(obj, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK) 
      

class WarehouseAPI(APIView):
      def get(self, request): 
        obj = Warehouse.objects.all()
        serializer = WarehouseSerializer(obj, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)
      

class HSESegmentAPI(APIView):
     def get(self, request): 
        obj = HSESegment.objects.all()
        serializer = HSESegmentSerializer(obj, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)


class GeneralHseAPI(APIView):
    def get(self, request): 
        obj = GeneralHse.objects.all()
        serializer = GeneralHSESerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self, request):
        data = request.data.copy()
        form_submit_date = data.get("formSubmitDate")
        category = data.get('category')
        category_value = data.get('categoryValue')
        general_hse_instance = None
        print(category_value)

        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response({'error': 'User does not have permission'}, status=status.HTTP_403_FORBIDDEN)

        try:
            segment_instance = None

            if category == 'hawkai':
                plant_instance = Plant.objects.filter(id=category_value)
                hawkai_obj= plant_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    plant=hawkai_obj
                )

            elif category == 'homescape':
                homescape_instance = HomeScape.objects.filter(cluster=category_value)
                homescape_obj=homescape_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    homescape=homescape_obj
                )
                

            elif category == 'warehouse':
                warehouse_instance = Warehouse.objects.filter(code=category_value)
                warehouse_obj=warehouse_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    warehouse=warehouse_obj
                )

            # if segment_instance and not segment_instance.segment:
            #     segment_instance.segment = category
            #     segment_instance.save()

            hse_instance, created = HSE.objects.get_or_create(
                hse_segment=segment_instance,
                formSubmittedDate=form_submit_date,
                defaults={"form_status": 0},
            )

            if created:
                hse_instance.created_by = request.user
                hse_instance.save()

            if hse_instance.form_status == 1:
                return Response({'error': 'Form already submitted'}, status=status.HTTP_400_BAD_REQUEST)

            general_hse_instance = GeneralHse(hse=hse_instance)
            serializer = GeneralHSESerializer(general_hse_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.created_by = request.user
                instance.formSubmitted = True
                instance.save()

                return Response({'id': instance.id, 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        data = request.data.copy()
        id = data.get("toBeUpdatedId")

        data['updated_by'] = request.user.id

        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
            print(hse_user)
        except HSEUser.DoesNotExist:
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)

        try:
            existing_instance = GeneralHse.objects.get(id=id)

            if existing_instance.hse.form_status == 1:
                return Response('Form has already been submitted', status=status.HTTP_400_BAD_REQUEST)

        except GeneralHse.DoesNotExist:
            return Response('GeneralHse instance does not exist', status=status.HTTP_400_BAD_REQUEST)


        serializer = GeneralHSESerializer(existing_instance, data=data, partial=True)

        if serializer.is_valid():
            instance = serializer.save()
            instance.updated_at = timezone.now()
            instance.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

       
class HseTrainingsAPI(APIView):
    def get(self, request):
        obj = HSETraining.objects.all()
        serializer = HSETrainingsSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data.copy()
        form_submit_date = data.get("formSubmitDate")
        category = data.get('category')
        category_value = data.get('categoryValue')
        hse_training_instance = None

        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response({'error': 'User does not have permission'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            segment_instance = None

            if category == 'hawkai':
                plant_instance = Plant.objects.filter(id=category_value)
                hawkai_obj= plant_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    plant=hawkai_obj
                )

            elif category == 'homescape':
                homescape_instance = HomeScape.objects.filter(cluster=category_value)
                homescape_obj=homescape_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    homescape=homescape_obj
                )
                

            elif category == 'warehouse':
                warehouse_instance = Warehouse.objects.filter(code=category_value)
                warehouse_obj=warehouse_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    warehouse=warehouse_obj
                )

            if segment_instance and not segment_instance.segment:
                segment_instance.segment = category
                segment_instance.save()

            hse_instance, created = HSE.objects.get_or_create(
                hse_segment=segment_instance,
                formSubmittedDate=form_submit_date,
                defaults={"form_status": 0},
            )

            if created:
                hse_instance.created_by = request.user
                hse_instance.save()

            if hse_instance.form_status == 1:
                return Response({'error': 'Form already submitted'}, status=status.HTTP_400_BAD_REQUEST)

            hse_training_instance = HSETraining(hse=hse_instance)
            serializer = HSETrainingsSerializer(hse_training_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.created_by = request.user
                instance.formSubmitted = True
                instance.save()

                return Response({'id': instance.id, 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def put(self, request):
        data = request.data.copy()
        id = data.get("toBeUpdatedId") 

        data['updated_by'] = request.user.id


        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)
        
        try:
            existing_instance = HSETraining.objects.get(id=id)
            print(existing_instance.hse.form_status)

            if existing_instance.hse.form_status == 1:
                return Response('Form has already been submitted', status=status.HTTP_400_BAD_REQUEST)
            
        except HSETraining.DoesNotExist:
                return Response('HSE Training instance does not exist', status=status.HTTP_400_BAD_REQUEST)

        serializer = HSETrainingsSerializer(existing_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            instance.updated_at = timezone.now()
            instance.formSubmitted = True
            instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class HseObservationAPI(APIView):
    def get(self, request):
        obj = HSEObservation.objects.all()
        serializer = HSEObservationSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        form_submit_date = data.get("formSubmitDate")
        category = data.get('category')
        category_value = data.get('categoryValue')
        hse_observation_instance = None

        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response({'error': 'User does not have permission'}, status=status.HTTP_403_FORBIDDEN)

        try:
            segment_instance = None

            if category == 'hawkai':
                plant_instance = Plant.objects.filter(id=category_value)
                hawkai_obj= plant_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    plant=hawkai_obj
                )

            elif category == 'homescape':
                homescape_instance = HomeScape.objects.filter(cluster=category_value)
                homescape_obj=homescape_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    homescape=homescape_obj
                )
                

            elif category == 'warehouse':
                warehouse_instance = Warehouse.objects.filter(code=category_value)
                warehouse_obj=warehouse_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    warehouse=warehouse_obj
                )

            if segment_instance and not segment_instance.segment:
                segment_instance.segment = category
                segment_instance.save()

            hse_instance, created = HSE.objects.get_or_create(
                hse_segment=segment_instance,
                formSubmittedDate=form_submit_date,
                defaults={"form_status": 0},
            )

            if created:
                hse_instance.created_by = request.user
                hse_instance.save()

            if hse_instance.form_status == 1:
                return Response({'error': 'Form already submitted'}, status=status.HTTP_400_BAD_REQUEST)
            
            hse_observation_instance,created=HSEObservation.objects.get_or_create(
                hse=hse_instance

            )

            serializer = HSEObservationSerializer(hse_observation_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.created_by = request.user
                instance.formSubmitted = True
                instance.save()

                return Response({'id': instance.id, 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    def put(self, request):
        data = request.data.copy()
        id = data.get("toBeUpdatedId") 

        data['updated_by'] = request.user.id

        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)
        
        try:
            existing_instance = HSEObservation.objects.get(id=id)
            print(existing_instance.hse.form_status)

            if existing_instance.hse.form_status == 1:
                return Response('Form has already been submitted', status=status.HTTP_400_BAD_REQUEST)
            
        except HSEObservation.DoesNotExist:
                return Response('HSE Observation instance does not exist', status=status.HTTP_400_BAD_REQUEST)

        serializer = HSEObservationSerializer(existing_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            instance.updated_at = timezone.now()

            instance.formSubmitted = True
            instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ManagementAPI(APIView):
    def get(self, request):
        obj = ManagementVisit.objects.all()
        serializer = ManagementSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 

    def post(self, request):
        data = request.data.copy()
        form_submit_date = data.get("formSubmitDate")
        category = data.get('category')
        category_value = data.get('categoryValue')
        hse_management_instance = None

        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response({'error': 'User does not have permission'}, status=status.HTTP_403_FORBIDDEN)

        try:
            segment_instance = None

            if category == 'hawkai':
                plant_instance = Plant.objects.filter(id=category_value)
                hawkai_obj= plant_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    plant=hawkai_obj
                )

            elif category == 'homescape':
                homescape_instance = HomeScape.objects.filter(cluster=category_value)
                homescape_obj=homescape_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    homescape=homescape_obj
                )
                

            elif category == 'warehouse':
                warehouse_instance = Warehouse.objects.filter(code=category_value)
                warehouse_obj=warehouse_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    warehouse=warehouse_obj
                )


            if segment_instance and not segment_instance.segment:
                segment_instance.segment = category
                segment_instance.save()

            hse_instance, created = HSE.objects.get_or_create(
                hse_segment=segment_instance,
                formSubmittedDate=form_submit_date,
                defaults={"form_status": 0},
            )

            if created:
                hse_instance.created_by = request.user
                hse_instance.save()

            if hse_instance.form_status == 1:
                return Response({'error': 'Form already submitted'}, status=status.HTTP_400_BAD_REQUEST)

            hse_management_instance = ManagementVisit(hse=hse_instance)
            serializer = ManagementSerializer(hse_management_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.created_by = request.user
                instance.formSubmitted = True
                instance.save()

                return Response({'id': instance.id, 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data.copy()
        id = data.get("toBeUpdatedId") 

        data['updated_by'] = request.user.id


        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)
  
        try:
            existing_instance = ManagementVisit.objects.get(id=id)

            if existing_instance.hse.form_status == 1:
                return Response('Form has already been submitted', status=status.HTTP_400_BAD_REQUEST)
            
        except ManagementVisit.DoesNotExist:
                return Response('Management Visits instance does not exist', status=status.HTTP_400_BAD_REQUEST)

        serializer = ManagementSerializer(existing_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            instance.updated_at = timezone.now()

            instance.formSubmitted = True
            instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class IncidentsAPI(APIView):
    def get(self, request):
        obj = Incidents.objects.all()
        serializer = IncidentsSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        # form_submit_date = datetime.strptime(data.get("formSubmitDate"), "%Y-%m-%d")
        # start_range = datetime.strptime(data.get("startRange"), "%Y-%m-%d")
        # end_range = datetime.strptime(data.get("endRange"), "%Y-%m-%d")
        


        # if form_submit_date < start_range or form_submit_date > end_range:
        #    return Response({'Cannot submit the form for this date'}, status=status.HTTP_400_BAD_REQUEST)

    
    def post(self, request):
        data = request.data.copy()
        form_submit_date = data.get("formSubmitDate")
        category = data.get('category')
        category_value = data.get('categoryValue')
        incident_instance = None

        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response({'error': 'User does not have permission'}, status=status.HTTP_403_FORBIDDEN)

        try:
            segment_instance = None

            if category == 'hawkai':
                plant_instance = Plant.objects.filter(id=category_value)
                hawkai_obj= plant_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    plant=hawkai_obj
                )

            elif category == 'homescape':
                homescape_instance = HomeScape.objects.filter(cluster=category_value)
                homescape_obj=homescape_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    homescape=homescape_obj
                )
                

            elif category == 'warehouse':
                warehouse_instance = Warehouse.objects.filter(code=category_value)
                warehouse_obj=warehouse_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    warehouse=warehouse_obj
                )


            if segment_instance and not segment_instance.segment:
                segment_instance.segment = category
                segment_instance.save()

            hse_instance, created = HSE.objects.get_or_create(
                hse_segment=segment_instance,
                formSubmittedDate=form_submit_date,
                defaults={"form_status": 0},
            )

            if created:
                hse_instance.created_by = request.user
                hse_instance.save()

            if hse_instance.form_status == 1:
                return Response({'error': 'Form already submitted'}, status=status.HTTP_400_BAD_REQUEST)

            incident_instance = Incidents(hse=hse_instance)
            serializer = IncidentsSerializer(incident_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.created_by = request.user
                instance.formSubmitted = True
                instance.save()

                return Response({'id': instance.id, 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        data = request.data.copy()
        id = data.get("toBeUpdatedId") 
        data['updated_by'] = request.user.id


        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)

        
        try:
            existing_instance = Incidents.objects.get(id=id)
            print(existing_instance.hse.form_status)

            if existing_instance.hse.form_status == 1:
                return Response('Form has already been submitted', status=status.HTTP_400_BAD_REQUEST)
            
        except Incidents.DoesNotExist:
                return Response('Incident instance does not exist', status=status.HTTP_400_BAD_REQUEST)

        serializer = IncidentsSerializer(existing_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            instance.updated_at = timezone.now()

            instance.formSubmitted = True
            instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class HSEView(APIView):


    def get(self, request): 
        obj = HSE.objects.all()
        serializer = HSESerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  
            

    def post(self, request):
        data = request.data
        start_range = datetime.strptime(data.get("startRange"), "%Y-%m-%d")
        end_range = datetime.strptime(data.get("endRange"), "%Y-%m-%d")
        plant_code=data.get('plant_id')

        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response('User does not have permission', status=status.HTTP_403_FORBIDDEN)

        # print(plant_code)
        # print(start_range)
        # print(end_range)

        hse_queryset = HSE.objects.filter(
            Q(formSubmittedDate__gte=start_range) &
            Q(formSubmittedDate__lte=end_range) &
            Q(plant_code=plant_code)
        )

        # Iterate through each HSE object and check the formSubmitted status of related instances
        general_hse_statuses = []
        hse_trainings_statuses = []
        hse_observation_statuses = []
        management_visits_statuses = []
        incidents_statuses = []

        for hse_object in hse_queryset:
            general_hse_statuses.extend(hse_object.generalhse_set.values_list('formSubmitted', flat=True))
            hse_trainings_statuses.extend(hse_object.hsetrainingsmodel_set.values_list('formSubmitted', flat=True))
            hse_observation_statuses.extend(hse_object.hseobservation_set.values_list('formSubmitted', flat=True))
            management_visits_statuses.extend(hse_object.ManagementVisit_set.values_list('formSubmitted', flat=True))
            incidents_statuses.extend(hse_object.incidents_set.values_list('formSubmitted', flat=True))

        # Check if any formSubmitted is False
        if False in general_hse_statuses or False in hse_trainings_statuses or False in hse_observation_statuses or False in management_visits_statuses or False in incidents_statuses:
            return Response("Form not submitted for all instances", status=status.HTTP_400_BAD_REQUEST)
        
        hse_queryset.update(form_status=1)


        response_data = {
            "general_hse_statuses": general_hse_statuses,
            "hse_trainings_statuses": hse_trainings_statuses,
            "hse_observation_statuses": hse_observation_statuses,
            "management_visits_statuses": management_visits_statuses,
            "incidents_statuses": incidents_statuses,
        }


        return Response(response_data, status=status.HTTP_200_OK)
   

class AllModelsListView(generics.ListAPIView):
    def get(self, request):
        date = request.query_params.get('date', None)
        category = request.query_params.get('category', None)
        category_value = request.query_params.get('category_value', None)
        hse_segment = None

        if category == 'hawkai':
            hse_segment = HSESegment.objects.filter(segment=category)
        elif category == 'homescape':
            hse_segment = HSESegment.objects.filter(segment=category)
        elif category == 'warehouse':
            hse_segment = HSESegment.objects.filter(segment=category)

        if not hse_segment.exists():
            return Response({'error': 'No matching segment found'}, status=400)
        
        hse_segment_obj = hse_segment.first()


        hse_instance=HSE.objects.filter(formSubmittedDate=date,hse_segment=hse_segment_obj)
        if  hse_instance.exists():


            hse_obj=hse_instance.first()
            
            child1_data = hse_obj.generalhse_set.all()
            child2_data = hse_obj.hsetraining_set.all()
            child3_data = hse_obj.hseobservation_set.all()
            child4_data = hse_obj.managementvisit_set.all()
            child5_data = hse_obj.incidents_set.all()

            child1_serializer = GeneralHSESerializer(child1_data, many=True)
            child2_serializer = HSETrainingsSerializer(child2_data, many=True)
            child3_serializer = HSEObservationSerializer(child3_data, many=True)
            child4_serializer = ManagementSerializer(child4_data, many=True)
            child5_serializer = IncidentsSerializer(child5_data, many=True)
        
            response_data = {
                "hse_status": hse_obj.form_status,
                "General HSE": child1_serializer.data,
                "HSE Training": child2_serializer.data,
                "HSE Observation": child3_serializer.data,
                "Management Visits": child4_serializer.data,
                "Incidents": child5_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response('Data does not exists ', status=status.HTTP_404_NOT_FOUND)

                                       
       
class SubObservationAPI(APIView):

    def get(self, request):
        date = request.query_params.get('date', None)
        category = request.query_params.get('category', None)
        category_value = request.query_params.get('category_value', None)

        hse_segment = HSESegment.objects.filter(segment=category).first()

        if not hse_segment:
            return Response({'error': 'No matching segment found'}, status=400)

        hse_instance = HSE.objects.filter(formSubmittedDate=date, hse_segment=hse_segment).first()

        if not hse_instance:
            return Response({'error': 'No matching HSE instances found'}, status=404)

        hse_observation = HSEObservation.objects.filter(hse=hse_instance).first()

        if not hse_observation:
            return Response({'error': 'HSE Observation does not exist'}, status=status.HTTP_404_NOT_FOUND)

        hse_observation_forms = SubObservation.objects.filter(hse_observation=hse_observation)

        if hse_observation_forms.exists():
            serializer = SubObservationSerializer(hse_observation_forms, many=True)
            return Response({'data': serializer.data, 'status': hse_instance.form_status})
        else:
            return Response({"detail": "HSEObservationForm not found", 'form_status': hse_instance.form_status}, status=status.HTTP_404_NOT_FOUND)



    def post(self, request):
        data = request.data.copy()
        form_Submit_date=data.get("formSubmitDate")
        date_value=data.get('date')
        time_value=data.get('time')

        category = data.get('segment_category')
        category_value = data.get('categoryValue')
     
        combined_datetime = datetime.strptime(f'{date_value} {time_value}', '%Y-%m-%d %H:%M')

        fixed_timezone_offset = '+05:30'
        datetime_format = combined_datetime.strftime(f'%Y-%m-%dT%H:%M:%S{fixed_timezone_offset}')

        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response({'error': 'User does not have permission'}, status=status.HTTP_403_FORBIDDEN)

       
        try:
            segment_instance = None

            if category == 'hawkai':
                plant_instance = Plant.objects.filter(id=category_value)
                hawkai_obj= plant_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    plant=hawkai_obj
                )

            elif category == 'homescape':
                homescape_instance = HomeScape.objects.filter(cluster=category_value)
                homescape_obj=homescape_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    homescape=homescape_obj
                )
                

            elif category == 'warehouse':
                warehouse_instance = Warehouse.objects.filter(code=category_value)
                warehouse_obj=warehouse_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    warehouse=warehouse_obj
                )


            if segment_instance and not segment_instance.segment:
                segment_instance.segment = category
                segment_instance.save()

            hse_instance, created = HSE.objects.get_or_create(
                hse_segment=segment_instance,
                formSubmittedDate=form_Submit_date,
                defaults={"form_status": 0},
            )

            if created:
                hse_instance.created_by = request.user
                hse_instance.save()

            if hse_instance.form_status == 1:
                return Response({'error': 'Form already submitted'}, status=status.HTTP_400_BAD_REQUEST)
            
            hse_observation = HSEObservation.objects.get_or_create(hse=hse_instance,submittedDate=form_Submit_date)

            if not hse_observation:
                hse_observation = HSEObservation(hse=hse_instance,submittedDate=form_Submit_date)
                hse_observation.save()

            data['observation_datetime']=datetime_format
            data['created_by']=request.user.id
            data['hse_observation']=hse_observation[0].id

            serializer = SubObservationSerializer(data=data)

            if serializer.is_valid():
                hse_observation_form =serializer.save()
               

                return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)


        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StopWorkAPI(APIView):

    def get(self, request):
        date = request.query_params.get('date', None)
        category = request.query_params.get('category', None)
        category_value = request.query_params.get('category_value', None)

        hse_segment = HSESegment.objects.filter(segment=category).first()

        if not hse_segment:
            return Response({'error': 'No matching segment found'}, status=400)

        hse_instance = HSE.objects.filter(formSubmittedDate=date, hse_segment=hse_segment).first()

        if not hse_instance:
            return Response({'error': 'No matching HSE instances found'}, status=404)

        hse_observation = HSEObservation.objects.filter(hse=hse_instance).first()

        if not hse_observation:
            return Response({'error': 'HSE Observation does not exist'}, status=status.HTTP_404_NOT_FOUND)

        hse_observation_forms = StopWork.objects.filter(hse_observation=hse_observation)

        if hse_observation_forms.exists():
            serializer = StopWorkSerializer(hse_observation_forms, many=True)
            return Response({'data': serializer.data, 'status': hse_instance.form_status})
        else:
            return Response({"detail": "StopWork Form not found", 'form_status': hse_instance.form_status}, status=status.HTTP_404_NOT_FOUND)

    
  
    def post(self, request):
        data = request.data.copy()
        form_Submit_date=data.get("formSubmitDate")
        date_value=data.get('date')
        time_value=data.get('time')

        category = data.get('segment_category')
        category_value = data.get('categoryValue')
     
        combined_datetime = datetime.strptime(f'{date_value} {time_value}', '%Y-%m-%d %H:%M')

        fixed_timezone_offset = '+05:30'
        datetime_format = combined_datetime.strftime(f'%Y-%m-%dT%H:%M:%S{fixed_timezone_offset}')

        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response({'error': 'User does not have permission'}, status=status.HTTP_403_FORBIDDEN)

        try:
            segment_instance = None

            if category == 'hawkai':
                plant_instance = Plant.objects.filter(id=category_value)
                hawkai_obj= plant_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    plant=hawkai_obj
                )

            elif category == 'homescape':
                homescape_instance = HomeScape.objects.filter(cluster=category_value)
                homescape_obj=homescape_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    homescape=homescape_obj
                )
                

            elif category == 'warehouse':
                warehouse_instance = Warehouse.objects.filter(code=category_value)
                warehouse_obj=warehouse_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    warehouse=warehouse_obj
                )


            if segment_instance and not segment_instance.segment:
                segment_instance.segment = category
                segment_instance.save()

            hse_instance, created = HSE.objects.get_or_create(
                hse_segment=segment_instance,
                formSubmittedDate=form_Submit_date,
                defaults={"form_status": 0},
            )

            if created:
                hse_instance.created_by = request.user
                hse_instance.save()

            if hse_instance.form_status == 1:
                return Response({'error': 'Form already submitted'}, status=status.HTTP_400_BAD_REQUEST)
            
            hse_observation = HSEObservation.objects.get_or_create(hse=hse_instance,submittedDate=form_Submit_date)

            if not hse_observation:
                hse_observation = HSEObservation(hse=hse_instance,submittedDate=form_Submit_date)
                hse_observation.save()

            data['stopwork_datetime']=datetime_format
            data['created_by']=request.user.id
            data['hse_observation']=hse_observation[0].id

            serializer = StopWorkSerializer(data=data)

            if serializer.is_valid():
                hse_observation_form =serializer.save()
                # hse_observation_form.hse_observation = hse_observation
                # hse_observation_form.save()

                return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)


        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
class ViolationMemoAPI(APIView):

    def get(self, request):
        date = request.query_params.get('date', None)
        category = request.query_params.get('category', None)
        category_value = request.query_params.get('category_value', None)

        hse_segment = HSESegment.objects.filter(segment=category).first()

        if not hse_segment:
            return Response({'error': 'No matching segment found'}, status=400)

        hse_instance = HSE.objects.filter(formSubmittedDate=date, hse_segment=hse_segment).first()

        if not hse_instance:
            return Response({'error': 'No matching HSE instances found'}, status=404)

        hse_observation = HSEObservation.objects.filter(hse=hse_instance).first()

        if not hse_observation:
            return Response({'error': 'HSE Observation does not exist'}, status=status.HTTP_404_NOT_FOUND)

        hse_observation_forms = ViolationMemo.objects.filter(hse_observation=hse_observation)

        if hse_observation_forms.exists():
            serializer = ViolationMemoSerializer(hse_observation_forms, many=True)
            return Response({'data': serializer.data, 'status': hse_instance.form_status})
        else:
            return Response({"detail": "Violation Form not found", 'form_status': hse_instance.form_status}, status=status.HTTP_404_NOT_FOUND)
   

 
        
    def post(self, request):
        data = request.data.copy()
        form_Submit_date=data.get("formSubmitDate")
        date_value=data.get('date')

        category = data.get('segment_category')
        category_value = data.get('categoryValue')
     
      
        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response({'error': 'User does not have permission'}, status=status.HTTP_403_FORBIDDEN)

        try:
            segment_instance = None

            if category == 'hawkai':
                plant_instance = Plant.objects.filter(id=category_value)
                hawkai_obj= plant_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    plant=hawkai_obj
                )

            elif category == 'homescape':
                homescape_instance = HomeScape.objects.filter(cluster=category_value)
                homescape_obj=homescape_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    homescape=homescape_obj
                )
                

            elif category == 'warehouse':
                warehouse_instance = Warehouse.objects.filter(code=category_value)
                warehouse_obj=warehouse_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    warehouse=warehouse_obj
                )


            if segment_instance and not segment_instance.segment:
                segment_instance.segment = category
                segment_instance.save()

            hse_instance, created = HSE.objects.get_or_create(
                hse_segment=segment_instance,
                formSubmittedDate=form_Submit_date,
                defaults={"form_status": 0},
            )

            if created:
                hse_instance.created_by = request.user
                hse_instance.save()

            if hse_instance.form_status == 1:
                return Response({'error': 'Form already submitted'}, status=status.HTTP_400_BAD_REQUEST)
            
            hse_observation = HSEObservation.objects.get_or_create(hse=hse_instance,submittedDate=form_Submit_date)

            if not hse_observation:
                hse_observation = HSEObservation(hse=hse_instance,submittedDate=form_Submit_date)
                hse_observation.save()

            data['stopwork_date']=date_value
            data['created_by']=request.user.id
            data['hse_observation']=hse_observation[0].id

            serializer = ViolationMemoSerializer(data=data)

            if serializer.is_valid():
               hse_observation_form =serializer.save()

            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)


        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class IncidentAPI(APIView):

    def get(self, request):
        date = request.query_params.get('date', None)
        category = request.query_params.get('category', None)
        category_value = request.query_params.get('category_value', None)

        hse_segment = HSESegment.objects.filter(segment=category).first()

        if not hse_segment:
            return Response({'error': 'No matching segment found'}, status=400)

        hse_instance = HSE.objects.filter(formSubmittedDate=date, hse_segment=hse_segment).first()

        if not hse_instance:
            return Response({'error': 'No matching HSE instances found'}, status=404)

        hse_incident = Incidents.objects.filter(hse=hse_instance).first()

        if not hse_incident:
            return Response({'error': 'Incident object does not exist'}, status=status.HTTP_404_NOT_FOUND)

        hse_incident_form = SubIncident.objects.filter(incidents=hse_incident)

        if hse_incident_form.exists():
            serializer = SubIncidentSerializer(hse_incident_form, many=True)
            return Response({'data': serializer.data, 'status': hse_instance.form_status})
        else:
            return Response({"detail": "Incident Form not found", 'form_status': hse_instance.form_status}, status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request):
        data = request.data.copy()
        form_Submit_date=data.get("formSubmitDate")
        date_value=data.get('incident_date')
        time_value=data.get('incident_time')

        category = data.get('segment_category')
        category_value = data.get('categoryValue')
     
        combined_datetime = datetime.strptime(f'{date_value} {time_value}', '%Y-%m-%d %H:%M')

        fixed_timezone_offset = '+05:30'
        datetime_format = combined_datetime.strftime(f'%Y-%m-%dT%H:%M:%S{fixed_timezone_offset}')

        try:
            hse_user = HSEUser.objects.get(user=request.user, hse_permission=True)
        except HSEUser.DoesNotExist:
            return Response({'error': 'User does not have permission'}, status=status.HTTP_403_FORBIDDEN)

       
        try:
            segment_instance = None

            if category == 'hawkai':
                plant_instance = Plant.objects.filter(id=category_value)
                hawkai_obj= plant_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    plant=hawkai_obj
                )

            elif category == 'homescape':
                homescape_instance = HomeScape.objects.filter(cluster=category_value)
                homescape_obj=homescape_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    homescape=homescape_obj
                )
                

            elif category == 'warehouse':
                warehouse_instance = Warehouse.objects.filter(code=category_value)
                warehouse_obj=warehouse_instance.first()

                segment_instance, _ = HSESegment.objects.get_or_create(
                    segment=category,
                    warehouse=warehouse_obj
                )


            if segment_instance and not segment_instance.segment:
                segment_instance.segment = category
                segment_instance.save()

            hse_instance, created = HSE.objects.get_or_create(
                hse_segment=segment_instance,
                formSubmittedDate=form_Submit_date,
                defaults={"form_status": 0},
            )

            if created:
                hse_instance.created_by = request.user
                hse_instance.save()

            if hse_instance.form_status == 1:
                return Response({'error': 'Form already submitted'}, status=status.HTTP_400_BAD_REQUEST)
            
            hse_incident = Incidents.objects.get_or_create(hse=hse_instance,submittedDate=form_Submit_date)

            if not hse_incident:
                hse_incident = Incidents(hse=hse_instance,submittedDate=form_Submit_date)
                hse_incident.save()

            data['incident_datetime']=datetime_format
            data['created_by']=request.user.id
            data['incidents']=hse_incident[0].id

            serializer = SubIncidentSerializer(data=data)

            if serializer.is_valid():
                hse_incident_form =serializer.save()
               

                return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)


        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)






