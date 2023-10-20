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
    
    # def post(self, request):
    #     data = request.data
    #     week_number = data.get("week_number", None)
    #     year = data.get("year", None)
    #     entry_id = request.data.get("toBeUpdatedId1")
    #     general_hse_instance = None

    #     plant = Plant.objects.filter(id=10000).first()
    #     hse = HSE.objects.filter(week_number=week_number, year=year).first()

    #     if hse:
    #         if hse.form_status == 1:
    #             return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

    #         if entry_id:
    #             try:
    #                 general_hse_instance = GeneralHse.objects.get(id=entry_id)
    #             except GeneralHse.DoesNotExist:
    #                 general_hse_instance = None

    #         if not general_hse_instance:
    #             parent_instance, created = HSE.objects.update_or_create(
    #                 week_number=week_number,
    #                 year=year,
    #                 plant_code=plant,
    #                 defaults={"form_status": 0},
    #             )
    #             general_hse_instance = GeneralHse(parent=parent_instance)

    #         serializer = GeneralHSESerializer(general_hse_instance, data=data)
    #         if serializer.is_valid():
    #             instance = serializer.save()
    #             instance.save()
    #             return HttpResponseRedirect('/api/my_html')

    #     else:
    #         parent_instance, created = HSE.objects.get_or_create(
    #             week_number=week_number,
    #             year=year,
    #             plant_code=plant,
    #             defaults={"form_status": 0},
    #         )
    #         general_hse_instance = GeneralHse(parent=parent_instance)

    #     serializer = GeneralHSESerializer(general_hse_instance, data=data)

    #     if serializer.is_valid():
    #         instance = serializer.save()
    #         instance.save()
    #         return HttpResponseRedirect('/api/my_html')


    #     return Response('HSE object does not exist', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)
        general_hse_instance = None

        plant = Plant.objects.filter(id=10000).first()
        hse = HSE.objects.filter(week_number=week_number, year=year).first()

        if hse:
            if hse.form_status == 1:
                return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

            existing_instance = GeneralHse.objects.filter(parent=hse).first()

            if existing_instance:
                existing__id = existing_instance.id
                print(' ID:', existing__id)

                serializer = GeneralHSESerializer(existing_instance, data=data)

            else:
                parent_instance, created = HSE.objects.update_or_create(
                    week_number=week_number,
                    year=year,
                    plant_code=plant,
                    defaults={"form_status": 0},
                )
                general_hse_instance = GeneralHse(parent=parent_instance)
                print('Creating a new  instance:', general_hse_instance)

                serializer = GeneralHSESerializer(general_hse_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.save()
                return HttpResponseRedirect('/api/my_html')

        else:
            parent_instance, created = HSE.objects.update_or_create(
                week_number=week_number,
                year=year,
                plant_code=plant,
                defaults={"form_status": 0},
            )
            general_hse_instance = GeneralHse(parent=parent_instance)

            serializer = GeneralHSESerializer(general_hse_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.save()
                return HttpResponseRedirect('/api/my_html')

        return Response('HSE object does not exist', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        serializer = GeneralHSESerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        obj = GeneralHse.objects.get(id=data["id"])
        serializer = GeneralHSESerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        obj = GeneralHse.objects.get(id=data["id"])
        obj.delete()
        return Response({"message": "Person deleted successfully"})


class HSETrainingsAPI(APIView):
    def get(self, request):
        obj = HSETrainingsModel.objects.all()
        serializer = HSETrainingsSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     data = request.data
    #     week_number = data.get("week_number", None)
    #     year = data.get("year", None)
    #     entry_id = request.data.get("toBeUpdatedId2")
    #     hse_training_instance = None

    #     plant = Plant.objects.filter(id=10000).first()
    #     hse = HSE.objects.filter(week_number=week_number, year=year).first()

    #     if hse:
    #         if hse.form_status == 1:
    #             return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

    #         if entry_id:
    #             try:
    #                 hse_training_instance = HSETrainingsModel.objects.get(id=entry_id)
    #             except HSETrainingsModel.DoesNotExist:
    #                 hse_training_instance = None

    #         if not hse_training_instance:
    #             parent_instance, created = HSE.objects.update_or_create(
    #                 week_number=week_number,
    #                 year=year,
    #                 plant_code=plant,
    #                 defaults={"form_status": 0},
    #             )
    #             hse_training_instance = HSETrainingsModel(parent=parent_instance)

    #         serializer = HSETrainingsSerializer(hse_training_instance, data=data)
    #         if serializer.is_valid():
    #             instance = serializer.save()
    #             instance.save()
    #             return HttpResponseRedirect('/api/my_html')

    #     else:
    #         parent_instance, created = HSE.objects.get_or_create(
    #             week_number=week_number,
    #             year=year,
    #             plant_code=plant,
    #             defaults={"form_status": 0},
    #         )
    #         hse_training_instance = HSETrainingsModel(parent=parent_instance)

    #     serializer = HSETrainingsSerializer(hse_training_instance, data=data)
        
    #     if serializer.is_valid():
    #         instance = serializer.save()
    #         instance.save()
    #         return HttpResponseRedirect('/api/my_html')


    #     return Response('HSE object does not exist', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)
        hse_training_instance = None

        plant = Plant.objects.filter(id=10000).first()
        hse = HSE.objects.filter(week_number=week_number, year=year).first()

        if hse:
            if hse.form_status == 1:
                return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

            existing_instance = HSETrainingsModel.objects.filter(parent=hse).first()

            if existing_instance:
                existing__id = existing_instance.id
                print(' ID:', existing__id)

                serializer = HSETrainingsSerializer(existing_instance, data=data)

            else:
                parent_instance, created = HSE.objects.update_or_create(
                    week_number=week_number,
                    year=year,
                    plant_code=plant,
                    defaults={"form_status": 0},
                )
                hse_training_instance = HSETrainingsModel(parent=parent_instance)
                print('Creating a new  instance:', hse_training_instance)

                serializer = HSETrainingsSerializer(hse_training_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.save()
                return HttpResponseRedirect('/api/my_html')

        else:
            parent_instance, created = HSE.objects.update_or_create(
                week_number=week_number,
                year=year,
                plant_code=plant,
                defaults={"form_status": 0},
            )
            hse_training_instance = HSETrainingsModel(parent=parent_instance)

            serializer = HSETrainingsSerializer(hse_training_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.save()
                return HttpResponseRedirect('/api/my_html')

        return Response('HSE object does not exist', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        serializer = HSETrainingsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        obj = HSETrainingsModel.objects.get(id=data["id"])
        serializer = HSETrainingsSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        obj = HSETrainingsModel.objects.get(id=data["id"])
        obj.delete()
        return Response({"message": "Person deleted successfully"})


class HSEObservationAPI(APIView):
    def get(self, request):
        obj = HSEObservation.objects.all()
        serializer = HSEObservationSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     data = request.data
    #     week_number = data.get("week_number", None)
    #     year = data.get("year", None)
    #     entry_id = request.data.get("toBeUpdatedId3")
    #     observation_instance = None

    #     plant = Plant.objects.filter(id=10000).first()
    #     hse = HSE.objects.filter(week_number=week_number, year=year).first()

    #     if hse:
    #         if hse.form_status == 1:
    #             return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

    #         if entry_id:
    #             try:
    #                 observation_instance = HSEObservation.objects.get(id=entry_id)
    #             except HSEObservation.DoesNotExist:
    #                 observation_instance = None

    #         if not observation_instance:
    #             parent_instance, created = HSE.objects.update_or_create(
    #                 week_number=week_number,
    #                 year=year,
    #                 plant_code=plant,
    #                 defaults={"form_status": 0},
    #             )
    #             observation_instance = HSEObservation(parent=parent_instance)

    #         serializer = HSEObservationSerializer(observation_instance, data=data)
    #         if serializer.is_valid():
    #             instance = serializer.save()
    #             instance.save()
    #             return HttpResponseRedirect('/api/my_html')

    #     else:
    #         parent_instance, created = HSE.objects.update_or_create(
    #             week_number=week_number,
    #             year=year,
    #             plant_code=plant,
    #             defaults={"form_status": 0},
    #         )
    #         observation_instance = HSEObservation(parent=parent_instance)

    #     serializer = HSEObservationSerializer(observation_instance, data=data)
        
    #     if serializer.is_valid():
    #         instance = serializer.save()
    #         instance.save()
    #         return HttpResponseRedirect('/api/my_html')


    #     return Response('HSE object does not exist', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)
        hse_observation = None

        plant = Plant.objects.filter(id=10000).first()
        hse = HSE.objects.filter(week_number=week_number, year=year).first()

        if hse:
            if hse.form_status == 1:
                return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

            # Check if an incident object already exists
            existing_observation = HSEObservation.objects.filter(parent=hse).first()

            if existing_observation:
                # An incident object already exists; you can get its ID
                existing_observation_id = existing_observation.id
                print('Incident ID:', existing_observation_id)

                # Use existing_incident_id or perform any updates on the existing incident
                serializer = HSEObservationSerializer(existing_observation, data=data)

            else:
                # No existing incident object, create a new one
                parent_instance, created = HSE.objects.update_or_create(
                    week_number=week_number,
                    year=year,
                    plant_code=plant,
                    defaults={"form_status": 0},
                )
                hse_observation = HSEObservation(parent=parent_instance)
                print('Creating a new incident instance:', hse_observation)

                serializer = IncidentsSerializer(hse_observation, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.save()
                return HttpResponseRedirect('/api/my_html')

        else:
            parent_instance, created = HSE.objects.update_or_create(
                week_number=week_number,
                year=year,
                plant_code=plant,
                defaults={"form_status": 0},
            )
            hse_observation = HSEObservation(parent=parent_instance)

            serializer = HSEObservationSerializer(hse_observation, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.save()
                return HttpResponseRedirect('/api/my_html')

        return Response('HSE object does not exist', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        serializer = HSEObservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        obj = HSEObservation.objects.get(id=data["id"])
        serializer = HSEObservationSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        obj = HSEObservation.objects.get(id=data["id"])
        obj.delete()
        return Response({"message": "Person deleted successfully"})


class ManagementAPI(APIView):
    def get(self, request):
        obj = ManagementVisits.objects.all()
        serializer = ManagementSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     data = request.data
    #     week_number = data.get("week_number", None)
    #     year = data.get("year", None)
    #     entry_id = request.data.get("toBeUpdatedId4")
    #     management_visits_instance = None

    #     plant = Plant.objects.filter(id=10000).first()
    #     hse = HSE.objects.filter(week_number=week_number, year=year).first()

    #     if hse:
    #         if hse.form_status == 1:
    #             return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

    #         if entry_id:
    #             try:
    #                 management_visits_instance = ManagementVisits.objects.get(id=entry_id)
    #             except ManagementVisits.DoesNotExist:
    #                 management_visits_instance = None

    #         if not management_visits_instance:
    #             parent_instance, created = HSE.objects.update_or_create(
    #                 week_number=week_number,
    #                 year=year,
    #                 plant_code=plant,
    #                 defaults={"form_status": 0},
    #             )
    #             management_visits_instance = ManagementVisits(parent=parent_instance)

    #         serializer = ManagementSerializer(management_visits_instance, data=data)
    #         if serializer.is_valid():
    #             instance = serializer.save()
    #             instance.save()
    #             return HttpResponseRedirect('/api/my_html')

    #     else:
    #         parent_instance, created = HSE.objects.get_or_create(
    #             week_number=week_number,
    #             year=year,
    #             plant_code=plant,
    #             defaults={"form_status": 0},
    #         )
    #         management_visits_instance = ManagementVisits(parent=parent_instance)

    #     serializer = ManagementSerializer(management_visits_instance, data=data)
        
    #     if serializer.is_valid():
    #         instance = serializer.save()
    #         instance.save()
    #         return HttpResponseRedirect('/api/my_html')


    #     return Response('HSE object does not exist', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)
        management_instance = None

        plant = Plant.objects.filter(id=10000).first()
        hse = HSE.objects.filter(week_number=week_number, year=year).first()

        if hse:
            if hse.form_status == 1:
                return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

            existing_instance = ManagementVisits.objects.filter(parent=hse).first()

            if existing_instance:
                existing__id = existing_instance.id
                print(' ID:', existing__id)

                serializer = ManagementSerializer(existing_instance, data=data)

            else:
                parent_instance, created = HSE.objects.update_or_create(
                    week_number=week_number,
                    year=year,
                    plant_code=plant,
                    defaults={"form_status": 0},
                )
                management_instance = ManagementVisits(parent=parent_instance)
                print('Creating a new  instance:', management_instance)

                serializer = ManagementSerializer(management_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.save()
                return HttpResponseRedirect('/api/my_html')

        else:
            parent_instance, created = HSE.objects.update_or_create(
                week_number=week_number,
                year=year,
                plant_code=plant,
                defaults={"form_status": 0},
            )
            management_instance = ManagementVisits(parent=parent_instance)

            serializer = ManagementSerializer(management_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.save()
                return HttpResponseRedirect('/api/my_html')

        return Response('HSE object does not exist', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data
        serializer = ManagementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        obj = ManagementVisits.objects.get(id=data["id"])
        serializer = ManagementSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        obj = ManagementVisits.objects.get(id=data["id"])
        obj.delete()
        return Response({"message": "Person deleted successfully"})


class IncidentsAPI(APIView):
    def get(self, request):
        obj = Incidents.objects.all()
        serializer = IncidentsSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # def post(self, request):
    #     data = request.data
    #     week_number = data.get("week_number", None)
    #     year = data.get("year", None)
    #     entry_id = request.data.get("toBeUpdatedId5")
    #     incident_instance = None
    #     print(entry_id)

    #     plant = Plant.objects.filter(id=10000).first()
    #     hse = HSE.objects.filter(week_number=week_number, year=year).first()

    #     if hse:
    #         if hse.form_status == 1:
    #             return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

    #         if entry_id:
    #             try:
    #                 incident_instance = Incidents.objects.get(id=entry_id)
    #                 print('got the id')
    #                 print(incident_instance)
    #             except Incidents.DoesNotExist:
    #                 incident_instance = None

    #         if not incident_instance:
    #             parent_instance, created = HSE.objects.update_or_create(
    #                 week_number=week_number,
    #                 year=year,
    #                 plant_code=plant,
    #                 defaults={"form_status": 0},
    #             )
    #             incident_instance = Incidents(parent=parent_instance)
    #             print('did not got id ')
    #             print(incident_instance)

    #         serializer = IncidentsSerializer(incident_instance, data=data)
    #         if serializer.is_valid():
    #             instance = serializer.save()
    #             instance.save()
    #             return HttpResponseRedirect('/api/my_html')

    #     else:
    #         parent_instance, created = HSE.objects.update_or_create(
    #             week_number=week_number,
    #             year=year,
    #             plant_code=plant,
    #             defaults={"form_status": 0},
    #         )
    #         incident_instance = Incidents(parent=parent_instance)

    #     serializer = IncidentsSerializer(incident_instance, data=data)
        
    #     if serializer.is_valid():
    #         instance = serializer.save()
    #         instance.save()
    #         return HttpResponseRedirect('/api/my_html')


    #     return Response('HSE object does not exist', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)
        incident_instance = None

        plant = Plant.objects.filter(id=10000).first()
        hse = HSE.objects.filter(week_number=week_number, year=year).first()

        if hse:
            if hse.form_status == 1:
                return Response('Form already submitted', status=status.HTTP_400_BAD_REQUEST)

            existing_incident = Incidents.objects.filter(parent=hse).first()

            if existing_incident:
                existing_incident_id = existing_incident.id
                print('Incident ID:', existing_incident_id)

                serializer = IncidentsSerializer(existing_incident, data=data)

            else:
                parent_instance, created = HSE.objects.update_or_create(
                    week_number=week_number,
                    year=year,
                    plant_code=plant,
                    defaults={"form_status": 0},
                )
                incident_instance = Incidents(parent=parent_instance)
                print('Creating a new incident instance:', incident_instance)

                serializer = IncidentsSerializer(incident_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.save()
                return HttpResponseRedirect('/api/my_html')

        else:
            parent_instance, created = HSE.objects.update_or_create(
                week_number=week_number,
                year=year,
                plant_code=plant,
                defaults={"form_status": 0},
            )
            incident_instance = Incidents(parent=parent_instance)

            serializer = IncidentsSerializer(incident_instance, data=data)

            if serializer.is_valid():
                instance = serializer.save()
                instance.save()
                return HttpResponseRedirect('/api/my_html')

        return Response('HSE object does not exist', status=status.HTTP_400_BAD_REQUEST)



    def put(self, request):
        data = request.data
        serializer = IncidentsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def patch(self, request):
        data = request.data
        obj = Incidents.objects.get(id=data["id"])
        serializer = IncidentsSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        data = request.data
        obj = Incidents.objects.get(id=data["id"])
        obj.delete()
        return Response({"message": "Person deleted successfully"})


class ParentAPI(APIView):
    def get(self, request):
        obj = HSE.objects.all()
        serializer = HSESerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        week_number = data.get("week_number")
        year = data.get("year")
        from_status=1

        hse_instance = HSE.objects.get(week_number=week_number, year=year, plant_code=10000)
        hse_instance.form_status = from_status  # Update form_status to 1
        hse_instance.save()  # Save the changes

      
        return HttpResponseRedirect('/api/my_html')

    
    


class AllModelsListView(generics.ListAPIView):
    serializer_class = GeneralHSESerializer

    def get(self, request):
        week_number = self.request.query_params.get("week_number")
        year = self.request.query_params.get("year")
        plant_code = self.request.query_params.get("plant_code")
        # form_status = self.request.query_params.get('form_status')
        parent = HSE.objects.filter(
            week_number=week_number, year=year, plant_code=plant_code
        ).first()
        
       
        if parent:
            child1_data = GeneralHse.objects.filter(parent=parent)
            child2_data = HSETrainingsModel.objects.filter(parent=parent)
            child3_data = HSEObservation.objects.filter(parent=parent)
            child4_data = ManagementVisits.objects.filter(parent=parent)
            child5_data = Incidents.objects.filter(parent=parent)
            

            child1_serializer = GeneralHSESerializer(child1_data, many=True)
            child2_serializer = HSETrainingsSerializer(child2_data, many=True)
            child3_serializer = HSEObservationSerializer(child3_data, many=True)
            child4_serializer = ManagementSerializer(child4_data, many=True)
            child5_serializer = IncidentsSerializer(child5_data, many=True)
            
            

            response_data = {
                "week_number": week_number,
                "year": year,
                "plant_code": plant_code,
                "General HSE": child1_serializer.data,
                "HSE Training": child2_serializer.data,
                "HSE Observation": child3_serializer.data,
                "Management Visits": child4_serializer.data,
                "Incidents": child5_serializer.data,

            }

            return Response(response_data)
        else:
            return Response({"detail": "Parent data not found"}, status=404)



       
class HSEObservationFormAPI(APIView):

    def get(self, request):
        week_number = self.request.query_params.get("week_number")
        year = self.request.query_params.get("year")
        plant_code = self.request.query_params.get("plant_code")

        parent = HSE.objects.filter(week_number=week_number, year=year,plant_code=plant_code).first()
    
        if parent:
            hse_observation = HSEObservation.objects.filter(parent=parent).first()
            
            if hse_observation:
                hse_observation_forms = HSEObservationForm.objects.filter(hse_observation=hse_observation)

                if hse_observation_forms:
                    serializer = HSEObservationFormSerializer(hse_observation_forms, many=True)

                    return Response(serializer.data)
                else:
                    return Response({"detail": "HSEObservationForm not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "HSEObservation not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Parent data not found"}, status=status.HTTP_404_NOT_FOUND)



    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)
        plant = Plant.objects.filter(id=10000).first()

        hse = HSE.objects.filter(week_number=week_number, year=year).first()

        if not hse:
            parent_instance, created = HSE.objects.update_or_create(
                week_number=week_number,
                year=year,
                plant_code=plant,
                defaults={"form_status": 0},
            )

        hse = HSE.objects.filter(week_number=week_number, year=year).first()
        hse_observation = HSEObservation.objects.filter(parent=hse).first()

        if not hse_observation:
            # Create a new instance of HSEObservation with null values
            hse_observation = HSEObservation(parent=hse)
            hse_observation.save()

        # Continue with the code for saving HSEObservationForm
        serializer = HSEObservationFormSerializer(data=data)

        if serializer.is_valid():
            hse_observation_form = serializer.save()
            hse_observation_form.hse_observation = hse_observation
            hse_observation_form.save()

            return HttpResponseRedirect('/api/my_form/')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        

class StopWorkFormAPI(APIView):

    def get(self, request):
        week_number = self.request.query_params.get("week_number")
        year = self.request.query_params.get("year")
        plant_code = self.request.query_params.get("plant_code")

        parent = HSE.objects.filter(week_number=week_number, year=year,plant_code=plant_code).first()
    
        if parent:
            hse_observation = HSEObservation.objects.filter(parent=parent).first()
            
            if hse_observation:
                stop_work_forms = StopWorkForm.objects.filter(hse_observation=hse_observation)

                if stop_work_forms:
                    serializer = StopWorkFormSerializer(stop_work_forms, many=True)

                    return Response(serializer.data)
                else:
                    return Response({"detail": "HSEObservationForm not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "HSEObservation not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Parent data not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)

        hse = HSE.objects.filter(week_number=week_number, year=year).first()

        if hse:
            hse_observation = HSEObservation.objects.filter(parent=hse).first()

            if hse_observation:
                serializer = StopWorkFormSerializer(data=data)

                if serializer.is_valid():
                    stop_work_form = serializer.save()

                    stop_work_form.hse_observation = hse_observation
                    stop_work_form.save()

                    # return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return HttpResponseRedirect('/api/my_stopwork/')

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Create a new instance of HSEObservation with null values
                hse_observation = HSEObservation(parent=hse)
                hse_observation.save()

                # Continue with the code for saving StopWorkForm
                serializer = StopWorkFormSerializer(data=data)

                if serializer.is_valid():
                    stop_work_form = serializer.save()
                    stop_work_form.hse_observation = hse_observation
                    stop_work_form.save()

                    # return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return HttpResponseRedirect('/api/my_stopwork/')
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'HSE object not found for the specified week_number and year.'}, status=status.HTTP_404_NOT_FOUND)

        
    
class ViolationMemoAPI(APIView):

    def get(self, request):
        week_number = self.request.query_params.get("week_number")
        year = self.request.query_params.get("year")
        plant_code = self.request.query_params.get("plant_code")

        parent = HSE.objects.filter(week_number=week_number, year=year,plant_code=plant_code).first()
    
        if parent:
            hse_observation = HSEObservation.objects.filter(parent=parent).first()
            
            if hse_observation:
                violation_memo_forms = ViolationMemoForm.objects.filter(hse_observation=hse_observation)

                if violation_memo_forms:
                    serializer = ViolationFormSerializer(violation_memo_forms, many=True)

                    return Response(serializer.data)
                else:
                    return Response({"detail": "HSEObservationForm not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "HSEObservation not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Parent data not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)

        hse = HSE.objects.filter(week_number=week_number, year=year).first()
        
        if hse:
            hse_observation = HSEObservation.objects.filter(parent=hse).first()

            if hse_observation:
                serializer = ViolationFormSerializer(data=data)

                if serializer.is_valid():
                    violation_memo_form = serializer.save()

                    violation_memo_form.hse_observation = hse_observation
                    violation_memo_form.save()

                    # return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return HttpResponseRedirect('/api/violation_memo/')
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Create a new instance of HSEObservation with null values
                hse_observation = HSEObservation(parent=hse)
                hse_observation.save()

                # Continue with the code for saving ViolationForm
                serializer = ViolationFormSerializer(data=data)

                if serializer.is_valid():
                    violation_memo_form = serializer.save()
                    violation_memo_form.hse_observation = hse_observation
                    violation_memo_form.save()

                    # return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return HttpResponseRedirect('/api/violation_memo/')
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'HSE object not found for the specified week_number and year.'}, status=status.HTTP_404_NOT_FOUND)

        

class IncidentFormAPI(APIView):

    def get(self, request):
        week_number = self.request.query_params.get("week_number")
        year = self.request.query_params.get("year")
        plant_code = self.request.query_params.get("plant_code")

        parent = HSE.objects.filter(week_number=week_number, year=year,plant_code=plant_code).first()
    
        if parent:
            incident = Incidents.objects.filter(parent=parent).first()
            
            if incident:
                incident_form = IncidentForm.objects.filter(incident_instance=incident)

                if incident_form:
                    serializer = IncidentFormSerializer(incident_form, many=True)

                    return Response(serializer.data)
                else:
                    return Response({"detail": "Incidet Form not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "Incident  not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "HSE data not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # def post(self, request):
    #     data = request.data
    #     week_number = data.get("week_number", None)
    #     year = data.get("year", None)

    #     incident= HSE.objects.filter(week_number=week_number, year=year).first()
        
        
    #     if incident:
    #         hse_incident = Incidents.objects.filter(parent=incident).first()
    #         print(hse_incident)

    #         if hse_incident:
    #             serializer = IncidentFormSerializer(data=data)

    #             if serializer.is_valid():
    #                 incident_form = serializer.save()

    #                 incident_form.incident_instance = hse_incident
    #                 incident_form.save()

    #                 # return Response(serializer.data, status=status.HTTP_201_CREATED)
    #                 return HttpResponseRedirect('/api/my_incident_form/')
                  
    #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             hse_incident = Incidents(parent=incident)
    #             hse_incident.save()

    #             # Continue with the code for saving ViolationForm
    #             serializer = IncidentFormSerializer(data=data)

    #             if serializer.is_valid():
    #                 incident_form = serializer.save()
    #                 incident_form.incident_instance = hse_incident
    #                 incident_form.save()

    #                 # return Response(serializer.data, status=status.HTTP_201_CREATED)
    #                 return HttpResponseRedirect('/api/my_incident_form/')
    #             else:
    #                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response({'error': 'HSE object not found for the specified week_number and year.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)
        plant = Plant.objects.filter(id=10000).first()

        hse = HSE.objects.filter(week_number=week_number, year=year).first()

        if not hse:
            parent_instance, created = HSE.objects.update_or_create(
                week_number=week_number,
                year=year,
                plant_code=plant,
                defaults={"form_status": 0},
            )

        hse = HSE.objects.filter(week_number=week_number, year=year).first()
        hse_incident = Incidents.objects.filter(parent=hse).first()

        if not hse_incident:
            # Create a new instance of HSEObservation with null values
            hse_incident = Incidents(parent=hse)
            hse_incident.save()

        # Continue with the code for saving HSEObservationForm
        serializer = IncidentFormSerializer(data=data)

        if serializer.is_valid():
            hse_incident_from = serializer.save()
            hse_incident_from.incident_instance = hse_incident
            hse_incident_from.save()

            return HttpResponseRedirect('/api/my_incident_form/')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







