from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from django.template.response import TemplateResponse
from django.http import HttpResponse
from rest_framework import generics
from django.shortcuts import render


class MyTemplateView(APIView):
    def get(self, request):
        return TemplateResponse(request, "index.html")


class GeneralHSEAPI(APIView):
    def get(self, request):
        obj = GeneralHse.objects.all()
        serializer = GeneralHSESerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)
        entry_id = request.data.get("toBeUpdatedId1")
        general_hse_instance = None

        if entry_id:
            try:
                general_hse_instance = GeneralHse.objects.get(id=entry_id)
            except GeneralHse.DoesNotExist:
                general_hse_instance = None

        if not general_hse_instance:
            parent_instance, created = ParentModel.objects.get_or_create(
                week_number=week_number,
                year=year,
                plant_code=10000,
                defaults={"form_status": 0},
            )
            general_hse_instance = GeneralHse(parent=parent_instance)

        serializer = GeneralHSESerializer(general_hse_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            instance.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return render(request, "index.html")

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)
        entry_id = request.data.get("toBeUpdatedId2")
        hse_training_instance = None

        if entry_id:
            try:
                hse_training_instance = HSETrainingsModel.objects.get(id=entry_id)
            except HSETrainingsModel.DoesNotExist:
                hse_training_instance = None

        if not hse_training_instance:
            parent_instance, created = ParentModel.objects.get_or_create(
                week_number=week_number,
                year=year,
                plant_code=10000,
                defaults={"form_status": 0},
            )
            hse_training_instance = HSETrainingsModel(parent=parent_instance)

        serializer = HSETrainingsSerializer(hse_training_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            instance.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return render(request, "index.html")

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)
        entry_id = request.data.get("toBeUpdatedId3")
        print(request.data)
        print(entry_id)
        hse_observation_instance = None

        if entry_id:
            try:
                hse_observation_instance = HSEObservation.objects.get(id=entry_id)
            except HSEObservation.DoesNotExist:
                hse_observation_instance = None

        if not hse_observation_instance:
            parent_instance, created = ParentModel.objects.get_or_create(
                week_number=week_number,
                year=year,
                plant_code=10000,
                defaults={"form_status": 0},
            )
            hse_observation_instance = HSEObservation(parent=parent_instance)

        serializer = HSEObservationSerializer(hse_observation_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            instance.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return render(request, "index.html")

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)
        entry_id = request.data.get("toBeUpdatedId4")
        management_instance = None

        if entry_id:
            try:
                management_instance = ManagementVisits.objects.get(id=entry_id)

            except ManagementVisits.DoesNotExist:
                management_instance = None

        if not management_instance:
            parent_instance, created = ParentModel.objects.get_or_create(
                week_number=week_number,
                year=year,
                plant_code=10000,
                defaults={"form_status": 0},
            )
            management_instance = ManagementVisits(parent=parent_instance)

        serializer = ManagementSerializer(management_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            instance.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return render(request, "index.html")

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def post(self, request):
        data = request.data
        week_number = data.get("week_number", None)
        year = data.get("year", None)
        entry_id = request.data.get("toBeUpdatedId5")
        incident_instance = None

        parent = ParentModel.objects.filter(
            week_number=week_number, year=year, plant_code=10000
        ).first()
        print(parent)

        if parent:
            generalHse = GeneralHse.objects.filter(parent_id=parent.id).first()
            HseObservation = HSEObservation.objects.filter(parent_id=parent.id).first()
            HseTraining = HSETrainingsModel.objects.filter(parent_id=parent.id).first()
            managementvisits = ManagementVisits.objects.filter(
                parent_id=parent.id
            ).first()
            print(generalHse)
            print(HseObservation)
            print(HseTraining)
            print(managementvisits)

        if (
            not generalHse
            or not HseObservation
            or not HseTraining
            or not managementvisits
        ):
            # return Response(
            #     {"error": "Please fill all the intial form."},
            #     status=status.HTTP_400_BAD_REQUEST,
            # )
              alert_message = "Please fill all the above fields "
              return render(request,'index.html',{'message': alert_message})

        if entry_id:
            try:
                print(entry_id)
                incident_instance = Incidents.objects.get(id=entry_id)

            except Incidents.DoesNotExist:
                incident_instance = None

        if not incident_instance:
            parent_instance, created = ParentModel.objects.update_or_create(
                week_number=week_number,
                year=year,
                plant_code=10000,
                defaults={"form_status": 1},
            )
            incident_instance = Incidents(parent=parent_instance)

        serializer = IncidentsSerializer(incident_instance, data=data)

        if serializer.is_valid():
            instance = serializer.save()
            instance.save()

            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return render(request, "index.html")

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        obj = ParentModel.objects.all()
        serializer = ParentModelSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllModelsListView(generics.ListAPIView):
    serializer_class = GeneralHSESerializer

    def get(self, request):
        week_number = self.request.query_params.get("week_number")
        year = self.request.query_params.get("year")
        plant_code = self.request.query_params.get("plant_code")
        # form_status = self.request.query_params.get('form_status')
        parent = ParentModel.objects.filter(
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
