import coreapi, coreschema, csv, json
from datetime import datetime
from rest_framework import status, viewsets, serializers
from rest_framework.schemas import AutoSchema
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Employees


create_schema = AutoSchema(
    manual_fields=[coreapi.Field("EMPLOYEE_ID", required=True, location="form", schema=coreschema.String()),
                   coreapi.Field("FIRST_NAME", required=True, location="form", schema=coreschema.String()),
                   coreapi.Field("LAST_NAME", required=True, location="form", schema=coreschema.String()),
                   coreapi.Field("EMAIL", required=True, location="form", schema=coreschema.String()),
                   coreapi.Field("PHONE_NUMBER", required=True, location="form", schema=coreschema.String()),
                   coreapi.Field("HIRE_DATE", required=True, location="form", schema=coreschema.String()),
                   coreapi.Field("JOB_ID", required=True, location="form", schema=coreschema.String()),
                   coreapi.Field("SALARY", required=True, location="form", schema=coreschema.String()),
                   coreapi.Field("COMMISSION_PCT", required=True, location="form", schema=coreschema.String()),
                   coreapi.Field("MANAGER_ID", required=True, location="form", schema=coreschema.String()),
                   coreapi.Field("DEPARTMENT_ID", required=True, location="form", schema=coreschema.String())]
                   )


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        managed = False
        model = Employees
        fields = "__all__"


class TransactionsViewSet(viewsets.ViewSet):
    """
    REST APIs demonstrating basic crud operations.
    """

    @action(detail=False, methods=["GET"])
    def list_all_employees(self, request):
        """
        Get a list of all the employees with all the details.
        """
        try:
            queryset = Employees.objects.all().order_by("HIRE_DATE")
            serializer = EmployeesSerializer(queryset, many=True)
            resp = []
            for line in serializer.data:
                employee_details = dict(line)
                employee_details["HIRE_DATE"] = datetime.strftime(datetime.strptime(employee_details["HIRE_DATE"], "%Y-%m-%d"), "%d-%b-%y")
                resp.append(employee_details)
            return Response(resp, status=status.HTTP_200_OK)
        except Exception as exc:
            return Response(str(exc), status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, url_path="retrieve_employee_with_employee_id/(?P<EMPLOYEE_ID>\w+)", methods=["GET"])
    def retrieve_employee_with_employee_id(self, request, EMPLOYEE_ID=None):
        """
        Fetch details of an employee using EmployeeID.
        """
        try:
            queryset = Employees.objects.filter(EMPLOYEE_ID=EMPLOYEE_ID)
            serializer = EmployeesSerializer(queryset, many=True)
            employee_details = dict(serializer.data[0])
            employee_details["HIRE_DATE"] = datetime.strftime(datetime.strptime(employee_details["HIRE_DATE"], "%Y-%m-%d"), "%d-%b-%y")
            return Response(employee_details, status=status.HTTP_200_OK)
        except Exception as exc:
            return Response(str(exc), status=status.HTTP_200_OK)

    @action(detail=False, schema=create_schema, methods=["POST"])
    def add_new_employee(self, request):
        """
        Add a new employee to the Employee db.
        """
        try:
            queryset = Employees.objects.create(EMPLOYEE_ID = request.data["EMPLOYEE_ID"],
                                                FIRST_NAME = request.data["FIRST_NAME"],
                                                LAST_NAME = request.data["LAST_NAME"],
                                                EMAIL = request.data["EMAIL"],
                                                PHONE_NUMBER = request.data["PHONE_NUMBER"],
                                                HIRE_DATE = datetime.strftime(datetime.strptime(request.data["HIRE_DATE"], "%d-%b-%y"), "%Y-%m-%d"),
                                                JOB_ID = request.data["JOB_ID"],
                                                SALARY = request.data["SALARY"],
                                                COMMISSION_PCT = request.data["COMMISSION_PCT"],
                                                MANAGER_ID = request.data["MANAGER_ID"],
                                                DEPARTMENT_ID = request.data["DEPARTMENT_ID"]
                                                )
            return Response("Created", status=status.HTTP_200_OK)
        except Exception as exc:
            return Response(str(exc), status=status.HTTP_200_OK)
