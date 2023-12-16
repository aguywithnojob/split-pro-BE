from ..models import Group
from ..metadata_serializers import MetaDataResponseSerializer

class GetFriendsMetaData:
    def __init__(self,request, model, key_id, filter_params={}) -> None:
        self.filter_params = filter_params
        self.request = request
        self.model = model
        self.key_id = key_id

    def process(self):
        user = self.request.user
        
        if self.key_id:
            self.filter_params['groups__in'] = [self.key_id]
        
        else:
            group_ids = Group.objects.filter(customers__in=[user.customer.id]).values_list('id', flat=True)
            self.filter_params['groups__in'] = group_ids

        data = self.model(**self.filter_params).distinct()

        return self.format(data)

    @staticmethod
    def format(data):
        formated_records = []

        for record in data:
            formated_records.append({
                'value': getattr(record,'id'),
                'label': getattr(record,'name')
            })

        return MetaDataResponseSerializer(formated_records,many = True)
        
        
    def __call__(self):
        return self.process()