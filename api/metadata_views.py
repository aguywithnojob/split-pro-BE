from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from .models import Group, Customer
from .processor_functions import DefaultProcessor, GetFriendsMetaData

META_MODEL_MAPPER = {
    "groups": dict(
        model = Group.objects.filter,
        processor = DefaultProcessor
    ),
    "friends": dict(
        model = Customer.objects.filter,
        processor = GetFriendsMetaData
    ),
    "category": dict(
        model = Customer.objects.filter, # model will be changed/replaced later
        processor = DefaultProcessor
    )
}

class MetaData(APIView, LoginRequiredMixin):
    permission_classes = [IsAuthenticated]

    def get(self, request, kind, key_id=None):
        """
            Get metadata
                kind: groups or friends

        """
        if kind not in META_MODEL_MAPPER:
            return Response({"message": "Invalid kind"}, status=status.HTTP_400_BAD_REQUEST)
        
        processor = META_MODEL_MAPPER[kind]['processor']
        model = META_MODEL_MAPPER[kind]['model']
        
        try:
            response = processor(
                model = model, 
                request = request, 
                key_id = key_id
            )().data

        except NotImplementedError:
            return Response({"message": "Metadata not implemented"}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(response, status=status.HTTP_200_OK)