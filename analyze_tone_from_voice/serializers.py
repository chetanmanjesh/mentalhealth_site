from rest_framework import serializers
from .models import Depression, Stress, Person2

class DepressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depression
        fields = '__all__'

class StressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stress
        fields = '__all__'

class Person2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Person2
        fields = ('comments','disorder')
