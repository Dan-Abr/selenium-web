# third-party
from rest_framework import serializers

# local Django
from .models import *


class E2ETestParamsSerializer(serializers.ModelSerializer):
    # Serialize e2e-test parameters.
    class Meta:
        model = E2ETestParamsModel
        fields = '__all__'


class E2ETestResultsSerializer(serializers.ModelSerializer):
    # Serialize e2e-test results.
    class Meta:
        model = E2ETestResultsModel
        fields = '__all__'