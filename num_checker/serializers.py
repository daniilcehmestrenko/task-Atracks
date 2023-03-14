from rest_framework import serializers

from .models import Registry


class RegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Registry
        fields = ['operator', 'region']
