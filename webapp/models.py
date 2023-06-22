from django.db import models

class CooperativeSociety(models.Model):
    sector_name = models.CharField(max_length=100 , null=True,blank=' ',default='')
    sector_address = models.CharField(max_length=200,null=True,blank=' ',default='')
    sector_state = models.CharField(max_length=50,null=True,blank=' ',default='')
    sector_district = models.CharField(max_length=50,null=True,blank=' ',default='')
    sector_registration_date = models.DateField(null=True,blank=' ',default='')
    sector_area_of_operation = models.CharField(max_length=100,null=True,blank=' ',default='')
    sector_sector_type = models.CharField(max_length=100,null=True,blank=' ',default='')
    
    def __str__(self):
        return self.sector_name
