from django.db import models

class tbl_ReturnReason(models.Model):
    return_id = models.AutoField(primary_key=True)
    return_reason = models.CharField(max_length=30)

    class Meta:
        db_table = '[tbl_ReturnReason]'
   

class tbl_ReturnFeedbackSubmission(models.Model):
    date_of_return=models.DateField()
    market_place = models.CharField(max_length=100)
    return_item_id = models.CharField(max_length=100)
    order_reference = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    return_id = models.BigIntegerField()
    customer_details = models.CharField(max_length=100)
    reason_description = models.TextField()
    is_deleted=models.BooleanField()

    class Meta:
        db_table = '[tbl_ReturnFeedbackSubmission]'
   


 
