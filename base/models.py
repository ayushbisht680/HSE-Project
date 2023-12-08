from django.db import models

class Plant(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Plant code')
    name = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200,  null=True, blank=True)
    country = models.CharField(max_length=200,null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Plant" 
        verbose_name_plural = "Plant"


    def __str__(self):
        return f" Plant- ID: {self.id}"
    

class HomeScape(models.Model):
    cluster = models.CharField(max_length=20)

    class Meta:
        verbose_name = "HomeScape" 
        verbose_name_plural = "HomeScape"
       
    def __str__(self):
        return f" {self.id}, Cluster {self.cluster}"



class Warehouse(models.Model):
    code = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Warehouse" 
        verbose_name_plural = "Warehouse"
  
    def __str__(self):
        return f" {self.id}, Warehouse Code {self.code}"

 

