import csv
from datetime import datetime
from django.test import TestCase
from .models import Employees


class TestTransactions(TestCase):
    """
    Test class to test all CRUD operations.
    """
    @classmethod
    def setUpTestData(cls):
        with open("E:\msf\REST_APIs_for_CRUD_Operations_Using_Django\CRUD_Operations\\test_data\employees.csv", errors="ignore") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            employee_list = []
            for row in enumerate(reader):
                (
                    EMPLOYEE_ID,
                    FIRST_NAME,
                    LAST_NAME,
                    EMAIL,
                    PHONE_NUMBER,
                    HIRE_DATE,
                    JOB_ID,
                    SALARY,
                    COMMISSION_PCT,
                    MANAGER_ID,
                    DEPARTMENT_ID
                ) = row[1]
                if MANAGER_ID == ' - ':
                    MANAGER_ID = None
                if COMMISSION_PCT == ' - ':
                    COMMISSION_PCT = None
                employee_list.append(Employees(
                                                EMPLOYEE_ID,
                                                FIRST_NAME,
                                                LAST_NAME,
                                                EMAIL,
                                                PHONE_NUMBER,
                                                datetime.strftime(datetime.strptime(HIRE_DATE, "%d-%b-%y"), '%Y-%m-%d'),
                                                JOB_ID,
                                                SALARY,
                                                COMMISSION_PCT,
                                                MANAGER_ID,
                                                DEPARTMENT_ID
                                                ))
        Employees.objects.bulk_create(employee_list)

    def test_list_all_employees(self):
        response = self.client.get("/Transactions/list_all_employees/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 50)
