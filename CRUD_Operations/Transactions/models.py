from django.db import models


class Employees(models.Model):
    """
    Model class for a set of employees.
    """
    EMPLOYEE_ID = models.IntegerField(primary_key=True)
    FIRST_NAME = models.CharField(max_length=50, null=False)
    LAST_NAME = models.CharField(max_length=50, null=False)
    EMAIL = models.CharField(max_length=255, null=False)
    PHONE_NUMBER = models.CharField(max_length=20, null=False)
    HIRE_DATE = models.DateField(null=False)
    JOB_ID = models.CharField(max_length=20, null=False)
    SALARY = models.IntegerField(null=False)
    COMMISSION_PCT = models.TextField(null=True)
    MANAGER_ID = models.IntegerField(null=True)
    DEPARTMENT_ID = models.IntegerField(null=True)
