from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import HSESegment, Plant, HomeScape, Warehouse

class HSESegmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.plant_instance = Plant.objects.create(id='10000')
        self.homescape_instance = HomeScape.objects.create(cluster='Noida')
        self.warehouse_instance = Warehouse.objects.create(code='12344')

        self.hse_segment_with_plant = HSESegment.objects.create(segment='Segment A', plant=self.plant_instance)
        self.hse_segment_with_homescape = HSESegment.objects.create(segment='Segment B', homescape=self.homescape_instance)
        self.hse_segment_with_warehouse = HSESegment.objects.create(segment='Segment C', warehouse=self.warehouse_instance)

    def test_hse_segment_representation(self):
        self.assertEqual(str(self.hse_segment_with_plant), 'Segment A - Plant 1')
        self.assertEqual(str(self.hse_segment_with_homescape), 'Segment B - HomeScape 1')
        self.assertEqual(str(self.hse_segment_with_warehouse), 'Segment C - Warehouse 1')

    def test_hse_segment_api(self):
        url = reverse('hse-segment-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        data = {'segment': 'New Segment', 'plant': self.plant_instance.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HSESegment.objects.filter(segment='New Segment').count(), 1)
