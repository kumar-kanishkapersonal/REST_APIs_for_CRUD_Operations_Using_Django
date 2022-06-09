from datetime import datetime
import coreapi
import coreschema
from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema
from .models import Employees


class CustomSchema(AutoSchema):
    """
    Schema class for all the APIs.
    """
    manual_fields = []

    def get_manual_fields(self, path, method):
        fields = []
        if method.lower() in ["get", "delete"]:
            self.manual_fields = []
            fields = [coreapi.Field("EMPLOYEE_ID", required=True, location="query", schema=coreschema
                                    .String())]
        elif method.lower() == "post":
            self.manual_fields = []
            fields = [coreapi.Field("EMPLOYEE_ID", required=True, location="form", schema=coreschema.String()),
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
        elif method.lower() == "patch":
            self.manual_fields = []
            fields = [coreapi.Field("EMPLOYEE_ID", required=True, location="form", schema=coreschema.String()),
                      coreapi.Field("FIRST_NAME", required=True, location="form", schema=coreschema.String()),
                      coreapi.Field("LAST_NAME", required=True, location="form", schema=coreschema.String()),
                      coreapi.Field("EMAIL", required=True, location="form", schema=coreschema.String()),
                      coreapi.Field("PHONE_NUMBER", required=True, location="form", schema=coreschema.String()),
                      coreapi.Field("HIRE_DATE", required=True, location="form", schema=coreschema.String()),
                      coreapi.Field("JOB_ID", required=True, location="form", schema=coreschema.String()),
                      coreapi.Field("SALARY", required=True, location="form", schema=coreschema.String()),
                      coreapi.Field("COMMISSION_PCT", required=True, location="form", schema=coreschema.String()),
                      coreapi.Field("MANAGER_ID", required=True, location="form", schema=coreschema.String()),
                      coreapi.Field("DEPARTMENT_ID", required=True, location="form", schema=coreschema.String()),
                      coreapi.Field("EMPLOYEE_ID", required=True, location="query", schema=coreschema.String())]
        elif method.lower() == "put":
            self.manual_fields = []
            fields = [coreapi.Field("EMPLOYEE_ID", required=True, location="query", schema=coreschema.String()),
                      coreapi.Field("ATTRIBUTE", required=True, location="query", schema=coreschema.String()),
                      coreapi.Field("VALUE", required=True, location="query", schema=coreschema.String())]
        for field in fields:
            self.manual_fields.append(field)
        return self.manual_fields


class EmployeesSerializer(serializers.ModelSerializer):
    """
    Serializer class for model.
    """
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
            if queryset.exists():
                for line in serializer.data:
                    employee_details = dict(line)
                    employee_details["HIRE_DATE"] = datetime.strftime(
                        datetime.strptime(employee_details["HIRE_DATE"], "%Y-%m-%d"), "%d-%b-%y")
                    resp.append(employee_details)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND, data="Not Found")
            return Response(status=status.HTTP_200_OK, data=resp)
        except Exception as exc:
            return Response(status=status.HTTP_404_NOT_FOUND, data=str(exc))

    @action(detail=False, methods=["GET"], schema=CustomSchema())
    def retrieve_employee_with_employee_id(self, request):
        """
        Fetch details of an employee using EmployeeID.
        """
        try:
            employee_id = request.query_params.get("EMPLOYEE_ID")
            queryset = Employees.objects.filter(EMPLOYEE_ID=employee_id)
            serializer = EmployeesSerializer(queryset, many=True)
            employee_details = dict(serializer.data[0])
            employee_details["HIRE_DATE"] = datetime.strftime(
                datetime.strptime(employee_details["HIRE_DATE"], "%Y-%m-%d"), "%d-%b-%y")
            return Response(status=status.HTTP_200_OK, data=employee_details)
        except IndexError:
            return Response(status=status.HTTP_404_NOT_FOUND, data="Employee not found.")
        except Exception as exc:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=str(exc))

    @action(detail=False, schema=CustomSchema(), methods=["POST"])
    def add_new_employee(self, request):
        """
        Add a new employee to the Employee db.
        """
        try:
            Employees.objects.create(EMPLOYEE_ID=request.data["EMPLOYEE_ID"],
                                     FIRST_NAME=request.data["FIRST_NAME"],
                                     LAST_NAME=request.data["LAST_NAME"],
                                     EMAIL=request.data["EMAIL"],
                                     PHONE_NUMBER=request.data["PHONE_NUMBER"],
                                     HIRE_DATE=datetime.strftime(
                                         datetime.strptime(request.data["HIRE_DATE"], "%d-%b-%y"), "%Y-%m-%d"),
                                     JOB_ID=request.data["JOB_ID"],
                                     SALARY=request.data["SALARY"],
                                     COMMISSION_PCT=request.data["COMMISSION_PCT"],
                                     MANAGER_ID=request.data["MANAGER_ID"],
                                     DEPARTMENT_ID=request.data["DEPARTMENT_ID"])
            return Response(status=status.HTTP_200_OK, data="Created")
        except Exception as exc:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(exc))

    @action(detail=False, methods=["PATCH"], schema=CustomSchema())
    def edit_employee(self, request):
        """
        Edit any or all details of an employee.
        """
        try:
            requested_id = request.query_params.get("EMPLOYEE_ID")
            Employees.objects.filter(EMPLOYEE_ID=requested_id).update(
                EMPLOYEE_ID=request.data["EMPLOYEE_ID"],
                FIRST_NAME=request.data["FIRST_NAME"],
                LAST_NAME=request.data["LAST_NAME"],
                EMAIL=request.data["EMAIL"],
                PHONE_NUMBER=request.data["PHONE_NUMBER"],
                HIRE_DATE=datetime.strftime(datetime.strptime(request.data["HIRE_DATE"], "%d-%b-%y"), "%Y-%m-%d"),
                JOB_ID=request.data["JOB_ID"],
                SALARY=request.data["SALARY"],
                COMMISSION_PCT=request.data["COMMISSION_PCT"],
                MANAGER_ID=request.data["MANAGER_ID"],
                DEPARTMENT_ID=request.data["DEPARTMENT_ID"])
            return Response(status=status.HTTP_200_OK, data="Modified")
        except Exception as exc:
            return Response(status=status.HTTP_404_NOT_FOUND, data=str(exc))

    @action(detail=False, methods=["PUT"], schema=CustomSchema())
    def edit_employee_single_field(self, request):
        """
        Edit any one attribute of the employee.
        """
        try:
            employee_id = request.query_params.get("EMPLOYEE_ID")
            attribute = request.query_params.get("ATTRIBUTE")
            value = request.query_params.get("VALUE")
            if attribute == "HIRE_DATE":
                value = datetime.strftime(datetime.strptime(value, "%d-%b-%y"), "%Y-%m-%d")
            Employees.objects.filter(EMPLOYEE_ID=employee_id).update(**{attribute: value})
            return Response(status=status.HTTP_200_OK, data="Modified")
        except Exception as exc:
            return Response(status=status.HTTP_304_NOT_MODIFIED, data=str(exc))

    @action(detail=False, methods=["DELETE"], schema=CustomSchema())
    def delete_employee(self, request):
        """
        Delete all details of an employee.
        """
        try:
            employee_id = request.query_params.get("EMPLOYEE_ID")
            Employees.objects.filter(EMPLOYEE_ID=employee_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data="Deleted")
        except Exception as exc:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(exc))
