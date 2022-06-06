import coreapi, coreschema, csv
from datetime import datetime
from rest_framework import status, viewsets, serializers
from rest_framework.schemas import AutoSchema
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Employees


# custom_schema = AutoSchema(
#     manual_fields=[coreapi.Field("year", required=True, location="form", schema=coreschema.String()),
#                    coreapi.Field("drug_classification", required=True, location="form", schema=coreschema.String())])
#                    coreapi.Field("drug_classification", required=True, location="form", schema=coreschema.String())])


class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        managed = False
        model = Employees
        fields = '__all__'


class TransactionsViewSet(viewsets.ViewSet):
    """
    ViewSet to define API logic.
    """
    queryset = Employees.objects.all()

    @action(detail=False, methods=['GET'])
    def list_all_employees(self, request):
        try:
            serializer = EmployeesSerializer(self.queryset, many=True)
            resp = []
            for line in serializer.data:
                resp.append({
                            "EMPLOYEE_ID": line.get("EMPLOYEE_ID",),
                            "FIRST_NAME": line.get("FIRST_NAME",),
                            "LAST_NAME": line.get("LAST_NAME",),
                            "EMAIL": line.get("EMAIL",),
                            "PHONE_NUMBER": line.get("PHONE_NUMBER",),
                            "HIRE_DATE": datetime.strftime(datetime.strptime(line.get("HIRE_DATE"), '%Y-%m-%d'), "%d-%b-%y"),
                            "JOB_ID": line.get("JOB_ID",),
                            "SALARY": line.get("SALARY",),
                            "COMMISSION_PCT": line.get("COMMISSION_PCT",),
                            "MANAGER_ID": line.get("MANAGER_ID",),
                            "DEPARTMENT_ID": line.get("DEPARTMENT_ID"),
                            })
            return Response(resp, status=status.HTTP_200_OK)
        except Exception as exc:
            print(exc)
