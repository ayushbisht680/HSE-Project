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



class MyTemplateView(APIView):
    def get(self, request):
        return TemplateResponse(request, "index.html")
    
class MyFormView(APIView):
    def get(self, request):
        return TemplateResponse(request, "observation.html")
    
class MyStopWork(APIView):
    def get(self, request):
        return TemplateResponse(request, "stopwork.html")

class MyViolationMemo(APIView):
    def get(self, request):
        return TemplateResponse(request, "violationForm.html")

class MyIncidentForm(APIView):
    def get(self, request):
        return TemplateResponse(request, "incidentForm.html")

class MyListObservers(APIView):
     def get(self, request):
        return TemplateResponse(request, "mockDrill.html")

class DataTable(APIView):
    def get(self, request):
        return TemplateResponse(request, "dataTable.html")
    



class GeneralHSEAPI(APIView):
    def get(self, request): 
        obj = GeneralHse.objects.all()
        serializer = GeneralHSESerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        plant_code = data.get("plant_id")
        form_Submit_date=data.get("formSubmitDate")
        general_hse_instance = None

        form_submit_date = datetime.strptime(data.get("formSubmitDate"), "%Y-%m-%d")
        start_range = datetime.strptime(data.get("startRange"), "%Y-%m-%d")
        end_range = datetime.strptime(data.get("endRange"), "%Y-%m-%d")
        


        if form_submit_date < start_range or form_submit_date > end_range:
           return Response({'Cannot submit the form for this date'}, status=status.HTTP_400_BAD_REQUEST)


        plant = Plant.objects.filter(id=plant_code).first()

        hse_instance, created = HSE.objects.get_or_create(
            plant_code=plant,
            formSubmittedDate=form_Submit_date,
            defaults={"form_status": 0},
        )

        if hse_instance.form_status == 1:
            return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

        general_hse_instance = GeneralHse(hse=hse_instance)
        serializer = GeneralHSESerializer(general_hse_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            return Response({'id': instance.id, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        

    def put(self, request):
        data = request.data
        plant_code=data.get("plant_id")
        id = data.get("toBeUpdatedId") 
        submitted_date=data.get('submitted_date')
        print(submitted_date)

        
        try:
            existing_instance = GeneralHse.objects.get(id=id)
            print(existing_instance.hse.form_status)

            if existing_instance.hse.form_status == 1:
                return Response('Form has already been submitted', status=status.HTTP_400_BAD_REQUEST)
            
        except GeneralHse.DoesNotExist:
                return Response('GeneralHse instance does not exist', status=status.HTTP_400_BAD_REQUEST)

        serializer = GeneralHSESerializer(existing_instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HSETrainingsAPI(APIView):
    def get(self, request):
        obj = HSETrainingsModel.objects.all()
        serializer = HSETrainingsSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        plant_code = data.get("plant_id")
        hse_training_instance = None
        form_Submit_date=data.get("formSubmitDate")

        form_submit_date = datetime.strptime(data.get("formSubmitDate"), "%Y-%m-%d")
        start_range = datetime.strptime(data.get("startRange"), "%Y-%m-%d")
        end_range = datetime.strptime(data.get("endRange"), "%Y-%m-%d")
        


        if form_submit_date < start_range or form_submit_date > end_range:
           return Response({'Cannot submit the form for this date'}, status=status.HTTP_400_BAD_REQUEST)


        plant = Plant.objects.filter(id=plant_code).first()

        hse_instance, created = HSE.objects.get_or_create(
            plant_code=plant,
            formSubmittedDate=form_Submit_date,
            defaults={"form_status": 0},
        )
        print(hse_instance)

        if hse_instance.form_status == 1:
            return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

        hse_training_instance = HSETrainingsModel(hse=hse_instance)
        print(hse_training_instance)
        serializer = HSETrainingsSerializer(hse_training_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            return Response({'id': instance.id, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def put(self, request):
        data = request.data
        id = data.get("toBeUpdatedId") 

        print(id)
        print("Hello, it's a put request")
        
        try:
            existing_instance = HSETrainingsModel.objects.get(id=id)
            print(existing_instance.hse.form_status)

            if existing_instance.hse.form_status == 1:
                return Response('Form has already been submitted', status=status.HTTP_400_BAD_REQUEST)
            
        except HSETrainingsModel.DoesNotExist:
                return Response('HSE Training instance does not exist', status=status.HTTP_400_BAD_REQUEST)

        serializer = HSETrainingsSerializer(existing_instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class HSEObservationAPI(APIView):
    def get(self, request):
        obj = HSEObservation.objects.all()
        serializer = HSEObservationSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        plant_code = data.get("plant_id")
        form_Submit_date=data.get("formSubmitDate")
        hse_observation_instance = None

        form_submit_date = datetime.strptime(data.get("formSubmitDate"), "%Y-%m-%d")
        start_range = datetime.strptime(data.get("startRange"), "%Y-%m-%d")
        end_range = datetime.strptime(data.get("endRange"), "%Y-%m-%d")
        


        if form_submit_date < start_range or form_submit_date > end_range:
           return Response({'Cannot submit the form for this date'}, status=status.HTTP_400_BAD_REQUEST)

        plant = Plant.objects.filter(id=plant_code).first()

        hse_instance, created = HSE.objects.get_or_create(
            plant_code=plant,
            formSubmittedDate=form_Submit_date,
            defaults={"form_status": 0},
        )

        if hse_instance.form_status == 1:
            return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

        hse_observation_instance = HSEObservation.objects.filter(hse=hse_instance,submittedDate=form_Submit_date).first()

        if not hse_observation_instance:
            hse_observation_instance=HSEObservation(hse=hse_instance)


        serializer = HSEObservationSerializer(hse_observation_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            return Response({'id': instance.id, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def put(self, request):
        data = request.data
        id = data.get("toBeUpdatedId") 
        
        try:
            existing_instance = HSEObservation.objects.get(id=id)
            print(existing_instance.hse.form_status)

            if existing_instance.hse.form_status == 1:
                return Response('Form has already been submitted', status=status.HTTP_400_BAD_REQUEST)
            
        except HSEObservation.DoesNotExist:
                return Response('HSE Observation instance does not exist', status=status.HTTP_400_BAD_REQUEST)

        serializer = HSEObservationSerializer(existing_instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ManagementAPI(APIView):
    def get(self, request):
        obj = ManagementVisits.objects.all()
        serializer = ManagementSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 

    def post(self, request):
        data = request.data
        plant_code = data.get("plant_id")
        management_instance = None
        form_Submit_date=data.get("formSubmitDate")

        form_submit_date = datetime.strptime(data.get("formSubmitDate"), "%Y-%m-%d")
        start_range = datetime.strptime(data.get("startRange"), "%Y-%m-%d")
        end_range = datetime.strptime(data.get("endRange"), "%Y-%m-%d")
        


        if form_submit_date < start_range or form_submit_date > end_range:
           return Response({'Cannot submit the form for this date'}, status=status.HTTP_400_BAD_REQUEST)


        plant = Plant.objects.filter(id=plant_code).first()

        hse_instance, created = HSE.objects.get_or_create(
            plant_code=plant,
            formSubmittedDate=form_Submit_date,

            defaults={"form_status": 0},
        )
        print(hse_instance)

        if hse_instance.form_status == 1:
            return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

        management_instance = ManagementVisits(hse=hse_instance)
        print(management_instance)
        serializer = ManagementSerializer(management_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            return Response({'id': instance.id, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        id = data.get("toBeUpdatedId") 

        print(id)
        print("Hello, it's a put request")
        
        try:
            existing_instance = ManagementVisits.objects.get(id=id)
            print(existing_instance.hse.form_status)

            if existing_instance.hse.form_status == 1:
                return Response('Form has already been submitted', status=status.HTTP_400_BAD_REQUEST)
            
        except ManagementVisits.DoesNotExist:
                return Response('Management Visits instance does not exist', status=status.HTTP_400_BAD_REQUEST)

        serializer = ManagementSerializer(existing_instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class IncidentsAPI(APIView):
    def get(self, request):
        obj = Incidents.objects.all()
        serializer = IncidentsSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        data = request.data
        plant_code = data.get("plant_id")
        incident_instance = None
        form_Submit_date=data.get("formSubmitDate")
        form_submit_date = datetime.strptime(data.get("formSubmitDate"), "%Y-%m-%d")
        start_range = datetime.strptime(data.get("startRange"), "%Y-%m-%d")
        end_range = datetime.strptime(data.get("endRange"), "%Y-%m-%d")
        


        if form_submit_date < start_range or form_submit_date > end_range:
           return Response({'Cannot submit the form for this date'}, status=status.HTTP_400_BAD_REQUEST)


        plant = Plant.objects.filter(id=plant_code).first()

        hse_instance, created = HSE.objects.get_or_create(
            plant_code=plant,
            formSubmittedDate=form_Submit_date,
            defaults={"form_status": 0},
        )
        print(hse_instance)

        if hse_instance.form_status == 1:
            return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

        incident_instance = Incidents.objects.filter(hse=hse_instance,submittedDate=form_Submit_date).first()
        if not incident_instance:

            incident_instance = Incidents(hse=hse_instance)


        serializer = IncidentsSerializer(incident_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            return Response({'id': instance.id, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def put(self, request):
        data = request.data
        id = data.get("toBeUpdatedId") 

        
        try:
            existing_instance = Incidents.objects.get(id=id)
            print(existing_instance.hse.form_status)

            if existing_instance.hse.form_status == 1:
                return Response('Form has already been submitted', status=status.HTTP_400_BAD_REQUEST)
            
        except Incidents.DoesNotExist:
                return Response('Incident instance does not exist', status=status.HTTP_400_BAD_REQUEST)

        serializer = IncidentsSerializer(existing_instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class HSEAPI(APIView):
    def get(self, request):
        obj = HSE.objects.all()
        serializer = HSESerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        start_range = datetime.strptime(data.get("startRange"), "%Y-%m-%d")
        end_range = datetime.strptime(data.get("endRange"), "%Y-%m-%d")

        hse_objects = HSE.objects.filter(
            formSubmittedDate__gte=start_range,
            formSubmittedDate__lte=end_range
        )
        hse_objects.update(form_status=1)
        return Response('Changed the form Status to 1', status=status.HTTP_201_CREATED)


        # return HttpResponseRedirect('/api/my_html')

    

class AllModelsListView(generics.ListAPIView):
    serializer_class = GeneralHSESerializer

    def get(self, request):
        date= request.query_params.get('date', None) 
        
        child1_data = GeneralHse.objects.filter(submittedDate=date)
        child2_data = HSETrainingsModel.objects.filter(submittedDate=date)
        child3_data = HSEObservation.objects.filter(submittedDate=date)
        child4_data = ManagementVisits.objects.filter(submittedDate=date)
        child5_data = Incidents.objects.filter(submittedDate=date)
            

        child1_serializer = GeneralHSESerializer(child1_data, many=True)
        child2_serializer = HSETrainingsSerializer(child2_data, many=True)
        child3_serializer = HSEObservationSerializer(child3_data, many=True)
        child4_serializer = ManagementSerializer(child4_data, many=True)
        child5_serializer = IncidentsSerializer(child5_data, many=True)
            
            

        response_data = {
                "General HSE": child1_serializer.data,
                "HSE Training": child2_serializer.data,
                "HSE Observation": child3_serializer.data,
                "Management Visits": child4_serializer.data,
                "Incidents": child5_serializer.data,

            }

        return Response(response_data)


       
class HSEObservationFormAPI(APIView):

    def get(self, request):
        plant_code =self.request.query_params.get("plant_code")
        form_Submit_date=self.request.query_params.get("formSubmitDate")

        hse = HSE.objects.filter(formSubmittedDate=form_Submit_date,plant_code=plant_code).first()

    
        if hse:                
            hse_observation = HSEObservation.objects.filter(hse=hse).first()
            
            if hse_observation:
                hse_observation_forms = HSEObservationForm.objects.filter(hse_observation=hse_observation)

                if hse_observation_forms:
                    serializer = HSEObservationFormSerializer(hse_observation_forms, many=True)

                    return Response({'data':serializer.data,'status':hse.form_status})
                else:
                    return Response({"detail": "HSEObservationForm not found",'form_status':hse.form_status}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "HSEObservation not found",'form_status':hse.form_status}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "hse data not found"}, status=status.HTTP_404_NOT_FOUND)



    def post(self, request):
        data = request.data
        plant_code = data.get("plant_id")
        form_Submit_date=data.get("formSubmitDate")

        print(form_Submit_date)

        plant = Plant.objects.filter(id=plant_code).first()

        hse = HSE.objects.filter(formSubmittedDate=form_Submit_date,plant_code=plant_code).first()

        if not hse:
            hse_instance, created = HSE.objects.update_or_create(
                plant_code=plant,
                formSubmittedDate=form_Submit_date,
                defaults={"form_status": 0},
            )

        hse = HSE.objects.filter(formSubmittedDate=form_Submit_date,plant_code=plant_code).first()

        hse_observation = HSEObservation.objects.filter(hse=hse,submittedDate=form_Submit_date).first()

        if not hse_observation:
            # check if my this line of code is correct
            hse_observation = HSEObservation(hse=hse,submittedDate=form_Submit_date)
            hse_observation.save()

        serializer = HSEObservationFormSerializer(data=data)

        if serializer.is_valid():
            hse_observation_form = serializer.save()
            hse_observation_form.hse_observation = hse_observation
            hse_observation_form.save()

            
            redirect_url = f"/api/observation_form_/?date={form_Submit_date}"
            # redirect_url = f"/api/my_html/?date={form_Submit_date}"

            # return HttpResponseRedirect(redirect_url)
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class StopWorkFormAPI(APIView):

    def get(self, request):
        plant_code = self.request.query_params.get("plant_code")
        form_Submit_date=self.request.query_params.get("formSubmitDate")

        hse = HSE.objects.filter(formSubmittedDate=form_Submit_date,plant_code=plant_code).first()
    
        if hse:
            hse_observation = HSEObservation.objects.filter(hse=hse).first()
            
            if hse_observation:
                stop_work_forms = StopWorkForm.objects.filter(hse_observation=hse_observation)

                if stop_work_forms:
                    serializer = StopWorkFormSerializer(stop_work_forms, many=True)

                    return Response({'data':serializer.data,'status':hse.form_status})
                else:
                    return Response({"detail": "StopWork Form not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "HSEObservation not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "hse data not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        data = request.data
        plant_code = data.get("plant_id")
        form_Submit_date=data.get("formSubmitDate")
        print(form_Submit_date)

        plant = Plant.objects.filter(id=plant_code).first()

        hse = HSE.objects.filter(formSubmittedDate=form_Submit_date,plant_code=plant_code).first()

        if not hse:
            hse_instance, created = HSE.objects.update_or_create(
                plant_code=plant,
                formSubmittedDate=form_Submit_date,
                defaults={"form_status": 0},
            )

        hse = HSE.objects.filter(formSubmittedDate=form_Submit_date,plant_code=plant_code).first()

        hse_observation = HSEObservation.objects.filter(hse=hse,submittedDate=form_Submit_date).first()

        if not hse_observation:
            hse_observation = HSEObservation(hse=hse,submittedDate=form_Submit_date)
            hse_observation.save()

        serializer = StopWorkFormSerializer(data=data)

        if serializer.is_valid():
            hse_observation_form = serializer.save()
            hse_observation_form.hse_observation = hse_observation
            hse_observation_form.save()

            
            redirect_url = f"/api/stopwork_form_/?date={form_Submit_date}"
            # return HttpResponseRedirect(redirect_url)
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    
class ViolationMemoAPI(APIView):

    def get(self, request):
        plant_code = self.request.query_params.get("plant_code")
        form_Submit_date=self.request.query_params.get("formSubmitDate")

        hse = HSE.objects.filter(formSubmittedDate=form_Submit_date,plant_code=plant_code).first()
    
        if hse:
            hse_observation = HSEObservation.objects.filter(hse=hse).first()
            
            if hse_observation:
                stop_work_forms = ViolationMemoForm.objects.filter(hse_observation=hse_observation)

                if stop_work_forms:
                    serializer = ViolationFormSerializer(stop_work_forms, many=True)

                    return Response({'data':serializer.data,'status':hse.form_status})
                else:
                    return Response({"detail": "Violation Form not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "HSEObservation not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "hse data not found"}, status=status.HTTP_404_NOT_FOUND)
   

    def post(self, request):
        data = request.data
        plant_code = data.get("plant_id")
        form_Submit_date=data.get("formSubmitDate")

        plant = Plant.objects.filter(id=plant_code).first()

        hse = HSE.objects.filter(formSubmittedDate=form_Submit_date,plant_code=plant_code).first()

        if not hse:
            hse_instance, created = HSE.objects.update_or_create(
                plant_code=plant,
                formSubmittedDate=form_Submit_date,
                defaults={"form_status": 0},
            )

        hse = HSE.objects.filter(formSubmittedDate=form_Submit_date,plant_code=plant_code).first()

        hse_observation = HSEObservation.objects.filter(hse=hse,submittedDate=form_Submit_date).first()

        if not hse_observation:
            hse_observation = HSEObservation(hse=hse,submittedDate=form_Submit_date)
            hse_observation.save()

        serializer = ViolationFormSerializer(data=data)

        if serializer.is_valid():
            hse_observation_form = serializer.save()
            hse_observation_form.hse_observation = hse_observation
            hse_observation_form.save()

            
            redirect_url = f"/api/violation_memo_/?date={form_Submit_date}"
            # return HttpResponseRedirect(redirect_url)
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        

class IncidentFormAPI(APIView):

    def get(self, request):
        plant_code = self.request.query_params.get("plant_code")
        form_Submit_date=self.request.query_params.get("formSubmitDate")

        hse = HSE.objects.filter(formSubmittedDate=form_Submit_date,plant_code=plant_code).first()
    
        if hse:
            incident = Incidents.objects.filter(hse=hse).first()
            
            if incident:
                incident_form = IncidentForm.objects.filter(incidents=incident)

                if incident_form:
                    serializer = IncidentFormSerializer(incident_form, many=True)

                    return Response({'data':serializer.data,'status':hse.form_status})
                else:
                    return Response({"detail": "Incident Form not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "Incident Object  not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Incident data not found"}, status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request):
        data = request.data
        plant_code = data.get("plant_id")
        form_Submit_date=data.get("formSubmitDate")

        plant = Plant.objects.filter(id=plant_code).first()


        hse = HSE.objects.filter(formSubmittedDate=form_Submit_date,plant_code=plant_code).first()

        if not hse:
            hse_instance, created = HSE.objects.update_or_create(
                plant_code=plant,
                formSubmittedDate=form_Submit_date,
                defaults={"form_status": 0},
            )

        hse = HSE.objects.filter(formSubmittedDate=form_Submit_date,plant_code=plant_code).first()
        hse_incident = Incidents.objects.filter(hse=hse,submittedDate=form_Submit_date).first()

        if not hse_incident:
            hse_incident = Incidents(hse=hse,submittedDate=form_Submit_date)
            hse_incident.save()

        serializer = IncidentFormSerializer(data=data)

        if serializer.is_valid():
            hse_incident_from = serializer.save()
            hse_incident_from.incidents = hse_incident
            hse_incident_from.save()

            redirect_url = f"/api/incident_form_/?date={form_Submit_date}"

            # return HttpResponseRedirect(redirect_url)
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







