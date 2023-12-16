"""
ALL PROCESSOR FUNCTIONS GO HERE
"""

from .friends import *
from ..metadata_serializers import MetaDataResponseSerializer

class DefaultProcessor:
    def __init__(self,request, model ,filter_params = {}) -> None:
        self.filter_params = filter_params
        self.request = request
        self.model = model

    def process(self):
        raise NotImplementedError("Your need to impletement the process method")
    
    def __call__(self):
        return self.process()