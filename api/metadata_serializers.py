from rest_framework import serializers

# Response Serializers
class MetaDataResponseSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=255)
    value = serializers.CharField(max_length=255)

    
