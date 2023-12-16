from rest_framework import serializers
from .models import Customer, Group, Expense, Balance,  Settlement
from .helper import convert_epoch_to_datetime

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email','avatar', 'mobile','timestamp']
    
    def to_representation(self, instance):
        representation = super(CustomerSerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        return representation

class FriendsSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','name']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(GroupSerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        FriendsData = CustomerSerializer(instance.customers, many=True).data
        
        friends_list = []
        for friend in FriendsData:
            if self.context.get('user_id') != friend['id']: 
                friends_list.append(friend['name']) 
        
        representation['customers'] = friends_list
        # need to put balance amount for each friend later
        # representation['settlements'] = 
        return representation
    
class GroupFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
    
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(ExpenseSerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        representation['updatetimestamp'] = convert_epoch_to_datetime(representation['updatetimestamp'])
        FriendsData = CustomerSerializer(instance.split_on, many=True).data
        representation['paid_by'] = {'id':instance.paid_by.id, 'name':instance.paid_by.name}
        friends_list = []
        for friend in FriendsData:
            if self.context.get('user_id') != friend['id']: 
                friends_list.append({'id':friend['id'],'name':friend['name']}) 
        
        representation['split_on'] = friends_list

        representation['group'] = {'id':instance.group.id, 'name':instance.group.name}
        return representation

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'item', 'amount', 'group','paid_by' ,'split_on','timestamp', 'updatetimestamp']
    
    def to_representation(self, instance):
        representation = super(ActivitySerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        representation['updatetimestamp'] = convert_epoch_to_datetime(representation['updatetimestamp'])
        friend_data = CustomerSerializer(instance.split_on, many=True).data
        friends_list = []
        for friend in friend_data:
            if self.context.get('user_email') != friend['email']: 
                friends_list.append(friend['name']) 
        representation['split_on'] = friends_list

        if self.context.get('user_email') != instance.paid_by.email :
            representation['share'] = -(instance.amount/len(friends_list))
        else: 
            representation['share'] = round(instance.amount - (instance.amount/len(friends_list)),2)
        
        representation['paid_by'] = instance.paid_by.name
        representation['group'] = instance.group.name
        return representation

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(BalanceSerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        return representation

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super(SettlementSerializer, self).to_representation(instance)
        representation['timestamp'] = convert_epoch_to_datetime(representation['timestamp'])
        return representation
