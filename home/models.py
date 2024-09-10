from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Teachers(models.Model):
    faculty_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

class Students(models.Model):
    reg_no = models.IntegerField(primary_key=True)
    supervisor_id = models.IntegerField()
    student_name = models.CharField(max_length=50)
    #honor_student = models.CharField(max_length=5)

class Marks(models.Model):
    reg_no = models.IntegerField()
    subject_id = models.CharField(max_length=20)
    subject_name = models.CharField(max_length=20)
    marks = models.IntegerField()

@receiver(pre_delete, sender=Students)
def delete_student_marks(sender, instance, **kwargs):
    Marks.objects.filter(reg_no=instance.reg_no).delete()