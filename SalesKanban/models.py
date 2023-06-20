from django.db import models

class tbl_SalesProjections(models.Model):
    projection_id = models.AutoField(primary_key=True)
    projection_title = models.CharField(max_length=50)
    filter_start_date=models.DateField()
    filter_end_date=models.DateField()
    target_value = models.BigIntegerField()
    class Meta:
        db_table = '[tbl_SalesProjections]'
