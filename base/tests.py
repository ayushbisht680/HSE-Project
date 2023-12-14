from django.test import TestCase
from .models import *
from app.models import *


class PlantModelTest(TestCase):
    def setUp(self):
        self.plant_instance = Plant.objects.create(
            id=1,
            name='Test Plant',
            latitude=12.345,
            longitude=67.890,
            pincode=12345,
            city='Test City',
            state='Test State',
            country='Test Country',
            address='Test Address',
        )

    def test_model_str_method(self):
        expected_str = f' Plant- ID: {self.plant_instance.id}'
        self.assertEqual(str(self.plant_instance), expected_str)
 


    def test_model_fields(self):
        self.assertEqual(self.plant_instance.name, 'Test Plant')
        self.assertEqual(self.plant_instance.latitude, 12.345)


class HomeScapeModelTest(TestCase):
    def setUp(self):
        self.homescape_instance = HomeScape.objects.create(cluster='Test Cluster')

    def test_model_str_method(self):
        expected_str = f" Cluster {self.homescape_instance.cluster}"
        self.assertEqual(str(self.homescape_instance), expected_str)

    def test_model_fields(self):
        self.assertEqual(self.homescape_instance.cluster, 'Test Cluster')


class WarehouseModelTest(TestCase):
    def setUp(self):
        self.warehouse_instance = Warehouse.objects.create(code='Test Code')

    def test_model_str_method(self):
        expected_str = f" Warehouse {self.warehouse_instance.code}"
        self.assertEqual(str(self.warehouse_instance), expected_str)

    def test_model_fields(self):
        self.assertEqual(self.warehouse_instance.code, 'Test Code')


        







