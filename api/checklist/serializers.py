from rest_framework import serializers

from .models import Checklist

class ChecklistSerializer(serializers.ModelSerializer):

    class Meta:

        model = Checklist
        fields = '__all__'

        extra_kwargs = {

            'id': {'required': False},
            'board': {'required': False},
            'created_at': {'required': False},
            'updated_at': {'required': False}

        }

        read_only_fields = [

            'id', 'board', 'created_at', 'updated_at'

        ]